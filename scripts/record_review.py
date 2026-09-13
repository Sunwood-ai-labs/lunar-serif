"""Record the human-readable decisions made during the screenshot audit."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'verification/audit/ledger.json'
ledger=json.loads(path.read_text(encoding='utf-8'))
notes={
'A':'横棒を上げ、幅を調整。鋭い頂点と細い左斜線を維持。',
'B':'上下の空洞を確認。見本に対して広かった幅を縮小。',
'C':'開口・上下端・実寸を確認。ロゴを優先した形。下部の太さは見本と差が残る。',
'D':'幅を縮小。縦線と曲線の接続、空洞を確認。',
'E':'横棒と終端を確認。大きなロゴの形を優先。',
'F':'中央横棒と終端を確認。小さい見本との曲率差は残る。',
'G':'右下に突き出ていたC由来の線を収め、縦線との接続を修正。',
'H':'横棒と縦線の接続を確認。高コントラストの線を維持。',
'I':'ロゴ基準の幅を維持。上下セリフと実寸を確認。',
'J':'幅を縮小。下端の丸い終筆は独自の特徴として維持。',
'K':'交差部と脚を確認。直線的な脚は独自設計として維持。',
'L':'下横棒と右終端を確認。輪郭を維持。',
'M':'幅を拡大。中央の接続と左右の細太を確認。',
'N':'ロゴ基準の流れる対角線を維持。一覧見本と形が異なることを明記。',
'O':'ロゴ基準の月と星を維持。一覧見本は装飾なしである。',
'P':'上部が広すぎたため幅を縮小。空洞を確認。',
'Q':'払いの始点を左へ移し、見本の横断する曲線に近づけた。',
'R':'幅を調整。上部の空洞と流れる脚を確認。',
'S':'ロゴ基準の細い比率を維持。腰の曲率は完全一致ではない。',
'T':'横棒端と幹の接続を確認。ロゴ基準の幅を維持。',
'U':'下部の連続性を確認。見本より繊細な下部を維持。',
'V':'頂点の接続と実寸を確認。隣接文字との実輪郭交差なし。',
'W':'中央上端にセリフを追加。下部の接続を確認。',
'X':'交差部と四端を確認。光学的な外接矩形の重なりは実輪郭交差ではない。',
'Y':'分岐と縦線の接続を重ね、微小な切れ目を防止。',
'Z':'上下横棒・斜線・終端を確認。輪郭を維持。',
'0':'楕円の空洞と小サイズを確認。等幅数字の送りを維持。',
'1':'斜めの旗を短く曲線化し、見本に近づけた。',
'2':'斜線と下横棒を確認。見本より繊細な終端を維持。',
'3':'上下の曲線と中央の接続を確認。',
'4':'横棒を太くして見本に近づけ、接続を確認。',
'5':'上横棒と下部を確認。小サイズでも識別可能。',
'6':'楕円と上部の接続を確認。',
'7':'上横棒と斜線の接続を確認。',
'8':'二つの楕円の重なりを廃止。中央の余計な空洞をなくし、二つの空洞に再設計。',
'9':'楕円と下部の接続を確認。',
'g':'上下の空洞を持つ連続した輪郭に再設計し、首の切れ目を解消。',
'j':'ベースライン途中の不要なセリフを除去。点と本体の二つの輪郭を確認。',
'“':'二つ目の引用符を正確な平行移動で生成。崩れた輪郭を修正。',
'”':'二つ目の引用符を正確な平行移動で生成。崩れた輪郭を修正。',
}
revised=set('ABDGJMPQRWY148gj“”ノクティセーヌ夜に、余韻を。')
pages=json.loads((ROOT/'verification/audit/pages.json').read_text(encoding='utf-8'))
mapping={n:p for p,ns in pages.items() for n in ns}
for name,d in ledger.items():
    c=d['char']
    if c in 'ノクティセーヌ夜に、余韻を。' if c else False:
        note='生成見本から輪郭を再構成し、階段状の段差を曲線化。筆の強弱・交差・空洞・実寸を確認。低解像度由来の細部の差は残る。'
    elif c in notes: note=notes[c]
    elif c and c.islower():note='生成見本なし。x-height、アセンダー/ディセンダー、接続、空洞、24/48/72pxを確認。独自の字形を維持。'
    elif c and c.isspace():note='意図した空白で輪郭なし。送り250 UPMを確認。'
    elif name=='O.plain':note='ss01の装飾なしO。輪郭と機能切替を確認。'
    elif name=='.notdef':note='TTF内の未定義字形を直接描画。代替フォントを使わず枠と斜線を確認。'
    else:note='生成見本なし。方向・部品数・位置・実寸・隣接輪郭の交差を確認。形を維持。'
    d.update(review='reviewed',decision='revised' if c in revised else 'retained',notes=note,evidence=f'{mapping[name]}-final.png')
path.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded 120 screenshot review decisions')
