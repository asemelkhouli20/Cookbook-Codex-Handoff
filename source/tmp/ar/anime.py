import fitz,sys,io
from PIL import Image,ImageOps,ImageDraw,ImageChops
src='output/pdf/Weekly_Meal_Cards.pdf'
d=fitz.open(src); im=Image.open(sys.argv[1]).convert('RGB')
ims=[]
for k in range(6):
 w,h=im.size;x,y=k%3,k//3
 a=im.crop((round(x*w/3)+2,round(y*h/2)+2,round((x+1)*w/3)-2,round((y+1)*h/2)-2))
 mask=ImageChops.difference(a,Image.new('RGB',a.size,'white')).convert('L').point(lambda v:255 if v>25 else 0)
 a=a.crop(mask.getbbox() or (0,0,*a.size));ims.append(a)
def data(a):
 b=io.BytesIO();a.save(b,'JPEG',quality=93);return b.getvalue()
# Cover artwork lies below the existing title, description, and navigation text.
bg=Image.new('RGB',(900,1780),'#fff4ea');pen=ImageDraw.Draw(bg)
pen.rounded_rectangle((34,32,866,1748),radius=85,fill='#ffe8ec',outline='#ecc0c6',width=4)
pen.rounded_rectangle((64,68,836,1718),radius=65,fill='#fff8ed')
pen.rounded_rectangle((85,605,815,1560),radius=230,fill='#ffeaed',outline='#f0cbd0',width=4)
for x,y in [(104,150),(795,182),(104,505),(789,520),(100,1370),(778,1400),(112,1530),(796,704)]:
 pen.polygon([(x,y-15),(x+5,y-4),(x+15,y),(x+5,y+4),(x,y+15),(x-5,y+4),(x-15,y),(x-5,y-4)],fill='#dfab69')
hero=ImageOps.contain(ims[0],(662,855)); xy=((900-hero.width)//2,1080-hero.height//2)
# White background blends into a white inset with a pastel border.
pen.rounded_rectangle((xy[0]-10,xy[1]-14,xy[0]+hero.width+10,xy[1]+hero.height+14),radius=30,fill='white')
bg.paste(hero,xy)
d[0].replace_image(d[0].get_images()[0][0],stream=data(bg))
gals={2:0,5:1,6:1,7:1,36:2,37:2,56:3,61:4,63:5,64:5}
count=0
for page in [v[2] for v in d.get_toc() if 5<=v[2]<=81]+[2]:
 p=d[page-1]; gal=page in gals
 key=gals[page] if gal else 1 if page<36 else 2 if page<56 else 3 if page<61 else 4 if page<63 else 5
 obstacles=[fitz.Rect(w[:4]) for w in p.get_text('words')]+[fitz.Rect(v['bbox']) for v in p.get_image_info()]+[l['from'] for l in p.get_links()]
 # The illustrated indexes have a clear left margin in their masthead; the
 # recipe cards have a free left-hand area beside the tools or storage notes.
 slots=([(15,7,105,110),(12,9,87,93),(8,4,60,56)] if gal else [(19,452,113,548),(16,462,92,538),(16,484,78,546),(9,12,49,52)])
 if page==62:slots=[(130,12,179,61),(130,5,168,43),(18,235,48,262)]
 picks=[fitz.Rect(bb) for bb in slots if not any(fitz.Rect(bb).intersects(z) for z in obstacles)]
 if not picks:
  for y in range(449,529,4):
   for x in range(17,160,5):
    bb=fitz.Rect(x,y,x+44,y+44)
    if not any(bb.intersects(z) for z in obstacles):picks=[bb];break
   if picks:break
 assert picks,page
 box=picks[0];p.draw_rect(box,radius=.15,color=(.93,.82,.82),fill=(1,1,1),width=.6);p.insert_image(box+ (3,3,-3,-3),stream=data(ims[key]));count+=1
d.save('tmp/ar/anime.pdf',garbage=3,deflate=True)
old=fitz.open(src);new=fitz.open('tmp/ar/anime.pdf');assert new.get_toc()==old.get_toc() and len(new)==101
for a,b in zip(old,new):
 assert a.get_text()==b.get_text()
 assert [(l.get('page'),l.get('uri')) for l in a.get_links()]==[(l.get('page'),l.get('uri')) for l in b.get_links()]
print(count)
can=Image.new('RGB',(900,593),'white')
for k,p in enumerate([1,5,8]):
 pix=new[p-1].get_pixmap(matrix=fitz.Matrix(2/3,2/3));can.paste(Image.frombytes('RGB',(pix.width,pix.height),pix.samples),(300*k,0))
can.save('tmp/ar/anime_preview.jpg')
