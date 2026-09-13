"""Check every encoded visible pair for actual filled-outline intersections."""
from pathlib import Path
import json
import pathops
from fontTools.ttLib import TTFont
from fontTools.pens.transformPen import TransformPen
from build import KERN
ROOT=Path(__file__).resolve().parents[1]
font=TTFont(ROOT/'outputs/LUNARSERIF-Regular.ttf'); gs=font.getGlyphSet()
chars={chr(c):n for c,n in font.getBestCmap().items() if font['glyf'][n].numberOfContours}
paths={}
for c,n in chars.items():
    p=pathops.Path();gs[n].draw(p.getPen());paths[c]=p
collisions=[];examined=0
for a,an in chars.items():
    A=font['glyf'][an]
    for b,bn in chars.items():
        B=font['glyf'][bn];shift=font['hmtx'][an][0]+KERN.get((a,b),0)
        if A.xMax<=shift+B.xMin or A.yMax<=B.yMin or B.yMax<=A.yMin:continue
        examined+=1
        p=pathops.Path();gs[bn].draw(TransformPen(p.getPen(),(1,0,0,1,shift,0)))
        intersection=pathops.op(paths[a],p,pathops.PathOp.INTERSECTION)
        if abs(intersection.area)>.1:collisions.append({'pair':a+b,'area_upm2':round(abs(intersection.area),3)})
report={'visible_characters':len(chars),'pairs_checked':len(chars)**2,'bbox_overlap_pairs':examined,'filled_outline_collisions':collisions}
(ROOT/'verification/audit/spacing.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
assert not collisions,'Adjacent glyphs intersect; revise spacing'
