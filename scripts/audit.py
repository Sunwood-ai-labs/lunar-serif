"""All-glyph browser audit with reference ROIs and a persistent review ledger."""
from pathlib import Path
import json,html,hashlib
from PIL import Image
from fontTools.ttLib import TTFont
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'verification/audit'
OUT.mkdir(exist_ok=True)
REF={}
def row(chars,ranges,y,Y):
    for c,(x,X) in zip(chars,ranges): REF[c]=[x-2,y,X+3,Y]
row('ABCDEFGHIJKLM',[(895,928),(949,973),(992,1023),(1042,1072),(1092,1117),(1136,1159),(1178,1213),(1233,1262),(1283,1292),(1310,1323),(1344,1374),(1393,1418),(1436,1478)],380,440)
row('NOPQRSTUVWXYZ',[(894,926),(939,975),(990,1013),(1028,1066),(1079,1110),(1126,1148),(1163,1194),(1210,1240),(1256,1289),(1303,1353),(1368,1398),(1412,1442),(1456,1483)],450,510)
row('0123456789',[(897,927),(966,975),(1015,1040),(1077,1101),(1136,1163),(1200,1223),(1261,1286),(1323,1349),(1386,1409),(1447,1472)],535,590)
row('ノクティセーヌ',[(993,1024),(1054,1088),(1114,1155),(1172,1195),(1219,1261),(1285,1325),(1342,1378)],640,704)
row('夜に、余韻を。',[(962,1031),(1055,1103),(1126,1141),(1177,1245),(1263,1327),(1350,1397),(1411,1429)],720,803)
im=Image.open(ROOT/'references/01-lunar-serif.png').convert('L')
for c,box in list(REF.items()):
    b=im.crop(box).point(lambda p:255 if p<100 else 0).getbbox()
    if b: REF[c]=[box[0]+b[0],box[1]+b[1],box[0]+b[2],box[1]+b[3]]
font=TTFont(ROOT/'outputs/LUNARSERIF-Regular.ttf')
meta=json.loads((ROOT/'sources/metrics.json').read_text(encoding='utf-8'))
old=json.loads((OUT/'ledger.json').read_text(encoding='utf-8')) if (OUT/'ledger.json').exists() else {}
ledger={}
for name,m in meta.items():
    g=font['glyf'][name]
    bounds=[g.xMin,g.yMin,g.xMax,g.yMax] if g.numberOfContours else None
    ledger[name]={**old.get(name,{}),'char':m['char'],'advance':m['advance'],'bounds':bounds,'reference_roi':REF.get(m['char']),'review':old.get(name,{}).get('review','pending')}
(OUT/'ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
groups={'upper':'ABCDEFGHIJKLMNOPQRSTUVWXYZ','digits':'0123456789','lower':'abcdefghijklmnopqrstuvwxyz','japanese':'ノクティセーヌ夜に、余韻を。','symbols':''.join(v['char'] for v in meta.values() if v['char'] and not v['char'].isalnum() and v['char'] not in 'ノクティセーヌ夜に、余韻を。')}
pages={}
for group,chars in groups.items():
    names=[n for n,m in meta.items() if m['char'] and m['char'] in chars]
    if group=='symbols': names+=['O.plain','.notdef']
    for i in range(0,len(names),6): pages[f'{group}-{i//6+1}']=names[i:i+6]
def actual(name,family):
    data=ledger[name]; bounds=data['bounds']
    if not bounds:return '<span class="empty">空白・輪郭なし</span>'
    x,y,X,Y=bounds
    # Include complete glyph bounds rather than assuming Latin cap height.
    c=data['char'] or ('O' if name=='O.plain' else '\ufffd')
    if name=='.notdef':
        from fontTools.pens.svgPathPen import SVGPathPen
        pen=SVGPathPen(font.getGlyphSet());font.getGlyphSet()[name].draw(pen)
        return f'<svg viewBox="{x-20} {-Y-20} {X-x+40} {Y-y+40}" height="135"><path transform="scale(1,-1)" d="{pen.getCommands()}"/></svg>'
    feature='font-feature-settings:&quot;ss01&quot; 1;' if name=='O.plain' else ''
    return f'<svg viewBox="{x-20} {-Y-20} {X-x+40} {Y-y+40}" height="135" style="font-family:{family};font-size:1000px;{feature}"><text x="0" y="0">{html.escape(c)}</text></svg>'
def card(name):
    d=ledger[name];ref=d['reference_roi']
    if ref:
        x,y,X,Y=ref
        refsvg=f'<svg viewBox="{x-1} {y-1} {X-x+2} {Y-y+2}" height="135"><image href="../../references/01-lunar-serif.png" width="1536" height="1024"/></svg>'
    else:refsvg='<span class="empty">生成見本なし<br>設計・実寸で評価</span>'
    char=d['char'] or ('O' if name=='O.plain' else '')
    return f'<article><h2>{html.escape(char)} <small>{name}</small></h2><div class="samples"><section><label>生成見本</label>{refsvg}</section><section><label>現行 135px</label>{actual(name,"Current")}</section></div><div class="sizes"><span style="font-size:24px">{html.escape(char)}</span><span style="font-size:48px">{html.escape(char)}</span><span style="font-size:72px">{html.escape(char)}</span></div><footer>advance {d["advance"]} · {html.escape(d["review"])}</footer></article>'
head='''<!doctype html><html lang="ja"><meta charset="utf-8"><title>LUNAR SERIF 全字形監査</title><style>
@font-face{font-family:Current;src:url(../../outputs/LUNARSERIF-Regular.woff2?v='''+hashlib.sha256((ROOT/'outputs/LUNARSERIF-Regular.woff2').read_bytes()).hexdigest()[:10]+''')}
*{box-sizing:border-box}body{margin:20px;background:#fff;color:#111;font:14px/1.4 system-ui}h1{font-size:20px}nav{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px}a{color:#345}main{display:grid;grid-template-columns:1fr 1fr;gap:18px}article{border:1px solid #ddd;padding:12px;min-width:0}h2{font-size:20px;margin:0 0 12px}small{font:12px system-ui;color:#666}.samples{display:grid;grid-template-columns:1fr 1fr;gap:20px}.samples section{min-width:0}label{display:block;color:#666;font-size:12px;margin-bottom:10px}svg{max-width:100%;overflow:hidden}.empty{display:inline-block;height:135px;color:#999;padding:20px}.sizes{font-family:Current;display:flex;gap:25px;align-items:baseline;height:95px}footer{color:#666;font-size:11px}#status{font-size:12px}
</style><h1>LUNAR SERIF 全120字形監査</h1><nav>'''
nav=''.join(f'<a href="?page={p}">{p}</a>' for p in pages)
contents={p:''.join(card(n) for n in ns) for p,ns in pages.items()}
end='''<p id="status">loading</p><main id="cards"></main><script type="application/json" id="data">'''+json.dumps(contents,ensure_ascii=False)+'''</script><script>const p=new URLSearchParams(location.search).get('page')||'upper-1';document.getElementById('cards').innerHTML=JSON.parse(document.getElementById('data').textContent)[p];document.fonts.load('100px Current').then(f=>document.getElementById('status').textContent=f.length?'WOFF2 loaded — '+p:'FONT LOAD FAILED');</script>'''
(OUT/'index.html').write_text(head+nav+'</nav>'+end,encoding='utf-8')
(OUT/'pages.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'{len(ledger)} glyphs; {sum(bool(d["reference_roi"]) for d in ledger.values())} references; {len(pages)} pages')
