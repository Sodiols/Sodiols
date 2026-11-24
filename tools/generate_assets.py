#!/usr/bin/env python3
"""Generate self-contained 3D-inspired animated GitHub README assets.
Requires Pillow, numpy, opencv-python; Inter fonts available for regeneration.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import cv2, math, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True, parents=True)
BOLD='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
MED='/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'
REG='/usr/share/fonts/opentype/inter/Inter-Regular.otf'
SEM='/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
MONO='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
BG=(10,15,27)
WHITE=(245,247,255)
MUTED=(151,161,187)
VIO=(159,139,255)
CYAN=(100,222,238)
ORANGE=(255,171,114)

def font(path,size): return ImageFont.truetype(path,size)
def mix(a,b,t): return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))
def rgba(color,a=255): return (*color,a)

def txt(draw, xy, s, size=24, color=WHITE, face=REG, anchor=None, spacing=0, **kw):
    if spacing:
        x,y=xy
        for char in s:
            draw.text((x,y),char,font=font(face,size),fill=color,anchor=anchor,**kw)
            x+=draw.textlength(char,font=font(face,size))+spacing
        return x
    draw.text(xy,s,font=font(face,size),fill=color,anchor=anchor,**kw)

def rr(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def gradient(w,h,primary=BG,glows=None):
    y,x=np.mgrid[0:h,0:w]
    arr=np.zeros((h,w,3), dtype=np.float32)
    for i,c in enumerate(primary): arr[:,:,i]=c + (y/h)*4
    for cx,cy,sx,sy,color,amt in (glows or []):
        g=np.exp(-(((x-cx)/sx)**2+((y-cy)/sy)**2)*1.6)*amt
        for k in range(3): arr[:,:,k] += g*color[k]
    return Image.fromarray(np.uint8(np.clip(arr,0,255)),'RGB').convert('RGBA')

def soft_glow(im, center, rad, col, alpha=160):
    w,h=im.size
    layer=Image.new('RGBA',(w,h))
    d=ImageDraw.Draw(layer)
    x,y=center
    d.ellipse((x-rad,y-rad,x+rad,y+rad), fill=rgba(col,alpha))
    blurred=layer.filter(ImageFilter.GaussianBlur(rad*.48))
    im.alpha_composite(blurred)

def chip(d, x,y,text_, fill, fg, outline=None, size=16,padx=18,h=42):
    f=font(SEM,size)
    bb=d.textbbox((0,0),text_,font=f)
    w=bb[2]+2*padx
    rr(d,(x,y,x+w,y+h),h//2,fill,outline,width=1)
    d.text((x+padx,y+(h-size)//2-2),text_,font=f,fill=fg)
    return w

def cube(d,cx,cy,s,angle=0,bright=VIO):
    # Isometric cube with shifting orientation. All faces have accurate shared edges.
    ox=math.cos(angle)*s*.28
    oy=math.sin(angle)*s*.1
    A=(cx,cy-s*.48)
    B=(cx+s*.49+ox,cy-s*.2+oy)
    C=(cx,cy+s*.1)
    D=(cx-s*.49+ox,cy-s*.2-oy)
    E=(cx+s*.49+ox,cy+s*.38+oy)
    F=(cx,cy+s*.66)
    G=(cx-s*.49+ox,cy+s*.38-oy)
    d.polygon([A,B,C,D],fill=(86,79,164),outline=(207,198,255))
    d.polygon([D,C,F,G],fill=(56,58,113),outline=(183,166,244))
    d.polygon([B,E,F,C],fill=(112,95,193),outline=(218,213,255))
    for poly in [[A,B,C,D],[D,C,F,G],[B,E,F,C]]:
        d.line(poly+[poly[0]],fill=rgba(bright,255),width=2)
    d.line([C,F],fill=(214,208,255),width=2)


def ring_3d(d,cx,cy,rx=52,ry=20,phase=0):
    # Tilted elliptical ring, highlight moves around the perimeter.
    for i in range(72):
        a0=i*math.tau/72
        a1=(i+1)*math.tau/72
        p0=(cx+math.cos(a0)*rx,cy+math.sin(a0)*ry+math.cos(a0+phase)*3)
        p1=(cx+math.cos(a1)*rx,cy+math.sin(a1)*ry+math.cos(a1+phase)*3)
        bright=(math.sin(a0-phase)+1)/2
        col=mix((56,86,139),CYAN,.2+bright*.8)
        d.line([p0,p1],fill=col,width=5 if bright>.8 else 3)
    d.ellipse((cx-8,cy-8,cx+8,cy+8),fill=(235,240,255))

def browser_panel():
    w,h=600,400
    im=Image.new('RGBA',(w,h))
    d=ImageDraw.Draw(im)
    rr(d,(2,2,w-3,h-3),21,(20,27,44,250),outline=(104,114,156,255),width=2)
    rr(d,(12,12,w-14,h-14),13,(17,23,38,255))
    d.line((12,55,w-14,55),fill=(66,74,105),width=2)
    for i,c in enumerate([(247,119,117),(251,201,110),(96,211,155)]):
        d.ellipse((31+i*20,30,41+i*20,40),fill=c)
    txt(d,(110,22),'studio / build / production',16,(174,185,210),MONO)
    rr(d,(23,68,185,h-20),11,(23,33,54))
    txt(d,(38,87),'EXPLORER',14,(125,137,165),SEM)
    for i,(lab,c) in enumerate([('app',VIO),('components',CYAN),('lib',(197,200,214)),('public',(197,200,214)),('package.json',ORANGE)]):
        y=124+i*44
        if i==1: rr(d,(32,y-6,178,y+28),6,(48,49,83))
        d.ellipse((41,y+7,49,y+15),fill=c)
        txt(d,(60,y+3),lab,15,(202,210,233),REG)
    txt(d,(222,83),'experience.tsx',17,WHITE,SEM)
    d.line((210,111,569,111),fill=(49,60,85),width=1)
    lines=[
        (('01   ',MUTED),('export',VIO),(' default ',WHITE),('function',CYAN)),
        (('02   ',MUTED),('  CreateExperience() {',WHITE)),
        (('03   ',MUTED),('  const ',VIO),('quality',CYAN),(' = {',WHITE)),
        (('04   ',MUTED),('    design: ',WHITE),('"intentional"',ORANGE)),
        (('05   ',MUTED),('    motion: ',WHITE),('"meaningful"',ORANGE)),
        (('06   ',MUTED),('    product: ',WHITE),('"functional"',ORANGE)),
        (('07   ',MUTED),('  };',WHITE)),
        (('08   ',MUTED),('  return ',VIO),('<SomethingGreat />',CYAN)),
        (('09   ',MUTED),('}',WHITE)),
    ]
    for ix, segs in enumerate(lines):
        x=218
        y=133+ix*26
        for seg,col in segs:
            txt(d,(x,y),seg,13,col,MONO)
            x+=d.textlength(seg,font=font(MONO,13))
    rr(d,(213,374,575,390),7,(33,43,63))
    txt(d,(227,376),'main*    TypeScript     UTF-8     UTF-8',11,(155,173,195),MONO)
    return im

BROWSER=browser_panel()

def perspective_overlay(base,src,dest):
    sw,sh=src.size
    srcpts=np.float32([[0,0],[sw,0],[sw,sh],[0,sh]])
    dstpts=np.float32(dest)
    m=cv2.getPerspectiveTransform(srcpts,dstpts)
    a=np.array(src.convert('RGBA'))
    warp=cv2.warpPerspective(a,m,(base.width,base.height),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0,0))
    base.alpha_composite(Image.fromarray(warp,'RGBA'))

def hero_frame(k,N=30):
    w,h=1200,474
    t=k/N*math.tau
    im=gradient(w,h,glows=[(1020,200,430,380,(43,48,94),.72),(725,380,460,200,(19,55,73),.42),(200,-100,350,220,(23,29,72),.2)])
    d=ImageDraw.Draw(im,'RGBA')
    # technical top/bottom rails
    d.line([(40,29),(1160,29)],fill=(114,130,175,45),width=1)
    d.line([(40,442),(1160,442)],fill=(114,130,175,55),width=1)
    for x in range(640,1230,42):
        d.line([(x,443),(x+190,475)],fill=(93,107,170,22),width=1)
    for y in [365,393,420,448]: d.line([(630,y),(1200,y)],fill=(93,107,170,22),width=1)
    # left dot + eyebrow
    d.ellipse((51,69,67,85),fill=rgba(CYAN,255))
    txt(d,(84,63),'BUILDING INTERFACES THAT MATTER',16,(149,226,225),SEM,spacing=1)
    txt(d,(48,122),'SODIOL',94,WHITE,BOLD)
    txt(d,(48,220),'SAYEM',94,WHITE,BOLD)
    # small accent bar, descriptor
    rr(d,(55,337,103,345),4,rgba(VIO))
    txt(d,(121,328),'FULL STACK DEVELOPER',21,(206,213,234),SEM,spacing=1)
    txt(d,(56,390),'DESIGN  /  CODE  /  SHIP',16,(148,160,190),MONO)
    txt(d,(1040,450),'SYLHET, BANGLADESH',12,(140,150,176),MONO)
    # soft shadows and far glow behind card
    soft_glow(im,(930+math.sin(t)*7,250),125,(72,65,161),78)
    floaty=math.sin(t)*7
    xshift=math.sin(t+.7)*9
    corners=[(645+xshift,83+floaty),(1087+xshift,50+floaty),(1121+xshift,377+floaty),(663+xshift,405+floaty)]
    shad=[(x+18,y+25) for x,y in corners]
    shadow=Image.new('RGBA',im.size)
    sd=ImageDraw.Draw(shadow)
    sd.polygon(shad,fill=(0,0,0,150))
    im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(22)))
    perspective_overlay(im,BROWSER,corners)
    d=ImageDraw.Draw(im)
    # independent orbiting shapes (in front of card)
    cdx=1060+int(math.cos(t)*20); cdy=354+int(math.sin(t)*11)
    ring_3d(d,cdx,cdy,47,15,t)
    soft_glow(im,(cdx,cdy),28,(43,179,228),70)
    d=ImageDraw.Draw(im)
    cube(d,1060+math.sin(t)*24,105+math.sin(t+.5)*15,49,t)
    # dotted curved trajectory
    for j in range(14):
        a=j/14*math.pi*.9+t*.08
        px=1152+30*math.cos(a);py=230+90*math.sin(a)
        d.ellipse((px-1.5,py-1.5,px+1.5,py+1.5),fill=rgba(VIO,110))
    # active minimal UI labels
    rr(d,(609,390,731,423),15,(36,47,74),outline=(90,105,159))
    d.ellipse((623,401,632,410),fill=CYAN)
    txt(d,(640,398),'LIVE BUILD',13,(212,221,243),SEM)
    return im.convert('RGB')

def make_gif(frames,path,duration=125,colors=128):
    # quantization with palette first reference for stable colors
    indexed=[f.quantize(colors=colors,method=Image.Quantize.FASTOCTREE,dither=Image.Dither.NONE) for f in frames]
    indexed[0].save(str(path),format='GIF',save_all=True,append_images=indexed[1:],duration=duration,loop=0,optimize=True,disposal=2)

print('Rendering hero GIF...')
hero=[hero_frame(i,30) for i in range(30)]
make_gif(hero,OUT/'hero-3d.gif',130,128)
hero[4].save(OUT/'hero-still.png',optimize=True)

# Animation: retro-futuristic terminal, cursor types code with single line changing
TERMW,TERMH=1140,245
lines=['> npm run create:experience', 'Building interfaces that feel as good as they work.', '✓ Responsive layouts     ✓ Product thinking     ✓ Real-world code']

def terminal_frame(step,N=34):
    im=gradient(TERMW,TERMH,(13,20,35),glows=[(850,210,500,250,(54,32,121),.38)])
    d=ImageDraw.Draw(im,'RGBA')
    rr(d,(2,2,TERMW-3,TERMH-3),22,(16,24,40,245),outline=(87,96,140,180),width=2)
    rr(d,(18,18,TERMW-18,56),13,(27,35,56))
    for i,c in enumerate([(252,118,116),(252,194,115),(98,215,171)]):d.ellipse((37+i*24,31,50+i*24,44),fill=c)
    txt(d,(135,27),'sayem@studio: ~/build',17,(173,185,213),MONO)
    # Static lines plus typewriter dynamic third line
    txt(d,(50,83),lines[0],23,CYAN,MONO)
    txt(d,(50,123),lines[1],20,(228,233,249),MONO)
    frame=step/N
    # line appears, holds, then resets, seamless pause
    count=int(max(0,min(1,(frame-.10)/.63))*len(lines[2]))
    typed=lines[2][:count]
    txt(d,(50,165),typed,18,(172,159,253),MONO)
    if (step//3)%2==0:
        tw=d.textlength(typed,font=font(MONO,18))
        rr(d,(51+tw,166,53+tw,187),1,(213,220,250))
    txt(d,(967,210),'OUTPUT 01 / 01',13,(128,143,172),MONO)
    return im.convert('RGB')
print('Rendering terminal GIF...')
terminal=[terminal_frame(i,34) for i in range(34)]
make_gif(terminal,OUT/'terminal.gif',150,100)

# Four wide, graphic project covers with a cohesive system + distinctive identity.
CARD_W,CARD_H=790,340

def base_card(index,accent,title,description,label):
    im=gradient(CARD_W,CARD_H,(14,20,34),glows=[(680,160,290,260,accent,.24)])
    d=ImageDraw.Draw(im,'RGBA')
    rr(d,(3,3,CARD_W-4,CARD_H-4),20,(15,22,37,200),outline=(98,109,146,95),width=2)
    d.line([(33,45),(758,45)],fill=(128,133,165,80),width=1)
    txt(d,(36,18),f'FEATURED / {index:02d}',13,(150,162,192),MONO,spacing=1)
    txt(d,(36,95),title,49,WHITE,BOLD)
    txt(d,(39,162),description,18,(171,186,209),REG)
    rr(d,(39,246,202,287),16,(32,40,57),outline=rgba(accent,190))
    txt(d,(58,257),label,15,accent,SEM)
    return im

def project_tara():
    im=base_card(1,(200,109,141),'TARA','Fashion commerce / Storefront','E-COMMERCE')
    d=ImageDraw.Draw(im,'RGBA')
    # Three pseudo-perspective shopping cards
    d.polygon([(479,82),(617,61),(629,295),(482,305)],fill=(86,45,62),outline=(181,113,140))
    d.polygon([(587,72),(725,91),(716,307),(576,292)],fill=(246,241,235),outline=(227,195,199))
    d.polygon([(528,94),(658,83),(664,304),(529,306)],fill=(231,215,216),outline=(240,220,220))
    # garment silhouette in foreground editorial fashion look
    d.ellipse((584,126,607,153),fill=(166,103,115))
    d.polygon([(583,156),(561,179),(576,206),(580,206),(581,245),(622,245),(619,206),(626,204),(639,179),(612,156)],fill=(122,48,73))
    d.polygon([(581,242),(622,242),(643,282),(557,282)],fill=(171,94,113))
    txt(d,(545,104),'T A R A',25,(112,47,67),BOLD)
    return im

def project_husna():
    im=base_card(2,(227,207,179),'Husnalogy','Invitations / Personalisation','CUSTOMIZER')
    d=ImageDraw.Draw(im,'RGBA')
    # layered wedding stationery cards, isolated as abstract graphic (not screenshot)
    d.polygon([(498,104),(660,80),(690,278),(522,303)],fill=(56,59,66),outline=(153,143,135))
    d.polygon([(536,93),(709,115),(677,309),(512,288)],fill=(244,236,228),outline=(226,207,196))
    d.polygon([(559,98),(739,93),(734,293),(551,296)],fill=(255,250,243),outline=(221,211,197))
    # details
    txt(d,(590,143),'THE',13,(104,98,87),REG)
    txt(d,(575,161),'WEDDING',18,(91,82,77),BOLD)
    d.line([(590,201),(708,201)],fill=(197,170,150),width=2)
    txt(d,(582,211),'an invitation',15,(151,128,116),MED)
    d.arc((615,226,669,275),50,305,fill=(164,143,122),width=2)
    return im

def project_portfolio():
    im=base_card(3,(156,146,255),'Portfolio','Selected work / Creative development','WEB EXPERIENCE')
    d=ImageDraw.Draw(im,'RGBA')
    # tilted browser collage
    d.polygon([(475,103),(703,86),(718,264),(496,292)],fill=(52,49,94),outline=(130,115,219))
    d.polygon([(501,74),(724,112),(700,304),(474,275)],fill=(36,43,71),outline=(155,149,253))
    txt(d,(508,137),'SODIOL',28,(239,239,255),BOLD)
    txt(d,(508,169),'SAYEM',28,(156,146,255),BOLD)
    d.line([(510,218),(666,236)],fill=(98,220,237),width=5)
    d.line([(510,235),(621,250)],fill=(139,133,208),width=3)
    cube(d,705,84,42,.55)
    return im

def project_chat():
    im=base_card(4,(90,210,232),'PriChat','Private servers / Room-based chat','CHAT PLATFORM')
    d=ImageDraw.Draw(im,'RGBA')
    rr(d,(495,75,740,295),22,(24,42,61),outline=(100,164,184),width=2)
    rr(d,(508,89,726,133),11,(32,59,81))
    d.ellipse((518,101,535,118),fill=CYAN)
    txt(d,(546,102),'private room',14,(225,233,250),SEM)
    rr(d,(516,154,653,184),11,(54,74,110))
    txt(d,(529,159),'Hey, welcome!',13,WHITE,REG)
    rr(d,(573,197,718,230),11,(46,119,135))
    txt(d,(591,203),'Thanks! :)',14,WHITE,REG)
    rr(d,(515,254,711,282),9,(42,53,75))
    txt(d,(529,260),'Message...',13,(137,159,185),REG)
    return im

for fn,func in [('project-tara.png',project_tara),('project-husnalogy.png',project_husna),('project-portfolio.png',project_portfolio),('project-prichat.png',project_chat)]:
    img=func();img.convert('RGB').save(OUT/fn,optimize=True)

# Matching accessible action badges as local static images (clickable from README).
def button_image(name,subtitle,col,filename):
    w,h=296,68
    im=Image.new('RGBA',(w,h),(0,0,0,0));d=ImageDraw.Draw(im,'RGBA')
    rr(d,(2,2,w-3,h-3),17,(24,31,51,255),outline=rgba(col,190),width=2)
    rr(d,(13,13,58,56),12,rgba(col,45),outline=rgba(col,100))
    # simple icon arrow in square
    d.line([(27,42),(45,25)],fill=col,width=3)
    d.line([(35,25),(45,25),(45,35)],fill=col,width=3)
    txt(d,(74,13),name,18,WHITE,SEM)
    txt(d,(75,38),subtitle,13,MUTED,REG)
    return im

for name,subtitle,color,filename in [
 ('VIEW PORTFOLIO','Explore selected work',VIO,'cta-portfolio.png'),
 ('GITHUB','Explore repositories',CYAN,'cta-github.png'),
 ('LET\'S CONNECT','Get in touch',ORANGE,'cta-email.png')]:
    button_image(name,subtitle,color,filename).save(OUT/filename,optimize=True)

# Compact divider in normal PNG to avoid SVG image animation restrictions.
D=Image.new('RGBA',(1140,50),(0,0,0,0));dd=ImageDraw.Draw(D)
dd.line([(0,25),(470,25)],fill=(83,98,139),width=2)
dd.line([(670,25),(1140,25)],fill=(83,98,139),width=2)
for i,c in enumerate([VIO,CYAN,ORANGE]):
    cx=560+i*24
    dd.polygon([(cx,18),(cx+7,25),(cx,32),(cx-7,25)],fill=c)
D.save(OUT/'divider.png',optimize=True)


# Custom tech board with editorial labels and genuinely useful technologies.
def toolkit_image():
    w,h=1140,424
    im=gradient(w,h,(13,20,34),glows=[(1000,200,350,300,(68,48,132),.29)])
    d=ImageDraw.Draw(im,'RGBA')
    rr(d,(3,3,w-4,h-4),22,(17,25,42,230),outline=(86,105,143,180),width=2)
    txt(d,(32,22),'TOOLKIT / 2026',14,(167,176,211),MONO,spacing=1)
    txt(d,(32,56),'Technologies I work with',33,WHITE,BOLD)
    d.line([(32,104),(1108,104)],fill=(82,92,129),width=1)
    groups=[
      ('LANGUAGES', ['JavaScript','TypeScript','HTML5','CSS3'],VIO),
      ('INTERFACE', ['React','Next.js','Tailwind CSS','Bootstrap'],CYAN),
      ('BACKEND & DATA', ['Node.js','Supabase','Firebase','PostgreSQL','REST APIs'],ORANGE),
      ('WORKFLOW', ['Git','GitHub','Authentication','Responsive UI'],(166,217,184)),
    ]
    for row,(lab,tags,accent) in enumerate(groups):
        y=121+row*73
        d.ellipse((33,y+18,44,y+29),fill=accent)
        txt(d,(58,y+13),lab,15,(175,186,215),SEM)
        x=296
        for tag in tags:
            f=font(SEM,16)
            tw=d.textlength(tag,font=f)
            width=int(tw+33)
            rr(d,(x,y+4,x+width,y+46),12,(31,42,62),outline=(61,79,110))
            txt(d,(x+16,y+16),tag,16,(230,235,248),SEM)
            x+=width+10
        if row<3:d.line([(33,y+65),(1107,y+65)],fill=(54,65,89),width=1)
    return im.convert('RGB')
toolkit_image().save(OUT/'toolkit.png',optimize=True)

print('Assets created:')
for path in OUT.iterdir(): print(path.name,round(path.stat().st_size/1024),'KB')
