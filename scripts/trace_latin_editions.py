"""Reconstruct approved image capitals as editable cubic curves, not font copies.

The input is a raster design proposal. Pixel boundaries are simplified and
rounded; sharp corners remain sharp. The source ledger retains every image ROI.
"""
from pathlib import Path
from collections import defaultdict
from itertools import groupby
import json
import math
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]

def fit(points,error=1.0):
    """Least-squares cubic fitting, recursively split at maximum deviation."""
    def add(a,b):return (a[0]+b[0],a[1]+b[1])
    def sub(a,b):return (a[0]-b[0],a[1]-b[1])
    def mul(a,t):return (a[0]*t,a[1]*t)
    def dot(a,b):return a[0]*b[0]+a[1]*b[1]
    def unit(a):return mul(a,1/(math.hypot(*a) or 1))
    def rec(p,t1,t2):
        if len(p)==2:
            d=math.dist(*p)/3
            return [(p[0],add(p[0],mul(t1,d)),add(p[-1],mul(t2,d)),p[-1])]
        u=[0.]
        for a,b in zip(p,p[1:]):u.append(u[-1]+math.dist(a,b))
        u=[v/u[-1] for v in u]
        c00=c01=c11=x0=x1=0.
        for q,t in zip(p,u):
            b0=(1-t)**3;b1=3*t*(1-t)**2;b2=3*t*t*(1-t);b3=t**3
            a1=mul(t1,b1);a2=mul(t2,b2)
            v=sub(q,add(mul(p[0],b0+b1),mul(p[-1],b2+b3)))
            c00+=dot(a1,a1);c01+=dot(a1,a2);c11+=dot(a2,a2);x0+=dot(a1,v);x1+=dot(a2,v)
        det=c00*c11-c01*c01
        a=(x0*c11-x1*c01)/det if abs(det)>1e-9 else 0
        b=(c00*x1-c01*x0)/det if abs(det)>1e-9 else 0
        dist=math.dist(p[0],p[-1])
        if min(a,b)<dist*1e-5 or max(a,b)>dist*3:a=b=dist/3
        ctrl=(p[0],add(p[0],mul(t1,a)),add(p[-1],mul(t2,b)),p[-1])
        errors=[]
        for q,t in zip(p,u):
            v=(0.,0.)
            for c,w in zip(ctrl,[(1-t)**3,3*t*(1-t)**2,3*t*t*(1-t),t**3]):v=add(v,mul(c,w))
            errors.append(math.dist(q,v))
        split=max(range(1,len(p)-1),key=lambda i:errors[i])
        if errors[split]<=error:return [ctrl]
        tangent=unit(sub(p[max(0,split-12)],p[min(len(p)-1,split+12)]))
        return rec(p[:split+1],t1,tangent)+rec(p[split:],mul(tangent,-1),t2)
    return rec(points,unit(sub(points[min(12,len(points)-1)],points[0])),unit(sub(points[max(0,len(points)-13)],points[-1])))

def simplify(pts,tol):
    if len(pts)<3:return pts
    a,b=pts[0],pts[-1];dx,dy=b[0]-a[0],b[1]-a[1];n=math.hypot(dx,dy)
    dist=[abs(dx*(a[1]-p[1])-(a[0]-p[0])*dy)/n if n else math.dist(a,p) for p in pts]
    i=max(range(len(pts)),key=lambda i:dist[i])
    if dist[i]<=tol:return [a,b]
    return simplify(pts[:i+1],tol)[:-1]+simplify(pts[i:],tol)

def trace(im,box,baseline,scale):
    x0,y0,x1,y1=box
    # Recover subpixel boundaries from antialias coverage before fitting curves.
    zoom=4
    raster=im.crop(box).resize(((x1-x0)*zoom,(y1-y0)*zoom),Image.Resampling.BICUBIC)
    black={(x,y) for y in range(raster.height) for x in range(raster.width) if raster.getpixel((x,y))<170}
    edges=set()
    for x,y in black:
        for a,b,n in [((x,y),(x+1,y),(x,y-1)),((x+1,y),(x+1,y+1),(x+1,y)),((x+1,y+1),(x,y+1),(x,y+1)),((x,y+1),(x,y),(x-1,y))]:
            if n not in black:edges.add((a,b))
    links=defaultdict(set)
    for a,b in edges:links[a].add(b)
    curves=[]
    while edges:
        a,b=min(edges);edges.remove((a,b));links[a].remove(b);pts=[a,b]
        while pts[-1]!=pts[0]:
            a=pts[-1];b=min(links[a]);links[a].remove(b);edges.remove((a,b));pts.append(b)
        pts.pop()
        area=sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(pts,pts[1:]+pts[:1]))/2
        if abs(area)<3*zoom*zoom:continue
        pts=[(x/zoom+x0,y/zoom+y0) for x,y in pts]
        split=max(range(len(pts)),key=lambda i:math.dist(pts[0],pts[i]))
        segments=fit(pts[:split+1],.9)+fit(pts[split:]+pts[:1],.9)
        def transform(p):return ((p[0]-x0)*scale+34,(baseline-p[1])*scale)
        path='M %.3f %.3f'%transform(segments[0][0])
        for segment in segments:
            path+=' C '+' '.join('%.3f %.3f'%transform(p) for p in segment[1:])
        curves.append({'path':path+' Z','hole':area<0})
    return curves

def main():
    specs={
      'text':('06-lunar-serif-latin-capitals.png',[(105,269,266,151),(311,501,474,154),(522,692,685,153)]),
      'title':('10-lunar-serif-crescent-c.png',[(502,621,610,97),(658,795,767,99),(811,930,922,99)])}
    for edition,(filename,rows) in specs.items():
        im=Image.open(ROOT/'references'/filename).convert('L');ledger={}
        for letters,(y0,y1,baseline,height) in zip(['ABCDEFGHI','JKLMNOPQR','STUVWXYZ'],rows):
            projection=[any(im.getpixel((x,y))<170 for y in range(y0,y1)) for x in range(im.width)]
            runs=[];x=0
            for ink,values in groupby(projection):
                n=len(list(values))
                if ink:runs.append((x,x+n))
                x+=n
            assert len(runs)==len(letters),(edition,letters,runs)
            for c,(left,right) in zip(letters,runs):
                box=[left-1,y0,right+1,y1];scale=700/height
                curves=trace(im,box,baseline,scale)
                ledger[f'uni{ord(c):04X}']={'char':c,'advance':round((right-left+2)*scale+68),'contours':curves,'reference':filename,'roi':box,'baseline':baseline,'scale':scale}
        (ROOT/'sources'/f'{edition}-reference.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
        print(edition, len(ledger),'reference glyphs reconstructed')
if __name__=='__main__':main()
