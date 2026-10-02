"""Imágenes para compartir enlaces (Open Graph, 1200×630) e iconos de la web."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT=Path(__file__).resolve().parent
F=ROOT/'fonts'
W,H=1200,630
RED=(227,34,42);RED2=(255,65,72);INK=(11,11,14);TXT=(244,241,236);WA=(37,211,102)

def font(name,size):return ImageFont.truetype(str(F/name),size)
def cover(img,w,h):
 r=max(w/img.width,h/img.height);img=img.resize((round(img.width*r),round(img.height*r)),Image.LANCZOS)
 x=(img.width-w)//2;y=(img.height-h)//2;return img.crop((x,y,x+w,y+h))
def shade(base):
 g=Image.new('L',(W,1))
 for x in range(W):g.putpixel((x,0),int(max(0,min(255,250-(x/W)*330))))
 g=g.resize((W,H));dark=Image.new('RGB',(W,H),(6,6,9))
 out=Image.composite(dark,base,g)
 v=Image.new('L',(1,H))
 for y in range(H):v.putpixel((0,y),int(max(0,(y/H-.55)/.45)*200))
 return Image.composite(dark,out,v.resize((W,H)))
def fit(draw,text,name,size,maxw):
 while size>20:
  f=font(name,size)
  if draw.textlength(text,font=f)<=maxw:return f
  size-=4
 return font(name,size)
def card(photo,lines,serif,kicker,logo,dest):
 photo=cover(Image.open(photo).convert('RGB'),W,H)
 if len(lines)==1:photo=Image.blend(photo,Image.new('RGB',(W,H),(6,6,9)),.42)
 base=shade(photo)
 # Sombra suave bajo el bloque de texto
 glow=Image.new('L',(W,H),0);ImageDraw.Draw(glow).rounded_rectangle((20,190,1120,480),radius=80,fill=150)
 base=Image.composite(Image.new('RGB',(W,H),(6,6,9)),base,glow.filter(ImageFilter.GaussianBlur(70)))
 d=ImageDraw.Draw(base)
 d.rectangle((0,0,W,6),fill=RED)
 lg=Image.open(logo).convert('RGBA');lw=300;lg=lg.resize((lw,round(lg.height*lw/lg.width)),Image.LANCZOS)
 base.paste(lg,(64,56),lg)
 kf=font('font-6.ttf',20)
 d.ellipse((64,214,76,226),fill=WA)
 d.text((88,208),kicker.upper(),font=kf,fill=(220,216,210))
 y=252
 if len(lines)>1:
  # Titular de portada: la palabra en cursiva acompaña a la última línea
  f=font('font-2.ttf',112)
  for i,ln in enumerate(lines):
   d.text((60,y),ln.upper(),font=f,fill=TXT)
   if i==len(lines)-1:
    sf=font('instrument-serif-italic.ttf',118)
    d.text((60+d.textlength(ln.upper()+' ',font=f),y-22),serif,font=sf,fill=RED2)
   y+=f.size*.9
 else:
  f=fit(d,lines[0].upper(),'font-2.ttf',132,1060)
  d.text((60,y),lines[0].upper(),font=f,fill=TXT)
  y+=f.size*.92+6
  sf=fit(d,serif,'instrument-serif-italic.ttf',58,1000)
  d.text((62,y),serif,font=sf,fill=RED2)
 pf=font('font-6.ttf',22);label='Presupuesto por WhatsApp'
 tw=d.textlength(label,font=pf);px,py=64,H-100
 d.rounded_rectangle((px,py,px+tw+56,py+54),radius=27,fill=WA)
 d.text((px+28,py+13),label,font=pf,fill=(4,33,15))
 d.text((px+tw+84,py+14),'Los Garres, Murcia',font=font('font-5.ttf',21),fill=(200,196,190))
 base.save(dest,'JPEG',quality=88,optimize=True,progressive=True)

def icons(out):
 for size,name in ((180,'apple-touch-icon.png'),(512,'icon-512.png'),(192,'icon-192.png'),(32,'favicon-32.png')):
  im=Image.new('RGB',(size*4,size*4),INK);d=ImageDraw.Draw(im)
  f=font('font-2.ttf',int(size*4*.78))
  bb=d.textbbox((0,0),'R',font=f);d.text(((size*4-(bb[2]-bb[0]))/2-bb[0],(size*4-(bb[3]-bb[1]))/2-bb[1]),'R',font=f,fill=RED)
  d.rectangle((0,size*4-size*4//14,size*4,size*4),fill=RED)
  im.resize((size,size),Image.LANCZOS).save(out/name)
