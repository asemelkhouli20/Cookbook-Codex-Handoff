import io,fitz,os
import numpy as np
from PIL import Image
src='tmp/ar/manga/big.pdf';dst='tmp/ar/manga/finished.pdf'
d=fitz.open(src);sizes={}
for p in d:
 for i in p.get_image_info(xrefs=True):
  x=i['xref'];r=fitz.Rect(i['bbox']);sizes[x]=max(sizes.get(x,0),r.width,r.height)
for x,size in sizes.items():
 if not x:continue
 item=d.extract_image(x)
 if not item or len(d.xref_stream_raw(x))<4200:continue
 im=Image.open(io.BytesIO(item['image'])).convert('RGB')
 lim=max(110,round(size*1.95))
 im.thumbnail((lim,lim),Image.Resampling.LANCZOS)
 b=io.BytesIO();im.save(b,'JPEG',quality=81,optimize=True)
 if len(b.getvalue())>=len(d.xref_stream_raw(x)):continue
 d.update_stream(x,b.getvalue(),compress=False)
 for key,v in [('Width',str(im.width)),('Height',str(im.height)),('BitsPerComponent','8'),('ColorSpace','/DeviceRGB'),('Filter','/DCTDecode'),('DecodeParms','null')]:d.xref_set_key(x,key,v)
d.save(dst,garbage=4,deflate=True,use_objstms=0)
orig=fitz.open(src);new=fitz.open(dst);assert len(new)==len(orig) and new.get_toc()==orig.get_toc()
checks=[]
for i,(a,b) in enumerate(zip(orig,new)):
 assert a.get_text()==b.get_text()
 assert [(l['kind'],l.get('page'),l.get('uri'),l['from']) for l in a.get_links()]==[(l['kind'],l.get('page'),l.get('uri'),l['from']) for l in b.get_links()]
 def arr(p):
  pix=p.get_pixmap(matrix=fitz.Matrix(1,1));return np.frombuffer(pix.samples,dtype=np.uint8).astype(float)
 checks.append((np.abs(arr(a)-arr(b)).mean(),i+1))
print(os.path.getsize(src),os.path.getsize(dst),sorted(checks,reverse=True)[:5]);assert max(checks)[0]<3
new[8].get_pixmap(matrix=fitz.Matrix(.8,.8)).save('tmp/ar/manga/stepspreview.png')
