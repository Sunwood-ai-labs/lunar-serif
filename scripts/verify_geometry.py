"""Regressions found by visual inspection, plus all-glyph bounds and coverage."""
from pathlib import Path
import json
from fontTools.ttLib import TTFont
ROOT=Path(__file__).resolve().parents[1]
f=TTFont(ROOT/'outputs/LUNARSERIF-Regular.ttf')
counts={n:f['glyf'][n].numberOfContours for n in f.getGlyphOrder()}
assert counts['uni0038']==3,'8 must have one outer contour and two counters'
assert counts['uni0067']==3,'g must have a connected body and two counters'
assert counts['uni006A']==2,'j needs one connected stem/hook plus its dot'
assert counts['uni201C']==counts['uni201D']==2,'double quotes need two separate comma outlines'
for n in ['uni201C','uni201D']:
    g=f['glyf'][n]; coords=g.coordinates; ends=g.endPtsOfContours
    parts=[list(coords[:ends[0]+1]),list(coords[ends[0]+1:ends[1]+1])]
    boxes=[(min(x for x,y in p),min(y for x,y in p),max(x for x,y in p),max(y for x,y in p)) for p in parts]
    assert boxes[0][1:4:2]==boxes[1][1:4:2],boxes
    assert abs(boxes[0][0]-boxes[1][0])==144,boxes
for n in f.getGlyphOrder():
    g=f['glyf'][n]
    if g.numberOfContours: assert -250<=g.yMin<g.yMax<=850,(n,g.yMin,g.yMax)
pages=json.loads((ROOT/'verification/audit/pages.json').read_text(encoding='utf-8'))
listed=[n for v in pages.values() for n in v]
assert len(listed)==len(set(listed))==len(f.getGlyphOrder())==120
assert set(listed)==set(f.getGlyphOrder())
report={'glyphs_covered':len(listed),'duplicate_audit_entries':0,'all_vertical_bounds':True,'regression_contours':{n:counts[n] for n in ['uni0038','uni0067','uni006A','uni201C','uni201D']},'double_quote_translation_exact':True}
(ROOT/'verification/audit/geometry.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
