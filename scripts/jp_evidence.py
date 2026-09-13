"""Tie the final Japanese font, acceptance results and reviewed captures together."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'verification/japanese'
checks = json.loads((OUT / 'checks.json').read_text(encoding='utf-8'))
coverage = json.loads((ROOT / 'outputs/japanese-coverage.json').read_text(encoding='utf-8'))
assert checks['passes'] and checks['glyphs'] == coverage['glyphs']
assert not checks['harfbuzz']['skipped']
assert checks['harfbuzz']['passes']
expected = [f'reference-{i}.png' for i in range(1,10)] + [f'supplement-{i}.png' for i in range(1,4)] + [
    'supplement-vertical.png', 'desktop-hero.png', 'desktop-input-48.png',
    'desktop-input-16.png', 'desktop-plain-o.png', 'desktop-reading.png',
    'desktop-vertical-ruby.png', 'mobile-hero.png', 'mobile-input.png']
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
fonts = {name: digest(ROOT / 'outputs' / name) for name in coverage['files']}
assert fonts == coverage['files']
evidence = {
    'captured_on': '2026-09-13', 'manifest_created_utc': datetime.now(timezone.utc).isoformat(),
    'font_family': coverage['family'], 'version': coverage['version'],
    'encoded_characters': coverage['encoded_characters'], 'glyphs': coverage['glyphs'],
    'font_sha256': fonts, 'checks_sha256': digest(OUT / 'checks.json'),
    'reference_characters_visually_reviewed': 50,
    'supplemental_characters_visually_reviewed': 261,
    'screenshot_count': len(expected),
    'screenshots_sha256': {name: digest(OUT / name) for name in expected},
    'browser_observations': {
        'font_load_nonempty': True, 'plain_o_toggle_changes_visible_glyph': True,
        'sizes_tested_px': [16,24,48], 'vertical_ruby_contained_after_fix': True,
        'missing_unicorn_input_reported': 1,
        'mobile_viewport': {'width':390,'height':844,'horizontal_overflow_count':0},
    },
    'limitations': 'All 15624 characters were checked by cmap; individual visual review covers the reference and supplemental sets plus reading samples.',
}
(OUT / 'evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f"Evidence recorded: {len(expected)} screenshots, {coverage['glyphs']} glyphs")
