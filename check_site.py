from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
ROOT=Path(__file__).resolve().parent/'dist'
class Page(HTMLParser):
 def __init__(self):
  super().__init__();self.refs=[];self.ids=set();self.titles=[];self.title=False;self.h1=0;self.desc=None;self.errors=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:
   if a['id'] in self.ids:self.errors.append('Duplicate id: '+a['id'])
   self.ids.add(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='title':self.title=True
  if tag=='meta' and a.get('name')=='description':self.desc=a.get('content')
  if tag=='img' and not a.get('alt'):self.errors.append('Missing image alt')
  for key in ('href','src'):
   if a.get(key):self.refs.append(a[key])
  if a.get('srcset'):
   self.refs.extend(x.strip().split()[0] for x in a['srcset'].split(','))
 def handle_endtag(self,tag):
  if tag=='title':self.title=False
 def handle_data(self,data):
  if self.title:self.titles.append(data)
pages={p:Page() for p in ROOT.rglob('*.html')}
for p,parser in pages.items():parser.feed(p.read_text(encoding='utf-8'))
errors=[];checks=0
for p,page in pages.items():
 errors.extend(str(p.relative_to(ROOT))+': '+e for e in page.errors)
 if page.h1!=1:errors.append(str(p)+': expected one h1')
 if not page.desc:errors.append(str(p)+': missing description')
 for ref in page.refs:
  u=urlsplit(ref)
  if u.scheme or u.netloc:continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  checks+=1
  if not target.exists():errors.append(f'{p.name}: missing {ref}')
  elif u.fragment and target in pages and u.fragment not in pages[target].ids:errors.append(f'{p.name}: missing anchor {ref}')
 if '673 962 794' in p.read_text(encoding='utf-8'):errors.append('Obsolete phone exposed')
titles=[''.join(x.titles) for x in pages.values()]
if len(set(titles))!=len(titles):errors.append('Duplicate SEO title')
if len({x.desc for x in pages.values()})!=len(pages):errors.append('Duplicate SEO description')
result={'html_pages':len(pages),'local_links_and_assets_checked':checks,'unique_titles':len(set(titles)),'errors':errors}
print(json.dumps(result,ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
