"""Build an HTML contact sheet. Reference stays untouched; SVG viewBox crops only."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def crop(box,height):
    x,y,w,h=box
    return f'<svg viewBox="{x} {y} {w} {h}" width="{height*w/h}" height="{height}" style="max-width:100%"><image href="../../references/01-lunar-serif.png" width="1536" height="1024"/></svg>'

def live(text,height,family='Current'):
    import json
    meta=json.loads((ROOT/'sources/metrics.json').read_text(encoding='utf-8'))
    widths={v['char']:v['advance'] for v in meta.values() if v['char']}
    if family=='Before':
        from fontTools.ttLib import TTFont
        font=TTFont(ROOT/'verification/comparison/before/LUNARSERIF-Regular.ttf')
        widths={chr(c):font['hmtx'][n][0] for c,n in font.getBestCmap().items()}
    width=sum(widths[c] for c in text)+50
    japanese=any(ord(c)>0x3000 for c in text)
    top,vertical,baseline=(0,850,820) if japanese else (-15,740,700)
    return f'<svg class="live" viewBox="0 {top} {width} {vertical}" height="{height}" style="max-width:100%;font-family:{family};font-size:1000px;padding:0"><text x="0" y="{baseline}">{text}</text></svg>'

def triple(title,box,text,height):
    return f'<h2>{title}</h2><div class="triple"><section><label>生成見本</label>{crop(box,height)}</section><section><label>修正前 v1.000</label>{live(text,height,"Before")}</section><section><label>現在のフォント</label>{live(text,height)}</section></div>'

head='''<!doctype html><html lang="ja"><meta charset="utf-8"><title>LUNAR SERIF 見本との比較</title><style>
@font-face{font-family:Before;src:url('before/LUNARSERIF-Regular.woff2')}
@font-face{font-family:Current;src:url('../../outputs/LUNARSERIF-Regular.woff2?v=2')}
*{box-sizing:border-box}body{margin:24px;color:#111;background:white;font:14px/1.5 system-ui}h1{font-size:23px}h2{font-size:17px;margin-top:28px;border-top:1px solid #ddd;padding-top:12px}label{display:block;color:#666;font-size:13px;margin:8px 0 16px}.triple{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}section{min-width:0;overflow:hidden}.live{white-space:nowrap;line-height:1.2;font-kerning:normal;font-weight:400;padding-bottom:15px}.logo .live{font-size:clamp(40px,12.2vw,230px)}.logo svg{width:100%;height:auto}.note{color:#555;max-width:1000px}.nav{display:flex;gap:18px}svg{overflow:hidden} .dark{background:#111;color:white;padding:12px} .small .live{font-size:50px;letter-spacing:.08em}.wide{overflow:auto}#ready{font-size:12px;color:#666}
</style><h1>LUNAR SERIF — 生成見本 / 実フォント比較</h1><nav class="nav"><a href="?page=logo">ロゴ</a><a href="?page=detail">N・O・S</a><a href="?page=japanese">和文</a><a href="?page=alphabet">英字・数字</a></nav><p id="ready">フォント読み込み中</p>'''
pages={}
pages['logo']='<style>.logo svg{width:auto;height:162px}.logo svg.live{height:154px}</style><p class="note">黒い字面の高さを約150pxに揃えて比較。画像の横伸縮は行わない。実フォントはブラウザーのWOFF2組版。</p><div class="logo"><label>生成見本</label>'+crop((50,110,1460,230),162)+'<label>修正前 v1.000</label>'+live('NOCTISENE',154,'Before')+'<label>現在のフォント</label>'+live('NOCTISENE',154)+'</div>'
pages['detail']=triple('N — 対角線・右下の払い',(56,119,188,213),'N',210)+triple('O — 三日月・星・輪郭',(247,118,200,215),'O',210)+triple('S — 上下のボウルと曲線',(883,118,117,215),'S',210)
pages['japanese']='<p class="note">和文は行単位で比較。生成見本の筆致と独自字形の差を含む。</p>'+triple('ノクティセーヌ',(991,646,390,51),'ノクティセーヌ',38)+triple('夜に、余韻を。',(960,724,472,76),'夜に、余韻を。',38)
pages['japanese']+=triple('夜 — 縦線・払い',(960,724,74,76),'夜',130)+triple('余 — 横線・払い',(1175,724,73,76),'余',130)+triple('韻 — 音と員の密度',(1260,724,70,76),'韻',130)
pages['alphabet']='<p class="note">生成画像にある英大文字・数字を照合。小文字と追加記号は元画像に見本がないため、忠実度の評価対象外。見本の一覧は広い字間で配置されています。</p>'+triple('A–M',(892,384,593,53),'ABCDEFGHIJKLM',31)+triple('N–Z',(891,454,597,53),'NOPQRSTUVWXYZ',31)+triple('0–9',(894,537,582,51),'0123456789',31)
script='''<script>const page=new URLSearchParams(location.search).get('page')||'logo'; document.getElementById('body').innerHTML=JSON.parse(document.getElementById('pages').textContent)[page]||'';Promise.all([document.fonts.load('100px Before'),document.fonts.load('100px Current')]).then(()=>document.getElementById('ready').textContent='Before / Current WOFF2 loaded');</script>'''
import json
(ROOT/'verification/comparison/index.html').write_text(head+'<main id="body"></main><script type="application/json" id="pages">'+json.dumps(pages,ensure_ascii=False)+'</script>'+script,encoding='utf-8')
