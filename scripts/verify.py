"""HarfBuzz shaping, outline invariants, vector logo export, deterministic build."""
from pathlib import Path
import json, hashlib, subprocess, sys
import argparse
from types import SimpleNamespace
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
ROOT=Path(__file__).resolve().parents[1]
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--shaper-python',default=sys.executable)
    args=parser.parse_args()
    shaped=json.loads(subprocess.check_output([args.shaper_python,str(ROOT/'scripts/shape.py')],text=True,encoding='utf-8'))
    ft=TTFont(ROOT/'outputs/LUNARSERIF-Regular.ttf'); gs=ft.getGlyphSet(); order=ft.getGlyphOrder()
    def shape(text,features=None):
        key='plain' if features and features.get('ss01') else 'unkerned' if features and features.get('kern') is False else 'logo' if text=='NOCTISENE' else 'required'
        return SimpleNamespace(glyph_infos=[SimpleNamespace(codepoint=g['id']) for g in shaped[key]],glyph_positions=[SimpleNamespace(**g['position']) for g in shaped[key]])
    logo=shape('NOCTISENE'); plain=shape('NOCTISENE',{'ss01':True}); unkerned=shape('NOCTISENE',{'kern':False})
    assert order[logo.glyph_infos[1].codepoint]=='uni004F'
    assert order[plain.glyph_infos[1].codepoint]=='O.plain'
    adv=sum(p.x_advance for p in logo.glyph_positions)
    before=sum(p.x_advance for p in unkerned.glyph_positions)
    assert adv<before
    text='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ノクティセーヌ夜に、余韻を。'
    assert all(g.codepoint for g in shape(text).glyph_infos)
    assert all(-250<=ft['glyf'][n].yMin and ft['glyf'][n].yMax<=850 for n in order if ft['glyf'][n].numberOfContours)
    x=0;paths=[];gaps=[];prev=None
    for info,pos in zip(logo.glyph_infos,logo.glyph_positions):
        name=order[info.codepoint];glyph=ft['glyf'][name]
        left=x+glyph.xMin
        if prev is not None: gaps.append(left-prev)
        prev=x+glyph.xMax
        pen=SVGPathPen(gs);gs[name].draw(TransformPen(pen,(1,0,0,-1,x+pos.x_offset+80,800-pos.y_offset)))
        paths.append(f'<path d="{pen.getCommands()}"/>');x+=pos.x_advance
    assert min(gaps)>0,gaps
    for mode,bg,fg in [('black','white','#111111'),('white','#111111','white')]:
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {adv+160} 920"><rect width="100%" height="100%" fill="{bg}"/><g fill="{fg}">'+''.join(paths)+'</g></svg>\n'
        (ROOT/'specimens'/f'logo-{mode}.svg').write_text(svg,encoding='utf-8')
    old={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'outputs').glob('*') if p.suffix in ('.ttf','.woff2')}
    subprocess.run([sys.executable,str(ROOT/'scripts/build.py')],check=True,cwd=ROOT)
    new={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'outputs').glob('*') if p.suffix in ('.ttf','.woff2')}
    assert old==new,'Non-deterministic font build'
    report={'engine':'HarfBuzz '+shaped['version'],'logo_glyphs':[order[i.codepoint] for i in logo.glyph_infos],
        'logo_advance_upm':adv,'unkerned_advance_upm':before,'logo_bbox_gaps_upm':gaps,
        'ss01_plain_O':True,'missing_required_glyphs':False,'vertical_bounds_pass':True,
        'repeat_build_identical':True,'sha256':new}
    (ROOT/'verification/shaping.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
if __name__=='__main__': main()
