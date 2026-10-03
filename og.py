"""Imágenes para compartir enlaces (Open Graph, 1200×630) e iconos de la web.

Composición centrada: WhatsApp muchas veces enseña solo un recorte cuadrado del
centro (630×630), así que logo, titular y botón viven en esa zona segura.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT=Path(__file__).resolve().parent
F=ROOT/'fonts'
W,H=1200,630
SAFE=560  # ancho útil dentro del recorte cuadrado central
RED=(227,34,42);RED2=(255,65,72);INK=(11,11,14);TXT=(244,241,236);WA=(37,211,102)

def font(name,size):return ImageFont.truetype(str(F/name),size)
def cover(img,w,h):
 r=max(w/img.width,h/img.height);img=img.resize((round(img.width*r),round(img.height*r)),Image.LANCZOS)
 x=(img.width-w)//2;y=(img.height-h)//2;return img.crop((x,y,x+w,y+h))
def fit(draw,text,name,size,maxw):
 while size>20:
  f=font(name,size)
  if draw.textlength(text,font=f)<=maxw:return f
  size-=2
 return font(name,size)
def centered(d,y,text,f,fill):
 w=d.textlength(text,font=f);d.text(((W-w)/2,y),text,font=f,fill=fill);return w

def backdrop(photo):
 # Foto oscurecida, con un halo más oscuro en el centro para que el texto respire
 img=cover(Image.open(photo).convert('RGB'),W,H)
 img=Image.blend(img,Image.new('RGB',(W,H),(6,6,9)),.5)
 halo=Image.new('L',(W,H),0);ImageDraw.Draw(halo).ellipse((W/2-430,-40,W/2+430,H+40),fill=190)
 img=Image.composite(Image.new('RGB',(W,H),(6,6,9)),img,halo.filter(ImageFilter.GaussianBlur(90)))
 # Trama de puntos roja muy sutil en las esquinas, como en la web
 dots=Image.new('RGBA',(W,H),(0,0,0,0));dd=ImageDraw.Draw(dots)
 for y in range(0,H,12):
  for x in range(0,W,12):
   k=max(0,1-min(((x-0)**2+(y-H)**2)**.5,((x-W)**2+(y-0)**2)**.5)/420)
   if k>0:dd.ellipse((x-1.4,y-1.4,x+1.4,y+1.4),fill=(227,34,42,int(150*k)))
 img=img.convert('RGBA');img.alpha_composite(dots);return img.convert('RGB')

def card(photo,lines,serif,kicker,logo,dest):
 base=backdrop(photo);d=ImageDraw.Draw(base)
 d.rectangle((0,0,W,7),fill=RED);d.rectangle((0,H-7,W,H),fill=RED)
 lg=Image.open(logo).convert('RGBA');lw=380;lg=lg.resize((lw,round(lg.height*lw/lg.width)),Image.LANCZOS)
 base.paste(lg,((W-lw)//2,52),lg)
 # Rótulo pequeño con guiones a los lados
 kf=font('font-6.ttf',19);kt=kicker.upper()
 kw=d.textlength(kt,font=kf);ky=150
 d.text(((W-kw)/2,ky),kt,font=kf,fill=(214,210,204))
 d.line(((W-kw)/2-50,ky+11,(W-kw)/2-16,ky+11),fill=RED,width=2);d.line(((W+kw)/2+16,ky+11,(W+kw)/2+50,ky+11),fill=RED,width=2)
 y=188
 if len(lines)>1:
  # Titular de portada: «TU CASA, / A OTRO nivel.»
  a=lines[1].upper()+' ';size=124
  while True:
   f=font('font-2.ttf',size);sf=font('instrument-serif-italic.ttf',int(size*1.08))
   wa=d.textlength(a,font=f);wb=d.textlength(serif,font=sf)
   if wa+wb<=SAFE-40 and d.textlength(lines[0].upper(),font=f)<=SAFE-40:break
   size-=2
  y+=(124-size)*.5
  centered(d,y,lines[0].upper(),f,TXT);y+=f.size*.9
  x=(W-wa-wb)/2;d.text((x,y),a,font=f,fill=TXT);d.text((x+wa,y-int(f.size*.2)),serif,font=sf,fill=RED2)
  y+=f.size*1.02
 else:
  f=fit(d,lines[0].upper(),'font-2.ttf',120,SAFE)
  y=214+(120-f.size)*.7
  centered(d,y,lines[0].upper(),f,TXT);y+=f.size*.95+6
  sf=fit(d,serif,'instrument-serif-italic.ttf',50,SAFE-20)
  centered(d,y,serif,sf,RED2);y+=sf.size*1.25
 # Botón de WhatsApp centrado
 pf=font('font-6.ttf',23);label='Presupuesto por WhatsApp'
 tw=d.textlength(label,font=pf);bw=tw+64;py=H-128;px=(W-bw)/2
 d.rounded_rectangle((px,py,px+bw,py+56),radius=28,fill=WA)
 d.text((px+32,py+13),label,font=pf,fill=(4,33,15))
 cf=font('font-5.ttf',19);centered(d,H-56,'Los Garres · Murcia',cf,(190,186,180))
 base.save(dest,'JPEG',quality=88,optimize=True,progressive=True)

def icons(out):
 for size,name in ((180,'apple-touch-icon.png'),(512,'icon-512.png'),(192,'icon-192.png'),(32,'favicon-32.png')):
  im=Image.new('RGB',(size*4,size*4),INK);d=ImageDraw.Draw(im)
  f=font('font-2.ttf',int(size*4*.78))
  bb=d.textbbox((0,0),'R',font=f);d.text(((size*4-(bb[2]-bb[0]))/2-bb[0],(size*4-(bb[3]-bb[1]))/2-bb[1]),'R',font=f,fill=RED)
  d.rectangle((0,size*4-size*4//14,size*4,size*4),fill=RED)
  im.resize((size,size),Image.LANCZOS).save(out/name)
