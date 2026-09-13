"""Reconstruct the 14 reference Japanese glyphs as editable, smoothed outlines.

This traces the supplied generated concept image, never an installed font.
The source is low resolution; preserve its brush shapes without claiming
information that the raster does not contain.
"""
from pathlib import Path
from collections import defaultdict
from PIL import Image
import json,math
ROOT=Path(__file__).resolve().parents[1]
image=Image.open(ROOT/'references/01-lunar-serif.png').convert('L')
ledger=json.loads((ROOT/'verification/audit/ledger.json').read_text(encoding='utf-8'))

def simplify(points,tolerance=.9):
    if len(points)<3:return points
    a,b=points[0],points[-1];dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
    distances=[abs(dx*(a[1]-p[1])-(a[0]-p[0])*dy)/length if length else math.dist(a,p) for p in points]
    index=max(range(len(points)),key=lambda i:distances[i])
    if distances[index]<=tolerance:return [a,b]
    return simplify(points[:index+1],tolerance)[:-1]+simplify(points[index:],tolerance)

def contours(box):
    x0,y0,x1,y1=box
    black={(x,y) for y in range(y0,y1) for x in range(x0,x1) if image.getpixel((x,y))<150}
    edges=set()
    for x,y in black:
        for a,b,n in [((x,y),(x+1,y),(x,y-1)),((x+1,y),(x+1,y+1),(x+1,y)),((x+1,y+1),(x,y+1),(x,y+1)),((x,y+1),(x,y),(x-1,y))]:
            if n not in black:edges.add((a,b))
    result=[]
    while edges:
        first=min(edges);edges.remove(first);pts=[first[0],first[1]]
        while pts[-1]!=pts[0]:
            candidates=sorted(e for e in edges if e[0]==pts[-1])
            if not candidates:raise ValueError('Unclosed raster boundary')
            edge=candidates[0];edges.remove(edge);pts.append(edge[1])
        pts.pop()
        if len(pts)<8:continue
        split=max(range(len(pts)),key=lambda i:math.dist(pts[0],pts[i]))
        reduced=simplify(pts[:split+1])[:-1]+simplify(pts[split:]+pts[:1])[:-1]
        result.append(reduced)
    return result

out={}
for c in 'ノクティセーヌ夜に、余韻を。':
    name=f'uni{ord(c):04X}';box=ledger[name]['reference_roi']
    # Pad measured black bounds to retain antialias edge pixels.
    box=[box[0]-1,box[1]-1,box[2]+1,box[3]+1]
    kana=c in 'ノクティセーヌ';scale=14 if kana else 10
    baseline=704 if kana else 803
    width=800 if kana else (350 if c in '、。' else 850)
    ink_width=(box[2]-box[0])*scale;left=(width-ink_width)/2
    pieces=[]
    for points in contours(box):
        pts=[((x-box[0])*scale+left,(baseline-y)*scale) for x,y in points]
        area=sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(pts,pts[1:]+pts[:1]))/2
        if abs(area)<20:continue
        corners=[]
        for i,p in enumerate(pts):
            a,n=pts[i-1],pts[(i+1)%len(pts)]
            u=(p[0]-a[0],p[1]-a[1]);v=(n[0]-p[0],n[1]-p[1])
            cosine=(u[0]*v[0]+u[1]*v[1])/(math.hypot(*u)*math.hypot(*v))
            t=.12 if cosine<.57 and min(math.hypot(*u),math.hypot(*v))>scale*2.5 else .5
            if c=='。':t=.5
            enter=(p[0]+t*(a[0]-p[0]),p[1]+t*(a[1]-p[1]))
            leave=(p[0]+t*(n[0]-p[0]),p[1]+t*(n[1]-p[1]))
            corners.append((enter,p,leave))
        path=f'M {corners[0][0][0]:.3f} {corners[0][0][1]:.3f}'
        for i,(enter,p,leave) in enumerate(corners):
            nxt=corners[(i+1)%len(corners)][0]
            path+=f' Q {p[0]:.3f} {p[1]:.3f} {leave[0]:.3f} {leave[1]:.3f} L {nxt[0]:.3f} {nxt[1]:.3f}'
        path+=' Z'
        pieces.append({'path':path,'hole':area>0})
    out[name]={'char':c,'advance':width,'contours':pieces,'reference_roi':box,'scale':scale,'baseline':baseline}
(ROOT/'sources/japanese-reference.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Traced {len(out)} reference Japanese glyphs')
