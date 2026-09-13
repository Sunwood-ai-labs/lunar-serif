# 漢字96字のコンセプト見本

内蔵imagegenで生成。実際のフォントのレンダリングではなく、造形の方向性を比較するための提案です。

画像: `../references/03-lunar-serif-kanji-study-01.png`

## 対象文字

```
一 二 三 十 人 入 大 小 山 川 日 月
木 林 森 本 末 未 水 氷 火 炎 土 王
永 夜 余 韻 愛 心 静 星 雨 雪 雲 霧
海 湖 波 清 深 涼 流 涙 泳 渡 満 澄
花 草 葉 蓮 夢 薫 華 藤 薄 薔 薇 蕾
言 語 読 詩 話 記 調 論 識 議 護 響
国 園 図 回 困 間 門 開 閉 聞 闇 関
線 結 綾 織 美 麗 鶴 鳳 龍 鬱 曖 曜
```

## 目視確認

12列×8行の見本。少画数、木偏、さんずい、草冠、言偏、囲み、糸偏、高密度の文字を比較できるよう拡充しました。繊細な横画と明朝の縦画、払いの方向性を確認できます。

「鬱」は生成時に構造の崩れが見られ、対象セルのみ補正を指示しましたが、再生成後も十分に直っていません。正確な字形の原図としては未承認です。他の複雑な文字もフォント化前に個別照合が必要です。96字の正字形を保証する完成見本ではありません。

## 生成プロンプト

Create a NEW comprehensive KANJI TYPE DESIGN SPECIMEN, matching the attached LUNAR SERIF Japanese concept reference. This is a typography design proposal, not an existing font screenshot. Pure white background, crisp black lettering, exceptionally restrained gray rules, no illustrations or ornament, no website UI. High resolution landscape sheet. Main task: SHOW ALL 96 distinct kanji below in a spacious, perfectly ordered 12-column by 8-row grid. Do not omit, repeat, substitute, or invent characters. Each cell contains ONE large kanji only. No explanatory text in cells. All cells same optical em size. Small heading at top only: LUNAR SERIF — KANJI STUDY 01.
Exact rows, each 12 kanji:
一 二 三 十 人 入 大 小 山 川 日 月
木 林 森 本 末 未 水 氷 火 炎 土 王
永 夜 余 韻 愛 心 静 星 雨 雪 雲 霧
海 湖 波 清 深 涼 流 涙 泳 渡 満 澄
花 草 葉 蓮 夢 薫 華 藤 薄 薔 薇 蕾
言 語 読 詩 話 記 調 論 識 議 護 響
国 園 図 回 困 間 門 開 閉 聞 闇 関
線 結 綾 織 美 麗 鶴 鳳 龍 鬱 曖 曜
Design: elegant delicate high-contrast Japanese Mincho companion for the reference's tall flowing Latin; precise fine horizontal hairlines, slender substantial verticals, restrained triangular terminals, graceful long tapered sweeps, airy counters and quiet literary sophistication. Preserve CORRECT conventional Japanese kanji stroke structures and Japanese forms (not Chinese regional glyph variants), especially 未/末, 人/入, 水/氷, 鬱/響/薔/麗. Keep dense characters legible through open counters and optical stroke adjustments, not omissions. No heavy brush calligraphy, no sans serif, no random crescent/star motifs inside kanji. Consistent family across simple and complex characters. Make the characters the focus: generous evenly spaced grid fills the sheet, each glyph large enough to inspect. Use the attached reference only for the aesthetic; do not copy its limited eight-character layout or large Latin logo.

## 補正プロンプト

Edit this kanji specimen with one surgical correction. Preserve the entire 12-column, 8-row grid, all other 95 characters, typography, spacing and heading exactly. Correct ONLY row 8 column 10, the character 鬱. It must have the correct standard Japanese 29-stroke structure: upper 木 缶 木 arrangement, 冖 beneath, lower 鬯 on the left and three diagonal strokes 彡 on the right. No invented boxes or repeated components. Render 鬱 in the same elegant high-contrast Japanese Mincho design with clear fine strokes and correct proportions. Do not alter any other glyph.
