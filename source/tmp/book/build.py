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
for i,(num,tag,title,sub,items,_) in enumerate(rs):
 col,ac=pal[i];bg(cream);mark('r'+str(i),title);rect(0,482,420,208,col);check(678,ac)
 t(19,648,tag.upper(),9,'B',ac)
 for j,s in enumerate(titlelines[i]):t(17,596-j*33,s,30 if len(s)<10 else 25,'H')
 dish(i,218,497,190,149,(-5 if i%2 else 3))
 kcal=sub.split(' / ')[0].replace('About ','~');badge(20,505,kcal,ac)
 t(20,461,'Gather',21,'H',ac);t(125,462,'FOR ONE SERVING',9,'B')
 y=436
 for item in items:
  item=item.replace('(same batch as p. 4)','(from the rice bowl batch)').replace('(same batch as p. 6)','(from the potato & kofta batch)')
  fill(ac);c.circle(24,y+4,2.3,stroke=0,fill=1);y=lines(36,y,item,366,13.1,17)-4.5
 y-=12;t(20,y,'Make it',21,'H',ac);y-=24
 for j,s in enumerate(ss[i],1):slip(28,y+4,j,ac);y=lines(44,y,s,355,13,18)-8
 assert y>32,(title,y)
 foot(num+1);c.showPage()
bg(cream);mark('prep','Three batch-cooking sessions');check(678,red);t(20,634,'Batch-cook the week',29,'H');t(22,605,'Portion weights below are cooked weights.',11)
for j,(day,head,img,body) in enumerate([
('SATURDAY','Chicken + rice',2,'Cook 1,140 g chicken (about 1.5–1.6 kg raw). Pack 2 × 210 g for rice bowls, 2 × 150 g for pita dinners and 7 × 60 g for snack wraps. Divide 600 g cooked rice between the two bowls. Freeze later portions.'),
('MONDAY','Kofta + potatoes',4,'Cook 720 g kofta and 800 g potatoes. Pack 2 × 220 g kofta with 400 g potatoes each. Set aside 2 × 140 g kofta for pita dinners.'),
('WEDNESDAY','Tomato chicken pasta',6,'Triple the pasta recipe. Divide 600 g cooked chicken and 900 g cooked pasta between three boxes with sauce. Freeze Saturday’s box and thaw it in the fridge on Friday. Roll tuna wraps at dinner.')]):
 y=580-132*j;rect(18,y-119,384,124,pal[img][0]);dish(img,22,y-94,77,78);t(109,y-13,day,9,'B',pal[img][1]);t(109,y-37,head,17,'H');lines(109,y-56,body,283,10.4,13.3)
t(22,161,'Chill, freeze, reheat',18,'H',green);lines(22,137,'Chill rice within 1 hour. Freeze any rice you will eat more than 24 hours later. Refrigerate other cooked leftovers within 2 hours and use within 3–4 days or freeze. Reheat hot meals to 74°C. Keep yogurt and salad cold.',372,11.4,16)
t(22,54,'Storage guidance from USDA FSIS and the UK Food Standards Agency.',8,'S');foot(11);c.showPage();c.save()
