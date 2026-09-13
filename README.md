# LUNAR SERIF

NOCTISENE用のオリジナル・ディスプレイセリフ（Regular / 1.002）。流れるN、三日月と四芒星のO、細長いSを持つフォントです。既存フォントの改名・輪郭流用はしていません。欧文は独自輪郭、和文14文字は同梱の生成見本から再構成した輪郭です。

![文字見本](specimens/specimen.png)

## ダウンロードと確認

- [TTF](outputs/LUNARSERIF-Regular.ttf) / [WOFF2](outputs/LUNARSERIF-Regular.woff2)
- [文字入力プレビュー](preview.html)
- [全120字形の監査レポート](verification/audit/REPORT.md)
- [全字形の比較ページ](verification/audit/index.html) / [個別判断台帳](verification/audit/ledger.json)
- [黒ロゴSVG](specimens/logo-black.svg) / [白ロゴSVG](specimens/logo-white.svg)

GitHubのHTMLファイル表示はプレビューを実行しません。リポジトリをダウンロードし、作業フォルダーで `python -m http.server 8765 --bind 127.0.0.1` を実行して、ブラウザーで `http://127.0.0.1:8765/preview.html` を開いてください。

## 収録範囲

118文字・120字形。ASCII U+0020–007E、NBSP、×、–、—、‘、’、“、”、…と、「ノクティセーヌ」「夜に、余韻を。」に必要な和文14文字を収録。未定義字形と装飾なしOも含みます。日本語全文字、アクセント付き欧文、太字、斜体は未収録です。

Oは標準で月と星入り。OpenType `ss01` で装飾なしに切り替えられます。小文字oは通常形です。繊細な線を持つ見出し・ロゴ向け設計で、小さい本文での読みやすさは用途に合わせて確認してください。生成見本には小文字・追加記号がなく、これらは独自設計として評価しています。

```css
@font-face {
  font-family: 'Lunar Serif';
  src: url('./outputs/LUNARSERIF-Regular.woff2') format('woff2');
  font-weight: 400;
}
.logo {
  font-family: 'Lunar Serif', 'Yu Mincho', serif;
  font-weight: 400;
  font-kerning: normal;
}
.plain-o { font-feature-settings: 'ss01' 1; }
```

TTFは対応アプリに読み込んで使用できます。Windowsに導入する場合はTTFを開いて「インストール」を選びます。制作・検証時にはOSへインストールしていません。固定ロゴにはSVGを直接使用できます。

## 再ビルドと検証

Python 3.12と`requirements.txt`の依存パッケージを使用します。

```powershell
python -m venv .venv
& ./.venv/Scripts/python.exe -m pip install -r requirements.txt
& ./.venv/Scripts/python.exe -X utf8 scripts/design.py
& ./.venv/Scripts/python.exe -X utf8 scripts/build.py
& ./.venv/Scripts/python.exe -X utf8 scripts/audit.py
& ./.venv/Scripts/python.exe -X utf8 scripts/specimen.py
& ./.venv/Scripts/python.exe -X utf8 scripts/verify.py
& ./.venv/Scripts/python.exe -X utf8 scripts/verify_geometry.py
& ./.venv/Scripts/python.exe -X utf8 scripts/verify_spacing.py
```

`sources/glyphs/*.svg`と`metrics.json`を直接編集した場合は`build.py`から実行してください。`design.py`はSVG・metricsを上書きします。カーニングは`build.py`の`KERN`、和文の編集可能な輪郭は`sources/japanese-reference.json`にあります。和文を元画像から再抽出する場合のみ`trace_japanese.py`を実行してから`design.py`を実行します。参照領域は台帳内に記録しています。

このPCでは専用環境のfontTools拡張がWindowsのアプリケーション制御で拒否されたため、動作する既存Pythonで輪郭処理を実行し、HarfBuzzのみ専用環境を別プロセスで使用しました。ポリシーは変更していません。`verify.py --shaper-python <HarfBuzzが動作するPythonのパス>` で同じ分離が可能です。通常環境では上記の単一Pythonで実行できます。

## 1.002での改善

全120字形を23ページのブラウザースクリーンショットで確認しました。B/P等の幅、G/Qの終端、Yの接続、数字1/4/8、g/j、崩れていた二重引用符を修正。和文14文字は見本の筆致から再構成しました。可視116文字の全13,456組で実輪郭の交差がないことを検証しています。

TTF/WOFF2読み込み、必須文字、カーニング、ss01、再ビルドのハッシュ一致も検証。PNG文字見本はPillow/FreeType、SVGロゴはHarfBuzz組版のため、文字間に差が出る場合があります。

元画像は低解像度のデザイン案で、ロゴと文字一覧にも字形の揺れがあります。大きなロゴのN/O/S等を優先し、全輪郭の完全一致は主張していません。和文の微細な筆先・曲率にも再構成による差があります。以前の比較は[1.001の記録](verification/comparison/REPORT.md)、初版フォントは`verification/comparison/before/`に保持しています。

フォント・ソースの利用条件は[LICENSE.txt](LICENSE.txt)を参照してください。
