"""Compare all 52 accepted capitals with real TTF rasterizations."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont,ImageChops
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'verification/editions'
OUT.mkdir(parents=True,exist_ok=True)
records=[];html=[]
for edition in ['text','title']:
    ledger=json.loads((ROOT/'sources'/f'{edition}-reference.json').read_text())
    font=ImageFont.truetype(str(ROOT/'outputs'/f'LUNARSERIF{edition.title()}-Regular.ttf'),180)
    cells=[]
    for name,g in ledger.items():
        reference=Image.open(ROOT/'references'/g['reference']).convert('L').crop(g['roi'])
        mask=reference.point(lambda x:255 if x<170 else 0);reference=mask.crop(mask.getbbox())
        actual=Image.new('L',(500,400));d=ImageDraw.Draw(actual);d.text((100,200),g['char'],font=font,fill=255,anchor='ls')
        actual=actual.crop(actual.getbbox())
        widths=[];normalized=[]
        for im in [reference,actual]:
            w=round(im.width*120/im.height);widths.append(w)
            resized=im.resize((w,120),Image.Resampling.LANCZOS)
            cell=Image.new('L',(220,150));cell.paste(resized,((220-w)//2,15));normalized.append(cell)
        a,b=[im.point(lambda p:255 if p>127 else 0) for im in normalized]
        intersection=sum(ImageChops.multiply(a,b).histogram()[1:]);union=sum(ImageChops.lighter(a,b).histogram()[1:])
        iou=intersection/union
        records.append({'edition':edition,'char':g['char'],'roi':g['roi'],'silhouette_iou':round(iou,4),'width_ratio':round(widths[1]/widths[0],4)})
        cell=Image.new('RGB',(460,210),'white');dc=ImageDraw.Draw(cell);dc.text((12,7),f"{g['char']}   REFERENCE / FONT   IoU {iou:.3f}",fill='#444',font=ImageFont.load_default(15))
        for i,im in enumerate(normalized):cell.paste(ImageChops.invert(im).convert('RGB'),(10+i*225,45))
        cells.append(cell)
    for page in range(3):
        sheet=Image.new('RGB',(1380,670),'#eeeae1');ds=ImageDraw.Draw(sheet)
        ds.text((16,10),f'{edition.upper()} / {page+1} — Reference left, actual font right',fill='#333',font=ImageFont.load_default(20))
        for i,cell in enumerate(cells[page*9:(page+1)*9]):sheet.paste(cell,((i%3)*460,40+(i//3)*210))
        filename=f'{edition}-comparison-{page+1}.png';sheet.save(OUT/filename)
        html.append(f'<h2>{edition.title()} {page+1}/3</h2><img src="{filename}" alt="{edition} reference and actual font comparison page {page+1}">')
(OUT/'comparison.json').write_text(json.dumps(records,indent=2)+'\n')
(OUT/'comparison.html').write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>LUNAR SERIF 52字比較</title><style>body{background:#faf8f0;color:#444;font:16px Georgia;margin:30px}img{width:100%;max-width:1380px}h2{font-weight:400}</style><h1>採用画像と実フォント — 大文字52字</h1><p>左：採用画像、右：TTFの実描画。輪郭の比較用に高さを揃えています。IoUは黒い領域の重なり率で、字間や美しさの評価ではありません。</p><a href="../../editions.html">入力プレビューへ戻る</a>'+''.join(html),encoding='utf-8')
print('Compared',len(records),'capitals; minimum IoU',min(r['silhouette_iou'] for r in records))
