"""Render additional required previews from the exact encoded atlas, no artwork synthesis."""
from pathlib import Path
import sys, subprocess, json
from PIL import Image, ImageDraw

RUN = Path(__file__).parent
SCRIPTS = Path(r'[local path redacted]')
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(RUN / 'deps'))
from render_animation_previews import ROW_DURATIONS, save_preview
import imageio_ffmpeg

atlas_path = Path(sys.argv[1])
out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
atlas = Image.open(atlas_path).convert('RGBA')
frames_root = out / 'frames'
all_frames, durations = [], []
states = {}
for row, (state, timing) in enumerate(ROW_DURATIONS.items()):
    state_dir = frames_root / state; state_dir.mkdir(parents=True, exist_ok=True)
    frames = []
    for col in range(len(timing)):
        frame = atlas.crop((col*192,row*208,(col+1)*192,(row+1)*208))
        frame.save(state_dir / f'{col:02d}.png'); frames.append(frame)
    states[state] = frames
    all_frames.extend(frames); durations.extend(timing)
subprocess.run([sys.executable, str(SCRIPTS/'render_animation_previews.py'), '--frames-root',str(frames_root),'--output-dir',str(out)], check=True)
save_preview(all_frames,durations,out/'all-states.gif')
transition = states['idle'] + states['jumping'] + states['idle']
save_preview(transition, ROW_DURATIONS['idle']+ROW_DURATIONS['jumping']+ROW_DURATIONS['idle'], out/'idle-jump-idle.gif')
looks = [atlas.crop((i%8*192,(9+i//8)*208,(i%8+1)*192,(10+i//8)*208)) for i in range(16)]
save_preview(looks,[160]*16,out/'look-loop.gif')
stills = Image.new('RGB',(4*192,244),'#f4f1e9'); d=ImageDraw.Draw(stills)
for i,(label,frame) in enumerate([('Idle',states['idle'][0]),('Wave',states['waving'][2]),('Jump peak',states['jumping'][2]),('Needs help',states['waiting'][2])]):
    stills.paste(frame,(i*192,30),frame); d.text((i*192+8,8),label,fill='#263d40')
stills.save(out/'four-state-stills.png')
encoder = imageio_ffmpeg.write_frames(str(out/'all-states.mp4'),(192,208),fps=30,codec='libx264',pix_fmt_in='rgb24',pix_fmt_out='yuv420p',macro_block_size=1)
encoder.send(None)
for frame,ms in zip(all_frames,durations):
    bg=Image.new('RGB',frame.size,'#f4f1e9'); bg.paste(frame,mask=frame.getchannel('A'))
    for _ in range(max(1,round(ms*30/1000))): encoder.send(bg.tobytes())
encoder.close()
print(json.dumps({'ok':True,'source':str(atlas_path),'output':str(out)}))
