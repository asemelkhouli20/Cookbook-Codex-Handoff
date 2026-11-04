from pathlib import Path
from PIL import Image,ImageDraw
from zipfile import ZipFile
import fitz,hashlib,io,math
folder=Path('tmp/ar')
old=fitz.open('output/pdf/Weekly_Meal_Cards.pdf');new=fitz.open(folder/'meal_cute.pdf')
assert len(new)==len(old)==101 and old.get_toc()==new.get_toc()
for a,b in zip(old,new):
 assert [(x.get('page'),x.get('uri')) for x in a.get_links()]==[(x.get('page'),x.get('uri')) for x in b.get_links()]
 assert b.get_text().strip()
 b.get_pixmap(matrix=fitz.Matrix(.12,.12))
with ZipFile('output/Meal_Illustrations_PNG.zip') as z:
 assert z.testzip() is None and len(z.namelist())==35
 seen=set();sheet=Image.new('RGB',(7*140,5*150),'#fff7f1');pen=ImageDraw.Draw(sheet)
 for i,f in enumerate(z.namelist()):
  raw=z.read(f);seen.add(hashlib.sha256(raw).digest());im=Image.open(io.BytesIO(raw));assert im.format=='PNG' and im.mode=='RGBA' and im.getextrema()[-1]==(0,255)
  im.thumbnail((136,130));x=i%7*140;y=i//7*150;sheet.paste(im,(x+(140-im.width)//2,y),im);pen.text((x+64,y+132),str(i+1),fill='#563833')
 assert len(seen)==35
 sheet.save(folder/'sheet20.jpg')
can=Image.new('RGB',(1080,712))
for k,num in enumerate([5,8,9]):
 px=new[num-1].get_pixmap(matrix=fitz.Matrix(.8,.8));can.paste(Image.frombytes('RGB',(px.width,px.height),px.samples),(k*360,0))
can.save(folder/'proof20.jpg')
