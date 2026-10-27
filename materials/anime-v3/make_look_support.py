from PIL import Image
from pathlib import Path
r=Path(__file__).parent
a=Image.open(r/'qa/contact-sheet.png').convert('RGB')
ref=Image.open(r/'references/reference-02.png').convert('RGB')
left=Image.open(r/'decoded/look-anchors/270.png').convert('RGBA').resize((384,416))
for n in (9,10):
    b=Image.open(r/f'references/layout-guides/look-row-{n}.png').convert('RGB')
    out=Image.new('RGB',(1536,a.height+b.height),'white')
    out.paste(a,((out.width-a.width)//2,0))
    out.paste(ref,(0,0))
    out.paste(b,(0,a.height))
    if n==10:out.paste(left,(0,170),left)
    out.save(r/f'references/look-row-{n}-support.png')
