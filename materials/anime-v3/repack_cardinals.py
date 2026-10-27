from pathlib import Path
import sys, shutil, json
from PIL import Image
sys.path.insert(0,r'[local path redacted]')
from extract_strip_frames import remove_chroma_background, component_frame_groups, component_group_image, component_bounds
r=Path(__file__).parent
p=r/'decoded/look-cardinals.png'
shutil.copy2(p,r/'decoded/look-cardinals-original.png')
strip=remove_chroma_background(Image.open(p),(255,0,255),96)
groups=component_frame_groups(strip,4)
assert groups is not None and len(groups)==4
boxes=[component_bounds(g) for g in groups]
slot=max(b[2]-b[0] for b in boxes)+100
out=Image.new('RGBA',(slot*4,strip.height+40),(255,0,255,255))
for i,(g,b) in enumerate(zip(groups,boxes)):
    sprite=component_group_image(strip,g,padding=0)
    out.alpha_composite(sprite,(i*slot+(slot-sprite.width)//2,b[1]+20))
out.convert('RGB').save(p)
(r/'qa/cardinal-spacing-correction.json').write_text(json.dumps({'original_bounds':boxes,'new_slot_width':slot,'shared_scale':1,'method':'Recover complete connected groups and add chroma padding; no redrawing or clipping'},indent=2))
