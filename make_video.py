#!/usr/bin/env python3
"""Vertical 1080x1920 bilingual-sub short, same design as jensen-doom/04_video_6s.mp4.
--subs "t_end|中文|English" repeated (t_end in OUTPUT seconds; last sub runs to end).
Speed = (end-start)/duration if --fit, else 1 (original audio pitch kept via atempo)."""
import argparse, os, subprocess as sp, tempfile
from PIL import Image, ImageDraw
from render_card import F,B,R,ctext,ACCENT,BG,YEL
p=argparse.ArgumentParser()
p.add_argument('--video',required=True); p.add_argument('--start',type=float,required=True); p.add_argument('--end',type=float,required=True)
p.add_argument('--title',required=True); p.add_argument('--title_en',required=True)
p.add_argument('--subs',action='append',required=True); p.add_argument('--duration',type=float,default=6)
p.add_argument('--fit',action='store_true',help='atempo so start..end fills --duration'); p.add_argument('--out',required=True)
p.add_argument('--crop',help='ffmpeg crop w:h:x:y applied before scale (drop burned-in subs)')
a=p.parse_args(); td=tempfile.mkdtemp()
im=Image.new('RGBA',(1080,1920),BG+(255,)); d=ImageDraw.Draw(im)
d.rectangle([0,0,1080,10],fill=ACCENT)
y=ctext(d,260,a.title,F(B,70),'white'); ctext(d,y+10,a.title_en,F(R,38),(200,200,200)); im.save(td+'/tpl.png')
subs=[s.split('|') for s in a.subs]
for i,(_,zh,en) in enumerate(subs):
    s=Image.new('RGBA',(1080,400),(0,0,0,0)); d=ImageDraw.Draw(s)
    y=ctext(d,20,zh.replace('\\n','\n'),F(B,66),YEL); ctext(d,y+10,en.replace('\\n','\n'),F(R,44),'white'); s.save(f'{td}/s{i}.png')
S=(a.end-a.start)/a.duration if a.fit else 1.0
assert 0.5<=S<=2, 'atempo out of range'
cr=f"crop={a.crop}," if a.crop else ""
fc=f"[0:v]setpts=(PTS-STARTPTS)/{S},{cr}scale=1080:608,fps=30[v];[1:v][v]overlay=0:656[b0]"; prev=0
for i,(te,_,_) in enumerate(subs):
    te=float(te) if i<len(subs)-1 else 1e9
    fc+=f";[b{i}][{i+2}:v]overlay=0:1310:enable='between(t,{prev},{min(te,9999)})'[b{i+1}]"; prev=te
fc+=f";[b{len(subs)}]format=yuv420p[o];[0:a]asetpts=PTS-STARTPTS,atempo={S}[au]"
cmd=['ffmpeg','-v','error','-y','-ss',str(a.start),'-t',str(a.end-a.start),'-i',a.video,'-i',td+'/tpl.png']
for i in range(len(subs)): cmd+=['-i',f'{td}/s{i}.png']
cmd+=['-filter_complex',fc,'-map','[o]','-map','[au]','-t',str(a.duration),'-c:v','libx264','-crf','18','-c:a','aac','-b:a','192k','-movflags','+faststart',a.out]
sp.run(cmd,check=True); print(a.out,'speed',round(S,4))
