# LUNAR SERIF JP 日本語版の受入基準

日本語版の成果物は、次の二つを同じ版として配置する。

- `outputs/LUNARSERIFJP-Regular.ttf`
- `outputs/LUNARSERIFJP-Regular.woff2`

検証の入口は `scripts/verify_jp.py`、実用文の固定入力は
`verification/japanese/corpus.json` である。検証スクリプトは既存の
`outputs/LUNARSERIF-Regular.ttf`、`LICENSE.txt`、生成済みフォントを読み取るだけで、
既存の欧文フォントやソースを変更しない。

## 実行

FontTools と Brotli が動作する Python で次を実行する。Windows でこの作業フォルダーの
既存ランタイムを使う場合は次のコマンドになる。

```powershell
$py = 'C:\Prj\nikukyu-maru-font\.venv\Scripts\python.exe'
& $py -X utf8 scripts/verify_jp.py
```

全検査に合格すると終了コード `0`、一つでも必須検査に失敗すると終了コード `1` になる。
結果は標準出力へ JSON で出力するため、レビュー記録へ保存する場合は呼び出し側でリダイレクト
する。既定の入力を差し替える場合は `--font`、`--woff2`、`--corpus`、`--base-font` を使う。

縦組みの実動作を HarfBuzz でも確認する場合だけ、`uharfbuzz` が入った別 Python を指定する。
HarfBuzz は通常の受入検査の必須依存ではない。

```powershell
& $py -X utf8 scripts/verify_jp.py `
  --harfbuzz-python 'C:\path\to\harfbuzz\.venv\Scripts\python.exe'
```

既存のディスプレイ版が手元にない配布用検査では `--skip-base-outline` を指定できる。その場合、
N/O/S の保持検査だけが `skipped` になり、他の必須検査は省略されない。

## 検査する集合

JIS X 0208 の行・区を手作業で転記しない。スクリプトが各セルを
`ESC $ B` + 行・点 + `ESC ( B` のバイト列にし、Python の
`iso2022_jp` を `strict` で復号して一覧を作る。標準的な区分と期待数は次の通りである。

| 区分 | バイト行 | 期待数 |
| --- | --- | ---: |
| 特殊行（句読点、記号、かな、ギリシャ・キリル、罫線） | `0x21–0x2F` | 524 |
| 第一水準 | `0x30–0x4F` | 2,965 |
| 第二水準 | `0x50–0x74` | 3,390 |
| JIS X 0208 全収録 | `0x21–0x74` | 6,879 |

第一水準・第二水準・特殊行・全収録の各集合を Unicode `cmap` と照合する。対象の cmap
エントリが無い場合、存在しない glyph 名へ向く場合、`.notdef` へ向く場合は失敗とする。
Unicode cmap の形式 4 または 12 も確認する。

JIS 全収録とは別に、かな、濁点、半濁点、和文記号を名前付きの検査結果にする。さらに、
次の互換入力を欠落なく確認する。

- 半角 ASCII `U+0020–U+007E`
- 全角 ASCII `U+FF01–U+FF5E`
- 全角白括弧 `U+FF5F–U+FF60`
- JIS X 0201 半角句読点・カタカナ `U+FF61–U+FF9F`

濁点・半濁点は、かなの事前合成文字、JIS の `゛`・`゜`、半角入力の `ﾞ`・`ﾟ` を含む。
これにより、通常の日本語入力とレガシーな半角カナを同じ受入基準で確認できる。

## 実用コーパス

`corpus.json` の `required_examples` は `horizontal`、`vertical`、`mixed` の三種類を
含み、合計 300 Unicode code points 以上にする。`mixed` は日本語に ASCII、全角 ASCII、
または半角カナが混在する例、`vertical` は縦組みで問題になりやすい括弧・句読点を二種類
以上含む例とする。各例文と `required_character_sets` の全コードポイントを cmap に照合し、
missing がゼロであることを合格条件にする。

文章は、作品紹介、配信情報、UI 文言、URL・ID・時刻・価格、縦書きの手紙・展示カードなど、
フォントを実際に使う場面を含む。検査コードは文章を数千万通りの全ペアで交差させない。JIS
集合の完全照合、カテゴリ別集合、実用文章、OpenType の構造検査を組み合わせて、実行時間と
見逃しのバランスを取る。

## 縦組みとメタデータ

GSUB の `vert` と `vrt2` が存在し、それぞれ有効な lookup を持つことを確認する。OpenType
に `vmetrics` という七文字の feature tag はないため、この受入基準でいう `vmetrics` は
`vhea` と `vmtx` による縦メトリクスを指す。Unicode cmap が参照する全 glyph に縦メトリクス
があり、advance height が正であることを確認する。`VORG` は存在すれば結果に記録するが、
必須にはしない。`＿` `｜` `｟` `｠` `￣` は縦用字形を持つ必須サンプルとして、両 feature の
lookup が元 glyph を置換することも確認する。

ライセンスは、フォントの name table の ID 0（copyright）と ID 13（license description）に
内容があり、ライセンスを示す語が含まれることを確認する。JP 配布物では同梱
`outputs/LUNAR-SERIF-JP-OFL.txt` を優先して読み、SIL Open Font License の本文を含むことを
確認する。これが無い簡易環境ではルートの `LICENSE.txt` を読み取る。ID 14（license info URL）は
存在する場合に HTTP(S) URL であることを確認する。

TTF と WOFF2 は、glyph order、Unicode cmap、水平メトリクス、全 glyph の輪郭、GSUB feature、
name table を読み戻して比較する。WOFF2 の圧縮前後で集合や輪郭が変わる場合は失敗とする。

既存 `LUNARSERIF-Regular.ttf` が存在する場合は、そこから日本語コードポイントを除いた
104 個の独自欧文・記号について、対応 glyph の輪郭 SHA-256 と advance を日本語版と比較する。
代表例として N/O/S もこの集合に含まれ、さらに GSUB `ss01` が選ぶ plain O の輪郭と advance
も比較する。元フォントが無い場合だけ検査を `skipped` とする。

## 限界とレビュー時の読み方

この検査は JIS X 0208 と実用上の互換入力を保証する。JIS X 0213 の追加文字、IVS、絵文字、
言語ごとの字形差、OS ごとのレンダリング差までは保証しない。HarfBuzz の追加プローブを
実行した場合は、縦方向の shaping で `.notdef` が出ないことと、縦送りが発生することも結果に
含める。HarfBuzz の追加プローブでは、これら5字を `vert`/`vrt2` 有効時と両方無効時に
shape し、GID が変わり `.notdef` が出ないことを確認する。ブラウザーや DTP アプリの見た目は、
別途 `preview.html` などで確認する。
