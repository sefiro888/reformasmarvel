from pathlib import Path
import json, html, shutil
from PIL import Image

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'dist'
ASSETS=OUT/'assets'
ASSETS.mkdir(parents=True,exist_ok=True)
(OUT/'servicios').mkdir(exist_ok=True)
C=json.loads((ROOT/'contact-config.json').read_text(encoding='utf-8'))
WA_NUMBER=C['whatsapp_e164'].lstrip('+')
esc=html.escape

# slug, nombre, lema, foto, detalle, descripción, tareas, cómo preparar, opciones de la petición por WhatsApp
SERVICES=[
 ('albanileria','Albañilería','La base de una buena reforma.','Albañil trabajando en una reforma interior-13.png','Colocación precisa de ladrillos interiores-1.png','Distribuir, reparar y preparar los espacios es el primer paso para dar forma a una reforma. La albañilería conecta la estructura del trabajo con los acabados que se ven cada día.','Tabiques y distribución interior|Reparación y preparación de paredes|Trabajos de albañilería en reformas','Cuéntanos qué espacio quieres cambiar y qué uso tendrá. Las medidas, el estado de las paredes y las instalaciones existentes ayudan a definir el alcance.','Levantar o quitar tabiques|Abrir o cerrar huecos|Reparar paredes|Reforma de una estancia|Reforma integral'),
 ('electricidad','Electricidad','Instalaciones pensadas para tu día a día.','Instalación eléctrica moderna en vivienda renovada-12.png','Caja empotrada y cableado ordenado-3.png','Una reforma también es una oportunidad para revisar cómo se utiliza la electricidad: dónde hacen falta enchufes, cómo iluminar los espacios y qué instalaciones conviene adaptar.','Revisión de necesidades eléctricas|Puntos de luz, mecanismos y enchufes|Adaptación de instalaciones en reformas','Indica qué estancias vas a reformar, qué equipos utilizas y si has detectado algún problema. El alcance se concreta tras valorar la instalación.','Puntos de luz|Enchufes y mecanismos|Cuadro eléctrico|Instalación para una reforma|Revisar un problema'),
 ('fontaneria','Fontanería','Lo que no se ve también cuenta.','Fontanero revisando un baño moderno-11.png','Instalación impecable bajo el fregadero-5.png','En cocinas y baños, una instalación bien planteada importa tanto como el acabado. Coordinamos las necesidades de fontanería con la distribución y el resto de trabajos de la reforma.','Instalaciones en baños y cocinas|Adaptación de tomas y desagües|Reparaciones de fontanería','Explica si se trata de una reparación o de cambiar la distribución. Las fotografías del espacio y la ubicación de las tomas sirven como punto de partida.','Baño|Cocina|Mover tomas o desagües|Cambiar sanitarios|Reparación'),
 ('alicatado','Alicatado','El detalle que define el espacio.','Azulejos perfectos en un baño moderno-15.png','Instalación precisa de azulejos cerámicos-7.png','El revestimiento cambia la lectura de una cocina o un baño. La preparación del soporte, el formato elegido y la distribución de las piezas forman parte del trabajo de alicatado.','Revestimientos de baños y cocinas|Preparación de superficies|Colocación de piezas cerámicas','Comparte las medidas aproximadas y el tipo de pieza que te gusta. Si aún no has elegido el material, podemos valorar el trabajo a partir del espacio.','Baño|Cocina|Terraza o exterior|Cambiar el azulejo actual|Aún no he elegido pieza'),
 ('carpinteria','Carpintería','Madera, ajuste y carácter.','Carpintero instala puerta de madera-16.png','Ajuste preciso de armario en madera clara-9.png','Puertas y elementos de carpintería influyen en cómo se recorre y se aprovecha un espacio. Valoramos su instalación o adaptación como parte de la reforma.','Instalación de puertas interiores|Ajustes de elementos de carpintería|Carpintería vinculada a la reforma','Cuéntanos qué elementos necesitas cambiar, sus medidas aproximadas y el acabado que buscas. El material y los herrajes se concretan en el presupuesto.','Puertas interiores|Armarios|Ajustes y reparaciones|Rodapiés y remates'),
 ('pintura','Pintura','Una nueva luz para cada estancia.','Pintor profesional en salón luminoso-17.png','Acabado perfecto junto a la ventana-4.png','El color y el acabado tienen un efecto directo en la sensación de una habitación. Antes de pintar, conviene valorar el estado de la superficie y la preparación que necesita.','Pintura de paredes y techos|Preparación previa de superficies|Acabados de pintura en reformas','Indica las estancias, las medidas aproximadas y el estado de las paredes. Si hay humedades o grietas, conviene conocer su origen antes de definir el acabado.','Una estancia|Toda la vivienda|Techos|Hay humedades o grietas|Local o negocio'),
 ('enyesado','Enyesado','Superficies que hacen la diferencia.','Aplicación profesional de yeso en interior-14.png','Pared recién alisada junto a ventana-2.png','Una pared regular es el punto de partida de muchos acabados. El enyesado permite preparar y reparar superficies interiores, coordinando su ejecución con la pintura y otros trabajos.','Aplicación de yeso en interiores|Reparación de superficies|Preparación para acabados posteriores','Explica el estado del soporte y el acabado que buscas. Las fotografías ayudan a identificar las zonas que requieren una valoración más detallada.','Paredes|Techos|Reparar desperfectos|Dejar listo para pintar'),
 ('desescombro','Desescombro','Espacio despejado para seguir avanzando.','Retirada profesional de escombros-18.png','Retiro ordenado de escombros-6.png','La retirada de escombros forma parte de la organización de una reforma. El volumen, los accesos y el espacio disponible condicionan cómo se plantea el trabajo.','Retirada de escombros de reforma|Organización de la zona de trabajo|Despeje de espacios durante la obra','Comparte el volumen aproximado de material, la planta y los accesos. La gestión de los residuos y las condiciones del trabajo deben concretarse en el presupuesto.','Escombro de una obra|Vaciar una estancia|Durante una reforma|Planta baja|Piso con escaleras'),
 ('reparacion-fachadas','Reparación de fachadas','Cuidar el exterior empieza por el soporte.','Renovación profesional de fachada residencial-20.png','Reparación profesional de grieta en fachada-8.png','Una fachada requiere valorar tanto su acabado como el estado de sus superficies. La revisión del soporte ayuda a definir los trabajos de reparación y los medios necesarios.','Reparación de superficies exteriores|Tratamiento de zonas deterioradas|Acabados asociados a la reparación','Envía imágenes de las zonas afectadas y explica dónde se encuentran. Las causas del deterioro, los accesos y los permisos necesarios se valoran antes de concretar la intervención.','Grietas|Desconchados|Pintura exterior|Vivienda unifamiliar|Comunidad de vecinos'),
 ('tarima-flotante','Tarima flotante','Un suelo que une toda la estancia.','Colocación de tarima en salón luminoso-19.png','Pared recién alisada junto a ventana-2.png','El suelo marca el tono de una habitación. Para instalar tarima flotante conviene revisar el soporte y coordinar encuentros, puertas y remates con el resto de la reforma.','Instalación de tarima flotante|Valoración del soporte existente|Remates y encuentros del suelo','Indica la superficie aproximada, el suelo actual y el material que tienes previsto. El presupuesto debe recoger la preparación y los remates necesarios.','Salón|Dormitorios|Toda la vivienda|Sobre el suelo actual|Ya tengo el material'),
 ('impermeabilizaciones','Impermeabilizaciones','Proteger el espacio desde su origen.','Instalación de lámina impermeabilizante-10.png','Reparación profesional de grieta en fachada-8.png','Cuando aparece agua o humedad, el primer paso es entender su origen. La impermeabilización se plantea según el soporte, la zona afectada y las condiciones de uso.','Valoración de zonas con filtraciones|Preparación del soporte|Trabajos de impermeabilización','Explica cuándo aparece la humedad y qué zona afecta. Las fotografías orientan la primera conversación; la solución requiere valorar la causa y el estado del soporte.','Terraza|Cubierta|Humedad en paredes|Filtraciones|Baño o ducha'),
]
BY_SLUG={s[0]:s for s in SERVICES}
POWERS={'albanileria':'Levantar, abrir y dar forma a los espacios.','electricidad':'Llevar la luz y la energía justo donde hacen falta.','fontaneria':'Que el agua vaya siempre por donde debe.','alicatado':'Alinear cada pieza al milímetro.','carpinteria':'Ajustar la madera hasta que encaje.','pintura':'Cambiar la luz y el ánimo de una estancia.','enyesado':'Dejar las paredes listas para lucir.','desescombro':'Despejar la obra para que todo avance.','reparacion-fachadas':'Devolverle la cara a tu fachada.','tarima-flotante':'Renovar el suelo que pisas cada día.','impermeabilizaciones':'Plantar cara a humedades y filtraciones.'}
VILLAINS=[('La Humedad','Aparece en paredes y techos, mancha, huele y siempre vuelve. Para vencerla hay que encontrar su origen.','impermeabilizaciones','¡PLAF!'),('La Grieta','Empieza fina y va ganando terreno en fachadas y paredes. Conviene revisar el soporte antes de tapar.','reparacion-fachadas','¡CRAC!'),('El Apagón','Enchufes que no llegan, luces que fallan y regletas por todas partes. Una instalación que se quedó pequeña.','electricidad','¡ZZZT!'),('La Gotera','Un goteo bajo el fregadero que nadie ve… hasta que se ve. Tomas y desagües que piden revisión.','fontaneria','¡PLIC!'),('El Azulejo Rebelde','Suelto, roto o pasado de moda. Un baño o una cocina entera pendientes de él.','alicatado','¡CLONC!'),('El Escombro','Se acumula durante la obra y no deja avanzar. Volumen, accesos y retirada, bien organizados.','desescombro','¡BRRUM!')]
BURST='<svg class="burst" viewBox="0 0 200 200" aria-hidden="true"><path d="M100 4l14 40 36-24-8 42 44-4-32 30 40 22-44 8 22 38-40-18-6 44-26-36-26 36-6-44-40 18 22-38-44-8 40-22-32-30 44 4-8-42 36 24z"/></svg>'
def first_sentence(t):
 return t.split('. ')[0].rstrip('.')+'.'


ICONS={
 'albanileria':'<path d="M3 5h18v14H3zM3 9.7h18M3 14.3h18M8 5v4.7M16 5v4.7M12 9.7v4.6M5 9.7v4.6M19 9.7v4.6M8 14.3V19M16 14.3V19"/>',
 'electricidad':'<path d="M13 2 4.5 13.5H11L10 22l8.5-11.5H12z"/>',
 'fontaneria':'<path d="M12 3s6 6.4 6 11a6 6 0 0 1-12 0c0-4.6 6-11 6-11z"/><path d="M9.5 15a2.5 2.5 0 0 0 2.5 2.5"/>',
 'alicatado':'<path d="M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z"/>',
 'carpinteria':'<path d="M6 21V3h12v18M3.5 21h17M14.5 12h1"/>',
 'pintura':'<path d="M4 4h13v5H4zM17 6.5h3v5.5h-8v2.5"/><path d="M11 14.5h2V21h-2z"/>',
 'enyesado':'<path d="M3 17h13l5-9H8z"/><path d="M9 17v1.5A2.5 2.5 0 0 1 6.5 21H5"/>',
 'desescombro':'<path d="M2 6h11v10H2zM13 9.5h4.5L21 13v3h-8"/><circle cx="6" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
 'reparacion-fachadas':'<path d="M4 21V6l8-3 8 3v15M2.5 21h19M8.5 9h2M13.5 9h2M8.5 13h2M13.5 13h2M10 21v-4h4v4"/>',
 'tarima-flotante':'<path d="M3 4h18v16H3zM3 9.3h18M3 14.7h18M10 4v5.3M16 9.3v5.4M7 14.7V20"/>',
 'impermeabilizaciones':'<path d="M12 3a9 9 0 0 1 9 9H3a9 9 0 0 1 9-9zM12 12v6.5a2 2 0 0 0 4 0"/>',
}
def icon(slug,cls='ico'):
 return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ICONS[slug]}</svg>'
WA_ICON='<svg class="wa-ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a9.9 9.9 0 0 0-8.53 15L2 22l5.15-1.4A10 10 0 1 0 12 2Zm0 18a8 8 0 0 1-4.1-1.12l-.3-.18-3 .82.82-2.9-.2-.31A8 8 0 1 1 12 20Zm4.5-5.8c-.25-.12-1.48-.73-1.71-.81-.23-.08-.4-.12-.57.12-.17.25-.65.81-.8.98-.15.17-.3.19-.55.06-.25-.12-1.06-.39-2.02-1.25-.75-.67-1.25-1.5-1.4-1.75-.15-.25-.02-.39.11-.52.11-.11.25-.3.37-.44.12-.14.17-.25.25-.42.08-.17.04-.32-.02-.45-.06-.12-.57-1.37-.78-1.87-.21-.49-.42-.42-.57-.43h-.49c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1s.9 2.44 1.03 2.6c.12.17 1.77 2.7 4.28 3.78.6.26 1.07.42 1.44.53.61.19 1.16.16 1.6.1.49-.07 1.48-.61 1.69-1.2.21-.59.21-1.09.15-1.2-.07-.1-.23-.16-.48-.29Z"/></svg>'
ARROW='<svg class="arrow" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
PHONE='<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2"/></svg>'
INSTA='<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".6" fill="currentColor"/></svg>'

def wa_text(topic=''):
 if topic:
  return f'Hola, Reformarvel. Me gustaría pedir presupuesto de {topic}. ¿Podemos hablar?'
 return 'Hola, Reformarvel. He visto vuestra web y me gustaría pedir presupuesto para una reforma. ¿Podemos hablar?'
def wa(topic=''):
 from urllib.parse import quote
 return f'https://wa.me/{WA_NUMBER}?text={quote(wa_text(topic))}'

# ---------- Recursos ----------
def optimize(source,name):
 src=ROOT/source
 if not src.exists():src=ROOT.parent.parent.parent/source
 if not src.exists():
  if not (ASSETS/f'{name}-1400.webp').exists():raise FileNotFoundError(source)
  previous=json.loads((ROOT/'asset-catalog.json').read_text(encoding='utf-8'))
  return next(item for item in previous if item['name']==name)
 im=Image.open(src).convert('RGB')
 for width in (640,1400,2000):
  v=im.copy();v.thumbnail((width,1800));v.save(ASSETS/f'{name}-{width}.webp','WEBP',quality=84)
 return {'source':source,'name':name,'width':im.width,'height':im.height,'provenance':'illustrative'}

catalog=[]
for s in SERVICES:
 catalog.append(optimize(s[3],s[0]));catalog.append(optimize(s[4],s[0]+'-detail'))
(ROOT/'asset-catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy(ROOT/'brand'/'logo-transparent.webp',ASSETS/'logo.webp')
shutil.copy(ROOT/'vendor'/'lenis.min.js',ASSETS/'lenis.min.js')
shutil.copy(ROOT/'app.js',ASSETS/'app.js')
shutil.copytree(ROOT/'fonts',ASSETS/'fonts',dirs_exist_ok=True)
(ASSETS/'styles.css').write_text((ROOT/'font-faces.css').read_text(encoding='utf-8')+'\n'+(ROOT/'styles.css').read_text(encoding='utf-8'),encoding='utf-8')
(ASSETS/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0b0b0e"/><path d="M18 49V15h16q14 0 14 11 0 8-8 10l10 13H38L27 34v15zm9-24v5h7q5 0 5-3t-5-2z" fill="#e3222a"/></svg>',encoding='utf-8')
import og
(ASSETS/'og').mkdir(exist_ok=True)
LOGO=ROOT/'brand'/'logo-transparent.webp'
og.card(ASSETS/'albanileria-2000.webp',['Tu casa,','a otro'],'nivel.','Reformas y construcción',LOGO,ASSETS/'og'/'reformarvel.jpg')
for n,s_ in enumerate(SERVICES,1):
 og.card(ASSETS/f'{s_[0]}-2000.webp',[s_[1]],s_[2],f'Servicio {n:02} / {len(SERVICES)}',LOGO,ASSETS/'og'/f'{s_[0]}.jpg')
og.icons(ASSETS)
(ASSETS/'site.webmanifest').write_text(json.dumps({'name':C['company'],'short_name':'Reformarvel','start_url':'../index.html','display':'standalone','background_color':'#0b0b0e','theme_color':'#0b0b0e','icons':[{'src':'icon-192.png','sizes':'192x192','type':'image/png'},{'src':'icon-512.png','sizes':'512x512','type':'image/png'}]},ensure_ascii=False),encoding='utf-8')
(OUT/'.nojekyll').write_text('',encoding='utf-8')

# Antes y después: cada original une las dos fotos (izquierda antes, derecha después)
BEFORE_AFTER=[
 ('bano-completo','Antes y después_ baño renovado-2.png','Baño completo','banos','fontaneria','Sanitarios, revestimientos, mampara y mueble nuevos: el mismo espacio con otra luz.'),
 ('cuadro-electrico','Antes y después del cuadro eléctrico-1.png','Cuadro eléctrico','instalaciones','electricidad','De un cableado a la vista y un cuadro antiguo a una instalación ordenada y protegida.'),
 ('salon','Salón antes y después de reformar-7.png','Salón','interiores','pintura','Paredes saneadas, pintura y luz natural: el salón recupera su calidez.'),
 ('fachada','Fachada renovada_ antes y después-9.png','Fachada','exterior','reparacion-fachadas','Reparación de superficies deterioradas y acabado exterior de toda la fachada.'),
 ('suelo','Antes y después_ reforma de suelo-10.png','Suelo y paredes','interiores','tarima-flotante','De un suelo dañado por la humedad a una estancia luminosa con tarima.'),
 ('bano-alicatado','Antes y después_ baño renovado-4.png','Baño alicatado','banos','alicatado','Revestimiento nuevo y sanitarios actualizados con la misma distribución.'),
 ('carpinteria','Antes y después_ carpintería renovada-5.png','Puertas y armario','interiores','carpinteria','Puertas y frentes de armario renovados en madera clara.'),
 ('habitacion','Antes y después_ pared restaurada-3.png','Habitación restaurada','interiores','enyesado','Paredes reparadas, techo saneado y suelo nuevo para una habitación lista para vivir.'),
 ('pared','Pared renovada_ antes y después-6.png','Pared renovada','interiores','enyesado','Una pared desconchada, preparada, enlucida y pintada.'),
 ('escombros','De escombros a habitación despejada-8.png','De escombros a espacio limpio','interiores','desescombro','Retirada de escombro para dejar la estancia despejada y lista para seguir.'),
]
BA_FILTERS=[('todos','Todos'),('banos','Baños'),('interiores','Interiores'),('instalaciones','Instalaciones'),('exterior','Exterior')]
def split_ba(slug,source):
 src=ROOT/source
 if not src.exists():src=ROOT.parent.parent.parent/source
 if not src.exists():
  if (ASSETS/f'ba-{slug}-antes-1000.webp').exists():return
  raise FileNotFoundError(source)
 im=Image.open(src).convert('RGB');w,h=im.size
 for side,box in (('antes',(0,0,w//2,h)),('despues',(w//2,0,w,h))):
  half=im.crop(box)
  for width in (520,1000):
   v=half.copy();v.thumbnail((width,2000));v.save(ASSETS/f'ba-{slug}-{side}-{width}.webp','WEBP',quality=84)
for b in BEFORE_AFTER:split_ba(b[0],b[1])

def compare(b,base='',big=False,eager=False):
 slug,_,title,cat,svc,text=b
 sizes='(max-width: 700px) 100vw, 60vw' if big else '(max-width: 700px) 100vw, 33vw'
 img=lambda side,alt:f'<img src="{base}assets/ba-{slug}-{side}-1000.webp" srcset="{base}assets/ba-{slug}-{side}-520.webp 520w, {base}assets/ba-{slug}-{side}-1000.webp 1000w" sizes="{sizes}" width="768" height="1024" alt="{esc(alt)}" {"" if eager else "loading=lazy"} decoding="async">'
 return f'''<figure class="ba{" ba-big" if big else ""}" data-cat="{cat}">
 <div class="ba-stage" data-ba data-cursor="Arrastra">
  <div class="ba-after">{img("despues",title+": después (imagen ilustrativa)")}</div>
  <div class="ba-before">{img("antes",title+": antes (imagen ilustrativa)")}</div>
  <span class="ba-label ba-l">Antes</span><span class="ba-label ba-r">Después</span>
  <span class="ba-handle" aria-hidden="true"><span class="ba-knob"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l-6 6 6 6M15 6l6 6-6 6"/></svg></span></span>
  <input class="ba-range" type="range" min="0" max="100" value="50" aria-label="Comparar antes y después: {esc(title)}">
 </div>
 <figcaption><span class="ba-svc">{icon(svc)}{BY_SLUG[svc][1]}</span><b>{title}</b><span>{text}</span></figcaption>
</figure>'''

def image(name,alt,base='',eager=False,cls='',sizes='(max-width: 700px) 100vw, 60vw',big=False):
 has2000=(ASSETS/f'{name}-2000.webp').exists()
 srcset=f'{base}assets/{name}-640.webp 640w, {base}assets/{name}-1400.webp 1400w'+(f', {base}assets/{name}-2000.webp 2000w' if has2000 and big else '')
 load='fetchpriority="high"' if eager else 'loading="lazy"'
 return f'<img class="{cls}" src="{base}assets/{name}-1400.webp" srcset="{srcset}" sizes="{sizes}" width="1400" height="933" alt="{esc(alt)}" {load} decoding="async">'

# ---------- Piezas comunes ----------
def header(base,current=''):
 links=''.join(f'<li><a href="{base}servicios/{s[0]}.html" data-preview="{i}"{" aria-current=page" if s[0]==current else ""}><span class="n">{i+1:02}</span>{icon(s[0])}<span class="t">{s[1]}</span></a></li>' for i,s in enumerate(SERVICES))
 previews=''.join(f'<img src="{base}assets/{s[0]}-640.webp" alt="" loading="lazy" width="640" height="427" data-i="{i}">' for i,s in enumerate(SERVICES))
 return f'''<a class="skip" href="#contenido">Saltar al contenido</a>
<div class="progress" aria-hidden="true"></div>
<header class="header" data-header>
 <a class="brand" href="{base}index.html" aria-label="Reformarvel Construcciones, inicio"><img src="{base}assets/logo.webp" alt="Reformarvel Construcciones" width="1032" height="173"></a>
 <nav class="nav" aria-label="Navegación principal">
  <div class="nav-services">
   <button class="nav-link" type="button" aria-expanded="false" aria-controls="mega" data-mega-toggle>Servicios <span class="plus" aria-hidden="true"></span></button>
   <div class="mega" id="mega" data-mega>
    <div class="mega-in">
     <div class="mega-side"><p class="kicker">11 oficios · un solo equipo</p><p class="mega-title">De la base<br><em>al último remate.</em></p><div class="mega-preview" aria-hidden="true">{previews}</div></div>
     <ul class="mega-list">{links}</ul>
    </div>
   </div>
  </div>
  <a class="nav-link" href="{base}como-trabajamos.html"{" aria-current=page" if current=="como-trabajamos" else ""}>Cómo trabajamos</a>
  <a class="nav-link" href="{base}index.html#tu-peticion">Tu petición</a>
  <a class="nav-link" href="{base}index.html#preguntas">Preguntas</a>
 </nav>
 <a class="btn btn-red btn-sm header-cta magnetic" href="{wa()}" data-wa target="_blank" rel="noopener">{WA_ICON}<span>Presupuesto</span></a>
 <button class="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Abrir menú" data-burger><span></span><span></span></button>
</header>
<div class="menu" id="menu" data-menu hidden>
 <div class="menu-in">
  <p class="kicker">Servicios</p>
  <ul class="menu-list">{links}</ul>
  <div class="menu-foot">
   <a href="{base}como-trabajamos.html">Cómo trabajamos</a><a href="{base}index.html#tu-peticion">Tu petición</a><a href="{base}index.html#preguntas">Preguntas</a>
   <a class="btn btn-wa" href="{wa()}" data-wa target="_blank" rel="noopener">{WA_ICON}<span>Escríbenos por WhatsApp</span></a>
  </div>
 </div>
</div>'''

def marquee(base,reverse=False,outline=False):
 items=''.join(f'<a href="{base}servicios/{s[0]}.html">{s[1]}</a><span class="star" aria-hidden="true">✦</span>' for s in SERVICES)
 return f'<div class="marquee{" is-outline" if outline else ""}" data-marquee="{-1 if reverse else 1}"><div class="marquee-track">{items}</div></div>'

def cta(base,topic=''):
 label=f'Pedir presupuesto de {topic.lower()}' if topic else 'Escríbenos por WhatsApp'
 return f'''<section class="cta" data-sparks>
 <canvas class="sparks" aria-hidden="true"></canvas>
 <div class="cta-in">
  <p class="kicker reveal">Sin formularios · sin esperas</p>
  <h2 class="cta-title split">¿Empezamos<br><em>tu obra?</em></h2>
  <p class="lead reveal">Un mensaje de WhatsApp, unas fotos del espacio y lo que te gustaría cambiar. Con eso empezamos a hablar de tu reforma.</p>
  <div class="cta-actions reveal">
   <a class="btn btn-wa btn-xl magnetic" href="{wa(topic)}" data-wa target="_blank" rel="noopener">{WA_ICON}<span>{esc(label)}</span></a>
   <a class="btn btn-ghost magnetic" href="tel:{C['phone_e164']}">{PHONE}<span>{C['phone']}</span></a>
  </div>
 </div>
</section>'''

def footer(base):
 svc=''.join(f'<li><a href="{base}servicios/{s[0]}.html">{s[1]}</a></li>' for s in SERVICES)
 return f'''<footer class="footer">
 <div class="footer-top">
  <div class="footer-brand"><img src="{base}assets/logo.webp" alt="Reformarvel Construcciones" width="1032" height="173" loading="lazy"><p>Reformas y construcción en Los Garres, Murcia. Desde un cambio pequeño hasta una reforma a gran escala.</p></div>
  <div><p class="kicker">Servicios</p><ul class="footer-svc">{svc}</ul></div>
  <div><p class="kicker">Contacto</p><ul class="footer-contact">
   <li><a href="{wa()}" data-wa target="_blank" rel="noopener">{WA_ICON}WhatsApp</a></li>
   <li><a href="tel:{C['phone_e164']}">{PHONE}{C['phone']}</a></li>
   <li><a href="{C['instagram']}" target="_blank" rel="noopener noreferrer">{INSTA}@reformarvel</a></li>
   <li class="addr">{esc(C['address'])}<small>Dirección facilitada, pendiente de verificar.</small></li>
  </ul></div>
 </div>
 <p class="footer-word" aria-hidden="true">REFORMARVEL</p>
 <div class="footer-bottom"><span>© Reformarvel Construcciones</span><span>Imágenes ilustrativas: no documentan obras realizadas.</span><span>Empresa independiente, sin relación con Marvel ni con The Walt Disney Company. Estética de cómic de creación propia.</span><a href="{base}aviso-legal.html">Aviso legal</a><a href="{base}privacidad.html">Privacidad</a></div>
</footer>
<a class="wa-float" href="{wa()}" data-wa target="_blank" rel="noopener" aria-label="Escribir por WhatsApp"><span class="wa-bubble" data-wa-bubble>¿Hablamos de tu reforma?</span>{WA_ICON}</a>
<div class="cursor" aria-hidden="true"><span class="cursor-dot"></span><span class="cursor-ring"><b class="cursor-label"></b></span></div>
<div class="veil" aria-hidden="true"><span class="veil-mark">R</span></div>'''

def document(title,desc,body,base='',path='index.html',current='',topic='',page='home'):
 url=C['origin']+'/'+(path if path!='index.html' else '')
 og_name=current or 'reformarvel'
 og_alt=f'Reformarvel Construcciones · {topic}' if topic else 'Reformarvel Construcciones · Tu casa, a otro nivel'
 structured=json.dumps({'@context':'https://schema.org','@type':'HomeAndConstructionBusiness','name':C['company'],'telephone':C['phone_e164'],'url':C['origin'],'sameAs':[C['instagram']],'address':{'@type':'PostalAddress','addressLocality':'Los Garres','addressRegion':'Murcia','addressCountry':'ES'}},ensure_ascii=False).replace('</','<\\/')
 return f'''<!doctype html>
<html lang="es" class="no-js">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#0b0b0e">
<meta property="og:type" content="website"><meta property="og:site_name" content="Reformarvel Construcciones"><meta property="og:locale" content="es_ES"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{C['origin']}/assets/og/{og_name}.jpg"><meta property="og:image:secure_url" content="{C['origin']}/assets/og/{og_name}.jpg"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{esc(og_alt)}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{C['origin']}/assets/og/{og_name}.jpg">
<link rel="canonical" href="{url}">
<script type="application/ld+json">{structured}</script>
<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="{base}assets/favicon-32.png" sizes="32x32" type="image/png"><link rel="apple-touch-icon" href="{base}assets/apple-touch-icon.png"><link rel="manifest" href="{base}assets/site.webmanifest">
<link rel="preload" href="{base}assets/fonts/font-2.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="{base}assets/styles.css">
<script>document.documentElement.className='js';try{{if(!sessionStorage.getItem('rm-intro')&&{str(page=='home').lower()}&&!matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('show-intro');if(sessionStorage.getItem('rm-nav'))document.documentElement.classList.add('veil-in');sessionStorage.removeItem('rm-nav')}}catch(e){{}}</script>
<script src="{base}assets/lenis.min.js" defer></script>
<script src="{base}assets/app.js" defer></script>
</head>
<body class="page-{page}" data-wa-number="{WA_NUMBER}" data-topic="{esc(topic)}">
{intro() if page=='home' else ''}{header(base,current)}
<main id="contenido">
{body}
</main>
{footer(base)}
</body>
</html>'''

def intro():
 return '''<div class="intro" aria-hidden="true"><div class="intro-panel top"></div><div class="intro-panel bottom"></div><div class="intro-core"><img src="assets/logo.webp" alt="" width="1032" height="173"><span class="intro-line"></span><span class="intro-count"><b data-count-intro>00</b> / 100 · Preparando la obra</span></div></div>'''

# ---------- Configurador de la petición por WhatsApp ----------
SPACES='Piso|Casa|Local|Comunidad'
WHEN='Lo antes posible|En 1–3 meses|Estoy mirando opciones'
def chips(name,options,kind='checkbox',icons=False):
 out=[]
 for i,o in enumerate(options):
  ic=icon(o[0],'chip-ico') if icons else ''
  label=o[1] if icons else o
  value=o[1] if icons else o
  out.append(f'<label class="chip"><input type="{kind}" name="{name}" value="{esc(value)}"{" data-slug="+chr(34)+o[0]+chr(34) if icons else ""}>{ic}<span>{esc(label)}</span></label>')
 return ''.join(out)

def builder(service=None):
 if service:
  slug,name=service[0],service[1]
  first=f'<fieldset class="step"><legend><span class="step-n">01</span>¿Qué necesitas de {esc(name.lower())}?</legend><div class="chips">{chips("job",service[8].split("|"))}</div></fieldset>'
  title=f'Tu petición de <em>{esc(name.lower())}</em>,<br>lista en 20 segundos.'
 else:
  slug,name='',''
  first=f'<fieldset class="step"><legend><span class="step-n">01</span>¿Qué oficios necesitas?</legend><div class="chips chips-svc">{chips("svc",[(s[0],s[1]) for s in SERVICES],icons=True)}</div></fieldset>'
  title='Tu petición a medida,<br><em>lista en 20 segundos.</em>'
 return f'''<section class="builder" id="tu-peticion">
 <div class="builder-head"><p class="kicker reveal">Presupuesto por WhatsApp</p><h2 class="split">{title}</h2><p class="lead reveal">Marca lo que necesitas y el mensaje se escribe solo. Al pulsar, se abre WhatsApp con todo preparado: solo tienes que enviarlo y adjuntar fotos si las tienes.</p></div>
 <div class="builder-grid">
  <form class="builder-form" data-builder data-service="{esc(name)}" novalidate>
   {first}
   <fieldset class="step"><legend><span class="step-n">02</span>¿Dónde es la obra?</legend><div class="chips">{chips("space",SPACES.split("|"),"radio")}</div></fieldset>
   <fieldset class="step"><legend><span class="step-n">03</span>¿Para cuándo?</legend><div class="chips">{chips("when",WHEN.split("|"),"radio")}</div></fieldset>
   <fieldset class="step"><legend><span class="step-n">04</span>Unos detalles <small>(opcional)</small></legend>
    <div class="fields"><label class="field"><span>Tu nombre</span><input name="name" autocomplete="given-name" maxlength="60" placeholder="¿Cómo te llamas?"></label><label class="field"><span>Zona o localidad</span><input name="zone" maxlength="60" placeholder="Ej.: Los Garres"></label></div>
    <label class="field"><span>Cuéntanos tu idea</span><textarea name="notes" rows="3" maxlength="600" placeholder="Medidas aproximadas, qué te gustaría cambiar…"></textarea></label>
   </fieldset>
  </form>
  <div class="phone-wrap">
   <div class="phone" aria-live="polite">
    <div class="phone-top"><span class="phone-avatar">R</span><div><b>Reformarvel</b><small>Tu mensaje, listo para enviar</small></div></div>
    <div class="phone-chat"><div class="bubble" data-preview-msg></div><p class="phone-hint" data-preview-hint>Elige una opción y mira cómo se escribe ✍️</p></div>
   </div>
   <div class="phone-actions">
    <a class="btn btn-wa btn-xl magnetic" href="{wa(name.lower() if name else '')}" data-builder-send target="_blank" rel="noopener">{WA_ICON}<span>Enviar por WhatsApp</span></a>
    <button class="btn btn-ghost" type="button" data-builder-copy>Copiar mensaje</button>
   </div>
   <p class="phone-note" role="status" data-builder-status>No guardamos nada: el mensaje solo sale de tu móvil cuando tú lo envías.</p>
  </div>
 </div>
</section>'''

# ---------- Portada ----------
HERO=['albanileria','alicatado','electricidad','pintura','tarima-flotante','reparacion-fachadas']
slides=''.join(f'<div class="slide{" is-active" if i==0 else ""}" data-slide="{i}" data-topic="{esc(BY_SLUG[k][1])}" data-tag="{esc(BY_SLUG[k][2])}" data-desc="{esc(first_sentence(BY_SLUG[k][5]))}" data-tasks="{esc(BY_SLUG[k][6])}" data-href="servicios/{k}.html">{image(k,"Imagen ilustrativa: "+BY_SLUG[k][1].lower(),"",i==0,"",'100vw',True)}</div>' for i,k in enumerate(HERO))
dots=''.join(f'<button type="button" class="hero-dot{" is-active" if i==0 else ""}" data-go="{i}" aria-label="Ver {esc(BY_SLUG[k][1])}"><span class="hd-n">{i+1:02}</span><span class="hd-t">{BY_SLUG[k][1]}</span><span class="hd-bar"><i></i></span></button>' for i,k in enumerate(HERO))
first=BY_SLUG[HERO[0]]
svc_rows=''.join(f'''<li class="svc-row reveal" data-preview="{i}">
 <a class="svc-link" href="servicios/{s[0]}.html" data-cursor="Ver"><span class="svc-n">{i+1:02}</span><span class="svc-main"><span class="svc-name">{s[1]}</span><span class="svc-power"><b>Superpoder:</b> {POWERS[s[0]]}</span><span class="svc-more"><span><span class="svc-desc">{first_sentence(s[5])}</span><span class="svc-tasks">{''.join('<i>'+t+'</i>' for t in s[6].split('|'))}</span></span></span></span><span class="svc-tag">{s[2]}</span><span class="svc-thumb">{image(s[0],'Imagen ilustrativa: '+s[1].lower(),'',False,'','160px')}</span>{ARROW}</a>
 <a class="svc-wa" href="{wa(s[1].lower())}" data-wa="{esc(s[1].lower())}" target="_blank" rel="noopener" aria-label="Pedir presupuesto de {esc(s[1].lower())} por WhatsApp">{WA_ICON}</a>
</li>''' for i,s in enumerate(SERVICES))
villains=''.join(f'''<a class="villain reveal tilt" href="servicios/{slug}.html" data-cursor="Al rescate">
 <span class="v-sfx">{BURST}<b>{sfx}</b></span>
 <span class="v-tag">Villano nº {i+1:02}</span>
 <h3 class="v-name">{name}</h3>
 <p>{text}</p>
 <span class="v-hero">{icon(slug)}<span><small>Lo vence</small>{BY_SLUG[slug][1]}</span>{ARROW}</span>
</a>''' for i,(name,text,slug,sfx) in enumerate(VILLAINS))
float_imgs=''.join(f'<img src="assets/{s[0]}-640.webp" alt="" width="640" height="427" loading="lazy" data-i="{i}">' for i,s in enumerate(SERVICES))
STEPS=[('Nos escribes','Por WhatsApp, desde cualquier servicio de la web. Cuéntanos qué quieres cambiar, adjunta fotos o vídeos del espacio y, si las tienes, medidas aproximadas. Con eso ya podemos empezar a hablar.','pintura-detail','¡Hola! Quiero renovar el baño. Os mando fotos 📸'),('Valoramos','Estudiamos el espacio, las medidas y el estado de las instalaciones. Así definimos qué oficios hacen falta, en qué orden y qué conviene revisar antes de tapar nada.','electricidad-detail','Medidas tomadas. Vamos a ver qué necesita…'),('Presupuesto claro','Trabajos, materiales y condiciones se concretan por escrito antes de empezar, para que sepas qué incluye cada parte. Pedirlo no te compromete a nada.','alicatado-detail','Todo por escrito, sin sorpresas.'),('Manos a la obra','Cada oficio entra en su momento: primero lo que no se ve, después los acabados. Cuidamos la ejecución hasta el último remate.','carpinteria-detail','Último remate… ¡misión cumplida!')]
steps=''.join(f'<article class="chapter"><div class="chapter-img">{image(img,"Imagen ilustrativa del paso: "+t.lower(),"",False,"","(max-width: 900px) 90vw, 40vw")}<span class="panel-tag">Capítulo {i+1}</span><span class="speech">{b}</span></div><div class="chapter-copy"><span class="chapter-n">0{i+1}</span><h3>{t}</h3><p>{d}</p></div></article>' for i,(t,d,img,b) in enumerate(STEPS))
GALLERY=[('alicatado','Texturas y precisión'),('tarima-flotante','La calidez del suelo'),('pintura','Luz y acabados'),('reparacion-fachadas','Del interior al exterior'),('fontaneria-detail','Lo que no se ve'),('carpinteria','Madera y ajuste')]
gallery=''.join(f'<figure class="g-item g{i+1} reveal-img" data-lightbox="{i}"><div class="g-media" data-parallax>{image(k,"Imagen ilustrativa: "+t.lower(),"",False,"","(max-width: 700px) 100vw, 50vw",True)}</div><figcaption><span>{t}</span></figcaption></figure>' for i,(k,t) in enumerate(GALLERY))
FAQ=[('¿Cómo pido presupuesto?','Por WhatsApp. Desde cada servicio, el mensaje se prepara con lo que necesitas; tú solo lo envías. Si tienes fotos o medidas, adjúntalas en el mismo chat.'),('¿Hacéis trabajos pequeños?','Sí. Desde un cambio pequeño hasta una reforma a gran escala: una pared, un baño, un suelo o la casa entera.'),('¿Pedir presupuesto me compromete a algo?','No. El presupuesto es sin compromiso. Trabajos, materiales y condiciones se concretan antes de empezar.'),('¿Qué información conviene enviar?','Fotos del espacio, medidas aproximadas, qué quieres cambiar y cuándo te gustaría empezar. Cuanto más contexto, más fácil es valorar el trabajo.'),('¿Dónde estáis?','En Los Garres, Murcia. Si tu obra está en otra zona, pregúntanos por WhatsApp.')]
faq=''.join(f'<details class="faq-item reveal"><summary><span>{q}</span><i aria-hidden="true"></i></summary><div class="faq-a"><p>{a}</p></div></details>' for q,a in FAQ)

home=f'''<section class="hero" data-hero>
 <div class="hero-slides">{slides}</div>
 <div class="hero-shade" aria-hidden="true"></div>
 <div class="hero-spot" aria-hidden="true"></div>
 <div class="hero-in">
  <p class="kicker hero-kicker"><span class="pulse" aria-hidden="true"></span>Reformas y construcción · Los Garres, Murcia</p>
  <h1 class="hero-title"><span class="line"><span>Tu casa,</span></span><span class="line"><span>a otro <em>nivel.</em></span></span></h1>
  <div class="hero-now"><span class="now-label">Ahora:</span><span class="now-word" data-now>{first[1]}</span><span class="now-tag" data-now-tag>{first[2]}</span></div>
  <p class="now-desc" data-now-desc>{first_sentence(first[5])}</p>
  <ul class="now-tasks" data-now-tasks>{''.join('<li>'+t+'</li>' for t in first[6].split('|'))}</ul>
  <div class="hero-actions">
   <a class="btn btn-wa btn-lg magnetic" href="{wa(first[1].lower())}" data-hero-wa target="_blank" rel="noopener">{WA_ICON}<span>Pedir presupuesto de <b data-now-btn>{first[1].lower()}</b></span></a>
   <a class="btn btn-ghost magnetic" href="#servicios">Ver los 11 oficios</a>
  </div>
 </div>
 <div class="level" aria-hidden="true" data-level><span class="level-glass"><i class="level-bubble"></i><b></b><b></b></span><span class="level-txt">Mueve el ratón · <em data-level-txt>busca el nivel</em></span></div>
 <a class="badge" href="#tu-peticion" aria-label="Preparar tu petición por WhatsApp"><svg viewBox="0 0 200 200" aria-hidden="true"><defs><path id="circ" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs><text><textPath href="#circ">PRESUPUESTO SIN COMPROMISO · POR WHATSAPP · </textPath></text></svg><span class="badge-core">{WA_ICON}</span></a>
 <div class="hero-nav">
  <div class="hero-dots">{dots}</div>
  <div class="hero-arrows"><button type="button" class="round" data-prev aria-label="Anterior">{ARROW}</button><button type="button" class="round" data-next aria-label="Siguiente">{ARROW}</button></div>
 </div>
 <p class="hero-note">Imágenes ilustrativas</p>
 <div class="halftone ht-hero" aria-hidden="true"></div>
</section>
{marquee('')}
<section class="manifesto">
 <p class="kicker reveal">Toda casa tiene su historia de origen</p>
 <p class="manifesto-text" data-scrub>Un baño, una pared, un suelo o la casa entera. En una reforma se cruzan muchos oficios: en Reformarvel los reunimos para que tu idea avance con un mismo equipo, <em>de la base al acabado.</em></p>
 <div class="manifesto-cols">
  <p class="reveal">Una reforma rara vez es un solo trabajo. Cambiar un baño implica fontanería, electricidad, alicatado y remates; renovar un salón puede pedir yeso, pintura y un suelo nuevo. Cuando cada oficio va por su lado, la obra se alarga y los detalles se pierden.</p>
  <p class="reveal">Por eso planteamos cada reforma como una sola historia: escuchamos lo que quieres, valoramos el espacio y coordinamos los oficios necesarios para que cada uno entre en su momento. Tú hablas con un equipo; nosotros nos ocupamos del orden.</p>
 </div>
 <div class="stats">
  <div class="stat reveal"><b data-count="11">11</b><span>oficios bajo<br>un mismo nombre</span></div>
  <div class="stat reveal"><b data-count="1">1</b><span>chat de WhatsApp<br>para pedirlo todo</span></div>
  <div class="stat reveal"><b>0</b><span>compromiso al<br>pedir presupuesto</span></div>
 </div>
</section>
<section class="villains">
 <div class="halftone ht-villains" aria-hidden="true"></div>
 <div class="section-head"><p class="kicker reveal">Atención, vecinos</p><h2 class="split">Toda casa tiene<br><em>sus villanos.</em></h2><p class="lead reveal">Humedades que vuelven, grietas que crecen, enchufes que no llegan. Cada problema de una casa tiene un oficio capaz de plantarle cara. Elige a tu villano y te contamos cómo lo afrontamos.</p></div>
 <div class="v-grid">{villains}</div>
</section>
<section class="services" id="servicios">
 <div class="section-head"><p class="kicker reveal">01 — Los oficios</p><h2 class="split">Once oficios,<br><em>once superpoderes.</em></h2><p class="lead reveal">Cada oficio resuelve una parte de tu reforma. Pasa por encima para ver qué hace cada uno, entra para conocerlo a fondo o pulsa el icono de WhatsApp: el mensaje llega con el servicio ya escrito.</p></div>
 <ul class="svc-list" data-svc-list>{svc_rows}</ul>
 <div class="svc-float" aria-hidden="true" data-svc-float>{float_imgs}</div>
</section>
<section class="process" id="proceso" data-pin>
 <div class="pin-sticky">
  <div class="process-head"><p class="kicker">02 — Cómo trabajamos</p><h2>Tu reforma,<br><em>en cuatro capítulos.</em></h2><div class="pin-progress"><i></i></div><a class="process-more" href="como-trabajamos.html">Ver el método completo {ARROW}</a></div>
  <div class="pin-view"><div class="pin-track" data-pin-track>{steps}</div></div>
 </div>
</section>
<section class="teaser">
 <div class="teaser-copy"><p class="kicker reveal">La transformación</p><h2 class="split">Arrastra y mira<br><em>el cambio.</em></h2><p class="lead reveal">Desliza el control para pasar del antes al después. En la página de cómo trabajamos tienes diez transformaciones más, explicadas oficio por oficio.</p><a class="btn btn-red magnetic reveal" href="como-trabajamos.html">Ver cómo trabajamos {ARROW}</a><p class="ba-note reveal">Imágenes ilustrativas: muestran el tipo de cambio, no obras realizadas por Reformarvel.</p></div>
 {compare(BEFORE_AFTER[0],'',True)}
</section>
{builder()}
<section class="gallery" id="galeria">
 <div class="section-head"><p class="kicker reveal">03 — En detalle</p><h2 class="split">Los detalles<br><em>se ven.</em></h2><p class="lead reveal">Referencias visuales de nuestros oficios. Las imágenes son ilustrativas: no documentan obras realizadas por Reformarvel.</p></div>
 <div class="g-grid">{gallery}</div>
</section>
{marquee('',True,True)}
<section class="faq" id="preguntas">
 <div class="section-head"><p class="kicker reveal">04 — Preguntas</p><h2 class="split">Lo que todo el<br>mundo <em>pregunta.</em></h2></div>
 <div class="faq-list">{faq}</div>
</section>
{cta('')}
<div class="lightbox" data-lightbox-box hidden><button type="button" class="lb-close" aria-label="Cerrar">×</button><button type="button" class="lb-prev round" aria-label="Anterior">{ARROW}</button><figure><img alt=""><figcaption></figcaption></figure><button type="button" class="lb-next round" aria-label="Siguiente">{ARROW}</button></div>'''
(OUT/'index.html').write_text(document('Reformarvel Construcciones | Reformas en Los Garres, Murcia','Reformas pequeñas y a gran escala en Los Garres, Murcia. Once oficios de construcción y presupuesto sin compromiso por WhatsApp.',home),encoding='utf-8')

# ---------- Servicios ----------
for index,s in enumerate(SERVICES):
 slug,name,tag,photo,detail,desc,tasks,prepare,opts=s
 heading=name if slug!='impermeabilizaciones' else 'Impermea&shy;biliza&shy;ciones'
 prev=SERVICES[index-1];nxt=SERVICES[(index+1)%len(SERVICES)]
 related=[SERVICES[(index+k)%len(SERVICES)] for k in (2,3,4)]
 rel=''.join(f'<a class="rel-card tilt" href="{r[0]}.html" data-cursor="Ver"><div class="rel-img">{image(r[0],"Imagen ilustrativa: "+r[1].lower(),"../",False,"","(max-width: 700px) 90vw, 30vw")}</div><div class="rel-copy">{icon(r[0])}<h3>{r[1]}</h3><p>{r[2]}</p></div></a>' for r in related)
 task_items=''.join(f'<li class="reveal"><span class="tick" aria-hidden="true"></span>{t}</li>' for t in tasks.split('|'))
 page=f'''<section class="s-hero">
 <div class="s-hero-media" data-parallax-hero>{image(slug,"Imagen ilustrativa: "+name.lower(),"../",True,"","100vw",True)}</div>
 <div class="hero-shade" aria-hidden="true"></div>
 <div class="hero-spot" aria-hidden="true"></div>
 <div class="s-hero-in">
  <nav class="crumbs" aria-label="Ruta"><a href="../index.html">Inicio</a><span>/</span><a href="../index.html#servicios">Servicios</a><span>/</span><span aria-current="page">{name}</span></nav>
  <p class="kicker"><span class="s-icon">{icon(slug)}</span>{index+1:02} / 11 — Servicio</p>
  <h1 class="s-title{" long" if slug=="impermeabilizaciones" or len(name)>14 else ""}" data-letters>{heading}</h1>
  <p class="s-tag"><em>{tag}</em></p>
  <div class="hero-actions">
   <a class="btn btn-wa btn-lg magnetic" href="{wa(name.lower())}" data-wa="{esc(name.lower())}" target="_blank" rel="noopener">{WA_ICON}<span>Pedir presupuesto de {name.lower()}</span></a>
   <a class="btn btn-ghost magnetic" href="#tu-peticion">Prepararlo a medida</a>
  </div>
 </div>
 <p class="hero-note">Imagen ilustrativa</p>
 <a class="scroll-cue" href="#el-oficio" aria-label="Bajar"><span></span></a>
</section>
<section class="s-intro" id="el-oficio">
 <div><p class="kicker reveal">El oficio</p><h2 class="split">El trabajo detrás<br>del <em>resultado.</em></h2></div>
 <div><p class="lead big reveal">{desc}</p><h3 class="mini reveal">Qué podemos valorar</h3><ul class="ticks">{task_items}</ul><p class="muted reveal">El alcance concreto, los materiales y las condiciones se definen según cada espacio y presupuesto.</p></div>
</section>
<section class="s-detail">
 <figure class="reveal-img s-detail-img"><div class="g-media" data-parallax>{image(slug+"-detail","Imagen ilustrativa relacionada con "+name.lower(),"../",False,"","(max-width: 900px) 100vw, 55vw",True)}</div><figcaption>Referencia visual ilustrativa</figcaption></figure>
 <div class="s-detail-copy"><p class="kicker reveal">Antes de escribirnos</p><h2 class="split">Cuéntanos<br>los <em>detalles.</em></h2><p class="lead reveal">{prepare}</p><div class="tip reveal">{WA_ICON}<p><b>Truco:</b> en el chat de WhatsApp puedes adjuntar fotos y vídeos del espacio. Nos ayudan a entender el trabajo desde el primer mensaje.</p></div></div>
</section>
{marquee('../')}
{builder(s)}
<section class="related">
 <div class="section-head"><p class="kicker reveal">Otros oficios</p><h2 class="split">Todo está<br><em>conectado.</em></h2></div>
 <div class="rel-grid">{rel}</div>
</section>
<nav class="pager" aria-label="Servicio anterior y siguiente">
 <a class="pager-link prev" href="{prev[0]}.html" data-cursor="Ver"><small>{ARROW} Anterior</small><span>{prev[1]}</span>{image(prev[0],"", "../",False,"pager-img","40vw")}</a>
 <a class="pager-link next" href="{nxt[0]}.html" data-cursor="Ver"><small>Siguiente {ARROW}</small><span>{nxt[1]}</span>{image(nxt[0],"", "../",False,"pager-img","40vw")}</a>
</nav>
{cta('../',name)}'''
 (OUT/'servicios'/f'{slug}.html').write_text(document(f'{name} en Los Garres, Murcia | Reformarvel',f'{tag} Servicio de {name.lower()} de Reformarvel Construcciones en Los Garres, Murcia. Pide presupuesto sin compromiso por WhatsApp.',page,'../',f'servicios/{slug}.html',slug,name,'service'),encoding='utf-8')


# ---------- Cómo trabajamos ----------
METHOD=[
 ('Nos escribes','Todo empieza con un mensaje de WhatsApp. Desde cualquier servicio de la web el mensaje se prepara con lo que necesitas, y en el mismo chat puedes adjuntar fotos y vídeos del espacio.',['Qué quieres cambiar y para qué lo usas','Fotos o vídeos del espacio','Medidas aproximadas, si las tienes','Cuándo te gustaría empezar'],'pintura-detail','¡Hola! Quiero renovar el baño. Os mando fotos 📸'),
 ('Valoramos el espacio','Con la información que nos envías estudiamos el espacio, las medidas y el estado de las instalaciones. Así sabemos qué oficios hacen falta y qué conviene revisar antes de tapar nada.',['Estado del soporte: paredes, suelos, fachada','Instalaciones de agua y electricidad','Accesos y retirada de escombro','Orden en que entra cada oficio'],'electricidad-detail','Medidas tomadas. Vamos a ver qué necesita…'),
 ('Presupuesto claro','Trabajos, materiales y condiciones se concretan por escrito antes de empezar, para que sepas qué incluye cada parte. Pedir presupuesto no te compromete a nada.',['Trabajos detallados por oficio','Materiales y acabados','Condiciones antes de empezar','Sin compromiso por pedirlo'],'alicatado-detail','Todo por escrito, sin sorpresas.'),
 ('Manos a la obra','Cada oficio entra en su momento: primero lo que no se ve, después los acabados. Cuidamos la ejecución hasta el último remate y te mantenemos al tanto por el mismo chat.',['Primero instalaciones y soporte','Después revestimientos y acabados','Remates y encuentros cuidados','Seguimiento por WhatsApp'],'carpinteria-detail','Último remate… ¡misión cumplida!'),
]
method=''.join(f'''<article class="m-step">
 <div class="m-panel reveal"><div class="g-media" data-parallax>{image(img,"Imagen ilustrativa: "+t.lower(),"",False,"","(max-width: 900px) 100vw, 45vw")}</div><span class="panel-tag">Capítulo {i+1}</span><span class="speech is-static">{bubble}</span></div>
 <div class="m-copy"><span class="chapter-n">0{i+1}</span><h3 class="split">{t}</h3><p class="lead reveal">{d}</p><ul class="ticks">{''.join('<li class="reveal"><span class="tick" aria-hidden="true"></span>'+x+'</li>' for x in items)}</ul></div>
</article>''' for i,(t,d,items,img,bubble) in enumerate(METHOD))
filters=''.join(f'<button type="button" class="chip{" is-on" if k=="todos" else ""}" data-filter="{k}" aria-pressed="{"true" if k=="todos" else "false"}"><span>{n}</span></button>' for k,n in BA_FILTERS)
ba_grid=''.join(compare(b) for k,b in enumerate(BEFORE_AFTER) if k!=2)
PROMISES=[('Un solo chat','Pides, envías fotos, resuelves dudas y sigues la obra en la misma conversación de WhatsApp.'),('Todo por escrito','Trabajos, materiales y condiciones quedan concretados antes de empezar.'),('Oficios coordinados','Cada oficio entra en su momento para que la obra avance en orden.'),('Del pequeño cambio a la reforma completa','Una pared, un baño, un suelo o la casa entera.')]
promises=''.join(f'<div class="promise reveal"><span class="promise-n">0{i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i,(t,d) in enumerate(PROMISES))
how=f'''<section class="p-hero">
 <div class="halftone ht-villains" aria-hidden="true"></div>
 <div class="p-hero-in">
  <nav class="crumbs" aria-label="Ruta"><a href="index.html">Inicio</a><span>/</span><span aria-current="page">Cómo trabajamos</span></nav>
  <p class="kicker">El método Reformarvel</p>
  <h1 class="p-title"><span class="line"><span>Cómo</span></span><span class="line"><span>trabajamos<em>.</em></span></span></h1>
  <p class="lead big">Una reforma bien hecha es una historia bien contada: un primer mensaje, una valoración honesta, un presupuesto claro y cada oficio en su momento. Así la llevamos de la idea al último remate.</p>
  <div class="hero-actions"><a class="btn btn-wa btn-lg magnetic" href="{wa()}" data-wa target="_blank" rel="noopener">{WA_ICON}<span>Empezar por WhatsApp</span></a><a class="btn btn-ghost magnetic" href="#transformaciones">Ver transformaciones</a></div>
 </div>
 {compare(BEFORE_AFTER[2],'',True,True)}
</section>
{marquee('')}
<section class="method" id="metodo">
 <div class="section-head"><p class="kicker reveal">01 — El método</p><h2 class="split">Cuatro capítulos,<br><em>una sola historia.</em></h2><p class="lead reveal">Esto es lo que pasa desde que nos escribes hasta que la obra queda terminada, y lo que conviene tener a mano en cada momento.</p></div>
 {method}
</section>
<section class="transform" id="transformaciones">
 <div class="section-head"><p class="kicker reveal">02 — Transformaciones</p><h2 class="split">Arrastra y mira<br><em>la transformación.</em></h2><p class="lead reveal">Desliza cada imagen para pasar del antes al después. Filtra por tipo de espacio y pulsa el oficio para ver cómo lo trabajamos.</p></div>
 <div class="ba-filters chips" role="group" aria-label="Filtrar transformaciones">{filters}</div>
 <div class="ba-grid">{ba_grid}</div>
 <p class="ba-note">Imágenes ilustrativas: muestran el tipo de cambio que se consigue con cada oficio, no obras realizadas por Reformarvel.</p>
</section>
<section class="promises">
 <div class="section-head"><p class="kicker reveal">03 — Lo que puedes esperar</p><h2 class="split">Las reglas<br><em>de la casa.</em></h2></div>
 <div class="promise-grid">{promises}</div>
</section>
{builder()}
{cta('')}'''
ogsrc=Image.new('RGB',(1536,1024))
for k,side in enumerate(('antes','despues')):ogsrc.paste(Image.open(ASSETS/f'ba-salon-{side}-1000.webp').convert('RGB').resize((768,1024)),(k*768,0))
ogsrc.save(ASSETS/'og'/'_salon.webp');og.card(ASSETS/'og'/'_salon.webp',['Cómo trabajamos'],'Del primer mensaje al último remate.','El método Reformarvel',LOGO,ASSETS/'og'/'como-trabajamos.jpg');(ASSETS/'og'/'_salon.webp').unlink()
(OUT/'como-trabajamos.html').write_text(document('Cómo trabajamos | Reformarvel Construcciones','Así trabaja Reformarvel en Los Garres, Murcia: del primer WhatsApp al último remate en cuatro capítulos. Mira transformaciones de antes y después.',how,'','como-trabajamos.html','como-trabajamos','','how'),encoding='utf-8')

# ---------- Legales ----------
for slug,title in [('aviso-legal','Aviso legal'),('privacidad','Privacidad')]:
 if slug=='aviso-legal':
  content='<h2>Datos pendientes de completar</h2><p>Esta página es una plantilla de revisión. Deben completarse y verificarse la razón social del titular, su NIF/CIF, el domicilio legal y, cuando corresponda, los datos registrales antes de utilizarla como aviso legal definitivo.</p><dl><dt>Nombre comercial</dt><dd>Reformarvel Construcciones</dd><dt>Razón social y NIF/CIF</dt><dd>Pendientes de facilitar</dd><dt>Domicilio legal</dt><dd>Pendiente de verificar</dd></dl>'
 else:
  content='<h2>Cómo funciona esta web</h2><p>La web no tiene formularios que envíen datos a un servidor. Los botones de WhatsApp abren la aplicación con un mensaje preparado en tu dispositivo: solo se envía si tú lo decides, y desde ese momento la conversación se rige por las condiciones de WhatsApp.</p><p>No se han integrado herramientas de analítica, publicidad ni mapas externos. Las tipografías y los scripts se sirven desde esta misma web. Se usa el almacenamiento de sesión del navegador solo para no repetir la animación de entrada.</p><h2>Información pendiente</h2><p>Antes de utilizar esta página como política de privacidad definitiva, el titular debe aportar y revisar su identidad como responsable, las finalidades y bases del tratamiento, conservación, destinatarios y el canal para ejercer derechos. Esta plantilla no acredita cumplimiento legal.</p>'
 legal=f'<section class="legal"><p class="kicker">Documento pendiente de completar</p><h1>{title}</h1>{content}<p>Contacto: <a href="tel:{C["phone_e164"]}">{C["phone"]}</a> · <a href="mailto:{C["email"]}">{C["email"]}</a></p><a class="btn btn-ghost" href="index.html">Volver al inicio</a></section>'
 (OUT/f'{slug}.html').write_text(document(title+' | Reformarvel Construcciones',title+': información de revisión pendiente de completar para Reformarvel Construcciones.',legal,path=slug+'.html',page='legal'),encoding='utf-8')

manifest=ROOT/'.openai'/'hosting.json'
if manifest.exists():
 data=json.loads(manifest.read_text());data['static']={'directory':'dist'};manifest.write_text(json.dumps(data,indent=2)+'\n')
print('Generadas 14 páginas HTML y los recursos optimizados.')
