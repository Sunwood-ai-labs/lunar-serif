"""Measure aspect ratios, not a perceptual similarity score."""
from pathlib import Path
from PIL import Image
from fontTools.ttLib import TTFont
import json,hashlib
root=Path(__file__).resolve().parents[1]
reference=root/'references/01-lunar-serif.png'
im=Image.open(reference).convert('L')
fonts={key:TTFont(path) for key,path in {'before':root/'verification/comparison/before/LUNARSERIF-Regular.ttf','current':root/'outputs/LUNARSERIF-Regular.ttf'}.items()}
rows=[]
for char,box in [('N',(56,119,244,332)),('O',(247,118,447,333)),('S',(883,118,1000,333))]:
    bounds=im.crop(box).point(lambda p:255 if p<100 else 0).getbbox()
    x,y,X,Y=bounds
    row={'char':char,'reference_roi_xyxy':box,'reference_ink_width_height_ratio':(X-x)/(Y-y)}
    for key,font in fonts.items():
        g=font['glyf'][font.getBestCmap()[ord(char)]]
        ratio=(g.xMax-g.xMin)/(g.yMax-g.yMin)
        row[key+'_ratio']=ratio
        row[key+'_relative_ratio_error_percent']=100*abs(ratio/row['reference_ink_width_height_ratio']-1)
    rows.append(row)
report={'method':'Reference threshold <100 on manually selected hero ROIs; TTF outline bounding boxes. Ratios measure proportion only, not outline identity. N ROI excludes neighbouring O.','reference_sha256':hashlib.sha256(reference.read_bytes()).hexdigest(),'glyphs':rows}
(root/'verification/comparison/metrics.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(rows,indent=2))
