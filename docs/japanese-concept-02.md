# 和文コンセプト02 — デザイン提案

2026-09-13。built-in image_genで生成。実フォントのレンダリングではありません。

画像: [02-lunar-serif-japanese-concept.png](../references/02-lunar-serif-japanese-concept.png)

現行JP版は実用上の収録範囲・組版を整えた段階で、コンセプトへの造形的な一致は未完です。今回は元のN/O/Sを参照し、繊細な細太、流れるかな、余白のある字面を和文側へ展開する基準見本を作成しました。

画像の文字の揺れをそのまま全字へ広げず、代表字（永・夜・月・余・韻・愛・心・静、かな、濁点）で字面の大きさ・細太・払い・和欧文の重さを決め、その規則を実フォントへ適用する方針です。縦書きの約物位置と小サイズの可読性は実レンダリングで別途確認します。既存のTTF/WOFF2は今回変更していません。

## 生成プロンプト

```text
Use case: logo-brand. Create a NEW Japanese/Latin type-design concept specimen board for LUNAR SERIF / NOCTISENE, using the attached image only as the original visual reference. This is a proposed future font design, not a screenshot of an existing font. Portrait or landscape large high-resolution flat specimen on pure white, black lettering only, thin light gray section rules, generous negative space. No website UI, no moon illustration, no gradients, no paper perspective or textures, no decorative objects.
Art direction: nocturnal, intelligent, mature, literary intimacy, lingering resonance, quiet strength. Preserve the original reference's elegant high-contrast thin tall Latin proportions, flowing N diagonal, crescent moon plus four-point star INSIDE the uppercase O, supple narrow S. A single prominent NOCTISENE logo across the top, spelled exactly N O C T I S E N E.
Main focus: design a matching distinctive Japanese Mincho-style companion. Slim graceful stems, very fine hairlines but clearly connected strokes, restrained triangular terminals, long precise tapered sweeps, gently flowing kana, airy inner counters, modest optical glyph size and darkness relative to Latin. More delicate and literary than a generic large heavy textbook Mincho. No heavy brush calligraphy, no gothic/sans serif, no arbitrary stars or moons added to Japanese characters, no distortion of legitimate Japanese stroke structure. Japanese text must be correct, legible and unbroken.
Show these exact phrases, with substantial size:
「ノクティセーヌ」
「夜に、余韻を。」
「月明かりに、言葉がほどける。」
Show one mixed Latin/Japanese line: 「NOCTISENE と、静かな夜。」
Show a small vertical typography sample of 「夜に、余韻を。」 with proper vertical punctuation.
Bottom half: a generous character specimen strip with individual large Japanese characters 「永 夜 月 余 韻 愛 心 静」, and another kana strip 「あ か さ な は ま ら が ぱ ヴ」. Give ample spacing so no two glyphs collide. Keep glyph forms consistent between text examples and individual samples. These are reference shapes intended to guide subsequent outline design. Small heading at very top: LUNAR SERIF — JAPANESE CONCEPT 02. Do not include explanatory body text or claim these are real font renders. Harmonious, polished, editorial typography art direction, faithfully related to the supplied original logo.
```
