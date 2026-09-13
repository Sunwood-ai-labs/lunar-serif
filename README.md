# LUNAR SERIF

NOCTISENE用のオリジナル・ディスプレイセリフ初版（Regular / 1.001）。参考画像の流れるN、三日月と四芒星のO、しなやかなSを基準に、1000 UPMの輪郭から制作しました。既存フォントの改名・輪郭流用は行っていません。

## 成果物

- `outputs/LUNARSERIF-Regular.ttf`：デスクトップ用フォント。
- `outputs/LUNARSERIF-Regular.woff2`：Web用フォント。
- `sources/glyphs/*.svg`：120字形の編集可能な輪郭。座標はフォントのY上向きで、表示用transformを付与しています。
- `sources/metrics.json`：文字コードと送り幅。`sources/features.fea`：生成されたOpenType機能。
- `specimens/specimen.png`：フォントから実描画した文字見本。
- `specimens/logo-black.svg` / `logo-white.svg`：HarfBuzzのカーニングを適用したアウトラインロゴ。PNG版も同梱。
- `preview.html`：任意文字入力、サイズ、白抜き、装飾なしOを試すローカルページ。
- `verification/`：読み込み・収録文字・字形一覧・組版・再現性の検証記録。

## 収録範囲と使い方

118文字、120字形（未定義字形と代替Oを含む）。ASCII U+0020–007E、NBSP、×、–、—、‘、’、“、”、…、および「ノクティセーヌ」「夜に、余韻を。」に必要な和文14文字を収録しています。日本語全文字・アクセント付き欧文・太字・斜体は未収録です。

Oは標準で月と星入り。OpenTypeのスタイルセット01（`ss01`）で装飾なしに変更できます。小文字oは通常形です。繊細な線を持つ見出し・ロゴ向け設計なので、小さい本文では実寸で見え方を確認してください。和文は専用フレーズ向けに独自に簡略化した字形です。

TTFは対応アプリのフォント読み込み機能で使用できます。Windowsへのインストールを希望する場合はTTFを開いて「インストール」を選びます。この制作ではOSへのインストールは実施していません。文字列を編集しないロゴ用途ならSVGを直接配置できます。

Webでは次のように設定します。未収録の和文は利用環境の明朝体へフォールバックします。

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

`preview.html`をブラウザーで開くか、作業フォルダーで `python -m http.server 8765 --bind 127.0.0.1` を実行して `http://127.0.0.1:8765/preview.html` にアクセスしてください。ブラウザーで白抜き・ss01切り替え・和文入力を確認済みです。

## 再ビルド

Pythonと`requirements.txt`の依存パッケージを使用します。PowerShellでこのディレクトリに移動して実行してください。

```powershell
python -m venv .venv
& ./.venv/Scripts/python.exe -m pip install -r requirements.txt
& ./.venv/Scripts/python.exe -X utf8 scripts/build.py
& ./.venv/Scripts/python.exe -X utf8 scripts/specimen.py
& ./.venv/Scripts/python.exe -X utf8 scripts/verify.py
```

SVGまたはmetricsを直接編集した場合は`build.py`から実行します。設計コードを変更した場合のみ先に`design.py`を実行してください。`design.py`はSVGとmetricsを上書きします。カーニングは`build.py`の`KERN`を編集します（features.feaはビルドで再生成）。

### このPCでの実行記録（2026-09-13）

専用`.venv`のfontToolsネイティブ拡張はWindowsのアプリケーション制御で読み込みが拒否されました。ポリシーは変更せず、動作確認済みの既存Pythonで輪郭処理と描画を実行し、専用環境で動作するHarfBuzzを別プロセスで実行しました。既存環境のパッケージは変更していません。

```powershell
$fontPython = 'C:/Prj/nikukyu-maru-font/.venv/Scripts/python.exe'
& $fontPython -X utf8 scripts/design.py
& $fontPython -X utf8 scripts/build.py
& $fontPython -X utf8 scripts/specimen.py
& $fontPython -X utf8 scripts/verify.py --shaper-python C:/Prj/NOCTISENE/lunar-serif/.venv/Scripts/python.exe
```

検証結果：TTF/WOFF2のcmap一致、必須文字欠落0、上下の輪郭範囲正常、HarfBuzz 12.3.2によるss01切り替え成功、NOCTISENEの送り幅5188→5073 UPM、文字間の外接矩形間隔は全て正。連続ビルドで両フォントのSHA-256が一致しました。FreeTypeで文字見本と全字形一覧を描画し、参照画像とN/O/S・白抜きロゴを目視比較しました。PNGはPillowのBASIC組版、SVGはHarfBuzz組版のため、文字間に差が出る場合があります。

フォントとソースの扱いは`LICENSE.txt`を参照してください。

## 生成画像との比較（1.001）

スクリーンショット比較に基づきN/O/S等の比率、Oの月と星、和文の線と字間を調整しました。比較画像と残る差は[詳細レポート](verification/comparison/REPORT.md)に記載しています。特に和文の筆致は見本と異なり、完全再現ではありません。修正前フォントはerification/comparison/before/に保持しています。
