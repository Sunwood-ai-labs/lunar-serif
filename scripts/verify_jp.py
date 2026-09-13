"""Verify the broad Japanese LUNAR SERIF JP acceptance contract.

The JIS X 0208 inventory is intentionally generated here instead of copied
from a text file.  Each cell is wrapped in an ISO-2022-JP escape sequence and
decoded with Python's strict ``iso2022_jp`` codec.  This keeps the acceptance
set reproducible and makes accidental omissions in a hand-maintained list
visible.

The script has no HarfBuzz requirement.  FontTools checks the OpenType tables;
an optional ``--harfbuzz-python`` probe can be used when a separate Python
environment contains uharfbuzz.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FONT = ROOT / "outputs" / "LUNARSERIFJP-Regular.ttf"
DEFAULT_WOFF2 = ROOT / "outputs" / "LUNARSERIFJP-Regular.woff2"
DEFAULT_BASE_FONT = ROOT / "outputs" / "LUNARSERIF-Regular.ttf"
DEFAULT_CORPUS = ROOT / "verification" / "japanese" / "corpus.json"

JIS_FIRST_ROWS = range(0x30, 0x50)  # ku 16-47, JIS X 0208 first level
JIS_SECOND_ROWS = range(0x50, 0x75)  # ku 48-84, JIS X 0208 second level
JIS_SPECIAL_ROWS = range(0x21, 0x30)  # punctuation, kana, Greek/Cyrillic, box drawing
JIS_ALL_ROWS = range(0x21, 0x75)
JIS_COUNTS = {"special": 524, "first": 2965, "second": 3390, "all": 6879}

# These are the JIS X 0208 kana rows, including the JIS iteration marks.  The
# lists are kept explicit so the report names the categories people actually
# care about when reviewing a Japanese font.
HIRAGANA = (
    "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞ"
    "ただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽ"
    "まみむめもゃやゅゆょよらりるれろゎわゐゑをん"
)
KATAKANA = (
    "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾ"
    "タダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポ"
    "マミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶ"
)
DAKUTEN = (
    "゛がぎぐげござじずぜぞだぢづでどばびぶべぼ"
    "ガギグゲゴザジズゼゾダヂヅデドバビブベボヴ"
)
HANDAKUTEN = "゜ぱぴぷぺぽパピプペポ"

ASCII_HALF_WIDTH = "".join(chr(cp) for cp in range(0x20, 0x7F))
FULLWIDTH_ASCII = "".join(chr(cp) for cp in range(0xFF01, 0xFF5F))
# Fullwidth white parentheses sit immediately after the ASCII-derived range.
FULLWIDTH_BRACKETS = "｟｠"
FULLWIDTH_MACRON = "￣"
# U+FF61-U+FF9F is the complete JIS X 0201 halfwidth punctuation/kana block.
HALFWIDTH_KATAKANA = "".join(chr(cp) for cp in range(0xFF61, 0xFFA0))

VERTICAL_PUNCTUATION = set("、。…‥「」『』【】〔〕（）［］｛｝〈〉《》！？")
# These fullwidth marks have distinct vertical forms in the acceptance build.
VERTICAL_REQUIRED = "＿｜｟｠￣"


def decode_jis_cell(row: int, cell: int) -> str | None:
    """Decode one JIS X 0208 row/cell through Python's byte codec."""

    # Building the bytes numerically avoids shell/source encoding surprises
    # and documents that this is byte decoding, rather than Unicode guessing.
    payload = bytes((0x1B, 0x24, 0x42, row, cell, 0x1B, 0x28, 0x42))
    try:
        decoded = payload.decode("iso2022_jp", errors="strict")
    except UnicodeDecodeError:
        return None
    return decoded if len(decoded) == 1 else None


def enumerate_jis(rows: Iterable[int]) -> list[tuple[int, int, str]]:
    """Return valid (row, cell, character) records for the requested rows."""

    result: list[tuple[int, int, str]] = []
    for row in rows:
        for cell in range(0x21, 0x7F):
            char = decode_jis_cell(row, cell)
            if char is not None:
                result.append((row, cell, char))
    return result


def build_jis_inventory() -> dict[str, list[tuple[int, int, str]]]:
    """Build and sanity-check the JIS X 0208 acceptance inventory."""

    inventory = {
        "special": enumerate_jis(JIS_SPECIAL_ROWS),
        "first": enumerate_jis(JIS_FIRST_ROWS),
        "second": enumerate_jis(JIS_SECOND_ROWS),
        "all": enumerate_jis(JIS_ALL_ROWS),
    }
    counts = {key: len(value) for key, value in inventory.items()}
    if counts != JIS_COUNTS:
        raise RuntimeError(
            "iso2022_jp inventory changed: "
            f"expected {JIS_COUNTS}, decoded {counts}"
        )
    all_chars = [char for _, _, char in inventory["all"]]
    duplicate_chars = sorted(char for char, count in Counter(all_chars).items() if count > 1)
    if duplicate_chars:
        raise RuntimeError(
            "iso2022_jp produced duplicate JIS characters: "
            + " ".join(f"U+{ord(char):04X}" for char in duplicate_chars[:8])
        )
    return inventory


def codepoints(records: Iterable[tuple[int, int, str]]) -> set[int]:
    return {ord(char) for _, _, char in records}


def format_codepoint(cp: int) -> str:
    char = chr(cp)
    shown = repr(char) if char.isspace() else char
    return f"U+{cp:04X} {shown}"


def sample_codepoints(values: Iterable[int], limit: int = 24) -> list[str]:
    values = sorted(set(values))
    return [format_codepoint(cp) for cp in values[:limit]]


def best_cmap(font: TTFont) -> dict[int, str]:
    cmap = font.getBestCmap()
    return dict(cmap or {})


def names_snapshot(font: TTFont) -> list[tuple[int, int, int, int, str]]:
    if "name" not in font:
        return []
    return sorted(
        (
            record.nameID,
            record.platformID,
            record.platEncID,
            record.langID,
            record.toUnicode(),
        )
        for record in font["name"].names
    )


def feature_snapshot(font: TTFont) -> dict[str, dict[str, Any]]:
    """Return GSUB feature lookup references, including vertical features."""

    if "GSUB" not in font:
        return {}
    table = font["GSUB"].table
    feature_list = getattr(table, "FeatureList", None)
    if feature_list is None:
        return {}
    lookup_list = getattr(getattr(table, "LookupList", None), "Lookup", []) or []
    result: dict[str, dict[str, Any]] = {}
    for record in feature_list.FeatureRecord:
        tag = record.FeatureTag
        indices = list(getattr(record.Feature, "LookupListIndex", []) or [])
        valid = [index for index in indices if 0 <= index < len(lookup_list)]
        entry = result.setdefault(tag, {"lookup_indices": [], "lookup_count": 0})
        entry["lookup_indices"] = sorted(set(entry["lookup_indices"]) | set(indices))
        entry["lookup_count"] = len(
            sorted(set(entry["lookup_indices"]) & set(range(len(lookup_list))))
        )
        entry["invalid_lookup_indices"] = sorted(
            set(entry.get("invalid_lookup_indices", []))
            | {index for index in indices if index not in valid}
        )
    return result


def feature_targets_for_glyph(font: TTFont, tag: str, source_name: str) -> list[str]:
    """Find direct SingleSubst targets for one glyph in a GSUB feature."""

    if "GSUB" not in font:
        return []
    table = font["GSUB"].table
    records = getattr(getattr(table, "FeatureList", None), "FeatureRecord", []) or []
    lookup_list = getattr(getattr(table, "LookupList", None), "Lookup", []) or []
    targets: list[str] = []
    for record in records:
        if record.FeatureTag != tag:
            continue
        for index in getattr(record.Feature, "LookupListIndex", []) or []:
            if not 0 <= index < len(lookup_list):
                continue
            lookup = lookup_list[index]
            for subtable in getattr(lookup, "SubTable", []) or []:
                if lookup.LookupType == 7 and hasattr(subtable, "ExtSubTable"):
                    subtable = subtable.ExtSubTable
                mapping = getattr(subtable, "mapping", None)
                if mapping and source_name in mapping:
                    target = mapping[source_name]
                    targets.extend(target if isinstance(target, list) else [target])
    return sorted(set(targets))


def outline_digest(font: TTFont, glyph_name: str) -> str:
    """Digest a glyph's outline, resolving composites when necessary."""

    if "glyf" in font:
        # Compiled glyf bytes preserve contour geometry and component transforms
        # and are stable across a TTF/WOFF2 round trip when glyph order agrees.
        # Glyph.compile expects the glyf table (not the TTFont wrapper).  The
        # distinction matters for composite glyph components.
        payload = font["glyf"][glyph_name].compile(font["glyf"])
    else:
        pen = RecordingPen()
        font.getGlyphSet()[glyph_name].draw(pen)
        payload = repr(pen.value).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def outline_geometry_digest(font: TTFont, glyph_name: str) -> str:
    """Digest outline geometry without depending on glyf byte packing.

    WOFF2 and TTF can legally choose different flag packing while describing
    the same outline.  Comparing coordinates/endpoints/flags for simple glyphs
    and component transforms for composites avoids treating that packing as a
    visual difference.
    """

    if "glyf" in font:
        glyph = font["glyf"][glyph_name]
        if glyph.numberOfContours >= 0:
            coordinates = tuple(
                (int(round(point[0])), int(round(point[1])))
                for point in (getattr(glyph, "coordinates", None) or [])
            )
            payload: Any = (
                "simple",
                int(glyph.numberOfContours),
                coordinates,
                tuple(int(point) for point in (getattr(glyph, "endPtsOfContours", None) or [])),
                # Bit 3 is the compressed repeat marker, not an outline
                # property.  Ignore it so a different TTF/WOFF2 packing does
                # not look like a geometry change.
                tuple(int(flag) & 0xF7 for flag in (getattr(glyph, "flags", None) or [])),
            )
        else:
            components = []
            for component in getattr(glyph, "components", None) or []:
                transform = getattr(component, "transform", None)
                components.append(
                    (
                        component.glyphName,
                        int(getattr(component, "x", 0)),
                        int(getattr(component, "y", 0)),
                        tuple(float(value) for value in transform) if transform else None,
                    )
                )
            payload = ("composite", tuple(components))
    else:
        pen = RecordingPen()
        font.getGlyphSet()[glyph_name].draw(pen)
        payload = ("recording", pen.value)
    return hashlib.sha256(repr(payload).encode("utf-8")).hexdigest()


def glyph_geometry_digests(font: TTFont) -> dict[str, str]:
    return {name: outline_geometry_digest(font, name) for name in font.getGlyphOrder()}


def metric_snapshot(font: TTFont) -> dict[str, tuple[int, int]]:
    if "hmtx" not in font:
        return {}
    return {name: tuple(metrics) for name, metrics in font["hmtx"].metrics.items()}


def vertical_metric_snapshot(font: TTFont) -> dict[str, tuple[int, int]]:
    if "vmtx" not in font:
        return {}
    return {name: tuple(metrics) for name, metrics in font["vmtx"].metrics.items()}


def load_corpus(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]], set[str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    examples = data.get("required_examples")
    if not isinstance(examples, list) or not examples:
        raise ValueError("corpus.required_examples must be a non-empty list")
    texts: list[dict[str, Any]] = []
    for index, example in enumerate(examples):
        if not isinstance(example, dict):
            raise ValueError(f"required_examples[{index}] must be an object")
        text = example.get("text")
        layout = example.get("layout")
        if not isinstance(text, str) or not text:
            raise ValueError(f"required_examples[{index}].text must be non-empty")
        if layout not in {"horizontal", "vertical", "mixed"}:
            raise ValueError(
                f"required_examples[{index}].layout must be horizontal, vertical, or mixed"
            )
        texts.append({"id": example.get("id", f"example-{index + 1}"), "layout": layout, "text": text})

    required_chars: set[str] = set()
    character_sets = data.get("required_character_sets", {})
    if not isinstance(character_sets, dict):
        raise ValueError("corpus.required_character_sets must be an object")
    for name, chars in character_sets.items():
        if not isinstance(chars, str):
            raise ValueError(f"required_character_sets.{name} must be a string")
        required_chars.update(chars)
    return data, texts, required_chars


def check_codepoint_group(label: str, cps: set[int], cmap: dict[int, str], glyphs: set[str]) -> dict[str, Any]:
    missing = sorted(cp for cp in cps if cp not in cmap)
    notdef = sorted(cp for cp in cps if cmap.get(cp) == ".notdef")
    unknown = sorted(cp for cp in cps if cp in cmap and cmap[cp] not in glyphs)
    return {
        "expected": len(cps),
        "mapped": len(cps) - len(set(missing)),
        "missing": sample_codepoints(missing),
        "missing_count": len(missing),
        "notdef": sample_codepoints(notdef),
        "notdef_count": len(notdef),
        "unknown_glyph_count": len(unknown),
        "unknown_glyphs": sample_codepoints(unknown),
        "passes": not missing and not notdef and not unknown,
    }


def metadata_check(font: TTFont, license_path: Path) -> dict[str, Any]:
    values: dict[int, list[str]] = {}
    if "name" in font:
        for record in font["name"].names:
            try:
                value = record.toUnicode().strip()
            except Exception:
                value = ""
            if value:
                values.setdefault(record.nameID, []).append(value)
    unique_values = {key: sorted(set(items)) for key, items in values.items()}
    required_ids = [0, 1, 2, 4, 5, 6, 13]
    missing_ids = [name_id for name_id in required_ids if not unique_values.get(name_id)]
    license_text = " ".join(unique_values.get(0, []) + unique_values.get(13, []))
    license_marker = bool(
        re.search(r"license|licen[cs]e|OFL|SIL|許諾|利用条件|利用許諾", license_text, re.IGNORECASE)
    )
    license_file_text = license_path.read_text(encoding="utf-8") if license_path.is_file() else ""
    license_file_ok = bool(license_file_text.strip())
    license_file_mentions_open_font = bool(
        re.search(r"SIL\s+OPEN\s+FONT\s+LICENSE|OPEN\s+FONT\s+LICENSE|OFL", license_file_text, re.IGNORECASE)
    )
    urls = unique_values.get(14, [])
    url_ok = all(value.startswith(("http://", "https://")) for value in urls)
    result = {
        "required_name_ids": required_ids,
        "missing_name_ids": missing_ids,
        "license_description_present": bool(unique_values.get(13)),
        "license_marker_present": license_marker,
        "license_info_url_present": bool(urls),
        "license_info_url_valid": url_ok,
        "repository_license_file": str(license_path),
        "repository_license_file_ok": license_file_ok,
        "repository_license_file_mentions_open_font": license_file_mentions_open_font,
        "passes": not missing_ids and license_marker and license_file_ok and license_file_mentions_open_font and url_ok,
    }
    return result


def vertical_check(font: TTFont, cmap: dict[int, str], glyphs: set[str]) -> dict[str, Any]:
    features = feature_snapshot(font)
    required_features = {}
    for tag in ("vert", "vrt2"):
        item = features.get(tag, {})
        required_features[tag] = {
            "present": tag in features,
            "lookup_count": item.get("lookup_count", 0),
            "invalid_lookup_indices": item.get("invalid_lookup_indices", []),
            "passes": bool(item.get("lookup_count", 0)) and not item.get("invalid_lookup_indices"),
        }

    vertical_metrics: dict[str, Any] = {
        "vhea_present": "vhea" in font,
        "vmtx_present": "vmtx" in font,
        "VORG_present": "VORG" in font,
        "vhea_number_of_metrics": int(getattr(font["vhea"], "numberOfVMetrics", 0)) if "vhea" in font else 0,
    }
    vmetrics = vertical_metric_snapshot(font)
    mapped_names = {cmap[cp] for cp in cmap if cmap[cp] in glyphs}
    missing_metrics = sorted(name for name in mapped_names if name not in vmetrics)
    zero_height = sorted(name for name in mapped_names if name in vmetrics and vmetrics[name][0] <= 0)
    vertical_metrics.update(
        {
            "mapped_glyphs_checked": len(mapped_names),
            "vmtx_metrics": len(vmetrics),
            "missing_mapped_metrics_count": len(missing_metrics),
            "missing_mapped_metrics": missing_metrics[:24],
            "nonpositive_advance_height_count": len(zero_height),
            "passes": (
                vertical_metrics["vhea_present"]
                and vertical_metrics["vmtx_present"]
                and vertical_metrics["vhea_number_of_metrics"] > 0
                and not missing_metrics
                and not zero_height
            ),
        }
    )
    required_substitutions: dict[str, Any] = {}
    for char in VERTICAL_REQUIRED:
        cp = ord(char)
        source = cmap.get(cp)
        item: dict[str, Any] = {
            "source_glyph": source,
            "vert_targets": feature_targets_for_glyph(font, "vert", source) if source else [],
            "vrt2_targets": feature_targets_for_glyph(font, "vrt2", source) if source else [],
        }
        item["passes"] = bool(source) and any(target != source for target in item["vert_targets"]) and any(
            target != source for target in item["vrt2_targets"]
        )
        required_substitutions[f"U+{cp:04X} {char}"] = item
    return {
        "GSUB_features": sorted(features),
        "GSUB_feature_lookups": features,
        "required_features": required_features,
        "required_vertical_substitutions": required_substitutions,
        # OpenType has no seven-character `vmetrics` feature tag.  In this
        # acceptance contract, vmetrics means the vhea/vmtx vertical metrics
        # tables (VORG is useful but optional).
        "vmetrics": vertical_metrics,
        "passes": (
            all(item["passes"] for item in required_features.values())
            and all(item["passes"] for item in required_substitutions.values())
            and vertical_metrics["passes"]
        ),
    }


def compare_ttf_woff2(ttf: TTFont, woff2: TTFont) -> dict[str, Any]:
    ttf_order = ttf.getGlyphOrder()
    woff_order = woff2.getGlyphOrder()
    order_equal = ttf_order == woff_order
    ttf_cmap = best_cmap(ttf)
    woff_cmap = best_cmap(woff2)
    cmap_equal = ttf_cmap == woff_cmap
    ttf_metrics = metric_snapshot(ttf)
    woff_metrics = metric_snapshot(woff2)
    metrics_equal = ttf_metrics == woff_metrics
    names_equal = names_snapshot(ttf) == names_snapshot(woff2)

    outline_equal = False
    outline_mismatch_count: int | None = None
    if order_equal:
        # Compare semantic geometry rather than packed glyf bytes.  This also
        # keeps the check valid for CFF-based test fonts through RecordingPen.
        left = glyph_geometry_digests(ttf)
        right = glyph_geometry_digests(woff2)
        mismatches = [name for name in ttf_order if left.get(name) != right.get(name)]
        outline_mismatch_count = len(mismatches)
        outline_equal = not mismatches

    feature_equal = feature_snapshot(ttf) == feature_snapshot(woff2)
    return {
        "ttf_exists": True,
        "woff2_exists": True,
        "glyph_order_equal": order_equal,
        "cmap_equal": cmap_equal,
        "hmtx_equal": metrics_equal,
        "outline_equal": outline_equal,
        "outline_mismatch_count": outline_mismatch_count,
        "GSUB_features_equal": feature_equal,
        "name_metadata_equal": names_equal,
        "passes": all((order_equal, cmap_equal, metrics_equal, outline_equal, feature_equal, names_equal)),
    }


def compare_base_outlines(base: TTFont, jp: TTFont) -> dict[str, Any]:
    base_cmap = best_cmap(base)
    jp_cmap = best_cmap(jp)
    base_metrics = metric_snapshot(base)
    jp_metrics = metric_snapshot(jp)
    # The display source currently has 104 non-Japanese cmap entries.  Derive
    # this from the source cmap so the comparison remains correct if its
    # punctuation inventory changes, while keeping the expected count visible.
    display_cps = sorted(cp for cp in base_cmap if cp < 0x3000)
    result: dict[str, Any] = {
        "comparison_scope": "104 original display cmap entries (including N/O/S) plus ss01 plain O",
        "display_codepoints_expected": 104,
        "display_codepoints_checked": len(display_cps),
        "display_codepoints": {},
        "plain_o": {},
        "passes": len(display_cps) == 104,
    }
    for cp in display_cps:
        char = chr(cp)
        base_name = base_cmap.get(cp)
        jp_name = jp_cmap.get(cp)
        item: dict[str, Any] = {"base_glyph": base_name, "jp_glyph": jp_name}
        if not base_name or not jp_name:
            item["passes"] = False
            item["reason"] = "cmap entry missing"
        else:
            base_digest = outline_digest(base, base_name)
            jp_digest = outline_digest(jp, jp_name)
            base_advance = base_metrics.get(base_name, (None, None))[0]
            jp_advance = jp_metrics.get(jp_name, (None, None))[0]
            item.update(
                {
                    "base_outline_sha256": base_digest,
                    "jp_outline_sha256": jp_digest,
                    "base_advance": base_advance,
                    "jp_advance": jp_advance,
                    "passes": base_digest == jp_digest and base_advance == jp_advance,
                }
            )
        result["display_codepoints"][f"U+{cp:04X} {char!r}"] = item
        result["passes"] = result["passes"] and item["passes"]

    base_o = base_cmap.get(ord("O"))
    jp_o = jp_cmap.get(ord("O"))
    base_plain = feature_targets_for_glyph(base, "ss01", base_o) if base_o else []
    jp_plain = feature_targets_for_glyph(jp, "ss01", jp_o) if jp_o else []
    # Keep a useful fallback for fonts where the source feature is represented
    # by a named plain glyph but the GSUB table is subsetted during export.
    if not base_plain:
        base_plain = [name for name in base.getGlyphOrder() if name.endswith(".plain")]
    if not jp_plain:
        jp_plain = [name for name in jp.getGlyphOrder() if name.endswith(".plain")]
    plain_item: dict[str, Any] = {
        "base_glyphs": base_plain,
        "jp_glyphs": jp_plain,
        "passes": bool(base_plain) and bool(jp_plain) and len(base_plain) == len(jp_plain),
    }
    if plain_item["passes"]:
        pairs = []
        for base_name, jp_name in zip(base_plain, jp_plain):
            base_digest = outline_digest(base, base_name)
            jp_digest = outline_digest(jp, jp_name)
            base_advance = base_metrics.get(base_name, (None, None))[0]
            jp_advance = jp_metrics.get(jp_name, (None, None))[0]
            pairs.append(
                {
                    "base_glyph": base_name,
                    "jp_glyph": jp_name,
                    "base_outline_sha256": base_digest,
                    "jp_outline_sha256": jp_digest,
                    "base_advance": base_advance,
                    "jp_advance": jp_advance,
                    "passes": base_digest == jp_digest and base_advance == jp_advance,
                }
            )
        plain_item["pairs"] = pairs
        plain_item["passes"] = all(pair["passes"] for pair in pairs)
    result["plain_o"] = plain_item
    result["passes"] = result["passes"] and plain_item["passes"]
    return result


HARFBUZZ_PROBE = r'''
import json
import sys
from pathlib import Path
import uharfbuzz as hb

font_data = Path(sys.argv[1]).read_bytes()
face = hb.Face(font_data)
font = hb.Font(face)
font.scale = (face.upem, face.upem)
text = sys.argv[2]
result = {}
for feature in ("vert", "vrt2"):
    buf = hb.Buffer()
    buf.add_str(text)
    buf.direction = "ttb"
    buf.script = "hani"
    buf.language = "ja"
    hb.shape(font, buf, {feature: True})
    result[feature] = {
        "glyph_count": len(buf.glyph_infos),
        "notdef_count": sum(info.codepoint == 0 for info in buf.glyph_infos),
        "x_advance_sum": sum(pos.x_advance for pos in buf.glyph_positions),
        "y_advance_sum": sum(pos.y_advance for pos in buf.glyph_positions),
    }
vertical_required = "＿｜｟｠￣"
vertical_targets = {}
for char in vertical_required:
    shaped = {}
    for mode, features in (
        ("disabled", {"vert": False, "vrt2": False}),
        ("vert", {"vert": True, "vrt2": False}),
        ("vrt2", {"vert": False, "vrt2": True}),
    ):
        buf = hb.Buffer()
        buf.add_str(char)
        buf.direction = "ttb"
        buf.script = "hani"
        buf.language = "ja"
        hb.shape(font, buf, features)
        shaped[mode] = {
            "gids": [info.codepoint for info in buf.glyph_infos],
            "notdef_count": sum(info.codepoint == 0 for info in buf.glyph_infos),
        }
    vertical_targets["U+%04X" % ord(char)] = shaped
result["vertical_required"] = vertical_targets
print(json.dumps(result, ensure_ascii=False))
'''


def run_harfbuzz_probe(python_path: str, font_path: Path, text: str) -> dict[str, Any]:
    completed = subprocess.run(
        [python_path, "-X", "utf8", "-c", HARFBUZZ_PROBE, str(font_path), text],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(
            f"HarfBuzz probe failed ({completed.returncode}): {completed.stderr.strip()[-1000:]}"
        )
    return json.loads(completed.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", type=Path, default=DEFAULT_FONT, help="Japanese TTF to verify")
    parser.add_argument("--woff2", type=Path, default=DEFAULT_WOFF2, help="matching Japanese WOFF2")
    parser.add_argument("--base-font", type=Path, default=DEFAULT_BASE_FONT, help="existing display TTF for N/O/S comparison")
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS, help="required Japanese specimen corpus JSON")
    parser.add_argument(
        "--harfbuzz-python",
        "--shaper-python",
        dest="harfbuzz_python",
        help="optional Python executable containing uharfbuzz for a vertical shaping probe",
    )
    parser.add_argument("--skip-base-outline", action="store_true", help="skip comparison with the existing display TTF")
    args = parser.parse_args()

    issues: list[str] = []
    try:
        inventory = build_jis_inventory()
        corpus, examples, corpus_required_chars = load_corpus(args.corpus)
    except Exception as exc:
        print(json.dumps({"passes": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1

    if not args.font.is_file():
        print(json.dumps({"passes": False, "error": f"missing font: {args.font}"}, ensure_ascii=False, indent=2))
        return 1
    if not args.woff2.is_file():
        print(json.dumps({"passes": False, "error": f"missing WOFF2: {args.woff2}"}, ensure_ascii=False, indent=2))
        return 1

    try:
        font = TTFont(args.font)
        woff2 = TTFont(args.woff2)
    except Exception as exc:
        print(json.dumps({"passes": False, "error": f"font load failed: {exc}"}, ensure_ascii=False, indent=2))
        return 1

    cmap = best_cmap(font)
    glyphs = set(font.getGlyphOrder())
    jis_groups = {key: codepoints(value) for key, value in inventory.items()}
    coverage: dict[str, Any] = {}
    for key in ("special", "first", "second", "all"):
        coverage[f"jis_x0208_{key}"] = check_codepoint_group(key, jis_groups[key], cmap, glyphs)

    special_records = inventory["special"]
    kana_cps = codepoints(record for record in special_records if record[0] in (0x24, 0x25))
    symbol_cps = codepoints(record for record in special_records if record[0] in (0x21, 0x22, 0x28))
    groups = {
        "kana": kana_cps,
        "hiragana": {ord(char) for char in HIRAGANA},
        "katakana": {ord(char) for char in KATAKANA},
        "dakuten": {ord(char) for char in DAKUTEN},
        "handakuten": {ord(char) for char in HANDAKUTEN},
        "japanese_symbols": symbol_cps,
        "ascii_halfwidth": {ord(char) for char in ASCII_HALF_WIDTH},
        "fullwidth_ascii": {ord(char) for char in FULLWIDTH_ASCII},
        "fullwidth_brackets": {ord(char) for char in FULLWIDTH_BRACKETS},
        "fullwidth_macron": {ord(char) for char in FULLWIDTH_MACRON},
        "halfwidth_katakana": {ord(char) for char in HALFWIDTH_KATAKANA},
        "corpus_required_characters": {ord(char) for char in corpus_required_chars},
    }
    for name, cps in groups.items():
        coverage[name] = check_codepoint_group(name, cps, cmap, glyphs)

    # Every Unicode cmap target must resolve to an actual glyph; a .notdef
    # target is reported separately for required groups above.
    dangling_cmap = sorted((cp, name) for cp, name in cmap.items() if name not in glyphs)
    coverage["cmap"] = {
        "unicode_entries": len(cmap),
        "dangling_target_count": len(dangling_cmap),
        "dangling_targets": [f"U+{cp:04X} -> {name}" for cp, name in dangling_cmap[:24]],
        "passes": not dangling_cmap,
    }
    unicode_subtables = [table for table in getattr(font.get("cmap"), "tables", []) if table.isUnicode()]
    coverage["cmap"]["unicode_subtable_formats"] = sorted({table.format for table in unicode_subtables})
    coverage["cmap"]["has_format_4_or_12"] = any(table.format in (4, 12) for table in unicode_subtables)
    coverage["cmap"]["passes"] = coverage["cmap"]["passes"] and coverage["cmap"]["has_format_4_or_12"]

    corpus_text = "".join(example["text"] for example in examples)
    corpus_codepoints = sum(1 for char in corpus_text if char not in "\r\n")
    corpus_layouts = Counter(example["layout"] for example in examples)
    corpus_missing = sorted(ord(char) for char in set(corpus_text) | corpus_required_chars if ord(char) not in cmap)
    mixed_examples = [
        example
        for example in examples
        if example["layout"] == "mixed"
        and any(char in ASCII_HALF_WIDTH or char in FULLWIDTH_ASCII or char in HALFWIDTH_KATAKANA for char in example["text"])
        and any(ord(char) in jis_groups["all"] for char in example["text"])
    ]
    vertical_examples = [
        example
        for example in examples
        if example["layout"] == "vertical" and len(set(example["text"]) & VERTICAL_PUNCTUATION) >= 2
    ]
    corpus_result = {
        "minimum_codepoints": int(corpus.get("minimum_codepoints", 300)),
        "codepoints": corpus_codepoints,
        "layout_counts": dict(corpus_layouts),
        "required_layouts_present": all(corpus_layouts.get(layout, 0) for layout in ("horizontal", "vertical", "mixed")),
        "mixed_script_example_present": bool(mixed_examples),
        "vertical_punctuation_example_present": bool(vertical_examples),
        "missing_count": len(corpus_missing),
        "missing": sample_codepoints(corpus_missing),
        "passes": (
            corpus_codepoints >= int(corpus.get("minimum_codepoints", 300))
            and all(corpus_layouts.get(layout, 0) for layout in ("horizontal", "vertical", "mixed"))
            and bool(mixed_examples)
            and bool(vertical_examples)
            and not corpus_missing
        ),
    }

    vertical = vertical_check(font, cmap, glyphs)
    jp_license = ROOT / "outputs" / "LUNAR-SERIF-JP-OFL.txt"
    license_path = jp_license if jp_license.is_file() else ROOT / "LICENSE.txt"
    license_result = metadata_check(font, license_path)
    ttf_woff2 = compare_ttf_woff2(font, woff2)

    if args.skip_base_outline:
        base_result: dict[str, Any] = {"skipped": True, "passes": True}
    elif args.base_font.is_file():
        try:
            base = TTFont(args.base_font)
            base_result = compare_base_outlines(base, font)
        except Exception as exc:
            base_result = {"skipped": False, "passes": False, "error": str(exc)}
    else:
        base_result = {"skipped": True, "reason": f"missing optional base font: {args.base_font}", "passes": True}

    harfbuzz_result: dict[str, Any]
    if args.harfbuzz_python:
        try:
            probe_text = next(
                (example["text"] for example in examples if example["layout"] == "vertical"),
                "「月夜、静かな文字。」",
            )
            harfbuzz_result = {"skipped": False, "probe": run_harfbuzz_probe(args.harfbuzz_python, args.font, probe_text)}
            feature_probe_passes = all(
                result["notdef_count"] == 0 and result["y_advance_sum"] != 0
                for result in (
                    harfbuzz_result["probe"].get("vert", {}),
                    harfbuzz_result["probe"].get("vrt2", {}),
                )
            )
            target_probe_passes = True
            for target in harfbuzz_result["probe"].get("vertical_required", {}).values():
                disabled = target.get("disabled", {})
                for enabled_name in ("vert", "vrt2"):
                    enabled = target.get(enabled_name, {})
                    target_probe_passes = target_probe_passes and (
                        disabled.get("notdef_count", 1) == 0
                        and enabled.get("notdef_count", 1) == 0
                        and bool(disabled.get("gids"))
                        and bool(enabled.get("gids"))
                        and disabled.get("gids") != enabled.get("gids")
                    )
            harfbuzz_result["passes"] = feature_probe_passes and target_probe_passes
        except Exception as exc:
            harfbuzz_result = {"skipped": False, "passes": False, "error": str(exc)}
    else:
        harfbuzz_result = {"skipped": True, "passes": True, "reason": "pass --harfbuzz-python to run the optional probe"}

    checks = {
        "jis_x0208_first_second_and_special_cmap": all(
            coverage[f"jis_x0208_{key}"]["passes"] for key in ("special", "first", "second", "all")
        ),
        "kana_dakuten_handakuten_symbols_fullwidth_halfwidth": all(
            coverage[key]["passes"]
            for key in (
                "kana",
                "hiragana",
                "katakana",
                "dakuten",
                "handakuten",
                "japanese_symbols",
                "ascii_halfwidth",
                "fullwidth_ascii",
                "fullwidth_brackets",
                "fullwidth_macron",
                "halfwidth_katakana",
            )
        ),
        "corpus_missing_zero_and_layouts": corpus_result["passes"],
        "vertical_GSUB_and_vmetrics": vertical["passes"],
        "ttf_woff2_match": ttf_woff2["passes"],
        "license_metadata": license_result["passes"],
        "base_NOS_outlines": base_result["passes"],
        "optional_harfbuzz_probe": harfbuzz_result["passes"],
    }
    passed = all(checks.values())
    report = {
        "font": str(args.font),
        "woff2": str(args.woff2),
        "sha256": {
            "ttf": hashlib.sha256(args.font.read_bytes()).hexdigest(),
            "woff2": hashlib.sha256(args.woff2.read_bytes()).hexdigest(),
        },
        "family": font["name"].getDebugName(1) if "name" in font else None,
        "units_per_em": int(font["head"].unitsPerEm) if "head" in font else None,
        "glyphs": len(font.getGlyphOrder()),
        "cmap_entries": len(cmap),
        "jis_enumeration": {
            "codec": "iso2022_jp strict byte decode",
            "row_ranges": {"special": "0x21-0x2F", "first": "0x30-0x4F", "second": "0x50-0x74"},
            "counts": {key: len(value) for key, value in inventory.items()},
        },
        "coverage": coverage,
        "corpus": corpus_result,
        "vertical": vertical,
        "license": license_result,
        "ttf_woff2": ttf_woff2,
        "base_NOS_outlines": base_result,
        "harfbuzz": harfbuzz_result,
        "checks": checks,
        "passes": passed,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
