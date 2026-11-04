from recipes import *
from pathlib import Path
import glob,math
from PIL import Image,ImageChops
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit,ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
D=Path('tmp/finalbook');W,H=450,730
for ff,fil in [('S','DejaVuSans'),('B','DejaVuSans-Bold'),('H','DejaVuSerif-Bold')]:pdfmetrics.registerFont(TTFont(ff,'/usr/share/fonts/truetype/dejavu/'+fil+'.ttf'))
def load(prefix):return Image.open(glob.glob('generated_images/exec-'+prefix+'*.png')[0]).convert('RGB')
def grid(prefix,n,m):
 im=load(prefix);w,h=im.size;return [im.crop((round((j%n)*w/n),round((j//n)*h/m),round((j%n+1)*w/n),round((j//n+1)*h/m))) for j in range(n*m)]
a=grid('f1c8',5,5);b=grid('f315',4,4);extra=grid('4d4d',3,3);act=grid('4db4',4,4);bird=grid('6016',2,2);new=grid('f05d',4,3)+grid('899e',4,3)+[bird[1]]
picker=load('ebe9')
def pick(box):return picker.crop(box)
icons={'C':a[7],'B':a[18],'T':act[14],'R':a[10],'P':a[22],'X':a[5],'O':a[0],'U':a[8],'L':a[9],'A':b[11],'E':pick((20,787,317,945)),'S':b[9],'H':a[16],'G':a[1],'Z':a[1],'J':a[14],'I':a[12],'M':pick((380,1338,635,1455)),'Y':b[12],'N':grid('c99',3,3)[8],'K':extra[6],'D':b[10],'V':bird[3],'W':load('3139').crop((16,1082,335,1320))}
actions={'banana':icons['N'],'mix':act[0],'chill':act[2],'fold':act[4],'pan':act[13],'slice':act[9],'spread':act[3],'bowl':None,'fill':None,'shape':act[10],'air':act[6],'flake':act[14],'mash':icons['W'],'bird':bird[0],'carve':bird[3]}
# Avoid pictures of off-menu foods in generic action art. Use the actual ingredient or dish.
actions['slice']=icons['U'];actions['pan']=None;actions['mix']=None;actions['spread']=icons['H'];actions['mash']=None;actions['chill']=new[0]
burg=grid('e1f6',2,2);new.append(burg[0]);icons['Q']=burg[1];actions.update({'press':burg[2],'burgerpan':burg[3],'burger':burg[0]})
PAPER='#FFFAEE';INK='#332135';GREEN='#215E4C';GOLD='#F6CA55';WHITE='#FFFFFF';palette=[('#F7DACC','#92472D'),('#ECE4B9','#626025'),('#D5EBD8','#24634F'),('#F1D6A8','#865122'),('#DAE9F2','#2B5D75')]
c=Canvas('output/pdf/Weekly_Meal_Cards.pdf',pagesize=(W,H));c.setTitle('Fork, Spoon & Go! | Final illustrated cookbook')
def rect(x,y,w,h,color,r=0):
 c.setFillColor(HexColor(color));c.roundRect(x,y,w,h,r,fill=1,stroke=0)
def t(x,y,s,size=12,font='S',color=INK):
 c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,y,s)
def lines(x,y,s,w,sz,lead,font='S',color=INK):
 for line in simpleSplit(s,font,sz,w):t(x,y,line,sz,font,color);y-=lead
 return y
def image(im,x,y,w,h):
 scale=min(w/im.width,h/im.height);iw=im.width*scale;ih=im.height*scale;c.drawImage(ImageReader(im),x+(w-iw)/2,y+(h-ih)/2,iw,ih)
def page(dest,title,ac=GREEN):
 rect(0,0,W,H,PAPER);c.bookmarkPage(dest);c.addOutlineEntry(title,dest)
 for i in range(30):
  rect(i*15,720+(i%2)*5,15,5,ac)
def link(text,x,y,w,dest,ac=GREEN):
 rect(x,y,w,25,ac,6);t(x+9,y+8,text,9.6,'B',WHITE);c.linkRect(text,dest,(x,y,x+w,y+25),thickness=0)
def foot(n,menu='menu0'):
 rect(17,26,416,.6,INK);t(17,11,'FORK, SPOON & GO!',8,'B');t(333,11,'MENU    /    '+str(n),9,'B');c.linkRect('Menu',menu,(313,2,445,27),thickness=0);c.showPage()
def cal(q):return int(5*round(sum(F[k][1]*g/100 for k,g in q)/5))
assert all(cal(m[1])<700 for m in meals)
def group(i):
 if i<2:return ('BREAKFAST',0)
 if i in (2,25):return ('7 PM SNACK',1)
 if i<8 or i==24:return ('CHICKEN',2)
 if i<14:return ('BEEF',3)
 if i<18:return ('TUNA',4)
 return ('BEANS',1)
order=[0,1,2,25,24,*range(3,24)]
def menufor(i):return 'menu0' if order.index(i)<13 else 'menu1'
page('cover','Fork, Spoon & Go!');rect(0,0,W,H,GOLD);t(22,677,'THE BEGINNER COOKBOOK',12,'B');t(18,593,'Fork, Spoon',53,'H');t(20,523,'& Go!',67,'H');t(23,485,'26 recipes for one',20,'B')
image(bird[0],28,190,258,240);image(new[5],270,266,150,135);image(new[0],272,125,112,125)
rect(0,0,W,106,INK);link('Choose a recipe  →',20,51,201,'menu0');link('Roast a whole chicken  →',230,51,200,'roast');t(22,22,'Breakfast, wraps, bowls and a Sunday roast.',11,'S',WHITE);c.showPage()
for j,ids in enumerate([order[:13],order[13:]]):
 page('menu'+str(j),'Choose a meal '+str(j+1));t(18,677,'Choose a meal',29,'H');t(19,653,'Tap a row to open its picture card. Calories are per serving.',10.7)
 for n,i in enumerate(ids):
  y=605-n*40;m=meals[i];lab,p=group(i);cl,ac=palette[p];rect(15,y,420,37,cl,4);image(new[i],18,y+1,44,35);t(68,y+16,m[0],11.5,'B');t(68,y+4,lab+'   /   ~'+str(cal(m[1]))+' kcal',8,'S',ac);c.linkRect(m[0],'r'+str(i),(15,y,435,y+37),thickness=0)
 link('More meals  →' if j==0 else 'First menu  →',16,50,119,'menu'+str(1-j));link('Kitchen basics  →',142,50,130,'start');link('Bulk cooking  →',278,50,156,'batch');foot(j+2)
page('start','Before your first meal');t(18,674,'Before you start',28,'H')
blocks=[('01','Pick one card','Each card makes one meal. The time beside the title starts with the ingredients in the pictured state. “Cooked” means ready to eat. “Raw” means it still needs heat.',new[3]),('02','Measure with a scale','Put a bowl on the scale. Press zero. Add one food until the display matches its grams. Press zero again before adding the next food.',a[0]),('03','Choose ready ingredients','Plain cooked chicken, cooked rice or pasta, canned tuna in water, canned beans and prepared garlic yogurt are shortcuts. Drain tuna and beans before weighing. Rinse canned beans.',b[8]),('04','Check the middle','Push a clean food thermometer into the thickest part. Cook raw chicken to 74°C and raw ground beef to 71°C. Reheat chilled hot meals to 74°C throughout. Wash hands and tools after raw meat.',bird[2]),('05','Follow your own clock','Try breakfast at 10 am, lunch at 3 pm and the little chicken wrap or beef burger at 7 pm. Keep the banana for before training. Choose a dinner for after the gym. These cards give individual servings.',new[2])]
for j,(num,head,body,im) in enumerate(blocks):
 y=551-j*110;rect(15,y,420,100,WHITE,6);image(im,22,y+15,70,68);t(101,y+77,num+'   '+head,13,'B',GREEN);lines(101,y+57,body,323,12,16)
t(18,74,'Calorie estimates include the listed sauces and oils.',11,'B');lines(18,55,'Use the measured portions and check your product labels for brand differences.',409,10,13);foot(4)
for n,i in enumerate(order):
 name,q,tm,tool,steps=meals[i];lab,p=group(i);cl,ac=palette[p];page('r'+str(i),name,ac);rect(0,566,W,151,cl)
 t(17,694,lab+'    /    ONE SERVING',9.5,'B',ac);lines(17,653,name,255,24,28,'H');t(17,582,'~'+str(cal(q))+' kcal   •   '+tm,11.3,'B',ac);image(new[i],282,574,156,133)
 t(17,537,'What you need',19,'H',ac)
 for k,(f,g) in enumerate(q):
  x=15+105*(k%4);y=449-74*(k//4);rect(x,y,102,68,WHITE,6);image(icons[f],x+31,y+28,41,38)
  lab2=F[f][0];size=9.8
  while pdfmetrics.stringWidth(lab2,'B',size)>99:size-=.2
  t(x+(102-pdfmetrics.stringWidth(lab2,'B',size))/2,y+16,lab2,size,'B');gs=str(g)+' g';t(x+(102-pdfmetrics.stringWidth(gs,'S',10))/2,y+3,gs,10)
 t(18,349,'Make it',20,'H',ac);t(118,350,tool,10,'S',ac)
 for j,(hd,body,key) in enumerate(steps):
  top=331-j*93;rect(15,top-88,420,86,WHITE,6);im=actions[key] or (icons[q[0][0]] if j!=2 else new[i]);image(im,20,top-76,58,58)
  t(85,top-21,str(j+1)+'   '+hd,14,'B',ac)
  size=12.0
  while len(simpleSplit(body,'S',size,338))*size*1.22>54:size-=.2
  lines(86,top-40,body,337,size,size*1.22)
 if i==24:link('Whole bird oven guide  →',17,31,220,'roast',ac)
 foot(5+n,menufor(i))
page('batch','Bulk cooking | start here');t(18,673,'Cook for later',30,'H');t(19,641,'Everything in this section is for your prep days.',12)
for j,(head,txt,im,dest) in enumerate([
 ('1   Choose your meals','Pick one recipe for three meals and another for four. Decide which portions you will eat or freeze.',new[24],'quant0'),
 ('2   Cook the shared bases','Start rice or pasta first. Cook chicken or beef at the same time. Buy cooked beans, hummus and yogurt.',new[6],'bases'),
 ('3   Try the whole bird','One roast gives you breast, thigh and drumstick meat. Weigh the edible meat after cooking.',bird[0],'roast'),
 ('4   Fill your boxes','Label the cooking date. Keep wraps, cold dips and salad separate from the hot ingredients.',bird[3],'boxes')]):
 y=490-j*108;rect(15,y,420,98,WHITE,6);image(im,22,y+12,78,73);t(111,y+75,head,14,'B',GREEN);lines(111,y+53,txt,309,12,16);c.linkRect(head,dest,(15,y,435,y+98),thickness=0)
link('3- and 4-portion amounts  →',18,86,258,'quant0');link('Your prep days  →',284,86,148,'week');foot(31)
page('bases','Rice, pasta & meat');t(18,675,'Cook the shared bases',24,'H')
blocks=[('Rice cooker','Use the amount of water on your rice packet or the matching fill line for your cooker. Close the lid, press Cook and wait for Warm. Rest covered for 5 minutes. Fluff with a fork, then weigh the cooked portions. Allow about 25–40 minutes.',act[5]),('Pasta pot','Bring a pot of water to a rolling boil. Add egg-free pasta and stir. Start the packet timer. Taste one cooled piece. When tender, drain through a colander and weigh the cooked portions. Allow about 15–25 minutes including heating the water.',icons['P']),('Air-fryer chicken','Cut chicken into even strips about 2 cm thick. Spread in one layer. Air-fry at 190°C for about 12–16 minutes per load, turning halfway. The thickest strip must reach 74°C. Add 2-minute bursts if needed. Plain ready-cooked chicken also works.',act[6]),('Lean beef','For crumbs, break raw beef apart in a nonstick pan over medium heat. For kofta, shape into small logs and follow the kofta card. Check ground beef reaches 71°C. Allow 10–15 minutes per pan or fryer load. Use oil from the selected recipe.',act[10])]
for j,(hd,txt,im) in enumerate(blocks):
 y=504-j*134;rect(15,y,420,125,WHITE,6);image(im,22,y+30,73,66);t(103,y+102,hd,15,'B',GREEN);lines(103,y+80,txt,322,12,16)
foot(32)
page('roast','Whole chicken | oven guide');t(18,674,'Roast a whole chicken',24,'H');t(19,645,'1 unstuffed bird, 1.4–1.8 kg   •   Oven at 177°C / 350°F',11,'B')
for j,(hd,txt,im) in enumerate([
 ('Set up','Allow about 1¾–2 hours including heating and resting. Heat the oven to 177°C (350°F). Place a rack in a roasting pan. Remove packaging and any giblet bag from inside the bird.',bird[0]),
 ('Place in the oven','Pat dry with paper towel. Put the whole chicken breast-side up on the rack. Leave the cavity empty. Wash hands and clean the work surface. Roast for about 75–90 minutes.',bird[0]),
 ('Check three spots','Start checking at 75 minutes. Insert a thermometer in the thickest breast, inner thigh and inner wing, away from bone. All must reach 74°C. If any spot is lower, roast longer and check again.',bird[2]),
 ('Rest, carve and weigh','Rest for 10 minutes. Pull a leg outward and cut through its joint. Slice breast meat down each side of the breastbone. Remove bones. Weigh your meat and any skin before plating or boxing.',bird[3])]):
 y=504-j*129;rect(15,y,420,120,WHITE,6);image(im,19,y+18,91,83);t(117,y+97,str(j+1)+'   '+hd,14,'B',GREEN);lines(117,y+76,txt,307,11.8,15.6)
lines(18,84,'Ready-made option: buy a plain whole rotisserie chicken. Weigh the same edible serving and check the label for added fats or sauces.',410,11.5,15);foot(33)
page('week','Your three prep days');t(18,675,'Three prep days',26,'H');t(18,645,'A suggested week. Cook only the dishes you choose.',11)
for j,(hd,body,im) in enumerate([
 ('Saturday  /  whole chicken + rice','Start the oven, then the rice cooker. While the bird roasts, portion cold dips and wash cucumber. After carving, weigh meat for a roast dinner, pepper rice bowls and snack wraps. Freeze later portions. A bird’s yield varies.',bird[0]),
 ('Monday  /  beef + pasta','Boil pasta and cook beef in a pan or shape kofta. Set aside 75 g raw beef for each 7 pm burger swap. Choose a beef pasta dish for one day and lettuce cups or kofta rice for another. Allow roughly 35–60 minutes for 3–4 servings, depending on pan space.',new[9]),
 ('Wednesday  /  beans + tuna','Drain canned beans, corn and tuna. Mix one cold salad. Roast peppers or cook chickpea patties if you want another hot option. Allow about 20–45 minutes depending on your choices.',new[22])]):
 y=497-j*139;rect(15,y,420,129,WHITE,6);image(im,21,y+28,78,73);t(110,y+105,hd,13.8,'B',GREEN);lines(110,y+83,body,316,12,16)
t(18,183,'Example: roast dinner + snack wrap',16,'H');lines(18,155,'For 3 days, portion 450 g roast meat for dinners and 180 g chicken for wraps. For 4 days, use 600 g and 240 g. Weigh after carving. Use skinless chicken for the snack estimate.',408,12,17)
foot(34)
page('boxes','Cool, store and reheat');t(18,674,'Box it up',29,'H')
for j,(hd,body,im) in enumerate([
 ('Cool promptly','Divide hot food into shallow boxes and refrigerate promptly, within 2 hours (1 hour if hotter than 32°C). Keep the fridge at 4°C or colder.',bird[3]),
 ('Freeze later rice portions','Cool cooked rice within 1 hour. Refrigerate only what you will eat within 24 hours. Freeze the rest promptly. Thaw in the fridge and reheat once, until steaming throughout.',act[5]),
 ('Label your boxes','Write the cooking date on each box. Most cooked leftovers keep 3–4 days in the fridge. Freeze later portions early. Follow shorter use-by dates on store-bought food.',b[15]),
 ('Reheat one serving','Use a microwave-safe dish. Cover loosely. Heat, stir and check several spots. Hot leftovers must reach 74°C. Add cold lettuce, cucumber and yogurt afterward.',act[8])]):
 y=509-j*118;rect(15,y,420,109,WHITE,6);image(im,21,y+20,74,70);t(108,y+86,hd,14,'B',GREEN);lines(108,y+65,body,318,12,16)
lines(18,119,'Calories are estimates from typical ingredient values. Tortillas, hummus, yogurt dressings and roast chicken skin vary. Use your product labels and weigh the listed portions.',412,10.5,14)
t(18,62,'Safety guidance: FoodSafety.gov, USDA FSIS and the UK Food Standards Agency.',8.7);foot(35)
# Final quantities only. Three cards per scaling page. Links point to the one-serving cards.
for s0 in range(0,len(order),3):
 p=s0//3;page('quant'+str(p),'Portion planner '+str(p+1));t(18,675,'Portion planner',25,'H');t(18,644,'Weigh each ingredient once, then split evenly into boxes.',11)
 for j,i in enumerate(order[s0:s0+3]):
  name,q,tm,tool,steps=meals[i];base=619-j*185;rect(15,base-173,420,171,WHITE,6)
  t(22,base-23,name,13,'B',GREEN);c.linkRect(name,'r'+str(i),(16,base-32,435,base-2),thickness=0)
  t(23,base-45,'INGREDIENT',8.6,'B');t(239,base-45,'3 PORTIONS',8.6,'B');t(336,base-45,'4 PORTIONS',8.6,'B')
  for k,(f,g) in enumerate(q):
   yy=base-64-k*15;t(23,yy,F[f][0],10.4);t(241,yy,str(3*g)+' g',10.4,'B');t(339,yy,str(4*g)+' g',10.4,'B')
 if s0+3<len(order):link('Next amounts  →',18,44,150,'quant'+str(p+1))
 link('Bulk guide  →',276,44,155,'batch');foot(36+p)
c.save()
print('recipes',len(meals),'calories',[(m[0],cal(m[1])) for m in meals])
