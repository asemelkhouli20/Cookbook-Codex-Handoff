import fitz,subprocess,io,json
from pathlib import Path
from PIL import Image
from zipfile import ZipFile,ZIP_STORED
from collections import Counter
base=Path('tmp/waifu'); direct=base/'out'; direct.mkdir(exist_ok=True)
r=fitz.open(base/'large.pdf')
for p in r:p.wrap_contents();p.clean_contents()
r.save(base/'clean.pdf',garbage=4,deflate=True)
out=direct/'Weekly_Meal_Cards.pdf'
subprocess.run(['/usr/bin/python3','-c','import pikepdf,sys; p=pikepdf.open(sys.argv[1]);p.remove_unreferenced_resources();p.save(sys.argv[2],linearize=True,recompress_flate=True,object_stream_mode=pikepdf.ObjectStreamMode.generate)',str(base/'clean.pdf'),str(out)],check=True)
prev=fitz.open('output/pdf/Weekly_Meal_Cards.pdf');new=fitz.open(out);assert len(new)==len(prev)==101;assert new.get_toc()==prev.get_toc()
def links(p):return [(v['kind'],v.get('page'),v.get('uri'),v['from']) for v in p.get_links()]
for a,b in zip(prev,new):
 assert links(a)==links(b),a.number
 if a.number not in [0]:assert a.get_text()==b.get_text(),a.number
pages=base/'reading';pages.mkdir(exist_ok=True)
chapter='مدخل الكتاب';bookmarks={t[2]:t[1].replace('/',' - ') for t in new.get_toc()};dirs={v[2]:v[1].replace('/',' - ') for v in new.get_toc() if v[0]==1}
for i,p in enumerate(new,1):
 chapter=dirs.get(i,chapter);title=bookmarks.get(i,title if i>1 else 'الغلاف')
 pix=p.get_pixmap(matrix=fitz.Matrix(1.55,1.55),alpha=False);im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);dest=pages/chapter/f'{i:03} - {title}.png';dest.parent.mkdir(exist_ok=True);im.quantize(256).save(dest,optimize=True)
 if i in [1,8,9,44]:dest2=Path('/mnt/data')/f'Cookbook-Page-{i}.png';dest2.write_bytes(dest.read_bytes())
exec((base/'zipnames.py').read_text())
art=base/'png'
for folder,name in [(art,'Cooking-Illustrations-PNG.zip'),(pages,'Cookbook-Pages-PNG.zip')]:
 paths=sorted(folder.rglob('*.png'));assert len(paths)>95
 with ZipFile(direct/name,'w',compression=ZIP_STORED) as z:
  for f in paths:z.write(f,zipname(folder,f.relative_to(folder)))
 with ZipFile(direct/name) as z:assert z.testzip() is None
 print(name,len(paths), (direct/name).stat().st_size,flush=True)
print('PDF',out.stat().st_size,'pages',len(new),flush=True)
