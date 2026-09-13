# 全120字形のスクリーンショット監査 — 1.002

2026-09-13。全120字形の個別拡大と24/48/72px表示を確認し、23ページの最終スクリーンショットを保存しました。生成見本があるのは50文字です。残る70字形は独自設計・空白・代替O・未定義字形として確認しています。

数字8の余分な空洞、gの切れ目、jの途中のセリフ、二重引用符の破損を修正。A/B/D/J/M/P/R等の比率や接続を調整し、G/Q/W/Yも修正しました。和文14文字は生成見本から曲線を再構成しています。

可視116文字の全13,456隣接組をアウトラインの積集合で検証し、実輪郭の交差は0件でした。外接矩形が重なる27組も輪郭自体は重なりません。TTF/WOFF2読み込み、カーニング、ss01、輪郭範囲、回帰検証、同じビルドのSHA-256一致も確認しています。

## 証拠と制限

各行のリンクが最終スクリーンショットです。`ledger.json`に個別判断、`evidence.json`に最終フォントと画像のハッシュ、`geometry.json`と`spacing.json`に機械検証結果を保存しています。ブラウザーでWOFF2をロードし、ロード結果が空でないことを確認して撮影しました。

これは全輪郭の完全一致という判定ではありません。元の生成画像は低解像度で、ロゴと小さな一覧にも違いがあります。N/O/S等はロゴの形を優先。和文は筆致を復元しつつ微細な段差を曲線化したため、筆先や曲率には再構成による差が残ります。小さい本文専用のフォントとしては設計していません。

## 全字形の個別判断

| 字形 | 処理 | 確認・判断 | スクリーンショット |
|---|---|---|---|
| A (uni0041) | revised | 横棒を上げ、幅を調整。鋭い頂点と細い左斜線を維持。 | [画像](upper-1-final.png) |
| B (uni0042) | revised | 上下の空洞を確認。見本に対して広かった幅を縮小。 | [画像](upper-1-final.png) |
| C (uni0043) | retained | 開口・上下端・実寸を確認。ロゴを優先した形。下部の太さは見本と差が残る。 | [画像](upper-1-final.png) |
| D (uni0044) | revised | 幅を縮小。縦線と曲線の接続、空洞を確認。 | [画像](upper-1-final.png) |
| E (uni0045) | retained | 横棒と終端を確認。大きなロゴの形を優先。 | [画像](upper-1-final.png) |
| F (uni0046) | retained | 中央横棒と終端を確認。小さい見本との曲率差は残る。 | [画像](upper-1-final.png) |
| G (uni0047) | revised | 右下に突き出ていたC由来の線を収め、縦線との接続を修正。 | [画像](upper-2-final.png) |
| H (uni0048) | retained | 横棒と縦線の接続を確認。高コントラストの線を維持。 | [画像](upper-2-final.png) |
| I (uni0049) | retained | ロゴ基準の幅を維持。上下セリフと実寸を確認。 | [画像](upper-2-final.png) |
| J (uni004A) | revised | 幅を縮小。下端の丸い終筆は独自の特徴として維持。 | [画像](upper-2-final.png) |
| K (uni004B) | retained | 交差部と脚を確認。直線的な脚は独自設計として維持。 | [画像](upper-2-final.png) |
| L (uni004C) | retained | 下横棒と右終端を確認。輪郭を維持。 | [画像](upper-2-final.png) |
| M (uni004D) | revised | 幅を拡大。中央の接続と左右の細太を確認。 | [画像](upper-3-final.png) |
| N (uni004E) | retained | ロゴ基準の流れる対角線を維持。一覧見本と形が異なることを明記。 | [画像](upper-3-final.png) |
| O (uni004F) | retained | ロゴ基準の月と星を維持。一覧見本は装飾なしである。 | [画像](upper-3-final.png) |
| O.plain (O.plain) | retained | ss01の装飾なしO。輪郭と機能切替を確認。 | [画像](symbols-8-final.png) |
| P (uni0050) | revised | 上部が広すぎたため幅を縮小。空洞を確認。 | [画像](upper-3-final.png) |
| Q (uni0051) | revised | 払いの始点を左へ移し、見本の横断する曲線に近づけた。 | [画像](upper-3-final.png) |
| R (uni0052) | revised | 幅を調整。上部の空洞と流れる脚を確認。 | [画像](upper-3-final.png) |
| S (uni0053) | retained | ロゴ基準の細い比率を維持。腰の曲率は完全一致ではない。 | [画像](upper-4-final.png) |
| T (uni0054) | retained | 横棒端と幹の接続を確認。ロゴ基準の幅を維持。 | [画像](upper-4-final.png) |
| U (uni0055) | retained | 下部の連続性を確認。見本より繊細な下部を維持。 | [画像](upper-4-final.png) |
| V (uni0056) | retained | 頂点の接続と実寸を確認。隣接文字との実輪郭交差なし。 | [画像](upper-4-final.png) |
| W (uni0057) | revised | 中央上端にセリフを追加。下部の接続を確認。 | [画像](upper-4-final.png) |
| X (uni0058) | retained | 交差部と四端を確認。光学的な外接矩形の重なりは実輪郭交差ではない。 | [画像](upper-4-final.png) |
| Y (uni0059) | revised | 分岐と縦線の接続を重ね、微小な切れ目を防止。 | [画像](upper-5-final.png) |
| Z (uni005A) | retained | 上下横棒・斜線・終端を確認。輪郭を維持。 | [画像](upper-5-final.png) |
| a (uni0061) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-1-final.png) |
| b (uni0062) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-1-final.png) |
| c (uni0063) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-1-final.png) |
| d (uni0064) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-1-final.png) |
| e (uni0065) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-1-final.png) |
| f (uni0066) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-1-final.png) |
| g (uni0067) | revised | 上下の空洞を持つ連続した輪郭に再設計し、首の切れ目を解消。 | [画像](lower-2-final.png) |
| h (uni0068) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-2-final.png) |
| i (uni0069) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-2-final.png) |
| j (uni006A) | revised | ベースライン途中の不要なセリフを除去。点と本体の二つの輪郭を確認。 | [画像](lower-2-final.png) |
| k (uni006B) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-2-final.png) |
| l (uni006C) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-2-final.png) |
| m (uni006D) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-3-final.png) |
| n (uni006E) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-3-final.png) |
| o (uni006F) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-3-final.png) |
| p (uni0070) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-3-final.png) |
| q (uni0071) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-3-final.png) |
| r (uni0072) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-3-final.png) |
| s (uni0073) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-4-final.png) |
| t (uni0074) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-4-final.png) |
| u (uni0075) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-4-final.png) |
| v (uni0076) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-4-final.png) |
| w (uni0077) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-4-final.png) |
| x (uni0078) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-4-final.png) |
| y (uni0079) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-5-final.png) |
| z (uni007A) | retained | 生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。 | [画像](lower-5-final.png) |
| 0 (uni0030) | retained | 楕円の空洞と小サイズを確認。等幅数字の送りを維持。 | [画像](digits-1-final.png) |
| 1 (uni0031) | revised | 斜めの旗を短く曲線化し、見本に近づけた。 | [画像](digits-1-final.png) |
| 2 (uni0032) | retained | 斜線と下横棒を確認。見本より繊細な終端を維持。 | [画像](digits-1-final.png) |
| 3 (uni0033) | retained | 上下の曲線と中央の接続を確認。 | [画像](digits-1-final.png) |
| 4 (uni0034) | revised | 横棒を太くして見本に近づけ、接続を確認。 | [画像](digits-1-final.png) |
| 5 (uni0035) | retained | 上横棒と下部を確認。小サイズでも識別可能。 | [画像](digits-1-final.png) |
| 6 (uni0036) | retained | 楕円と上部の接続を確認。 | [画像](digits-2-final.png) |
| 7 (uni0037) | retained | 上横棒と斜線の接続を確認。 | [画像](digits-2-final.png) |
| 8 (uni0038) | revised | 二つの楕円の重なりを廃止。中央の余計な空洞をなくし、二つの空洞に再設計。 | [画像](digits-2-final.png) |
| 9 (uni0039) | retained | 楕円と下部の接続を確認。 | [画像](digits-2-final.png) |
| SPACE (uni0020) | retained | 意図した空白で輪郭なし。送り250 UPMを確認。 | [画像](symbols-1-final.png) |
| NBSP (uni00A0) | retained | 意図した空白で輪郭なし。送り250 UPMを確認。 | [画像](symbols-1-final.png) |
| . (uni002E) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-1-final.png) |
| , (uni002C) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-1-final.png) |
| : (uni003A) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-1-final.png) |
| ; (uni003B) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-1-final.png) |
| ! (uni0021) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-2-final.png) |
| ? (uni003F) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-2-final.png) |
| - (uni002D) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-2-final.png) |
| – (uni2013) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-2-final.png) |
| — (uni2014) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-2-final.png) |
| _ (uni005F) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-2-final.png) |
| / (uni002F) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-3-final.png) |
| \ (uni005C) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-3-final.png) |
| &#124; (uni007C) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-3-final.png) |
| ( (uni0028) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-3-final.png) |
| ) (uni0029) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-3-final.png) |
| [ (uni005B) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-3-final.png) |
| ] (uni005D) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-4-final.png) |
| { (uni007B) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-4-final.png) |
| } (uni007D) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-4-final.png) |
| ' (uni0027) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-4-final.png) |
| " (uni0022) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-4-final.png) |
| ` (uni0060) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-4-final.png) |
| ^ (uni005E) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-5-final.png) |
| ~ (uni007E) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-5-final.png) |
| + (uni002B) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-5-final.png) |
| = (uni003D) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-5-final.png) |
| < (uni003C) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-5-final.png) |
| > (uni003E) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-5-final.png) |
| * (uni002A) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-6-final.png) |
| # (uni0023) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-6-final.png) |
| $ (uni0024) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-6-final.png) |
| % (uni0025) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-6-final.png) |
| & (uni0026) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-6-final.png) |
| @ (uni0040) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-6-final.png) |
| ‘ (uni2018) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-7-final.png) |
| ’ (uni2019) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-7-final.png) |
| “ (uni201C) | revised | 二つ目の引用符を正確な平行移動で生成。崩れた輪郭を修正。 | [画像](symbols-7-final.png) |
| ” (uni201D) | revised | 二つ目の引用符を正確な平行移動で生成。崩れた輪郭を修正。 | [画像](symbols-7-final.png) |
| … (uni2026) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-7-final.png) |
| × (uni00D7) | retained | 生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。 | [画像](symbols-7-final.png) |
| ノ (uni30CE) | revised | 生成見本から輪郭を再構成し、階段状の段差を曲線化。筆の強弱・交差・空洞・実寸を確認。低解像度由来の細部の差は残る。 | [画像](japanese-1-final.png) |
| ク (uni30AF) | revised | 生成見本から輪郭を再構成し、階段状の段差を曲線化。筆の強弱・交差・空洞・実寸を確認。低解像度由来の細部の差は残る。 | [画像](japanese-1-final.png) |
| テ (uni30C6) | revised | 生成見本から輪郭を再構成し、階段状の段差を曲線化。筆の強弱・交差・空洞・実寸を確認。低解像度由来の細部の差は残る。 | [画像](japanese-1-final.png) |
| ィ (uni30A3) | revised | 生成見本から輪郭を再構成し、階段状の段差を曲線化。筆の強弱・交差・空洞・実寸を確認。低解像度由来の細部の差は残る。 | [画像](japanese-1-final.png) |
| セ (uni30BB) | revised | 生成見本から輪郭を再構成し、階段状の段差を曲線化。筆の強弱・交差・空洞・実寸を確認。低解像度由来の細部の差は残る。 | [画像](japanese-1-final.png) |
| ー (uni30FC) | revised | 生成見本から輪郭を再構成し、階段状の段差を曲線化。筆の強弱・交差・空洞・実寸を確認。低解像度由来の細部の差は残る。 | [画像](japanese-1-final.png) |
| ヌ (uni30CC) | revised | 生成見本から輪郭を再構成し、階段状の段差を曲線化。筆の強弱・交差・空洞・実寸を確認。低解像度由来の細部の差は残る。 | [画像](japanese-2-final.png) |
| に (uni306B) | revised | 生成見本から輪郭を再構成し、階段状の段差を曲線化。筆の強弱・交差・空洞・実寸を確認。低解像度由来の細部の差は残る。 | [画像](japanese-2-final.png) |
| を (uni3092) | revised | 生成見本から輪郭を再構成し、階段状の段差を曲線化。筆の強弱・交差・空洞・実寸を確認。低解像度由来の細部の差は残る。 | [画像](japanese-2-final.png) |
| 、 (uni3001) | revised | 生成見本から輪郭を再構成し、階段状の段差を曲線化。筆の強弱・交差・空洞・実寸を確認。低解像度由来の細部の差は残る。 | [画像](japanese-2-final.png) |
| 。 (uni3002) | revised | 生成見本から輪郭を再構成し、階段状の段差を曲線化。筆の強弱・交差・空洞・実寸を確認。低解像度由来の細部の差は残る。 | [画像](japanese-2-final.png) |
| 余 (uni4F59) | revised | 生成見本から輪郭を再構成し、階段状の段差を曲線化。筆の強弱・交差・空洞・実寸を確認。低解像度由来の細部の差は残る。 | [画像](japanese-2-final.png) |
| 夜 (uni591C) | revised | 生成見本から輪郭を再構成し、階段状の段差を曲線化。筆の強弱・交差・空洞・実寸を確認。低解像度由来の細部の差は残る。 | [画像](japanese-3-final.png) |
| 韻 (uni97FB) | revised | 生成見本から輪郭を再構成し、階段状の段差を曲線化。筆の強弱・交差・空洞・実寸を確認。低解像度由来の細部の差は残る。 | [画像](japanese-3-final.png) |
| .notdef (.notdef) | retained | TTF内の未定義字形を直接描画。代替フォントを使わず枠と斜線を確認。 | [画像](symbols-8-final.png) |
