# LUNAR SERIF 日本語基盤調査

調査日: 2026-09-13
対象: `lunar-serif` の独自欧文と、初版に含まれる日本語14字
目的: 既存フォントの改名ではなく、独自欧文を残した日本語対応版を作るための和文ドナーを決める

## 推奨

**Shippori Mincho の Regular TTF を採用する。** 実装で固定する取得物は次のGoogle Fontsリポジトリのコミットである。

- ドナーTTF（固定URL）: [`ShipporiMincho-Regular.ttf`](https://raw.githubusercontent.com/google/fonts/d0b2d1307ad5d6b579d627a6e5abd25952484b96/ofl/shipporimincho/ShipporiMincho-Regular.ttf)
- 固定コミット: [`d0b2d1307ad5d6b579d627a6e5abd25952484b96`](https://github.com/google/fonts/tree/d0b2d1307ad5d6b579d627a6e5abd25952484b96/ofl/shipporimincho)
- 固定メタデータ: [`METADATA.pb`](https://raw.githubusercontent.com/google/fonts/d0b2d1307ad5d6b579d627a6e5abd25952484b96/ofl/shipporimincho/METADATA.pb)
- 同梱ライセンス: [`OFL.txt`](https://raw.githubusercontent.com/google/fonts/d0b2d1307ad5d6b579d627a6e5abd25952484b96/ofl/shipporimincho/OFL.txt)
- 上流プロジェクト: [`fontdasu/ShipporiMincho`](https://github.com/fontdasu/ShipporiMincho)
- 取得物のSHA-256: `769b5269f0f9bc6534b352c0e6bd856a566e03ff788f107191c2d835863570b2`

この選択は、静的なRegular TTFをそのまま再現可能な入力にでき、上流READMEがひらがな・カタカナ・全角英数字・全角記号・縦書き用字形・かなの異体を明記しているためである。漢字はSILライセンスの源流明朝を基にした字形である。Google Fontsの日本語フォント監査でもShippori Minchoは「full set」と記録されている。選択した固定TTFの実測cmapは15,363文字である。今回の要求集合ではShippori単体に261文字の不足があり、260文字を固定Noto Serif JPから補い、残るU+2252（≒）は単純な独自輪郭で補う。最終JP版の実測cmapは15,624文字である。ただし、cmap数だけではJIS第一・第二水準や常用漢字の完全収録を証明できないため、下記の機械検証を出荷条件にする。

## LUNAR SERIFへの統合方針

日本語拡張版（`LUNAR SERIF JP`）では、Shipporiの日本語字形を**現在の14字にも適用する**。対象の14字は `ノ ク テ ィ セ ー ヌ に を 、 。 余 夜 韻` である。数千字をShipporiにしながらこの14字だけ既存の独自字形に残すと、払い・はね・セリフ・濁点の筆致が混在し、同一フォント内で目立つためである。

- 独自LUNAR SERIFの欧文輪郭、月と星の `O`、既存の欧文カーニングを保持する。
- JP版の日本語コードポイントはShippori由来を基本とする。Shipporiに不足するJIS記号・ギリシャ/キリル文字・全角記号・半角カナ等260文字は固定Noto Serif JPから補い、U+2252（≒）だけは独自の単純輪郭で補う。
- ShipporiとNotoの補助字形を含めても、14字はShippori由来に統一し、既存の独自14字をJP版へ混在させない。
- ドナーの欧文字形を採用してLUNARの欧文を置き換えない。生成済みJPビルドでは、元の欧文マッピングをLUNAR輪郭へ戻している。
- 既存のDisplay版は、ロゴと初版の意図を守るため、独自14字を保持する。Display版とJP版の日本語字形は同一にしない。
- Shipporiの名前を製品名として再利用せず、派生物の名前を `LUNAR SERIF JP` とする。これは既存フォントの単なる改名ではなく、独自欧文とOFL和文を組み合わせた新しい派生フォントである。

### Noto Serif JPによる不足分の補完

Shipporiを主ドナーとし、要求集合で不足した260文字だけをNoto Serif JPから補完する。実装で固定する取得物は次のGoogle Fontsリポジトリのコミットである。

- 補助TTF（固定URL）: [`NotoSerifJP[wght].ttf`](https://raw.githubusercontent.com/google/fonts/8b0a1d0f5983c89bc2b93f1b5fb55f9e252744b5/ofl/notoserifjp/NotoSerifJP%5Bwght%5D.ttf)
- 固定コミット: [`8b0a1d0f5983c89bc2b93f1b5fb55f9e252744b5`](https://github.com/google/fonts/tree/8b0a1d0f5983c89bc2b93f1b5fb55f9e252744b5/ofl/notoserifjp)
- 補助TTFのSHA-256: `2fd527ba12b6a44ec30d796d633360da0aeba6c5d4af1304ce12bb4dc15a7dfc`
- 同梱ライセンス: [`OFL.txt`](https://raw.githubusercontent.com/google/fonts/8b0a1d0f5983c89bc2b93f1b5fb55f9e252744b5/ofl/notoserifjp/OFL.txt)
- 出典: [Noto Serif JP metadata](https://raw.githubusercontent.com/google/fonts/8b0a1d0f5983c89bc2b93f1b5fb55f9e252744b5/ofl/notoserifjp/METADATA.pb)

補助は不足コードポイントの輪郭をRegular相当（`wght=400`）で静的化し、Noto側のGSUB/GPOSをそのままJP版へ混ぜない。Shipporiの縦組み機能を維持するため、補助字形に必要な縦書き代替だけはJP版の`vert`/`vrt2`へ明示的に追加する。固定Notoで不足するU+2252（≒）は別のUnicode文字に置換せず、JPビルドが生成する単純輪郭を使う。

## 候補比較

| 候補 | 公式取得物・ライセンス | かな・縦書き | JIS第一/第二水準・常用漢字 | 採否 |
| --- | --- | --- | --- | --- |
| **Shippori Mincho** | [fontdasu/ShipporiMincho](https://github.com/fontdasu/ShipporiMincho)、固定Google Fonts TTF、OFL-1.1 | 上流READMEがひらがな、カタカナ、全角記号、縦書き用字形、かな異体を明記 | 上流READMEはJISの水準名や常用漢字数を明記しない。Google Fontsの公式監査issueは「full set」と記録するが、選択ファイルでJIS表と常用漢字2,136字を照合する | **採用**。静的Regular TTF、取得URLとSHA-256を固定できる |
| Noto Serif JP | [google/fonts/ofl/notoserifjp](https://github.com/google/fonts/tree/main/ofl/notoserifjp)、[`NotoSerifJP[wght].ttf`](https://raw.githubusercontent.com/google/fonts/main/ofl/notoserifjp/NotoSerifJP%5Bwght%5D.ttf)、OFL-1.1 | Google metadataがHiragana/Katakanaを言語として記載。Noto CJK READMEは適切な縦組み字形と比例かなを明記 | Notoの公式標本はNoto Serif CJK JPについて43,029文字・65,535グリフと説明するが、これはCJK JP標本全体の説明であり、選択するGoogle Fonts TTFのJIS/常用漢字を別途測定する必要がある | 保留。200–900の可変TTFで、Regularの固定・サブセット化とLUNARの既存GSUB/GPOS統合がShipporiより重い |
| Source Han Serif JP | [adobe-fonts/source-han-serif](https://github.com/adobe-fonts/source-han-serif)、公式リリースの[`02_SourceHanSerif-VF.zip`](https://github.com/adobe-fonts/source-han-serif/releases/download/2.003R/02_SourceHanSerif-VF.zip)（TTF可変版）、OFL-1.1 | Noto CJKと同じCJK系統の公式READMEが水平・垂直字形を明記。JP言語版には比例かな | Adobe公式issueは対応範囲としてJIS X 0208/X 0213/X 0212を挙げる一方、別issueはJIS第二水準の不足字形を報告している。現行ファイルの機械照合が必要 | 保留。配布が可変TTF/OTF中心で、`Source`がReserved Font Name。今回の静的Regular統合には手順と確認事項が多い |

### 候補の公式根拠

- Shippori README: [文字範囲と縦書き用字形](https://raw.githubusercontent.com/fontdasu/ShipporiMincho/63431fee6c2cfea772325d6251d2935b7cfa7c6d/README.md)、[OFL.txt](https://raw.githubusercontent.com/fontdasu/ShipporiMincho/63431fee6c2cfea7723251d2935b7cfa7c6d/OFL.txt)
- Google FontsのShippori metadata: [固定コミットのMETADATA.pb](https://raw.githubusercontent.com/google/fonts/d0b2d1307ad5d6b579d627a6e5abd25952484b96/ofl/shipporimincho/METADATA.pb)
- Google Fontsの日本語監査: [Issue #7056](https://github.com/google/fonts/issues/7056)。監査上の「full set」は参考情報であり、リリース判定は実ファイルの照合で行う。
- Noto Serif JP metadata/license: [固定コミットのMETADATA.pb](https://raw.githubusercontent.com/google/fonts/8b0a1d0f5983c89bc2b93f1b5fb55f9e252744b5/ofl/notoserifjp/METADATA.pb)、[固定コミットのOFL.txt](https://raw.githubusercontent.com/google/fonts/8b0a1d0f5983c89bc2b93f1b5fb55f9e252744b5/ofl/notoserifjp/OFL.txt)
- Noto CJK Serif README: [公式README](https://raw.githubusercontent.com/notofonts/noto-cjk/main/Serif/README.md)、[Noto Serif CJK JP標本](https://notofonts.github.io/noto-docs/specimen/NotoSerifCJKjp/)
- Source Han Serif README/リリース: [公式README](https://raw.githubusercontent.com/adobe-fonts/source-han-serif/master/README.md)、[2.003Rリリース](https://github.com/adobe-fonts/source-han-serif/releases/tag/2.003R)、[LICENSE.txt](https://raw.githubusercontent.com/adobe-fonts/source-han-serif/release/LICENSE.txt)
- Source HanのJIS範囲・不足報告: [Issue #40](https://github.com/adobe-fonts/source-han-serif/issues/40)、[Issue #174](https://github.com/adobe-fonts/source-han-serif/issues/174)

## 文字範囲の判定と実装者向け検証

「JIS第一・第二水準」「常用漢字」「日本語が表示できる」は同じ条件ではない。JIS X 0208の第一・第二水準は符号化集合の区分で、常用漢字2,136字は行政上の別の字種集合である。したがって、Shippori入力の15,363文字や、補完後JP版の15,624文字というcmap数だけで合格にしない。

JP版の固定TTFについて、少なくとも次をコードポイント単位で測定し、欠落一覧を成果物に残す。

1. JIS X 0208第一水準・第二水準の全リスト。
2. 常用漢字2,136字（新字体だけでなく、テストデータが要求する異体・旧字体を別欄で扱う）。
3. ひらがな・カタカナの基本字、濁点・半濁点、結合文字、長音、拗促音、ゕゖ・ヷヺなどの拡張かな。
4. 日本語で頻出する句読点・括弧・全角記号と、縦書き用の互換字形。
5. OpenTypeの `vert` / `vrt2`（存在する場合は `vhal` / `vkrn` も）を有効にした縦書きレンダリング。ブラウザの `writing-mode: vertical-rl` と、HarfBuzz等の実際のシェーピング結果を確認する。
6. Noto補助260文字の全マッピングと、独自生成U+2252（≒）の輪郭・横組みメトリクス。補助したU+FF3F・U+FF5C・U+FF5F・U+FF60・U+FFE3は、`vert` / `vrt2`の置換後に縦書き字形へ到達することを個別に確認する。

実装後は、通常文、縦書き文、濁点かな、JIS第二水準の難字、常用漢字の全件を描画する。元の参照スクリーンショットと生成画像の比較では、次を同じ条件で確認する。

- 独自欧文の細長い比率、高コントラストのセリフ、流れる `N`、月と星の `O` が保たれているか。
- JP版で14字だけ筆致が変わる箇所がなく、Shipporiの和文とNoto補助字形の境界で線幅・重心・約物の送りが不自然にならないか。
- Display版では独自14字が保持され、JP版との差が意図した版違いとして読めるか。
- 小サイズ、本文サイズ、見出しサイズ、横組み、縦組みで欠け・過密・約物の向き・濁点の位置ずれがないか。

## ライセンスと配布条件

Shippori Mincho、Noto Serif JP、Source Han Serifは、確認した公式配布物がいずれもSIL Open Font License 1.1（OFL-1.1）である。OFL-1.1は、フォントの使用・研究・コピー・結合・埋め込み・改変・再配布を許可するが、次を守る必要がある。

- フォント単体または個別コンポーネントを単独販売しない。ソフトウェアやデザインへの同梱・埋め込み・販売は可能。
- 配布物に、各著作権表示とOFL本文（または容易に閲覧できる機械可読メタデータ）を含める。
- 改変版の主要フォント名にReserved Font Nameを使わない。Source Han Serifの `Source` はReserved Font Nameである。今回の製品名 `LUNAR SERIF JP` はこれに該当しない。
- フォントソフトウェアの全体をOFL-1.1で配布し、既存のカスタム許諾や別ライセンスを同じ派生フォントのライセンスとして併記しない。
- ドナー作者名を広告・推奨のように使わず、著作権表示と貢献の謝辞として記載する。

現行のルート[`LICENSE.txt`](../LICENSE.txt)は元版の独自LUNAR資産（Display版を含む）に適用する。JP派生版は、出力物に同梱した[`LUNAR-SERIF-JP-OFL.txt`](../outputs/LUNAR-SERIF-JP-OFL.txt)を適用し、`LUNARSERIFJP-Regular.ttf`・`LUNARSERIFJP-Regular.woff2`・そのフォントメタデータをOFL-1.1で配布する。この同梱OFLには、Shipporiの`Copyright 2021 The Shippori Mincho Project Authors`、Noto配布物の`Copyright 2012 Google Inc. All Rights Reserved.`と選択TTFの`(c) 2017-2024 Adobe (http://www.adobe.com/).`、OFL本文、および独自LUNAR欧文・統合部分の著作権表示を含める。JP版の主要フォント名は`LUNAR SERIF JP`とし、元版のカスタム許諾をJP派生版のライセンスとして併記しない。

## 実装時に固定する記録

JPビルドの再現性を保つため、次をリポジトリ内の実装記録に残す。

- ドナー固定URL、固定コミット、SHA-256、取得日。
- 補助ドナーNoto Serif JPの固定URL、固定コミット、SHA-256、取得日（`8b0a1d0f5983c89bc2b93f1b5fb55f9e252744b5` / `2fd527ba12b6a44ec30d796d633360da0aeba6c5d4af1304ce12bb4dc15a7dfc`）。
- 生成TTF/WOFF2のSHA-256と、cmap実測値（Shippori入力15,363文字、補完後JP版15,624文字）。
- Shippori不足の補助260文字と、独自に生成したU+2252（≒）1文字の内訳。
- JIS第一・第二水準、常用漢字、かな、縦書きの検証リストと欠落数。
- 元の14字をJP版でShipporiに置き換えたこと、Display版で保持したこと。
- Shippori/Noto両ドナーの著作権表示とOFL本文を同梱した場所。
