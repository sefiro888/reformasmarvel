"""Download the two open-license Google Fonts once; serve all fonts locally."""
from pathlib import Path
import urllib.request, re
ROOT=Path(__file__).resolve().parent
folder=ROOT/'fonts';folder.mkdir(exist_ok=True)
url='https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap'
req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
css=urllib.request.urlopen(req,timeout=30).read().decode()
for i,source in enumerate(dict.fromkeys(re.findall(r'url\((https://[^)]+)\)',css))):
 name=f'font-{i}'+('.woff2' if '.woff2' in source else '.ttf')
 (folder/name).write_bytes(urllib.request.urlopen(source,timeout=30).read())
 css=css.replace(source,'./fonts/'+name)
(ROOT/'font-faces.css').write_text(css,encoding='utf-8')
print('Tipografías descargadas para servir localmente.')
