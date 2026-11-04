from pathlib import Path
import json,io
from PIL import ImageOps
import numpy as np
ed=Path('tmp/finalbook/edition.py').read_text()
exec(ed[:ed.index('cover();menu();starter()')])
from nutrientcalc import cal,nutr
from reportlab.pdfbase import pdfmetrics
# Rebind text primitives so all inherited card elements use the same rounded family.
for alias,fil in [('CuteDisplay','Display'),('CuteBold','Bold'),('CuteBody','Regular')]:
 pdfmetrics.registerFont(TTFont(alias,'tmp/cutebook/'+fil+'.ttf'))
for alias,fil in [('S','CuteBody'),('B','CuteBold'),('H','CuteDisplay')]:
 pdfmetrics._fonts[alias]=pdfmetrics.getFont(fil)
PAPER='#FFF9F2';INK='#49333B';BLUE='#69516F';RED='#9A4B59';WHITE='#FFFFFF'
colors=[('#FFE9D2','#884C43'),('#DAEEE3','#376452'),('#FFDFE1','#8F4556'),('#FFF0BC','#755326'),('#E9E3FA','#5A4B79')]
H=890;c.setPageSize((W,H));c.setTitle('Fork, Spoon & Go! | The little lunchbox cookbook')
ASSETS=json.loads(Path('tmp/cutebook/assets.json').read_text())
def pieces(key,cols,rows):
 im=load(ASSETS[key]); arr=np.asarray(im);mask=np.min(arr,axis=2)<200
 def edges(axis,count):
  profile=mask.mean(axis=axis);s=len(profile);out=[0]
  for n in range(1,count):
   mid=s*n/count;r=int(s/count*.12);j=int(mid);ss=profile[j-r:j+r+1]
   cand=np.where(ss<=ss.min()+.008)[0];idx=cand[np.argmin(abs(cand-r))]
   out.append(j-r+int(idx))
  return out+[s]
 xs,ys=edges(0,cols),edges(1,rows);out=[]
 for v in range(rows):
  for u in range(cols):
   tile=im.crop((xs[u],ys[v],xs[u+1],ys[v+1]))
   a=np.asarray(tile);m=np.min(a,axis=2)<205;yy,xx=np.where(m)
   if len(xx):tile=tile.crop((max(0,int(xx.min())-5),max(0,int(yy.min())-5),min(tile.width,int(xx.max())+6),min(tile.height,int(yy.max())+6)))
   out.append(tile)
 return out
new=pieces('a',3,3)+pieces('b',3,3)+pieces('c',3,3)+pieces('d',3,2)
art=pieces('act',4,4);ingredients=pieces('ing',4,6);special=pieces('special',3,3)
icons=dict(zip('CBTKWDRPXOULAESHGJIMYNZQ',ingredients));icons['V']=special[2]
bird=[special[0],new[24],special[1],special[2]];burg=[new[25],icons['Q'],special[3],special[4]]
act=[art[2],art[2],art[12],art[2],art[9],art[5],art[7],art[4],art[14],art[1],special[5],art[7],art[6],art[8],special[8],art[2]]
exec(storytext)
storyboard.update({27:[icons['N'],special[6],new[27]],28:[special[7],art[6],new[28]],29:[art[1],icons['H'],new[29]],30:[art[3],special[7],new[30]],31:[art[5],art[2],new[31]],32:[art[3],new[32],new[32]]})
# Encode the painted stickers at print-friendly dimensions and keep the PDF small.
cache={}
def img(im,x,y,w,h):
 if id(im) not in cache:
  buf=io.BytesIO();im.save(buf,format='JPEG',quality=91,optimize=True);buf.seek(0);cache[id(im)]=ImageReader(buf)
 sc=min(w/im.width,h/im.height);iw,ih=im.width*sc,im.height*sc
 c.saveState();c.setBlendMode('Multiply');c.drawImage(cache[id(im)],x+(w-iw)/2,y+(h-ih)/2,iw,ih);c.restoreState()
def circ(x,y,r,color):
 c.setFillColor(HexColor(color));c.circle(x,y,r,fill=1,stroke=0)
def star(x,y,r,col):
 c.setFillColor(HexColor(col));p=c.beginPath()
 for k in range(8):
  a=k*math.pi/4;rr=r if k%2==0 else r*.3;xx=x+math.cos(a)*rr;yy=y+math.sin(a)*rr
  (p.moveTo if k==0 else p.lineTo)(xx,yy)
 p.close();c.drawPath(p,fill=1,stroke=0)
def scallop(y,col):
 for k in range(31):circ(k*15,y,7.65,col)
def cutehead(dest,title,level=0):
 rect(0,0,W,H,PAPER);c.bookmarkPage(dest);c.addOutlineEntry(title,dest,level)
 if dest.startswith('ch') or dest in ['menu0','guidemenu']:
  col='#F9DFE3';rect(0,815,W,75,col);scallop(814,col)
  t(21,848,'FORK, SPOON & GO!',18,'H',INK);t(238,849,'THE LITTLE LUNCHBOX COOKBOOK',8.7,'B',RED)
  for x in (19,433):star(x,878,4,'#BB7584')
bg=cutehead
def foot(dest,label='Chapter menu'):
 line(19,27,412,'#DBBFC1');t(19,11,'Fork, Spoon & Go!',10,'H',RED);t(186,12,label+'  ↑',9.2,'B',BLUE)
 c.linkRect(label,dest,(159,2,319,28),thickness=0);t(400,10,f'{c.getPageNumber():02}',12,'H',RED);c.showPage()
bottom=foot
def sec(y,n,txt,ac):
 circ(30,y+6,12,'#F1E1DB');t(24.5,y+2,n,9.5,'B',ac);t(52,y,txt,18,'H',ac)
 c.saveState();c.setStrokeColor(HexColor('#CFB9B0'));c.setLineWidth(.65);c.setDash(1,3);c.line(19,y-10,430,y-10);c.restoreState()
active=None
def titleband(cl,ac,eyebrow,name,meta,pic):
 rect(0,732,W,158,cl);scallop(732,cl)
 t(18,864,eyebrow,9.8,'B',ac)
 fs=26
 while len(simpleSplit(name,'H',fs,240))>2:fs-=.5
 lines(18,831,name,240,fs,fs+1,'H',INK)
 if active is not None:
  hint=['Chill overnight.','Toast seam-side down.','Dry lettuce before rolling.','Slice the pepper thinly.','Toss the dressing in last.','Cut across the roll.','Loosen rice clumps with a spoon.','Mash beans for a creamier sauce.','Make the logs equally thick.','Break the beef into small crumbs.','Keep the pepper halves upright.','Use the largest lettuce leaves.','Pack the cold pasta separately.','Press the fold closed.','Drain the tuna well.','Scoop out only the soft seeds.','Peel away from your fingers.','Keep the toast dry until serving.','Pat chickpeas dry before mashing.','Loosen hummus with warm water.','Leave room to fold both ends.','Grate the carrot so it cooks fast.','Pack the tortilla chips dry.','Shake the fryer basket halfway.','Weigh meat after removing bones.','Check the patty from the side.','Leave the peel on until gym time.','Press the oats to an even thickness.','Grate the carrot finely.','Keep tortillas apart from the dips.','Mash until the beans spread easily.','Use promptly chilled cooked rice.','Let the oats absorb the water.'][active]
  lines(19,782,hint,235,10.8,12.5,'B',ac)
 pill(18,746,meta,ac,PAPER)
 circ(352,808,70,'#FFFDF7');img(pic,272,748,159,119)
 star(275,853,5,ac);star(428,759,4,ac)
 if active is None:
  t(20,682,'From the kitchen notebook',18,'H',ac);line(19,669,411,'#D9C2B8')
 else:
  v=nutr(meals[active][1])
  t(20,713,'Nutrition per serving',14.3,'H',ac);t(337,714,'ESTIMATED',9.2,'B',ac)
  # Two rows, four same-width cells, each with explicit units.
  for n,(key,lab,unit) in enumerate([('protein','Protein','g'),('carbs','Carbs','g'),('fat','Fat','g'),('fiber','Fiber','g'),('calcium','Calcium','mg'),('iron','Iron','mg'),('potassium','Potassium','mg'),('vitc','Vitamin C','mg')]):
   x=18+104*(n%4);y=680-31*(n//4);rect(x,y,101,28,WHITE if n<4 else '#F4EDEB',7)
   value=v[key]
   vs=f'{value:.1f}' if key in ('iron','fiber') else str(int(round(value)))
   t(x+6,y+16,lab,8.8,'B',ac);t(x+6,y+3,vs+' '+unit,12.2,'B',INK)
def cover():
 bg('cover','Fork, Spoon & Go!');im=load(ASSETS['cover']);c.drawImage(ImageReader(im),0,0,W,H)
 t(28,846,'A BEGINNER’S PICTURE COOKBOOK',11,'B',RED)
 t(22,757,'Fork, Spoon',61,'H',INK);t(23,687,'& Go!',74,'H',INK)
 t(28,642,'Little meals for your whole day',21,'H',RED)
 pill(28,596,'33 picture recipes',RED,'#FFF8F4');pill(151,596,'8 breakfasts',BLUE,'#F4E9FF')
 link('Open the picture menu   →',25,30,194,'menu0','#845867');c.showPage()
def nutritionguide():
 bg('nutrition','How to read the nutrition notes');titleband('#E9E3FA','#655276','KITCHEN NOTEBOOK   /   NUTRITION','Your nutrition notes','Estimated for one serving',new[0])
 for n,(hd,tx,im) in enumerate([
 ('Read the top row','Protein, carbs and fat are macronutrients. Fiber is listed separately and is included in total carbs. All four amounts use grams (g).',icons['O']),
 ('Read the bottom row','Calcium, iron and potassium are minerals. Vitamin C is a vitamin. Each is shown in milligrams (mg). A rounded 0 can mean a very small amount.',icons['E']),
 ('Use your own portion','Values are for one recipe portion. A batch of four makes four servings with the same nutrition per serving. Calories are rounded to the nearest five.',art[10]),
 ('Where the numbers come from','Each ingredient weight is matched to a USDA FoodData Central SR Legacy entry. Garlic yogurt is modeled as 98% plain low-fat yogurt and 2% garlic. Cooked beans represent drained beans.',art[0])]):
  y=643-126*n;rect(18,y-112,414,108,WHITE,12);img(im,24,y-97,76,77);t(110,y-26,hd,15,'H',BLUE);lines(110,y-48,tx,305,12,16)
 lines(22,121,'Your brand, tortilla size, roasting method and how much skin you eat can change the numbers. Weigh the listed portions and check packaged-food labels.',402,12,16)
 rect(21,42,240,25,BLUE,9);t(31,50,'USDA food composition data  ↗',10,'B',WHITE)
 c.linkURL('https://fdc.nal.usda.gov/download-datasets/',(21,42,261,67),relative=0);bottom('menu0','Contents')
# Preserve the chapter structure while giving every option a new portrait.
menu_text=ed[ed.index('def menu():'):ed.index('def chapter(j):')].replace('Your day at a glance','What sounds good?').replace("sec(199,'06','Kitchen notebook',BLUE)","sec(199,'06','Kitchen notebook',BLUE)").replace(" bottom('menu0','Contents')"," link('Read the nutrition notes  →',18,34,211,'nutrition',RED);bottom('menu0','Contents')")
exec(menu_text)
# Each chapter starts like a tabbed page from the same café notebook.
def tape(x,y,cl):
 c.saveState();c.translate(x,y);c.rotate(4);rect(0,0,45,9,cl,2)
 for j in range(6):rect(4+j*7,0,2,9,'#FFFAF1')
 c.restoreState()
ch=ed[ed.index('def chapter(j):'):ed.index('storytext=')]
ch=ch.replace("t(18,712,title,33,'H',ac)","t(18,712,title,38,'H',ac);star(379,729,10,ac);star(398,740,4,ac);scallop(655,cl)")
ch=ch.replace("rect(x,top-hh,ww,hh,WHITE,8);img","rect(x+1.5,top-hh-1.5,ww,hh,'#E7DCD3',12);rect(x,top-hh,ww,hh,WHITE,12);tape(x+8,top-8,cl);img")
exec(ch)
cover();menu();starter();nutritionguide()
for j in range(5):
 chapter(j)
 for i in chapters[j][3]:
  active=i;card(i,j);active=None
guidemenu();guides();c.save()
