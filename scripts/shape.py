"""Run HarfBuzz independently so validation may use separate Python runtimes."""
from pathlib import Path
import json
import uharfbuzz as hb

root=Path(__file__).resolve().parents[1]
font=hb.Font(hb.Face((root/'outputs/LUNARSERIF-Regular.ttf').read_bytes()))
font.scale=(1000,1000)
result={'version':hb.version_string()}
required='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ノクティセーヌ夜に、余韻を。'
for key,text,features in [('logo','NOCTISENE',{}),('plain','NOCTISENE',{'ss01':True}),('unkerned','NOCTISENE',{'kern':False}),('required',required,{})]:
    buf=hb.Buffer();buf.add_str(text);buf.guess_segment_properties();hb.shape(font,buf,features)
    result[key]=[{'id':g.codepoint,'position':{'x_advance':p.x_advance,'x_offset':p.x_offset,'y_offset':p.y_offset}} for g,p in zip(buf.glyph_infos,buf.glyph_positions)]
print(json.dumps(result))
