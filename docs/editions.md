# 通常版とタイトル版

採用された2枚の画像を基準に、別々に選択できるTTF・WOFF2に仕上げました。

| 版 | フォント名 | 採用画像 | ダウンロード |
|---|---|---|---|
| 通常版 | LUNAR SERIF Text | [06](../references/06-lunar-serif-latin-capitals.png) | [TTF](../outputs/LUNARSERIFText-Regular.ttf) / [WOFF2](../outputs/LUNARSERIFText-Regular.woff2) |
| タイトル版 | LUNAR SERIF Title | [10](../references/10-lunar-serif-crescent-c.png) | [TTF](../outputs/LUNARSERIFTitle-Regular.ttf) / [WOFF2](../outputs/LUNARSERIFTitle-Regular.woff2) |

通常版は装飾なしのO。タイトル版は三日月形のC、三日月と四芒星を内包するO、弧を描くA・H・T、長いK・N・Q・Rの払いを持ちます。タイトル版のOpenType `ss01` は装飾なしOへの切り替えです。

## 使用方法

[入力・切り替え・ダウンロードのプレビュー](../editions.html)をローカルサーバーで開いてください。

```powershell
python -m http.server 8765 --bind 127.0.0.1
```

ブラウザーで `http://127.0.0.1:8765/editions.html` を開きます。TTFは対応するデザイン・組版アプリで使用できます。制作中にOSへインストールはしていません。

```css
@font-face {
  font-family: 'Lunar Title';
  src: url('./outputs/LUNARSERIFTitle-Regular.woff2') format('woff2');
}
.title { font-family: 'Lunar Title', serif; font-weight: 400; font-kerning: normal; }
.plain-o { font-feature-settings: 'ss01' 1; }
```

## 収録範囲と位置づけ

各118文字・120字形。ASCIIの英大文字・小文字・数字・基本記号、NBSP、×、ダッシュ・引用符・三点リーダー、および「ノクティセーヌ」「夜に、余韻を。」に必要な和文14文字です。

今回の採用画像が示す大文字26字を各版で再構成しました。小文字・数字・記号と和文は既存の独自輪郭を継承し、今回の画像から新たに採字したものではありません。日本語全般には別のJP版を使用してください。Textという版名も小さい本文での可読性を保証するものではなく、細線を生かした見出し向けです。

## 編集と再ビルド

`requirements.txt`のPython環境で次を実行します。

```powershell
python scripts/build_editions.py
python scripts/edition_specimen.py
python scripts/compare_editions.py
python scripts/verify_editions.py
```

採字範囲・輪郭の原本は `sources/text-reference.json` と `sources/title-reference.json`。採用画像からサブピクセル境界を抽出し、最小二乗のベジェ曲線に再構成しています。再抽出が必要な場合だけ `python scripts/trace_latin_editions.py` を実行します。

編集可能なSVGとメトリクスは `sources/text/` と `sources/title/` に出力されます。SVGを直接編集した場合は `build_editions.py` で上書きせず、次のようにビルドできます。

```powershell
python -c "import sys; sys.path.insert(0,'scripts'); import build; build.main('sources/title','LUNARSERIFTitle-Regular','LUNAR SERIF Title','1.000')"
```

元のDisplay版・JP版のファイルと採用画像は保持しています。利用条件は [LICENSE.txt](../LICENSE.txt) です。

## 比較と検証

- [全52字の比較](../verification/editions/comparison.html)：採用画像と実際のTTF描画を一字ずつ並べた6ページ。
- [通常版の実描画](../verification/editions/text-actual.png) / [タイトル版の実描画](../verification/editions/title-actual.png)
- [通常版の固定ロゴSVG](../specimens/text-logo.svg) / [タイトル版の固定ロゴSVG](../specimens/title-logo.svg)
- [読み込み・全ペア検査](../verification/editions/checks.json)

生成画像内にも、ロゴと一覧の字形・比率に揺れがあります。今回は各文字が分離したA–Z一覧を輪郭の基準とし、同じNやEは単語内でも同一字形に統一しています。微細なピクセルの凹凸は平滑化し、通常版Sの不自然な細い隙間は除去しました。画像の全ピクセルやロゴの字間を完全コピーしたものではありません。
