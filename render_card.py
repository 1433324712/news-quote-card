#!/usr/bin/env python3
"""Bilingual (ZH+EN) vertical quote card, 1080xH. Same design as jensen-doom 01-03."""
import argparse
from PIL import Image, ImageDraw, ImageFont
B='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'; R='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
ACCENT=(118,185,0); BG=(10,10,12); YEL=(255,214,0)
def F(p,s): return ImageFont.truetype(p,s,index=2)  # index 2 = SC
def ctext(d,y,t,f,fill,W=1080):
    for line in t.split('\n'):
        w=d.textlength(line,font=f); d.text(((W-w)/2,y),line,font=f,fill=fill); y+=int(f.size*1.3)
    return y
def card(frame,tag,top,top_en,bot,bot_en,H=1440,fy=None,crop=None):
    im=Image.new('RGB',(1080,H),BG); d=ImageDraw.Draw(im)
    fr=Image.open(frame).convert('RGB')
    if crop: w,h,x,y=map(int,crop.split(':')); fr=fr.crop((x,y,x+w,y+h))
    fr=fr.resize((1080,608))
    fy=fy if fy is not None else (H-608)//2
    d.rectangle([0,0,1080,8],fill=ACCENT)
    y=ctext(d,70,tag,F(B,34),ACCENT)
    y=ctext(d,y+20,top,F(B,78),'white'); ctext(d,y+5,top_en,F(R,38),(200,200,200))
    im.paste(fr,(0,fy))
    y=fy+608+50
    y=ctext(d,y,bot,F(B,52),YEL); ctext(d,y+10,bot_en,F(R,36),(220,220,220))
    return im
if __name__=='__main__':
    p=argparse.ArgumentParser(description='Use \\n in text args for line breaks.')
    for a in ['frame','tag','headline','headline_en','quote','quote_en','out']: p.add_argument('--'+a,required=True)
    p.add_argument('--crop',help='w:h:x:y crop of source frame before scaling (e.g. drop burned-in subs)'); p.add_argument('--height',type=int,default=1440); p.add_argument('--frame-y',type=int)
    a=p.parse_args(); u=lambda s:s.replace('\\n','\n')
    card(a.frame,u(a.tag),u(a.headline),u(a.headline_en),u(a.quote),u(a.quote_en),a.height,a.frame_y,a.crop).save(a.out)
    print(a.out)
