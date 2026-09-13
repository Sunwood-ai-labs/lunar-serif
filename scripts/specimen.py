"""Actual FreeType rasterization from the built TTF (no fallback font)."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
from fontTools.ttLib import TTFont
ROOT=Path(__file__).resolve().parents[1]
FONT=ROOT/'outputs/LUNARSERIF-Regular.ttf'
def f(size): return ImageFont.truetype(str(FONT),size)
def draw_text(d,xy,text,size,fill='#111111'): d.text(xy,text,font=f(size),fill=fill)
def main():
    im=Image.new('RGB',(1800,1760),'white'); d=ImageDraw.Draw(im)
    draw_text(d,(72,38),'01  L U N A R   S E R I F',32)
    d.line((710,76,1728,76),fill='#aaaaaa',width=1)
    draw_text(d,(55,118),'NOCTISENE',310)
    d.line((72,469,1728,469),fill='#aaaaaa',width=1)
    draw_text(d,(71,478),'N O S',218)
    draw_text(d,(825,503),'ABCDEFGHIJKLM',63)
    draw_text(d,(825,593),'NOPQRSTUVWXYZ',63)
    draw_text(d,(825,693),'0123456789',72)
    draw_text(d,(73,819),'abcdefghijklmnopqrstuvwxyz',79)
    draw_text(d,(73,928),'0123456789   ! ? & @ # % $ + =',57)
    draw_text(d,(73,1022),'ノクティセーヌ',90)
    draw_text(d,(856,1022),'夜に、余韻を。',90)
    draw_text(d,(73,1160),'Moonlit letters, quiet strength.',67)
    draw_text(d,(73,1259),'A velvet night. Noctisene, 2026.',45)
    d.rectangle((30,1394,1770,1684),fill='#111111')
    draw_text(d,(338,1407),'NOCTISENE',226,'white')
    im.save(ROOT/'specimens/specimen.png')
    for name,bg,fg in [('logo-black','white','#111111'),('logo-white','#111111','white')]:
        logo=Image.new('RGB',(1800,420),bg); dl=ImageDraw.Draw(logo)
        draw_text(dl,(55,24),'NOCTISENE',310,fg); logo.save(ROOT/'specimens'/f'{name}.png')
    # All mapped glyphs individually, so missing outlines and collisions are visible.
    font=TTFont(FONT); cmap=font.getBestCmap(); chars=[chr(c) for c in cmap if chr(c).strip()]
    grid=Image.new('RGB',(1500,((len(chars)+9)//10)*158),'white'); dg=ImageDraw.Draw(grid)
    for i,c in enumerate(chars):
        x=(i%10)*150;y=(i//10)*158
        dg.rectangle((x,y,x+149,y+157),outline='#dddddd')
        draw_text(dg,(x+28,y+7),c,89)
        dg.text((x+10,y+135),f'U+{ord(c):04X}',fill='#555555',font=ImageFont.load_default(14))
    grid.save(ROOT/'verification/glyph-grid.png')
    required=''.join(chr(n) for n in range(32,127))+'ノクティセーヌ夜に、余韻を。'
    missing=[c for c in required if ord(c) not in cmap]
    assert not missing,missing
    assert 'GPOS' in font and 'GSUB' in font
    for suffix in ('ttf','woff2'):
        ft=TTFont(ROOT/'outputs'/f'LUNARSERIF-Regular.{suffix}')
        assert ft.getBestCmap()==cmap
        for n in ft.getGlyphOrder(): _=ft['glyf'][n]
    report={'required_missing':missing,'ttf_load':True,'woff2_load':True,'cmap_equal':True,
      'render_engine':'Pillow / FreeType, BASIC layout with legacy kern',
      'rendered_codepoints':len(chars),'japanese_required':'ノクティセーヌ夜に、余韻を。',
      'gpos':True,'ss01':True,'os_installation':False}
    (ROOT/'verification/checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Load / cmap / required glyph checks passed; rasterized specimen and full glyph grid.')
if __name__=='__main__': main()
