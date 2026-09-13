"""Build the approved Latin text and title editions from original editable curves."""
from pathlib import Path
import copy
import json
import re
import design
import build
import pathops
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path

ROOT=Path(__file__).resolve().parents[1]

def emit(glyphs, destination):
    (destination/'glyphs').mkdir(parents=True,exist_ok=True)
    metadata={}
    for name,g in glyphs.items():
        p=''
        for raw in re.findall(r'M[^M]*?Z',g['path']):
            contour=pathops.Path(); parse_path(raw,contour.getPen())
            if contour.clockwise != (raw in design.HOLES): contour.reverse()
            pen=SVGPathPen(None); contour.draw(pen); p+=pen.getCommands()
        if 'transform' in g:
            pen=SVGPathPen(None); parse_path(p,TransformPen(pen,g['transform'])); p=pen.getCommands()
        (destination/'glyphs'/f'{name}.svg').write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {g["width"]} 1100"><g transform="translate(0 820) scale(1 -1)"><path d="{p}" fill="black"/></g></svg>\n',encoding='utf-8')
        metadata[name]={'char':g['char'],'advance':g['width']}
    (destination/'metrics.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    normal=copy.deepcopy(design.G)
    title=copy.deepcopy(design.G)
    for key,glyphs,family in [('text',normal,'LUNAR SERIF Text'),('title',title,'LUNAR SERIF Title')]:
        reference=ROOT/'sources'/f'{key}-reference.json'
        if not reference.exists():
            raise FileNotFoundError(str(reference))
        if reference.exists():
            for name,g in json.loads(reference.read_text(encoding='utf-8')).items():
                # S has no counter; remove the generated reference's stray hairline slit.
                if g['char']=='S':g['contours']=[c for c in g['contours'] if not c['hole']]
                glyphs[name]={'char':g['char'],'width':g['advance'],'path':''.join(c['path'] for c in g['contours'])}
                design.HOLES.update(c['path'] for c in g['contours'] if c['hole'])
            # A metric-compatible plain alternate for the title O.
            if key=='text': glyphs['O.plain']=dict(glyphs['uni004F'],char=None)
            else:
                g=glyphs['uni004F']; plain=copy.deepcopy(normal['O.plain'])
                plain['transform']=(g['width']/plain['width'],0,0,1,0,0);plain['width']=g['width']
                glyphs['O.plain']=plain
        source=ROOT/'sources'/key
        emit(glyphs,source)
        build.main(source,'LUNARSERIF'+key.title()+'-Regular',family,'1.000')
    print('Built Text and Title editions; legacy and JP binaries preserved.')

if __name__=='__main__': main()
