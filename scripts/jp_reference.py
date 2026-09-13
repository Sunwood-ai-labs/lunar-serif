"""Generate reference/Display/JP browser comparisons for all 50 evidenced characters."""
from pathlib import Path
import json, html, hashlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'verification/japanese'
OUT.mkdir(exist_ok=True)
ledger = json.loads((ROOT / 'verification/audit/ledger.json').read_text(encoding='utf-8'))
entries = [d for d in ledger.values() if d['reference_roi']]
pages = {}
for offset in range(0, len(entries), 6):
    cards = []
    for item in entries[offset:offset+6]:
        c = html.escape(item['char'])
        x, y, X, Y = item['reference_roi']
        cards.append(f'<article><h2>{c}</h2><div class="three"><div><label>生成画像</label><svg viewBox="{x-2} {y-2} {X-x+4} {Y-y+4}" height="110" style="width:{(X-x+4)*110/(Y-y+4):.2f}px"><image href="../../references/01-lunar-serif.png" width="1536" height="1024"/></svg></div><div><label>Display 1.002</label><span class="display glyph">{c}</span></div><div><label>JP 1.000</label><span class="jp glyph">{c}</span></div></div></article>')
    pages[str(offset//6+1)] = ''.join(cards)
font_hash = hashlib.sha256((ROOT / 'outputs/LUNARSERIFJP-Regular.woff2').read_bytes()).hexdigest()[:12]
source = '''<!doctype html><html lang="ja"><meta charset="utf-8"><title>LUNAR SERIF JP 生成画像比較</title><style>
@font-face{font-family:Display;src:url(../../outputs/LUNARSERIF-Regular.woff2);ascent-override:88%;descent-override:12%;line-gap-override:0%}
@font-face{font-family:JP;src:url(../../outputs/LUNARSERIFJP-Regular.woff2?v=HASH);ascent-override:88%;descent-override:12%;line-gap-override:0%}
*{box-sizing:border-box}body{margin:24px;color:#111;background:#fff;font:14px/1.5 system-ui}h1{font-size:22px;margin:0}nav{display:flex;gap:18px;margin:12px 0}h2{font:16px system-ui;margin:0 0 5px}.three{display:grid;grid-template-columns:repeat(3,1fr);text-align:center;gap:16px}label{display:block;font:12px system-ui;color:#666}article{border-top:1px solid #ccc;padding:12px 0;break-inside:avoid}.glyph{display:block;font-size:130px;line-height:1.2;height:156px}.display{font-family:Display}.jp{font-family:JP}svg{margin:14px 0;width:100%;max-width:200px}#status{font-weight:600;color:#456}
</style><h1>生成画像 / Display / JP — 全50文字比較</h1><p>同じ文字を画像と実WOFF2で比較。字形比較のため実フォントのem・ベースラインを統一。欧文は独自輪郭を保持。JP版の和文は、広い収録範囲で筆致を揃えるためしっぽり明朝を使用。</p><nav>'''.replace('HASH', font_hash)
source += ''.join(f'<a href="?page={p}">{p}</a>' for p in pages)
source += '</nav><p id="status">Loading fonts…</p><main></main><script type="application/json" id="pages">' + json.dumps(pages, ensure_ascii=False) + '''</script><script>
const page=new URLSearchParams(location.search).get('page')||'1';document.querySelector('main').innerHTML=JSON.parse(document.querySelector('#pages').textContent)[page]||'';
Promise.all([document.fonts.load('130px Display'),document.fonts.load('130px JP')]).then(results=>document.querySelector('#status').textContent=results.every(r=>r.length>0)?'Display + JP WOFF2 loaded / page '+page:'FONT LOAD FAILED');
</script></html>'''
(OUT / 'reference.html').write_text(source, encoding='utf-8')
(OUT / 'reference-pages.json').write_text(json.dumps({str(i//6+1): [d['char'] for d in entries[i:i+6]] for i in range(0,len(entries),6)}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(f'{len(entries)} characters, {len(pages)} comparison pages')

coverage = json.loads((ROOT / 'outputs/japanese-coverage.json').read_text(encoding='utf-8'))
chars = coverage['supplement']['added_characters'] + coverage['supplement']['original_geometric_symbols']
grids = {str(i//88+1): ''.join(f'<div class="cell"><span>{html.escape(c)}</span><small>U+{ord(c):04X}</small></div>' for c in chars[i:i+88]) for i in range(0,len(chars),88)}
grids['vertical'] = ''.join(f'<div class="cell"><small>U+{ord(c):04X} / 横</small><span>{c}</span><small>縦書き</small><span style="writing-mode:vertical-rl;text-orientation:mixed;height:120px;margin:auto">{c}</span></div>' for c in '＿｜｟｠￣')
supplement = '''<!doctype html><html lang="ja"><meta charset="utf-8"><title>JP 補完文字の実表示</title><style>
@font-face{font-family:JP;src:url(../../outputs/LUNARSERIFJP-Regular.woff2?v=HASH)}
body{margin:24px;font:14px system-ui;color:#111}h1{font-size:22px}nav{display:flex;gap:24px}main{display:grid;grid-template-columns:repeat(8,1fr);gap:6px;margin-top:18px}.cell{border:1px solid #ddd;text-align:center;min-width:0;padding:8px}.cell span{font:38px/1.25 JP;display:block}small{font:10px system-ui;color:#666}
</style><h1>日本語版の補完261文字 — 実WOFF2</h1><p>記号・ギリシャ文字・キリル文字・半角カナ。元画像には見本がないため、字形・欠け・配置を確認。</p><nav>'''.replace('HASH',font_hash)
supplement += ''.join(f'<a href="?page={p}">{p}</a>' for p in grids)
supplement += '</nav><p id="status">Loading fonts…</p><main></main><script type="application/json" id="pages">' + json.dumps(grids,ensure_ascii=False) + '''</script><script>
const page=new URLSearchParams(location.search).get('page')||'1';document.querySelector('main').innerHTML=JSON.parse(document.querySelector('#pages').textContent)[page];document.fonts.load('38px JP').then(f=>document.querySelector('#status').textContent=f.length?'JP WOFF2 loaded / page '+page:'FONT LOAD FAILED');</script></html>'''
(OUT / 'supplement.html').write_text(supplement,encoding='utf-8')
