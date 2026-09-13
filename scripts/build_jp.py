"""Reproducible Japanese edition: original Latin + credited OFL Shippori Mincho."""
from pathlib import Path
from copy import deepcopy
import hashlib
import json
from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools import subset
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from build import KERN

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'vendor/shippori-mincho/ShipporiMincho-Regular.ttf'
JP = set('ノクティセーヌ夜に、余韻を。')


def supplement_symbols(font):
    """Fill JIS non-kanji and halfwidth gaps without changing existing Japanese."""
    base_order = list(font.getGlyphOrder())
    folder = ROOT / 'vendor/noto-serif-jp'
    provenance = json.loads((folder / 'source.json').read_text(encoding='utf-8'))
    path = folder / 'NotoSerifJP-wght.ttf'
    assert hashlib.sha256(path.read_bytes()).hexdigest() == provenance['sha256']
    required = set(range(0xFF01, 0xFFA0))
    # FF5F/FF60 are white parentheses, included when the donor supplies them.
    for row in range(0x21, 0x75):
        for cell in range(0x21, 0x7F):
            try:
                char = bytes((27, 36, 66, row, cell, 27, 40, 66)).decode('iso2022_jp')
            except UnicodeDecodeError:
                continue
            required.add(ord(char))
    required.add(0xFFE3)  # fullwidth macron
    missing = required - set(font.getBestCmap())
    donor = TTFont(path, recalcTimestamp=False)
    geometric = {0x2252}  # two parallel strokes with opposed dots: approximately equal/image of
    assert not (missing - set(donor.getBestCmap()) - geometric)
    opts = subset.Options()
    opts.layout_features = ['vert', 'vrt2']
    selection = subset.Subsetter(options=opts)
    selection.populate(unicodes=missing - geometric)
    selection.subset(donor)
    donor = instantiateVariableFont(donor, {'wght': 400}, inplace=True)
    assert donor['head'].unitsPerEm == 1000
    glyphset = donor.getGlyphSet()
    vertical_mapping = {}
    for record in donor['GSUB'].table.FeatureList.FeatureRecord:
        if record.FeatureTag not in ('vert', 'vrt2'): continue
        for index in record.Feature.LookupListIndex:
            for table in donor['GSUB'].table.LookupList.Lookup[index].SubTable:
                table = getattr(table, 'ExtSubTable', table)
                vertical_mapping.update(getattr(table, 'mapping', {}))
    added = {}
    alternates = []
    vertical_rules = {}
    for cp, old in sorted(donor.getBestCmap().items()):
        new = f'supplement.uni{cp:04X}'
        pen = DecomposingRecordingPen(glyphset)
        glyphset[old].draw(pen)
        ttpen = TTGlyphPen(None)
        pen.replay(ttpen)
        font['glyf'][new] = ttpen.glyph()
        font['hmtx'][new] = donor['hmtx'][old]
        font['vmtx'][new] = donor['vmtx'][old]
        added[cp] = new
        if old in vertical_mapping:
            vertical_old = vertical_mapping[old]
            vertical_new = new + '.vert'
            pen = DecomposingRecordingPen(glyphset)
            glyphset[vertical_old].draw(pen)
            ttpen = TTGlyphPen(None)
            pen.replay(ttpen)
            font['glyf'][vertical_new] = ttpen.glyph()
            font['hmtx'][vertical_new] = donor['hmtx'][vertical_old]
            font['vmtx'][vertical_new] = donor['vmtx'][vertical_old]
            alternates.append(vertical_new)
            vertical_rules[new] = vertical_new
    # The Google Fonts Japanese subset omits U+2252. Construct this simple
    # mathematical mark explicitly; do not substitute a different Unicode symbol.
    for cp in sorted(missing & geometric):
        new = f'lunar.uni{cp:04X}'
        pen = TTGlyphPen(None)
        for left, bottom, right, top in [(180, 430, 820, 470), (180, 560, 820, 600)]:
            pen.moveTo((left,bottom)); pen.lineTo((left,top)); pen.lineTo((right,top)); pen.lineTo((right,bottom)); pen.closePath()
        for x, y in [(270, 720), (730, 310)]:
            pen.moveTo((x+30,y)); pen.qCurveTo((x+30,y-30),(x,y-30)); pen.qCurveTo((x-30,y-30),(x-30,y)); pen.qCurveTo((x-30,y+30),(x,y+30)); pen.qCurveTo((x+30,y+30),(x+30,y)); pen.closePath()
        font['glyf'][new] = pen.glyph()
        font['hmtx'][new] = (1000, 180)
        font['vmtx'][new] = (1000, 130)
        added[cp] = new
    font.setGlyphOrder(base_order + list(added.values()) + alternates)
    for table in font['cmap'].tables:
        if table.isUnicode() and table.format in (4, 12): table.cmap.update(added)
    provenance['added_characters'] = ''.join(chr(cp) for cp in sorted(added) if cp not in geometric)
    provenance['added_count'] = len(added) - len(missing & geometric)
    provenance['original_geometric_symbols'] = ''.join(chr(cp) for cp in sorted(missing & geometric))
    provenance['vertical_alternates'] = len(alternates)
    provenance['font_copyright'] = donor['name'].getDebugName(0)
    return provenance, vertical_rules


def append_layout(font, extra, tag):
    """Append independent lookups, keeping donor contextual indices untouched."""
    target, source = font[tag].table, extra[tag].table
    offset = len(target.LookupList.Lookup)
    target.LookupList.Lookup.extend(deepcopy(source.LookupList.Lookup))
    target.LookupList.LookupCount = len(target.LookupList.Lookup)
    added = []
    for record in deepcopy(source.FeatureList.FeatureRecord):
        record.Feature.LookupListIndex = [i + offset for i in record.Feature.LookupListIndex]
        existing = [i for i, r in enumerate(target.FeatureList.FeatureRecord) if r.FeatureTag == record.FeatureTag]
        if existing:
            for index in existing:
                feature = target.FeatureList.FeatureRecord[index].Feature
                feature.LookupListIndex.extend(record.Feature.LookupListIndex)
                feature.LookupCount = len(feature.LookupListIndex)
            added.extend(existing)
        else:
            added.append(len(target.FeatureList.FeatureRecord))
            target.FeatureList.FeatureRecord.append(record)
    for script in target.ScriptList.ScriptRecord:
        systems = [script.Script.DefaultLangSys] + [r.LangSys for r in script.Script.LangSysRecord]
        for system in systems:
            if system is not None:
                system.FeatureIndex = sorted(set(system.FeatureIndex) | set(added))
    unsorted = list(target.FeatureList.FeatureRecord)
    target.FeatureList.FeatureRecord.sort(key=lambda r: r.FeatureTag)
    remap = {i: next(j for j, r in enumerate(target.FeatureList.FeatureRecord) if r is record)
             for i, record in enumerate(unsorted)}
    for script in target.ScriptList.ScriptRecord:
        for system in [script.Script.DefaultLangSys] + [r.LangSys for r in script.Script.LangSysRecord]:
            if system is not None:
                system.FeatureIndex = sorted(remap[i] for i in system.FeatureIndex)
                system.FeatureCount = len(system.FeatureIndex)
                if system.ReqFeatureIndex != 0xFFFF:
                    system.ReqFeatureIndex = remap[system.ReqFeatureIndex]
    target.FeatureList.FeatureCount = len(target.FeatureList.FeatureRecord)


def main():
    provenance = json.loads((BASE.parent / 'source.json').read_text(encoding='utf-8'))
    assert hashlib.sha256(BASE.read_bytes()).hexdigest() == provenance['sha256']
    font = TTFont(BASE, recalcTimestamp=False)
    original = TTFont(ROOT / 'outputs/LUNARSERIF-Regular.ttf', recalcTimestamp=False)
    assert font['head'].unitsPerEm == original['head'].unitsPerEm == 1000
    supplemental, vertical_rules = supplement_symbols(font)
    cmap = original.getBestCmap()
    replaced = {cp: name for cp, name in cmap.items() if chr(cp) not in JP}
    names = {name: 'lunar.' + name for name in set(replaced.values()) | {'O.plain'}}
    order = font.getGlyphOrder() + sorted(names.values())
    font.setGlyphOrder(order)
    for old, new in names.items():
        font['glyf'][new] = deepcopy(original['glyf'][old])
        font['hmtx'][new] = original['hmtx'][old]
        glyph = font['glyf'][new]
        font['vmtx'][new] = (1000, 880 - getattr(glyph, 'yMax', 0))
    for table in font['cmap'].tables:
        if table.isUnicode() and table.format in (4, 12):
            table.cmap.update({cp: names[name] for cp, name in replaced.items()})
    # Keep all donor components intact: custom glyphs never overwrite a shared component.
    # Donor kana/J/Q stylistic set moves to ss19 so ss01 remains plain O only.
    for record in font['GSUB'].table.FeatureList.FeatureRecord:
        if record.FeatureTag == 'ss01':
            record.FeatureTag = 'ss19'
    extra = TTFont()
    extra.setGlyphOrder(order)
    fea = 'languagesystem DFLT dflt;\nfeature ss01 { sub lunar.uni004F by lunar.O.plain; } ss01;\nfeature kern {\n'
    for (a, b), value in KERN.items():
        left, right = names[cmap[ord(a)]], names[cmap[ord(b)]]
        fea += f'pos {left} {right} {value};\n'
        if a == 'O': fea += f'pos lunar.O.plain {right} {value};\n'
        if b == 'O': fea += f'pos {left} lunar.O.plain {value};\n'
    fea += '} kern;\n'
    for tag in ('vert', 'vrt2'):
        fea += f'feature {tag} {{\n' + ''.join(f'sub {old} by {new};\n' for old, new in vertical_rules.items()) + f'}} {tag};\n'
    addOpenTypeFeaturesFromString(extra, fea)
    for tag in ('GSUB', 'GPOS'):
        append_layout(font, extra, tag)
    if 'DSIG' in font: del font['DSIG']
    name = font['name']
    copyright_text = (name.getDebugName(0) or '') + '; ' + supplemental['font_copyright'] + '; Supplementary glyphs Copyright 2012 Google Inc. All Rights Reserved.; Original LUNAR SERIF Latin outlines Copyright 2026 NOCTISENE contributors.'
    values = {0: copyright_text, 1: 'LUNAR SERIF JP', 2: 'Regular',
              3: 'NOCTISENE:LUNARSERIFJP:1.000', 4: 'LUNAR SERIF JP Regular',
              5: 'Version 1.000', 6: 'LUNARSERIFJP-Regular',
              8: 'NOCTISENE contributors; Japanese base: The Shippori Mincho Project Authors',
              9: 'Original Latin: NOCTISENE contributors; Japanese: Shippori Mincho Project Authors',
              10: 'Original LUNAR SERIF Latin with Japanese glyphs derived from Shippori Mincho, supplemented by Noto Serif JP symbols and halfwidth kana. ss01: plain O; ss19: donor stylistic set.',
              11: 'https://github.com/Sunwood-ai-labs/lunar-serif',
              12: 'https://github.com/fontdasu/ShipporiMincho',
              13: 'Licensed under the SIL Open Font License, Version 1.1. See LUNAR-SERIF-JP-OFL.txt.',
              14: 'https://openfontlicense.org', 16: 'LUNAR SERIF JP', 17: 'Regular'}
    name.names = [r for r in name.names if r.nameID not in values]
    for key, value in values.items():
        name.setName(value, key, 3, 1, 0x409)
    font['head'].fontRevision = 1.0
    font['head'].created = font['head'].modified = 3872102400
    font['OS/2'].fsType = 0
    font['OS/2'].usWeightClass = 400
    font['OS/2'].recalcUnicodeRanges(font)
    font['OS/2'].recalcAvgCharWidth(font)
    path = ROOT / 'outputs/LUNARSERIFJP-Regular.ttf'
    font.save(path)
    font.flavor = 'woff2'
    font.save(path.with_suffix('.woff2'))
    license_text = (BASE.parent / 'OFL.txt').read_text(encoding='utf-8')
    license_text = license_text.replace('This Font Software is licensed',
        supplemental['font_copyright'] + '\nCopyright 2012 Google Inc. All Rights Reserved. (Noto Serif JP supplementary glyphs).\nCopyright 2026 NOCTISENE contributors (original LUNAR SERIF Latin outlines and integration).\n\nThis Font Software is licensed', 1)
    (ROOT / 'outputs/LUNAR-SERIF-JP-OFL.txt').write_text(license_text, encoding='utf-8')
    report = {'family': 'LUNAR SERIF JP', 'version': '1.000',
              'characters': ''.join(chr(cp) for cp in sorted(font.getBestCmap())),
              'encoded_characters': len(font.getBestCmap()), 'glyphs': len(order),
              'original_latin_characters': len(replaced), 'donor': provenance, 'supplement': supplemental,
              'files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (path, path.with_suffix('.woff2'))}}
    (ROOT / 'outputs/japanese-coverage.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"Built JP: {len(order)} glyphs / {len(font.getBestCmap())} characters; {len(replaced)} original Latin mappings")


if __name__ == '__main__':
    main()
