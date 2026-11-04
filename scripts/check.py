"""Check generated pages, local resources, anchors, and recipe isolation."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
ROOT=Path(__file__).resolve().parents[1]
class Document(HTMLParser):
    def __init__(self,path):
        super().__init__(); self.ids=set(); self.links=[]; self.recipes=0; self.h1=0; self.feed(path.read_text())
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, f'Duplicate id: {a["id"]}'
            self.ids.add(a['id'])
        if tag=='h1': self.h1+=1
        if tag=='article' and a.get('class')=='recipe': self.recipes+=1
        for key in ('href','src'):
            if key in a: self.links.append(a[key])
paths=[ROOT/'index.html', ROOT/'kitchen.html',*sorted((ROOT/'recipes').glob('*.html'))]
docs={p.resolve():Document(p) for p in paths}
for path,doc in docs.items():
    assert doc.h1==1, (path,'Must have exactly one page heading')
    for link in doc.links:
        url=urlsplit(link)
        if url.scheme or url.netloc: continue
        target=(path.parent/unquote(url.path)).resolve() if url.path else path
        assert target.exists(), (path,link,'Missing local target')
        if url.fragment and target in docs: assert unquote(url.fragment) in docs[target].ids,(path,link,'Missing anchor')
    assert doc.recipes==(1 if path.parent.name=='recipes' else 0),(path,'Recipe isolation')
catalog=docs[ROOT/'index.html']
recipe_links=[link for link in catalog.links if link.startswith('recipes/')]
assert len(recipe_links)==len(set(recipe_links))==35
print('PASS: 37 pages; 35 unique recipe links; isolated recipe content; local resources and anchors resolve.')
