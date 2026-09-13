"""Build directly from editable SVG outlines and metrics.json."""
from pathlib import Path
import json, xml.etree.ElementTree as ET, hashlib
import pathops
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.svgLib.path import parse_path
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString

ROOT=Path(__file__).resolve().parents[1]
KERN={('N','O'):-24,('O','C'):-18,('C','T'):-16,('T','I'):-19,('I','S'):-10,('S','E'):-10,('E','N'):-8,('N','E'):-10,
      ('A','V'):-62,('A','W'):-43,('A','Y'):-61,('T','A'):-52,('T','o'):-57,('T','a'):-49,('T','e'):-50,
      ('V','A'):-62,('V','o'):-42,('W','A'):-43,('Y','A'):-61,('Y','o'):-58,('L','T'):-29,('L','Y'):-40,
      ('F','o'):-30,('P','a'):-24,('r','.'):-23,('v','a'):-14,('w','a'):-12}
def main():
    meta=json.loads((ROOT/'sources/metrics.json').read_text(encoding='utf-8'))
    order=['.notdef']+[n for n in meta if n!='.notdef']
    glyphs={}; metrics={}; cmap={}; stats={}
    for name in order:
        svg=ET.parse(ROOT/'sources/glyphs'/f'{name}.svg')
        path=pathops.Path()
        for el in svg.iter('{http://www.w3.org/2000/svg}path'):
            parse_path(el.attrib['d'],path.getPen())
        if len(path): path=pathops.simplify(path,fix_winding=True)
        pen=TTGlyphPen(None)
        path.draw(Cu2QuPen(pen,max_err=.45,reverse_direction=True))
        glyph=pen.glyph(); glyphs[name]=glyph
        if glyph.numberOfContours:
            glyph.recalcBounds(None); lsb=glyph.xMin
            stats[name]=[glyph.xMin,glyph.yMin,glyph.xMax,glyph.yMax]
        else: lsb=0
        metrics[name]=(meta[name]['advance'],lsb)
        if meta[name]['char']: cmap[ord(meta[name]['char'])]=name
    fb=FontBuilder(1000,isTTF=True)
    fb.setupGlyphOrder(order); fb.setupCharacterMap(cmap); fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics); fb.setupHorizontalHeader(ascent=850,descent=-250,lineGap=80)
    fb.setupNameTable({'familyName':'LUNAR SERIF','styleName':'Regular','uniqueFontIdentifier':'NOCTISENE:LUNARSERIF:1.000',
        'fullName':'LUNAR SERIF Regular','psName':'LUNARSERIF-Regular','version':'Version 1.000',
        'copyright':'Original outlines created for NOCTISENE, 2026. See LICENSE.txt.',
        'description':'Original high-contrast display serif with a crescent and star O. ss01 selects plain O.',
        'licenseDescription':'See accompanying LICENSE.txt for the font and source usage grant.'})
    fb.setupOS2(version=4,sTypoAscender=850,sTypoDescender=-250,sTypoLineGap=80,usWinAscent=850,usWinDescent=250,
        sxHeight=460,sCapHeight=700,usWeightClass=400,usWidthClass=5,fsSelection=0xC0,fsType=0)
    fb.setupPost(); fb.setupMaxp()
    features='languagesystem DFLT dflt;\nlanguagesystem latn dflt;\nfeature ss01 { sub uni004F by O.plain; } ss01;\nfeature kern {\n'
    for (a,b),v in KERN.items():
        features+=f'pos uni{ord(a):04X} uni{ord(b):04X} {v};\n'
        if a=='O': features+=f'pos O.plain uni{ord(b):04X} {v};\n'
        if b=='O': features+=f'pos uni{ord(a):04X} O.plain {v};\n'
    features+='} kern;\n'
    (ROOT/'sources/features.fea').write_text(features,encoding='utf-8')
    addOpenTypeFeaturesFromString(fb.font,features)
    # Legacy kern supports simple rasterizers; modern shapers use GPOS.
    from fontTools.ttLib import newTable
    from fontTools.ttLib.tables._k_e_r_n import KernTable_format_0
    kern=newTable('kern'); kern.version=0
    sub=KernTable_format_0(); sub.version=0; sub.coverage=1
    sub.kernTable={(f'uni{ord(a):04X}',f'uni{ord(b):04X}'):v for (a,b),v in KERN.items()}
    kern.kernTables=[sub]; fb.font['kern']=kern
    fb.font['head'].created=3872102400; fb.font['head'].modified=3872102400
    fb.font.recalcTimestamp=False
    out=ROOT/'outputs/LUNARSERIF-Regular.ttf'; fb.save(out)
    fb.font.flavor='woff2'; fb.font.save(ROOT/'outputs/LUNARSERIF-Regular.woff2')
    report={'glyphs':len(order),'encoded_characters':len(cmap),'characters':''.join(chr(c) for c in sorted(cmap)),
            'bounds':stats,'kerning_pairs':len(KERN),'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'outputs').glob('*') if p.suffix in ('.ttf','.woff2')}}
    (ROOT/'verification/build.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Built {len(order)} glyphs / {len(cmap)} encoded characters. TTF + WOFF2.')
if __name__=='__main__': main()
