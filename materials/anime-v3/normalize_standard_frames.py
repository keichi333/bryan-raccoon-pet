"""Apply one documented scale per row to extracted generated pixels, preserving jumps."""
from pathlib import Path
import json
from PIL import Image

run = Path(__file__).parent
root = run/'frames'
manifest = json.loads((root/'frames-manifest.json').read_text())
corrections=[]
for row in manifest['rows']:
    state=row['state']
    factor=1.0 if state=='jumping' else (0.93 if state in ('running-right','running-left') else 0.74)
    paths=sorted((root/state).glob('*.png'))
    frames=[Image.open(p).convert('RGBA') for p in paths]
    bottoms=[f.getchannel('A').point(lambda a:255 if a>16 else 0).getbbox()[3] for f in frames]
    row_bottom=max(bottoms)
    for path,frame in zip(paths,frames):
        w,h=round(192*factor),round(208*factor)
        scaled=frame.resize((w,h),Image.Resampling.LANCZOS)
        target=Image.new('RGBA',(192,208))
        target.alpha_composite(scaled,(round(96-96*factor),round(202-row_bottom*factor)))
        target.save(path)
    corrections.append({'state':state,'shared_scale':factor,'source_row_bottom':row_bottom,'target_baseline':202})
(run/'qa'/'standard-registration.json').write_text(json.dumps({'purpose':'Match standing and airborne body size; preserve within-row motion with shared transforms','rows':corrections},indent=2))
print(json.dumps({'ok':True,'rows':corrections}))
