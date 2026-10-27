from pathlib import Path
import subprocess,sys
r=Path(__file__).parent.resolve()
s=Path(r'[local path redacted]')
def call(name,*args):subprocess.run([sys.executable,str(s/(name+'.py')),*map(str,args)],check=True)
call('extract_strip_frames','--decoded-dir',r/'decoded','--output-dir',r/'frames','--states','all','--method','auto')
subprocess.run([sys.executable,str(r/'normalize_standard_frames.py')],check=True)
call('inspect_frames','--frames-root',r/'frames','--json-out',r/'qa/review.json','--states','all','--require-components')
call('compose_atlas','--frames-root',r/'frames','--output',r/'final/spritesheet.png')
call('make_contact_sheet',r/'final/spritesheet.png','--output',r/'qa/contact-sheet.png')
call('render_animation_previews','--frames-root',r/'frames','--output-dir',r/'qa/standard-previews')
