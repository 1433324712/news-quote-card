#!/usr/bin/env python3
"""Download a video (direct URL or X/other via yt-dlp), transcribe with word timestamps, extract frames.
Outputs in --outdir: video.mp4, audio.raw, transcript.txt (segments), words.txt (word timings), frames/f_<sec>.png, contact.jpg"""
import argparse, os, subprocess as sp, numpy as np
p=argparse.ArgumentParser()
p.add_argument('--url'); p.add_argument('--video', help='local file instead of url')
p.add_argument('--outdir', required=True); p.add_argument('--lang', default='en')
p.add_argument('--model', default='small'); p.add_argument('--frames', default='', help='comma secs, default every 10s')
a=p.parse_args(); os.makedirs(a.outdir+'/frames', exist_ok=True); V=a.outdir+'/video.mp4'
if a.video: V=a.video
elif a.url.split('?')[0].endswith('.mp4'): sp.run(['curl','-sL','-o',V,a.url],check=True)
else: sp.run(['yt-dlp','-f','mp4/best','-o',V,a.url],check=True)  # pip install --break-system-packages yt-dlp
sp.run(['ffmpeg','-v','error','-y','-i',V,'-ac','1','-ar','16000','-f','f32le',a.outdir+'/audio.raw'],check=True)
dur=float(sp.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',V]))
from faster_whisper import WhisperModel   # pip install --break-system-packages faster-whisper
audio=np.fromfile(a.outdir+'/audio.raw',dtype=np.float32)  # numpy input avoids PyAV metadata_errors bug
segs,_=WhisperModel(a.model,compute_type='int8').transcribe(audio,language=a.lang,word_timestamps=True)
with open(a.outdir+'/transcript.txt','w') as T, open(a.outdir+'/words.txt','w') as Wd:
    for s in segs:
        T.write(f'{s.start:.1f}-{s.end:.1f} {s.text.strip()}\n')
        for w in s.words: Wd.write(f'{w.start:.2f}-{w.end:.2f} {w.word.strip()}\n')
ts=[float(x) for x in a.frames.split(',')] if a.frames else [t for t in range(2,int(dur),10)]
for t in ts: sp.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',V,'-frames:v','1',f'{a.outdir}/frames/f_{t:g}.png'],check=True)
sp.run(f"ffmpeg -v error -y -pattern_type glob -i '{a.outdir}/frames/*.png' -vf scale=320:-1,tile=4x{(len(ts)+3)//4} -frames:v 1 {a.outdir}/contact.jpg",shell=True)
print(open(a.outdir+'/transcript.txt').read()); print('duration',dur)
