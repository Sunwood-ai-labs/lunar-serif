"""Check both approved editions: binaries, alternates, outlines and all pairs."""
from pathlib import Path
import json,hashlib
import pathops
from fontTools.ttLib import TTFont
from fontTools.pens.transformPen import TransformPen
from build import KERN
ROOT=Path(__file__).resolve().parents[1];reports={}
for edition in ['Text','Title']:
    base='LUNARSERIF'+edition+'-Regular'
    font=TTFont(ROOT/'outputs'/f'{base}.ttf');web=TTFont(ROOT/'outputs'/f'{base}.woff2')
    cmap=font.getBestCmap();assert cmap==web.getBestCmap()
    assert all(i in cmap for i in range(32,127))
    assert font['name'].getDebugName(1)=='LUNAR SERIF '+edition
    assert font['OS/2'].fsType==0
    for n in font.getGlyphOrder():
        a=font['glyf'][n];b=web['glyf'][n]
        assert a.getCoordinates(font['glyf'])==b.getCoordinates(web['glyf']),n
        if a.numberOfContours:
            assert a.yMin>=-250 and a.yMax<=850,(n,a.yMin,a.yMax)
    assert font['hmtx']['O.plain'][0]==font['hmtx'][cmap[79]][0]
    substitutions={}
    for lookup in font['GSUB'].table.LookupList.Lookup:
        for subtable in lookup.SubTable:substitutions.update(getattr(subtable,'mapping',{}))
    assert substitutions[cmap[79]]=='O.plain'
    gs=font.getGlyphSet();chars={chr(c):n for c,n in cmap.items() if font['glyf'][n].numberOfContours}
    paths={}
    for c,n in chars.items():
        p=pathops.Path();gs[n].draw(p.getPen());paths[c]=p
        assert abs(p.area)>0,n
    collisions=[]
    for a,an in chars.items():
        A=font['glyf'][an]
        for b,bn in chars.items():
            B=font['glyf'][bn];shift=font['hmtx'][an][0]+KERN.get((a,b),0)
            if A.xMax<=shift+B.xMin or A.yMax<=B.yMin or B.yMax<=A.yMin:continue
            p=pathops.Path();gs[bn].draw(TransformPen(p.getPen(),(1,0,0,1,shift,0)))
            area=abs(pathops.op(paths[a],p,pathops.PathOp.INTERSECTION).area)
            if area>.1:collisions.append({'pair':a+b,'area':round(area,3)})
    reports[edition]={'characters':len(cmap),'glyphs':len(font.getGlyphOrder()),'pairs_checked':len(chars)**2,'collisions':collisions,'ttf_woff2_equal':True,'plain_o_substitution':True,'sha256':{suffix:hashlib.sha256((ROOT/'outputs'/f'{base}.{suffix}').read_bytes()).hexdigest() for suffix in ['ttf','woff2']}}
    alternate_collisions=[]
    alternate_chars=dict(chars,O='O.plain')
    for a,b in [(a,b) for a in chars for b in chars if a=='O' or b=='O']:
        an,bn=alternate_chars[a],alternate_chars[b]
        p=pathops.Path();q=pathops.Path();gs[an].draw(p.getPen())
        shift=font['hmtx'][an][0]+KERN.get((a,b),0)
        gs[bn].draw(TransformPen(q.getPen(),(1,0,0,1,shift,0)))
        area=abs(pathops.op(p,q,pathops.PathOp.INTERSECTION).area)
        if area>.1:alternate_collisions.append(a+b)
    reports[edition]['plain_o_collisions']=alternate_collisions
(ROOT/'verification/editions/checks.json').write_text(json.dumps(reports,indent=2)+'\n')
print(json.dumps(reports,indent=2))
assert not any(r['collisions'] for r in reports.values()),'Adjacent glyph collisions'
assert not any(r['plain_o_collisions'] for r in reports.values()),'Alternate O collisions'
