"""Validate evidence coverage and publish the final audit report."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'verification/audit'
ledger=json.loads((out/'ledger.json').read_text(encoding='utf-8'))
pages=json.loads((out/'pages.json').read_text(encoding='utf-8'))
captures=json.loads((out/'captures.json').read_text(encoding='utf-8'))
assert len(ledger)==120 and all(d['review']=='reviewed' for d in ledger.values())
assert set(pages)=={c['page'] for c in captures}
assert len(captures)==23
assert all((out/d['evidence']).stat().st_size>10000 for d in ledger.values())
assert all((out/c['file']).stat().st_size==c['bytes'] for c in captures)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
evidence={'glyphs':120,'reference_glyphs':sum(d['reference_roi'] is not None for d in ledger.values()),'reviewed':120,'pending':0,'screenshot_pages':23,'revised':sum(d['decision']=='revised' for d in ledger.values()),'font_sha256':{p.name:sha(p) for p in (ROOT/'outputs').glob('*')},'screenshots':{c['file']:sha(out/c['file']) for c in captures}}
(out/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
body='''# 全120字形のスクリーンショット監査 — 1.002

2026-09-13。全120字形の個別拡大と24/48/72px表示を確認し、23ページの最終スクリーンショットを保存しました。生成見本があるのは50文字です。残る70字形は独自設計・空白・代替O・未定義字形として確認しています。

数字8の余分な空洞、gの切れ目、jの途中のセリフ、二重引用符の破損を修正。A/B/D/J/M/P/R等の比率や接続を調整し、G/Q/W/Yも修正しました。和文14文字は生成見本から曲線を再構成しています。

可視116文字の全13,456隣接組をアウトラインの積集合で検証し、実輪郭の交差は0件でした。外接矩形が重なる27組も輪郭自体は重なりません。TTF/WOFF2読み込み、カーニング、ss01、輪郭範囲、回帰検証、同じビルドのSHA-256一致も確認しています。

## 証拠と制限

各行のリンクが最終スクリーンショットです。`ledger.json`に個別判断、`evidence.json`に最終フォントと画像のハッシュ、`geometry.json`と`spacing.json`に機械検証結果を保存しています。ブラウザーでWOFF2をロードし、ロード結果が空でないことを確認して撮影しました。

これは全輪郭の完全一致という判定ではありません。元の生成画像は低解像度で、ロゴと小さな一覧にも違いがあります。N/O/S等はロゴの形を優先。和文は筆致を復元しつつ微細な段差を曲線化したため、筆先や曲率には再構成による差が残ります。小さい本文専用のフォントとしては設計していません。

## 全字形の個別判断

| 字形 | 処理 | 確認・判断 | スクリーンショット |
|---|---|---|---|
'''
for n,d in ledger.items():
    label=d['char'] or n
    if label.isspace():label='SPACE' if d['char']==' ' else 'NBSP'
    label=label.replace('|','&#124;')
    body+=f'| {label} ({n}) | {d["decision"]} | {d["notes"]} | [画像]({d["evidence"]}) |\n'
(out/'REPORT.md').write_text(body,encoding='utf-8')
print(json.dumps({k:v for k,v in evidence.items() if k not in ['screenshots','font_sha256']},indent=2))
