"""Rasterize actual edition fonts for comparison with the two approved images."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from build import KERN
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'verification/editions'
OUT.mkdir(parents=True,exist_ok=True)
for edition in ['Text','Title']:
    path=ROOT/'outputs'/f'LUNARSERIF{edition}-Regular.ttf'
    im=Image.new('RGB',(1600,1100),'#faf8f0');d=ImageDraw.Draw(im)
    label=ImageFont.load_default(24)
    d.text((60,28),f'LUNAR SERIF {edition} / ACTUAL FONT',font=label,fill='#44434b')
    for text,y,width in [('NOCTISENE',130,1480),('ABCDEFGHI',450,1480),('JKLMNOPQR',630,1480),('STUVWXYZ',810,1480)]:
        size=230 if y==130 else 155
        font=ImageFont.truetype(str(path),size)
        if y==130:
            while d.textlength(text,font=font)>width:
                size-=1;font=ImageFont.truetype(str(path),size)
            d.text(((1600-d.textlength(text,font=font))/2,y),text,font=font,fill='#44434b',anchor='lt')
        else:
            cell=width/len(text)
            for i,c in enumerate(text):
                d.text((60+(i+.5)*cell,y),c,font=font,fill='#44434b',anchor='mt')
    im.save(OUT/f'{edition.lower()}-actual.png')
    ft=TTFont(path);gs=ft.getGlyphSet();cmap=ft.getBestCmap();x=0;commands=[]
    for i,c in enumerate('NOCTISENE'):
        name=cmap[ord(c)];pen=SVGPathPen(gs)
        gs[name].draw(TransformPen(pen,(1,0,0,-1,x+45,850)))
        commands.append(pen.getCommands())
        x+=ft['hmtx'][name][0]+(KERN.get((c,'NOCTISENE'[i+1]),0) if i<8 else 0)
    (ROOT/'specimens'/f'{edition.lower()}-logo.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x+90} 1100" role="img" aria-label="NOCTISENE"><path fill="#44434b" d="'+''.join(commands)+'"/></svg>\n',encoding='utf-8')
print('Rendered both actual TTF specimens.')
