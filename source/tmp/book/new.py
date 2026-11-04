from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit,ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
from scipy.ndimage import label
import numpy as np, math,ast,glob
from pathlib import Path
for ff,fil in [('S','DejaVuSans'),('B','DejaVuSans-Bold'),('H','DejaVuSerif-Bold')]:
 pdfmetrics.registerFont(TTFont(ff,'/usr/share/fonts/truetype/dejavu/'+fil+'.ttf'))
art=Image.open(glob.glob('generated_images/exec-c99*.png')[0]).convert('RGB')
imgs=[]
for i in range(9):
 w,h=art.size;x=i%3;y=i//3
 im=art.crop((round(w*x/3),round(h*y/3),round(w*(x+1)/3),round(h*(y+1)/3)))
 a=np.array(im); masks,n=label(a.min(axis=2)>220)
 ix=np.unique(np.concatenate([masks[0],masks[-1],masks[:,0],masks[:,-1]]))
 alpha=np.where(np.isin(masks,ix[ix!=0]),0,255).astype('uint8'); im.putalpha(Image.fromarray(alpha))
 imgs.append(im.crop(im.getbbox()))
W,H=420,690
c=Canvas('output/pdf/Weekly_Meal_Cards.pdf',pagesize=(W,H));c.setTitle('Fork, Spoon & Go! | A weekly meal-prep cookbook')
ink='#351D33'; cream='#FFF9EA';red='#B12F2A'; green='#215643'
pal=[('#F5DDE8','#763152'),('#FBE29E','#7C4020'),('#CDE6CA','#215643'),('#F9D4AA','#84421D'),('#F6CAAE','#892F26'),('#F4E1A8','#6B4724'),('#F6BDAA','#8F2D29'),('#CFE5E7','#28576A')]
def fill(col):c.setFillColor(HexColor(col))
def rect(x,y,w,h,col):fill(col);c.rect(x,y,w,h,fill=1,stroke=0)
def t(x,y,s,sz=12,f='S',col=ink):fill(col);c.setFont(f,sz);c.drawString(x,y,s)
def lines(x,y,s,width,size,leading,f='S',col=ink):
 for li in simpleSplit(s,f,size,width):t(x,y,li,size,f,col);y-=leading
 return y
def dish(i,x,y,w,h,angle=0):
 im=imgs[i];dw=min(w/im.width,h/im.height)*im.width;dh=dw*im.height/im.width
 c.saveState();c.translate(x+w/2,y+h/2);c.rotate(angle);c.drawImage(ImageReader(im),-dw/2,-dh/2,dw,dh,mask='auto');c.restoreState()
def check(y,col):
 for j in range(2):
  for i in range(28):
   if (j+i)%2==0:rect(i*15,y+j*6,15,6,col)
def badge(x,y,s,bg,tc=cream):
 w=pdfmetrics.stringWidth(s,'B',9)+18;fill(bg);c.roundRect(x,y-5,w,19,9,fill=1,stroke=0);t(x+9,y,s,9,'B',tc);return w
def mark(dest,title):c.bookmarkPage(dest);c.addOutlineEntry(title,dest)
def foot(pg):
 rect(20,32,380,0.6,ink);t(20,15,'FORK, SPOON & GO!',8,'B');t(298,15,'MENU  /  '+str(pg).zfill(2),8,'B');c.linkRect('menu','menu',(280,3,410,32),relative=0,thickness=0)
def slip(x,y,num,col):
 fill(col);c.circle(x,y,8.8,fill=1,stroke=0);t(x-3.5,y-3.5,str(num),10,'B',cream)
def bg(col):rect(0,0,W,H,col)
bg('#F7C54F');mark('cover','Fork, Spoon & Go!');check(668,red)
t(23,631,'THE WEEKNIGHT COOKBOOK',11,'B');t(20,554,'Fork, Spoon',54,'H');t(22,483,'& Go!',70,'H')
badge(25,448,'8 RECIPES',ink);badge(109,448,'3 COOKING DAYS',ink)
dish(6,-18,220,242,213,-12);dish(0,213,206,190,235,13);dish(8,11,93,135,93,-25);dish(1,133,80,223,125,9)
rect(0,0,W,67,ink);t(22,29,'A week of home cooking for one',15,'B',cream);c.linkRect('open menu','menu',(0,0,W,H),thickness=0);c.showPage()
bg(cream);mark('menu','Menu for the week');check(678,green);t(20,638,'The weekly menu',31,'H');t(23,610,'About 2,600 kcal a day  /  Tap a recipe to open it.',11,'S')
def entry(i,x,y,title,when):
 dish(i,x,y,53,52);t(x+63,y+31,when,9,'B',green);t(x+63,y+10,title,15,'B')
 c.linkRect(title,'r'+str(i),(x,y,x+368,y+52),thickness=0)
entry(0,24,545,'Overnight oats','10 AM   /   EVERY DAY');entry(1,24,489,'Small chicken wrap','7 PM   /   EVERY DAY')
dish(8,29,447,42,39);t(87,460,'Before the gym  •  1 medium banana',12,'B')
for j,(span,l,d) in enumerate([('SUN + MON',2,3),('TUE + WED',4,5),('THU + FRI + SAT',6,7)]):
 yy=317-j*112
 rect(20,yy+72,380,24,pal[l][0]);t(29,yy+79,span,10,'B',pal[l][1])
 for k,i in enumerate((l,d)):
  x=23+190*k;t(x,yy+53,('3 PM LUNCH','AFTER-GYM DINNER')[k],9,'B');dish(i,x,yy-3,48,48)
  titles=['','','Shawarma rice bowl','Chicken pita plate','Kofta & potatoes','Kofta pita plate','Chicken pasta','Tuna wraps']
  lines(x+53,yy+22,titles[i],128,12,15,'B');c.linkRect(titles[i],'r'+str(i),(x,yy-3,x+183,yy+65),thickness=0)
t(24,51,'Batch quantities & prep days  →  Page 11',12,'B',green);c.linkRect('Prep','prep',(20,42,350,68),thickness=0);foot(2);c.showPage()
tree=ast.parse(Path('tmp/pdfs/cards.py').read_text())
rs=[list(map(ast.literal_eval,e.value.args)) for e in tree.body if isinstance(e,ast.Expr) and isinstance(e.value,ast.Call) and isinstance(e.value.func,ast.Name) and e.value.func.id=='card']
titlelines=[['Overnight','oats'],['Chicken','snack wrap'],['Shawarma','rice bowl'],['Chicken','pita plate'],['Kofta &','potatoes'],['Kofta','pita plate'],['Tomato','chicken pasta'],['Tuna','wraps']]
ss=[
['Stir the oats, yogurt and peanut butter in a jar. Add water a spoonful at a time until easy to stir.','Scatter the berries on top. Cover and refrigerate overnight. Eat cold the next morning.'],
['Stir the garlic into the yogurt. Pat the lettuce and cucumber dry.','Spread the yogurt on the tortilla. Add chicken, lettuce and cucumber. Tuck in the sides and roll. Refrigerate until 7 pm.'],
['Start the rice in the rice cooker. Use the water amount printed on the packet.','Cut chicken into strips. Toss with paprika, cumin, garlic and half the oil. Air-fry in one layer at 190°C for 12–16 min, turning halfway, until it reaches 74°C.','Steam the vegetables until tender and add the remaining oil. Box with rice and chicken. Pack the yogurt, lemon and pinch of garlic as a dip.'],
['Reheat the cooked shawarma chicken to 74°C. Warm the pita if you like.','Dice the cucumber and tomato and dress with olive oil. Mix the yogurt, lemon and garlic.','Spread hummus over the pita and add chicken. Serve with the salad and garlic yogurt.'],
['Cut potatoes into 2 cm cubes. Toss with oil and air-fry at 200°C for 18–25 min, shaking twice, until tender.','Mix beef with onion and spices. Shape into short logs. Air-fry in one layer at 190°C for 10–15 min, turning halfway, until the center reaches 71°C.','Pack the kofta and potatoes together. Chop the cucumber and tomato. Pack the salad and yogurt separately.'],
['Reheat the kofta to 74°C. Slice it lengthwise to fit the pita.','Chop cucumber and tomato and toss with olive oil.','Spread hummus inside the pita, add kofta and spoon in some yogurt. Serve the rest with the salad.'],
['Boil pasta following its packet. Reserve a splash of cooking water, then drain.','Cut chicken into strips. Toss with garlic, oregano and half the oil. Air-fry at 190°C for 12–16 min, turning halfway, until the center reaches 74°C.','Warm sauce in the pasta pot. Add chicken, pasta, Parmesan and remaining oil. Loosen with a splash of pasta water.'],
['Drain the tuna well. Flake it with a fork and mix with yogurt, oil and lemon.','Spread hummus over both tortillas. Divide the tuna and cucumber between them.','Tuck in the sides and roll. If prepping ahead, keep the tortillas dry and fill them just before dinner.']]
def sheet(pattern,n):
 im=Image.open(glob.glob(pattern)[0]).convert('RGB');out=[]
 for iy in range(n):
  for ix in range(n):
   l,t0,r,b=[int(round(v)) for v in (ix*im.width/n,iy*im.height/n,(ix+1)*im.width/n,(iy+1)*im.height/n)]
   cell=im.crop((l,t0,r,b));a=np.array(cell);masks,_=label(a.min(axis=2)>228);edge=np.unique(np.r_[masks[0],masks[-1],masks[:,0],masks[:,-1]])
   cell.putalpha(Image.fromarray(np.uint8(~np.isin(masks,edge[edge>0]))*255));out.append(cell.crop(cell.getbbox()))
 return out
ings=sheet('generated_images/exec-f1*.png',5);acts=sheet('generated_images/exec-4d*.png',4)
def art(im,x,y,w,h):
 scale=min(w/im.width,h/im.height);ww=im.width*scale;hh=im.height*scale;c.drawImage(ImageReader(im),x+(w-ww)/2,y+(h-hh)/2,ww,hh,mask='auto')
# Short names and explicit unit weights make the illustrated shopping trays readable.
data=[
([(1,'Greek yogurt','250 g, low-fat'),(0,'Rolled oats','45 g'),(2,'Peanut butter','15 g'),(3,'Mixed berries','100 g'),(4,'Water','1–2 tbsp')], '',
 [(0,'Stir','Mix oats, yogurt and peanut butter in a jar. Add water until easy to stir.'),(1,'Top','Spoon the berries over the oats.'),(2,'Chill overnight','Seal the jar and refrigerate. Eat it cold in the morning.')]),
([(5,'Flour tortilla','1 small · 25 g'),(7,'Cooked chicken','60 g'),(1,'Plain yogurt','15 g'),(8,'Cucumber','20 g'),(9,'Lettuce','1 small leaf'),(13,'Garlic powder','1 pinch')],'',
 [(3,'Spread','Stir the garlic into the yogurt. Spread it over the tortilla.'),(4,'Fill & roll','Pat the greens dry. Add sliced chicken, cucumber sticks and lettuce. Fold the sides in and roll.'),(-2,'Pack cold','Refrigerate the wrap at work until 7 pm. Take a separate banana for before the gym.')]),
([(6,'Chicken breast','280 g raw'),(10,'Basmati rice','100 g dry'),(11,'Mixed veg','200 g'),(12,'Olive oil','20 g'),(1,'Plain yogurt','120 g'),(14,'Lemon juice','1 tsp'),(13,'Spices','See below')],'½ tsp paprika, ¼ tsp each cumin and garlic powder, plus a pinch of garlic for the dip.',
 [(5,'Start the rice','Cook with the water on the packet. Aim for 300 g cooked rice.'),(6,'Air-fry chicken','Toss strips with spices and half the oil. Cook in one layer at 190°C for 12–16 min. Turn halfway. Center: 74°C.'),(7,'Steam & pack','Steam veg until tender. Add the remaining oil. Pack with rice and 210 g cooked chicken. Mix yogurt, lemon and garlic for dipping.')]),
([(7,'Shawarma chicken','150 g cooked'),(15,'Pita','90 g'),(16,'Hummus','80 g'),(8,'Cucumber','75 g'),(17,'Tomato','75 g'),(1,'Plain yogurt','100 g'),(12,'Olive oil','5 g'),(14,'Lemon juice','1 tsp')],'For the yogurt dip, add a pinch of garlic powder.',
 [(8,'Warm','Reheat the batch chicken to 74°C. Warm the pita if you like.'),(9,'Chop & dress','Dice cucumber and tomato. Add the oil. Stir lemon and garlic into the yogurt.'),(15,'Fill the pita','Spread with hummus and add chicken. Serve the salad and garlic yogurt alongside.')]),
([(18,'Lean ground beef','285 g raw'),(19,'Grated onion','1 tbsp, squeezed'),(20,'Potatoes','480 g raw'),(12,'Olive oil','15 g'),(8,'Cucumber','75 g'),(17,'Tomato','75 g'),(1,'Plain yogurt','150 g'),(13,'Spices','See below')],'½ tsp cumin, ¼ tsp paprika and a pinch of black pepper.',
 [(11,'Roast potatoes','Cut into 2 cm cubes and toss with oil. Air-fry at 200°C for 18–25 min. Shake twice.'),(10,'Shape & air-fry','Mix beef, onion and spices. Shape into logs. Air-fry in one layer at 190°C for 10–15 min. Turn halfway. Center: 71°C.'),(9,'Pack','Box 220 g cooked kofta with 400 g cooked potatoes. Chop the salad and pack it and the yogurt separately.')]),
([(21,'Batch kofta','140 g cooked'),(15,'Pita','80 g'),(16,'Hummus','60 g'),(8,'Cucumber','75 g'),(17,'Tomato','75 g'),(1,'Plain yogurt','100 g'),(12,'Olive oil','5 g')],'',
 [(8,'Warm','Reheat the kofta to 74°C. Slice lengthwise to fit inside the pita.'),(9,'Chop','Dice cucumber and tomato. Toss with the olive oil.'),(15,'Fill the pita','Spread hummus inside. Add kofta and a spoonful of yogurt. Serve the rest with the salad.')]),
([(6,'Chicken breast','270 g raw'),(22,'Pasta','125 g dry'),(23,'Tomato sauce','150 g'),(12,'Olive oil','10 g'),(24,'Parmesan','15 g, grated'),(13,'Seasoning','See below')],'¼ tsp garlic powder and ¼ tsp dried oregano.',
 [(12,'Boil pasta','Cook following the packet. Save a splash of cooking water and drain. Aim for 300 g cooked pasta.'),(6,'Air-fry chicken','Toss strips with seasonings and half the oil. Air-fry in one layer at 190°C for 12–16 min. Turn halfway. Center: 74°C.'),(13,'Toss','Warm the sauce. Add pasta, 200 g cooked chicken, Parmesan and remaining oil. Loosen with pasta water.')]),
([(25,'Light tuna','150 g drained'),(5,'Tortillas','2 medium'),(16,'Hummus','80 g'),(1,'Plain yogurt','100 g'),(8,'Cucumber','100 g'),(12,'Olive oil','10 g'),(14,'Lemon juice','1 tsp')],'Choose tuna in water and tortillas around 150 kcal each.',
 [(14,'Flake','Drain the tuna. Flake with a fork and mix with yogurt, oil and lemon.'),(15,'Fill','Spread hummus on both tortillas. Slice cucumber into sticks. Divide tuna and cucumber between wraps.'),(4,'Roll','Tuck the sides in and roll. For meal prep, keep tortillas dry and fill just before dinner.')])]
for i,(num,tag,title,sub,items,_) in enumerate(rs):
 col,ac=pal[i];bg(cream);mark('r'+str(i),title)
 rect(0,584,420,106,col);check(681,ac)
 t(17,658,tag.upper(),9,'B',ac)
 hdr=['Overnight oats','Chicken snack wrap','Shawarma rice bowl','Chicken pita plate','Kofta & potatoes','Kofta pita plate','Tomato chicken pasta','Tuna wraps'][i]
 t(16,621,hdr,22 if len(hdr)>18 else 25,'H');badge(18,596,sub.split(' / ')[0].replace('About ','~'),ac)
 dish(i,316,588,95,83)
 parts,note,steps=data[i];t(17,555,'What you need',20,'H',ac);t(305,558,'1 SERVING',9,'B',ac)
 for j,(idx,name,amount) in enumerate(parts):
  row,slot=divmod(j,4);x=15+slot*98;y=464-row*86
  fill('#FFFFFF');c.roundRect(x,y,94,81,8,fill=1,stroke=0)
  art(ings[idx] if idx<25 else acts[14],x+19,y+33,55,44)
  for off,labeltxt,f,sz in [(19,name,'B',10),(6,amount,'S',10.1)]:
   while pdfmetrics.stringWidth(labeltxt,f,sz)>90:sz-=0.25
   t(x+(94-pdfmetrics.stringWidth(labeltxt,f,sz))/2,y+off,labeltxt,sz,f)
 if note:lines(18,362,note,382,10.1,12.2,'S',ac)
 t(17,320,'How to make it',20,'H',ac)
 for j,(idx,head,body) in enumerate(steps):
  y=225-j*90
  rect(15,y,390,84,'#FFFFFF')
  art(acts[idx] if idx>=0 else imgs[1],18,y+5,77,71)
  slip(107,y+68,j+1,ac);t(120,y+63,head,14,'B',ac)
  after=lines(102,y+44,body,295,11.6,14.3)
  assert after>=y-10,(title,body,after,y)
 foot(num+1);c.showPage()
bg(cream);mark('prep','Three batch-cooking sessions');check(678,red);t(20,634,'Batch-cook the week',29,'H');t(22,605,'Portion weights below are cooked weights.',11)
for j,(day,head,img,body) in enumerate([
('SATURDAY','Chicken + rice',2,'Cook 1,140 g chicken (about 1.5–1.6 kg raw). Pack 2 × 210 g for rice bowls, 2 × 150 g for pita dinners and 7 × 60 g for snack wraps. Divide 600 g cooked rice between the two bowls. Freeze later portions.'),
('MONDAY','Kofta + potatoes',4,'Cook 720 g kofta and 800 g potatoes. Pack 2 × 220 g kofta with 400 g potatoes each. Set aside 2 × 140 g kofta for pita dinners.'),
('WEDNESDAY','Tomato chicken pasta',6,'Triple the pasta recipe. Divide 600 g cooked chicken and 900 g cooked pasta between three boxes with sauce. Freeze Saturday’s box and thaw it in the fridge on Friday. Roll tuna wraps at dinner.')]):
 y=580-132*j;rect(18,y-119,384,124,pal[img][0]);dish(img,22,y-94,77,78);t(109,y-13,day,9,'B',pal[img][1]);t(109,y-37,head,17,'H');lines(109,y-56,body,283,10.4,13.3)
t(22,161,'Chill, freeze, reheat',18,'H',green);lines(22,137,'Chill rice within 1 hour. Freeze any rice you will eat more than 24 hours later. Refrigerate other cooked leftovers within 2 hours and use within 3–4 days or freeze. Reheat hot meals to 74°C. Keep yogurt and salad cold.',372,11.4,16)
t(22,54,'Storage guidance from USDA FSIS and the UK Food Standards Agency.',8,'S');foot(11);c.showPage();c.save()
