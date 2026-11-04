import fitz,re
from PIL import Image,ImageOps,ImageDraw
d=fitz.open('output/pdf/Weekly_Meal_Cards.pdf');assert len(d)==74
for i,p in enumerate(d):
 t=p.get_text()
 assert re.search('[\u0600-\u06ff\ufe70-\ufeff]',t),(i,t[:200])
 assert not re.search('[A-Za-z]{2,}',t),(i,t[:200])
 for l in p.get_links():
  assert 'uri' in l or 0<=l['page']<74
print(len(d.get_toc()),'bookmarks;',sum(len(p.get_links()) for p in d),'links')
ims=[]
for i in [0,6,16,26,60,64]:
 pix=d[i].get_pixmap(matrix=fitz.Matrix(.8,.8));ims.append(Image.frombytes('RGB',[pix.width,pix.height],pix.samples))
can=Image.new('RGB',(1080,1424),'white')
for k,im in enumerate(ims):can.paste(im,(k%3*360,k//3*712))
can.save('tmp/ar/check.jpg')
for i in [16,64]:
 d[i].get_pixmap().save(f'tmp/ar/p{i+1}.png')
