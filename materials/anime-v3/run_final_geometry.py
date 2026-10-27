"""Call mandatory bundled stages sequentially; stop on any actual script error."""
from pathlib import Path
import subprocess, sys
r=Path(__file__).parent.resolve()
s=Path(r'[local path redacted]')
def call(name,*args):
    subprocess.run([sys.executable,str(s/(name+'.py')),*map(str,args)],check=True)
raw=r/'final/spritesheet-extended-raw.png'
final=r/'final/spritesheet-extended.png'
call('assemble_extended_atlas','--base-atlas',r/'final/spritesheet.png','--registered-row-9',r/'decoded/look-row-9-registered.png','--row-9-registration',r/'qa/row-9-registration.json','--look-row-10',r/'decoded/look-row-10.png','--chroma-key','#FF00FF','--output',raw,'--manifest-output',r/'final/sprite-manifest.json')
call('despill_chroma_edges',raw,'--output',final,'--json-out',r/'qa/chroma-despill-extended.json','--chroma-key','#FF00FF')
call('validate_atlas',final,'--require-v2','--chroma-key','#FF00FF','--json-out',r/'final/validation-extended.json')
call('make_contact_sheet',final,'--output',r/'qa/contact-sheet-extended.png')
call('make_direction_qa_sheet',final,'--output',r/'qa/direction-sheet.png')
call('measure_direction_continuity',final,'--json-out',r/'qa/look-continuity.json')
call('make_direction_blind_qa_sheet',final,'--output',r/'qa/direction-blind.png','--answer-key',r/'qa/direction-blind-key.json')
subprocess.run([sys.executable,str(r/'make_delivery_previews.py'),str(final),str(r/'qa/final-previews')],check=True)
