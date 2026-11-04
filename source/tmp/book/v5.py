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
badge(25,448,'18 RECIPES',ink);badge(118,448,'3 COOKING DAYS',ink)
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
for x,w,caption,target in [(12,118,'First time? Start here','first'),(135,117,'More meals + times','hub'),(257,149,'3- or 4-day batches','batchmath')]:
 rect(x,40,w,27,green);t(x+6,50,caption,9,'B',cream);c.linkRect(caption,target,(x,40,x+w,67),thickness=0)
foot(2);c.showPage()
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
ings=sheet('generated_images/exec-f1*.png',5);acts=sheet('generated_images/exec-4db4*.png',4)
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
extra=sheet('generated_images/exec-4d4d*.png',3)
imgs.extend(extra[:4])
# The banana is index 8 in the original sheet.
ings.extend([acts[14],*extra[4:]])
names=['Overnight oats','Chicken snack wrap','Shawarma rice bowl','Chicken pita plate','Kofta & potatoes','Kofta pita plate','Tomato chicken pasta','Tuna wraps','Apple crunch bowl','Chicken pita pizza','Lemon chickpea rice','Kofta tomato penne']
def hero(i):return i if i<8 else i+1
def button(x,y,w,label,dest,color=green):
 fill(color);c.roundRect(x,y,w,28,8,fill=1,stroke=0);t(x+10,y+9,label,10,'B',cream);c.linkRect(label,dest,(x,y,x+w,y+28),thickness=0)
bg(cream);mark('first','Before you cook');check(678,green);t(18,634,'Your first prep session',25,'H');t(20,601,'Read once. Then cook one recipe at a time.',12)
for j,(head,body,ix) in enumerate([
 ('Measure one serving','Set an empty bowl on a kitchen scale. Press zero (tare). Add food until the screen shows the grams on the card. Zero it again before weighing the next ingredient.',0),
 ('Raw, dry or cooked?','Raw meat and dry rice or pasta are weighed before heating. Cooked weights are for packing your boxes. Water changes the weight as food cooks, so the yield may vary.',5),
 ('Use the right tools','A teaspoon (tsp) is 5 ml. A tablespoon (tbsp) is 15 ml. Use a clean board and knife for salad. After handling raw meat, wash hands and tools before touching ready-to-eat food.',9),
 ('Check the middle','Slide a food thermometer into the thickest piece from the side. Check chicken at 74°C, ground beef at 71°C and reheated leftovers at 74°C. Cook longer if the reading is low.',6),
 ('Make a bigger batch','Multiply the ingredients by the number of servings. Keep each air-fryer load in one layer and cook in rounds. Start with the same timer for each load and check the center.',11)]):
 y=489-j*100;art(acts[ix],17,y+12,62,64);t(88,y+65,head,15,'B',green);lines(88,y+45,body,311,11.3,15)
button(20,40,225,'Go to the batch quantities  →','prep');foot(3);c.showPage()
bg(cream);mark('swaps','Four extra recipes');check(678,red);t(18,632,'Four ways to mix it up',25,'H');lines(20,601,'Pick a swap instead of its matching meal. Prepare hot swaps on the same batch day.',379,12,17)
subs=['Breakfast  /  any morning','Dinner  /  Saturday chicken batch','Lunch  /  Saturday rice batch','Lunch  /  Monday kofta batch']
for j in range(4):
 y=440-j*102;rect(16,y,388,94,pal[j*2][0]);dish(hero(j+8),24,y+7,85,80);t(120,y+64,subs[j],10,'B',green);t(120,y+36,names[j+8],18,'H');t(120,y+15,'Open recipe  →',10,'B');c.linkRect(names[j+8],'r'+str(j+8),(16,y,404,y+94),thickness=0)
foot(4);c.showPage()
data += [
 ([(1,'Greek yogurt','250 g, low-fat'),(26,'Apple','100 g'),(0,'Rolled oats','40 g'),(2,'Peanut butter','15 g'),(27,'Cinnamon','¼ tsp')],'',[]),
 ([(15,'Pita','90 g'),(7,'Cooked chicken','150 g'),(23,'Tomato sauce','60 g'),(29,'Mozzarella','45 g, grated'),(12,'Olive oil','5 g'),(8,'Cucumber','100 g'),(1,'Plain yogurt','100 g')],'Use a whole flat pita as your pizza base.',[]),
 ([(7,'Cooked chicken','210 g'),(10,'Cooked rice','250 g'),(28,'Chickpeas','90 g drained'),(8,'Cucumber','100 g'),(1,'Plain yogurt','120 g'),(12,'Olive oil','15 g'),(14,'Lemon juice','2 tsp'),(30,'Parsley','1 tbsp chopped')],'Use canned chickpeas and the chicken and rice from your shawarma batch.',[]),
 ([(21,'Cooked kofta','220 g'),(22,'Dry penne','110 g'),(23,'Tomato sauce','150 g'),(24,'Parmesan','15 g'),(12,'Olive oil','5 g')],'For each lunch you swap, boil this pasta on Monday instead of cooking that portion of potatoes.',[])
]
skills=[
[(0,'Measure into a jar','Use a jar with a lid and room to stir (about 500 ml). Spoon in the yogurt, then add the dry oats and peanut butter.'),(0,'Loosen the mixture','Stir all the way to the bottom. Add 1 tbsp water. If the mixture is still stiff, stir in the second spoonful.'),(1,'Add the fruit','Rinse fresh berries and pat dry. Spread them on top. Leave a little space at the rim so the lid closes.'),(2,'Chill until breakfast','Close the lid and place in the fridge overnight. In the morning the oats should be soft. Stir and eat cold.')],
[(9,'Cut the filling','Take 60 g cooked chicken from your batch. Slice into thin strips on a clean board. Rinse the cucumber and lettuce, pat dry and cut the cucumber into thin sticks.'),(3,'Make the spread','Mix the yogurt with a pinch of garlic powder. Lay the tortilla flat and spread the mixture across the middle.'),(4,'Fold and roll','Line up the filling just below the middle. Fold the sides inward, lift the bottom edge over the filling and roll away from you.'),(-1,'Store seam-side down','Put the wrap in a lidded box with the folded edge underneath. Refrigerate at work until your 7 pm break.')],
[(5,'Start the rice cooker','Put dry rice in the inner pot. Add water using the ratio on your rice packet or the matching line in your cooker. Close the lid and press White Rice or Cook.'),
(6,'Season the chicken','Cut the raw chicken into strips about 2 cm thick. In a bowl, toss with paprika, cumin, garlic and half the oil. Wash hands, board and knife.'),
(6,'Turn and check','Lay strips in one layer. Air-fry at 190°C for 12–16 min. At 6–8 min, turn with tongs. Probe the thickest strip. If below 74°C, cook 2 min more and recheck.'),
(7,'Steam the vegetables','Put veg in a steamer basket above simmering water. Cover for 5–8 min, until a fork slides in easily. Lift out and toss with remaining oil.'),
(5,'Build the bowl','When rice switches to Warm, rest it covered 5 min and loosen with a fork. Pack about 300 g rice and 210 g cooked chicken with the veg. Mix yogurt, lemon and a pinch of garlic in a side cup.')],
[(8,'Warm the chicken','Put cooked chicken on a microwave-safe plate. Add a spoonful of water and cover loosely. Heat in 30-second bursts, turning pieces, until the center reaches 74°C.'),
(9,'Make the salad','Rinse cucumber and tomato. Cut into bite-size pieces on a clean board. Put in a bowl and toss with the oil.'),(3,'Mix the dip','In a small cup, stir the lemon juice and garlic powder into the yogurt until smooth.'),(15,'Build the plate','Lay pita flat, spread hummus over it and add the warm chicken. Serve the salad and yogurt alongside.')],
[(11,'Cut and roast potatoes','Scrub potatoes and cut into 2 cm cubes. Toss with oil. Air-fry in one layer at 200°C for 18–25 min. Shake at 8 and 16 min. They are ready when a fork slips through the middle.'),
(10,'Make the kofta mixture','Grate onion and squeeze out its juice. Mix the measured onion, beef and spices in a bowl. Divide into four equal pieces and roll each into a short log about 2 cm thick.'),
(10,'Cook the kofta','Set potatoes aside. Put kofta in one layer in the basket. Wash hands and tools. Air-fry at 190°C for 10–15 min. Turn the logs after 5–7 min.'),
(8,'Check the center','Insert a thermometer sideways into the thickest log. At 71°C it is ready. If lower, air-fry 2 more min and check again.'),
(9,'Pack lunch','Chop the cucumber and tomato. Pack them and the yogurt cold. Put about 220 g cooked kofta and 400 g cooked potatoes in the lunch box.')],
[(8,'Heat the kofta','Set 140 g cooked kofta in a microwave-safe dish. Add a splash of water, cover loosely and microwave in 30-second bursts until the middle reaches 74°C.'),
(9,'Slice and chop','Cut each kofta log lengthwise. Chop the rinsed cucumber and tomato into bite-size pieces. Toss the vegetables with olive oil.'),
(15,'Open the pita','Gently separate the two layers from one edge. If they stick, lay the pita flat and fold it around the filling instead.'),
(15,'Fill and serve','Spread the hummus inside. Add kofta and a spoonful of yogurt. Serve the rest of the yogurt with the salad.')],
[(12,'Start the pasta','Bring a pot of water to a rolling boil over high heat. Add dry pasta and stir. Set a timer for the shortest cooking time on the packet.'),
(6,'Season and air-fry','Cut chicken into 2 cm strips. Toss with garlic, oregano and half the oil. Air-fry in one layer at 190°C for 12–16 min. Turn halfway. Wash the board, knife and hands.'),
(6,'Check the chicken','Probe the thickest strip from the side. At 74°C it is ready. If lower, cook for 2 more min and recheck.'),
(12,'Taste and drain','At the timer, cool and taste one piece. It should be tender with no hard center. If needed, boil another minute. Scoop out a little pasta water, then drain in a colander.'),
(13,'Coat the pasta','Warm the tomato sauce in the empty pot on medium-low until it bubbles gently. Stir in the pasta, chicken, cheese and remaining oil. Add pasta water a spoonful at a time if dry.')],
[(14,'Drain the tuna','Open the can and tip the contents into a sieve over the sink. Press gently with a fork. Weigh 150 g drained tuna into a bowl.'),
(14,'Mix the filling','Break up large chunks with a fork. Stir in the yogurt, olive oil and lemon juice. Rinse the cucumber and slice into thin sticks.'),
(15,'Fill two tortillas','Lay both tortillas flat. Spread half the hummus on each. Divide tuna and cucumber between them in a short line just below the center.'),
(4,'Roll tight','Fold the left and right edges in. Lift the bottom flap over the filling and roll away from you. If packing ahead, store filling cold and assemble at dinner.')],
[(9,'Cut the apple','Rinse the apple. Cut into quarters on a board, cut away the core, then cut the flesh into small cubes. Weigh 100 g.'),
(0,'Make cinnamon yogurt','Spoon yogurt into a bowl. Stir in the cinnamon and peanut butter. If saving for work, cover and refrigerate.'),
(1,'Add the crunch','Scatter apple and rolled oats on top just before eating. Keep the oats in a separate small container if you want them crunchy.')],
[(15,'Build a pizza base','Lay pita flat. Brush the top with olive oil. Spread tomato sauce in a thin layer, leaving a finger-width border.'),
(9,'Add the toppings','Cut cooked batch chicken into small pieces. Spread evenly over the sauce and sprinkle mozzarella over the chicken. Cut pita in halves if your basket is small.'),
(6,'Melt and check','Air-fry in one layer at 175°C for 5–8 min. Check at 5 min. The cheese should melt and the thickest chicken piece should reach 74°C. Add short bursts if needed.'),
(9,'Slice and serve','Lift out with a spatula. Rest for 1 min and cut into wedges. Serve with cucumber sticks and the yogurt for dipping.')],
[(5,'Warm the base','Use fresh batch rice and chicken, or reheat chilled portions in a covered microwave-safe bowl with a splash of water. Stir in 30-second bursts until hot throughout (74°C).'),
(14,'Rinse the chickpeas','Empty canned chickpeas into a sieve. Rinse under cool water and shake off the water. Weigh 90 g.'),
(9,'Chop and mix','Dice the rinsed cucumber. Chop parsley leaves. Mix yogurt, lemon juice, olive oil and parsley in a small cup.'),
(7,'Build your bowl','Set warm rice and sliced chicken on one side. Add chickpeas and cucumber on the other. Spoon dressing over when ready to eat.')],
[(12,'Boil the penne','Bring a pot of water to a rolling boil. Add penne and stir. Set a timer for the shortest time on the packet. Taste one cooled piece. Boil a little longer if the center is hard.'),
(10,'Break up the kofta','Use cooked kofta from the Monday batch. Put it on a plate and break it into bite-size chunks with a fork.'),
(13,'Simmer the sauce','Put olive oil, tomato sauce and kofta into a pan on medium-low. Stir until small bubbles appear and the meat is hot throughout (74°C if reheating).'),
(13,'Finish the dish','Save a little pasta water. Drain penne in a colander. Add to the sauce, stir and sprinkle with Parmesan. Loosen with a spoonful of pasta water if needed.')]]
gear=['Jar with lid, spoon, kitchen scale','Board, knife, spoon, lidded box','Rice cooker, air fryer, steamer, tongs, thermometer','Microwave, plate, knife, board, small cup','Air fryer, grater, bowl, tongs, thermometer','Microwave, knife, board, plate','Pot, colander, air fryer, tongs, thermometer','Sieve, bowl, fork, knife, board','Knife, board, bowl, spoon','Air fryer, spatula, cutting board, thermometer','Microwave or fresh batch, sieve, bowl, spoon','Pot, colander, pan, fork, spoon']
when=['10 AM  /  EVERY DAY','7 PM  /  EVERY DAY','SUN + MON  /  3 PM','SUN + MON  /  DINNER','TUE + WED  /  3 PM','TUE + WED  /  DINNER','THU + FRI + SAT  /  3 PM','THU + FRI + SAT  /  DINNER','BREAKFAST SWAP','DINNER SWAP  /  SATURDAY PREP','LUNCH SWAP  /  SATURDAY PREP','LUNCH SWAP  /  MONDAY PREP']
kcal=[460,200,1060,780,1070,770,1040,800,450,770,1050,1060]
stage=['Chill overnight','Use cooked batch chicken','Start with raw chicken','Use the shawarma batch','Start with raw ground beef','Use Monday’s cooked kofta','Start with dry pasta','No cooking required','No cooking required','Use Saturday’s cooked chicken','Use Saturday’s rice and chicken','Use Monday’s cooked kofta']
ready=['Soft oats with no dry patches at the bottom.','A wrap that holds together when lifted.','Tender rice, fork-soft vegetables and chicken at 74°C.','Warm chicken, crisp salad and a cool yogurt dip.','Fork-tender potato cubes and kofta at 71°C inside.','Warm sliced kofta inside a hummus-lined pita.','Tender pasta coated evenly in sauce.','Two wraps with the seams tucked underneath.','Crunchy apple and oats over cinnamon yogurt.','Melted cheese, crisp edges and chicken at 74°C.','Warm chicken and rice with cool lemon dressing.','Soft penne with warm kofta in a light tomato sauce.']
newart=sheet('generated_images/exec-f315*.png',4)
imgs.extend(newart[:6]);ings.extend(newart[6:])
names+=['Banana-date yogurt pot','Chickpea potato chaat','Peanut chicken pasta','Tomato lentil soup','Tuna & corn potato','Bean & corn quesadillas']
# Added ingredient indices 31 dates, 32 tahini, 33 lentils, 34 corn, 35 beans, 36 carrot, 37 soy, 38 potato, 39 broth.
data+=[
 ([(1,'Greek yogurt','250 g'),(0,'Rolled oats','30 g'),(41,'Banana','50 g'),(31,'Pitted dates','20 g'),(32,'Tahini','15 g')],'Breakfast banana is separate from the pre-gym banana.',[]),
 ([(20,'Roast potatoes','350 g cooked'),(28,'Chickpeas','200 g drained'),(1,'Plain yogurt','150 g'),(17,'Tomato','100 g'),(12,'Olive oil','10 g'),(14,'Lemon juice','2 tsp'),(15,'Pita','65 g'),(13,'Ground cumin','½ tsp')],'Use plain roasted or boiled potatoes. The measured oil is the total for cooking and dressing.',[]),
 ([(7,'Cooked chicken','200 g'),(22,'Cooked penne','300 g'),(2,'Peanut butter','25 g'),(36,'Carrot','70 g'),(37,'Soy sauce','2 tsp'),(14,'Lemon juice','2 tsp'),(12,'Olive oil','5 g'),(4,'Warm water','2 tbsp')],'Set aside plain cooked pasta before adding red sauce to the rest of your batch.',[]),
 ([(33,'Canned lentils','250 g drained'),(23,'Tomato sauce','150 g'),(39,'Vegetable broth','200 ml'),(12,'Olive oil','10 g'),(15,'Pita','90 g'),(1,'Plain yogurt','100 g'),(13,'Ground cumin','½ tsp')],'Use ready-to-eat canned or pouched lentils.',[]),
 ([(20,'Potato','350 g raw'),(25,'Canned tuna','150 g drained'),(34,'Canned corn','80 g drained'),(1,'Plain yogurt','100 g'),(29,'Mozzarella','40 g'),(12,'Olive oil','10 g'),(14,'Lemon juice','1 tsp')],'Use two small potatoes of similar size or plain potato cubes from Monday’s batch.',[]),
 ([(5,'Flour tortillas','2 medium'),(35,'Black beans','150 g drained'),(34,'Canned corn','60 g drained'),(29,'Mozzarella','55 g'),(23,'Tomato sauce','50 g'),(1,'Plain yogurt','60 g'),(12,'Olive oil','5 g')],'Choose tortillas around 150 kcal each. Use the yogurt for dipping.',[])
]
ings.append(imgs[8])
gear+=['Bowl or jar, spoon, knife','Air fryer or saucepan, bowl, sieve','Pot, fork, grater, microwave','Saucepan, sieve, spoon','Microwave-safe plate, fork, knife','Frying pan, spatula, sieve']
when+=['BREAKFAST SWAP','LUNCH SWAP  /  MONDAY PREP','LUNCH SWAP  /  WEDNESDAY PREP','DINNER SWAP  /  ANY PREP DAY','DINNER SWAP  /  MONDAY PREP','DINNER SWAP  /  ANY PREP DAY']
kcal += [460,1050,1030,780,790,805]
stage+=['Assemble cold','Use Monday’s potatoes','Use Wednesday’s chicken and penne','Use canned lentils','Use cooked or microwave potatoes','Cook on your usual prep day']
ready+=['Creamy yogurt with separate crunchy and chewy toppings.','Fork-tender potatoes and crisp chopped tomato.','Hot chicken and penne evenly coated in sauce.','Hot soup with tender lentils and a lightly thickened broth.','A fork slides through the potato without resistance.','Golden tortillas with hot beans and melted cheese.']
skills+=[
 [(9,'Slice the toppings','Peel and slice 50 g banana. Check the dates for pits, remove any and chop the flesh into small pieces.'),(0,'Mix the base','Spoon yogurt into a jar. Stir in the tahini until smooth. Keep oats dry until serving if you like crunch.'),(1,'Layer and eat','Add oats, dates and banana. For a batch, portion the yogurt and dry toppings ahead and slice the banana when you eat.')],
 [(11,'Prepare the potatoes','Use plain cooked potatoes or cut raw potatoes into 2 cm cubes. Coat with part of the oil and air-fry at 200°C for 18–25 min. Shake twice. Stop when a fork slips into the center.'),(9,'Drain and chop','Rinse canned chickpeas in a sieve and shake dry. Dice the tomato. In a bowl, stir yogurt, cumin, lemon and the rest of the measured oil.'),(7,'Build the chaat','Put potatoes and chickpeas in a bowl. Top with tomato and yogurt sauce. Tear pita into pieces for scooping. Store the sauce separately until serving.')],
 [(12,'Prepare the base','Use cooked penne and chicken from Wednesday. To cook both from raw, use the chicken and pasta directions on the Tomato chicken pasta card, leaving out the tomato sauce.'),(0,'Whisk the sauce','Mix peanut butter, soy sauce, lemon juice, oil and warm water with a fork. Add a splash more water if it is too thick to pour.'),(13,'Toss and finish','Reheat chicken and pasta with a splash of water, stirring until 74°C throughout. Stir in the sauce. Grate carrot over the bowl and serve.')],
 [(14,'Drain the lentils','Tip the canned lentils into a sieve, rinse and shake off the water. Weigh 250 g for each bowl.'),(13,'Simmer','Put oil, lentils, cumin, tomato sauce and broth in a saucepan. Heat on medium until small bubbles appear. Turn heat down and cook 5–8 min, stirring occasionally.'),(0,'Finish','Mash a few spoonfuls of lentils against the side of the pot to thicken. Ladle into a bowl. Add yogurt at the table and serve with pita.')],
 [(11,'Soften the potatoes','Scrub and pierce the potatoes several times with a fork. Microwave on a microwave-safe plate on high for 5 min. Turn over, then heat in 1–2 min bursts until a fork slides through. Rest 2 min.'),
 (14,'Make the topping','Drain tuna and corn in a sieve. Break tuna up with a fork. Mix with corn, yogurt and lemon juice.'),(-1,'Split and fill','Split warm potatoes and loosen the centers with a fork. Drizzle with oil. Add mozzarella while hot, then spoon over the tuna mixture. Cooked potato cubes work the same way in a bowl.')],
 [(14,'Mash the beans','Drain and rinse the beans. Drain corn. Mash half the beans with a fork, stir in the rest and add corn and tomato sauce.'),(4,'Fill and fold','Lay out both tortillas. Spread filling on one half of each, add mozzarella, then fold the empty halves over the filling.'),(8,'Toast in a pan','Brush a pan with the measured oil. Heat on medium. Cook each folded tortilla for 2–3 min per side until golden and melted inside. Lower heat if it browns too quickly. Serve with yogurt.')]]
times=[('3–5 min + overnight chill','1 min to serve'),('20–30 min','3–5 min'),('30–45 min','5–8 min'),('25–35 min','5–8 min'),('40–55 min','5–8 min'),('25–35 min','5–8 min'),('25–35 min','5–8 min'),('5–8 min, no cooking','3–5 min'),('3–5 min, no cooking','2–3 min'),('30–40 min','10–15 min'),('30–45 min','5–8 min'),('30–40 min','6–10 min'),('3–5 min, no cooking','2–3 min'),('30–40 min','5–8 min'),('25–35 min','5–8 min'),('12–18 min, canned lentils','4–6 min to reheat'),('15–25 min','5–8 min'),('12–18 min, canned beans','5–8 min to reheat')]
# Short, explicit scaling labels below the one-person amount.
import re
def scaleamt(s,n):
 s=s.replace('½','0.5').replace('¼','0.25')
 if 'See below' in s:return 'see note'
 if '·' in s:s=s.split('·')[-1].strip()
 m=re.match(r'([\d.]+)(?:–([\d.]+))?\s*(.*)',s)
 if not m:return s
 a,b,unit=m.groups();unit=unit.split(',')[0].split(' raw')[0].split(' dry')[0].split(' cooked')[0].split(' drained')[0].split(' chopped')[0].strip()
 unit={'small leaf':'leaves','pinch':'pinches','medium':'pieces','medium tortillas':'pieces'}.get(unit,unit)
 return f'{float(a)*n:g}'+(f'–{float(b)*n:g}' if b else '')+' '+unit
for i,(parts,note,_) in enumerate(data):
 ac=pal[i%8][1];col=pal[i%8][0];p=5+2*i;dest='r'+str(i);how='how'+str(i)
 bg(cream);mark(dest,names[i]);rect(0,485,420,205,col);check(678,ac);t(18,648,when[i],10,'B',ac)
 for j,s in enumerate(simpleSplit(names[i], 'H',24,235)):t(17,606-j*29,s,24,'H')
 badge(20,535,'~'+format(kcal[i],',')+' kcal',ac);t(20,504,'1 SERVING',9,'B',ac);dish(hero(i),260,500,148,132)
 t(17,454,'Gather your ingredients',21,'H',ac)
 for j,(idx,name,amount) in enumerate(parts):
  row,slot=divmod(j,4);x=13+slot*99;y=327-row*108
  fill('#FFFFFF');c.roundRect(x,y,96,102,8,fill=1,stroke=0);art(ings[idx],x+10,y+51,76,46)
  for off,lab,font,sz in [(36,name,'B',10.4),(22,amount,'S',10.5)]:
   while pdfmetrics.stringWidth(lab,font,sz)>92:sz-=.25
   t(x+(96-pdfmetrics.stringWidth(lab,font,sz))/2,y+off,lab,sz,font)
  detail=scaleamt(amount,3)+'  /  '+scaleamt(amount,4)
  sz=9.1
  while pdfmetrics.stringWidth(detail,'B',sz)>91:sz-=.2
  t(x+(96-pdfmetrics.stringWidth(detail,'B',sz))/2,y+6,detail,sz,'B',ac)
 t(17,437,'BOTTOM LINE OF EACH TILE  =  3 SERVINGS  /  4 SERVINGS',9,'B',ac)
 if note:lines(17,202,note.replace('¼ tsp','¼ tsp').strip(),383,10.5,13,'S',ac)
 t(17,161,'Set out',12,'B',ac);lines(17,145,gear[i]+'.',380,11,14)
 t(17,110,'From start',10,'B',ac);t(100,110,times[i][0],11)
 t(17,91,'Ready bases',10,'B',ac);t(100,91,times[i][1],11);button(17,45,254,'Start cooking  →  '+str(len(skills[i]))+' illustrated steps',how,ac)
 foot(p);c.showPage()
 bg(cream);mark(how,names[i]+' / method');check(678,ac);t(17,650,'COOK ALONG  /  '+str(len(skills[i]))+' STEPS',10,'B',ac);t(17,612,names[i],25,'H',ink)
 n=len(skills[i]);h=min(136,470/n)
 for j,(idx,head,body) in enumerate(skills[i]):
  top=586-j*h;rect(14,top-h+5,392,h-7,'#FFFFFF');art(acts[idx] if idx>=0 else imgs[1],18,top-h+(h-70)/2+2,65,65)
  slip(98,top-20,j+1,ac);t(112,top-24,head,14,'B',ac)
  size=12.1
  while 40+(len(simpleSplit(body,'S',size,307))-1)*size*1.19>h-11:size-=0.15
  last=lines(90,top-40,body,307,size,size*1.19)
  assert last+15>=top-h+6,(i,j,h,body)
 t(17,90,'Ready when',12,'B',ac);lines(17,71,ready[i],382,12,14)
 c.linkRect('Back to ingredients',dest,(12,4,190,33),thickness=0);foot(p+1);t(126,15,'/  INGREDIENTS',8,'B',ac);c.showPage()
bg(cream);mark('prep','Three batch-cooking sessions');check(678,red);t(20,634,'Batch-cook the week',29,'H');t(22,605,'Base menu for 1 person. All box weights are cooked.',11)
for j,(day,head,img,body) in enumerate([
('SATURDAY','Chicken + rice',2,'Cook 1,140 g chicken (about 1.5–1.6 kg raw). Pack 2 × 210 g for rice bowls, 2 × 150 g for pita dinners and 7 × 60 g for snack wraps. Divide 600 g cooked rice between the two bowls. Freeze later portions.'),
('MONDAY','Kofta + potatoes',4,'Cook 720 g kofta and 800 g potatoes. Pack 2 × 220 g kofta with 400 g potatoes each. Set aside 2 × 140 g kofta for pita dinners.'),
('WEDNESDAY','Tomato chicken pasta',6,'Triple the pasta recipe. Divide 600 g cooked chicken and 900 g cooked pasta between three boxes with sauce. Freeze Saturday’s box and thaw it in the fridge on Friday. Roll tuna wraps at dinner.')]):
 y=580-132*j;rect(18,y-119,384,124,pal[img][0]);dish(img,22,y-94,77,78);t(109,y-13,day,9,'B',pal[img][1]);t(109,y-37,head,17,'H');lines(109,y-56,body,283,10.4,13.3)
t(22,161,'Chill, freeze, reheat',18,'H',green);lines(22,137,'Chill rice within 1 hour. Freeze any rice you will eat more than 24 hours later. Refrigerate other cooked leftovers within 2 hours and use within 3–4 days or freeze. Reheat hot meals to 74°C. Keep yogurt and salad cold.',372,11.4,16)
t(22,54,'Storage guidance from USDA FSIS and the UK Food Standards Agency.',8,'S');foot(41);c.showPage()
bg(cream);mark('hub','Prep once, choose meals');check(678,green);t(18,634,'Prep once, choose meals',25,'H');lines(20,601,'Start with the food you have. Times below assume the main components are cooked or bought ready.',380,12,16)
for j,(idx,kind) in enumerate([(12,'BREAKFAST'),(13,'LUNCH • POTATOES'),(14,'LUNCH • CHICKEN + PASTA'),(15,'DINNER • CANNED LENTILS'),(16,'DINNER • POTATOES'),(17,'DINNER • CANNED BEANS')]):
 y=508-j*67;rect(16,y,388,62,pal[j][0]);dish(hero(idx),19,y+3,63,55);t(90,y+43,kind,8,'B');t(90,y+24,names[idx],15,'H');t(90,y+8,times[idx][1]+' with components ready',9);c.linkRect('Open recipe','r'+str(idx),(16,y,404,y+62),thickness=0)
button(16,123,185,'4 more recipe swaps  →','swaps');button(209,123,195,'Cook or buy guide  →','buy')
button(16,43,185,'Weekly prep quantities  →','prep');button(209,43,195,'Storage by component  →','store');button(16,82,185,'3- or 4-day example  →','batchmath');button(209,82,195,'Meal timing index  →','timing');foot(42);c.showPage()
bg(cream);mark('buy','Cook once or buy ready');check(678,green);t(18,634,'Cook it or buy it?',27,'H');t(20,604,'Start with plain components and add flavor when serving.',11)
for j,(ix,head,body) in enumerate([
 (7,'Chicken and kofta','Batch-cook on Saturday or Monday. For a shortcut, buy fully cooked plain chicken strips or cooked lean kofta. Weigh the edible cooked portion. Raw, pre-shaped kofta still needs cooking.'),
 (10,'Rice, penne and potatoes','Cook plain bases in batches. Microwave rice pouches and plain cooked potatoes are quick alternatives. Weigh ready rice or pasta using the cooked amount. Follow the pack’s heating directions.'),
 (28,'Chickpeas, beans and lentils','Choose canned or pouched, already cooked. Drain in a sieve, rinse and weigh the drained food. A can’s total weight includes its liquid. No soaking or boiling needed.'),
 (1,'Yogurt, hummus and sauces','Buy plain low-fat yogurt, hummus and tomato pasta sauce in tubs or jars. Spoon out the recipe amount. Mix lemon or spices into one portion to vary the flavor.'),
 (11,'Vegetables, bread and fish','Use frozen steam-in-bag veg, prewashed salad, pita, tortillas and canned tuna in water. Keep bread dry. Drain tuna and store opened products according to the label.')]):
 y=511-96*j;art(ings[ix],17,y+7,65,65);t(90,y+62,head,13,'B',green);lines(90,y+43,body,309,10.8,14)
lines(18,86,'Oil, sauces and ready-seasoned products vary by brand. Use the label when comparing calories.',380,11,14)
button(18,42,205,'Plan a 3- or 4-day batch  →','batchmath');button(231,42,169,'Storage by component  →','store');foot(43);c.showPage()
bg(cream);mark('batchmath','Three days or four?');check(678,red);t(17,637,'Three days or four?',26,'H');lines(19,604,'Example for one person: a chicken lunch and a small chicken wrap each day. Dinners and breakfast are separate.',380,12,16)
rect(16,477,388,65,pal[2][0]);t(24,520,'3 days',15,'B');t(99,520,'2 shawarma bowls + 1 lemon rice bowl',11,'B');t(99,494,'Add 3 chicken snack wraps.',11)
rect(16,405,388,65,pal[1][0]);t(24,448,'4 days',15,'B');t(99,448,'2 shawarma bowls + 2 lemon rice bowls',11,'B');t(99,422,'Add 4 chicken snack wraps.',11)
t(20,380,'What to portion',16,'H');t(258,380,'3 days',11,'B');t(340,380,'4 days',11,'B')
for k,(lab,a,b) in enumerate([('Chicken, cooked','810 g','1,080 g'),('Basmati rice, cooked','850 g','1,100 g'),('Mixed veg for shawarma','400 g','400 g'),('Canned chickpeas, drained','90 g','180 g'),('Small tortillas','3','4')]):
 yy=351-25*k;rect(18,yy-7,383,22,'#FFFFFF' if k%2==0 else cream);t(23,yy,lab,11);t(257,yy,a,11,'B');t(338,yy,b,11,'B')
lines(19,220,'Chicken math: 210 g per lunch + 60 g per wrap = 270 g/day. Buy about 1.1 kg raw for 3 days or 1.45 kg for 4. Cooking yield varies. Weigh again after cooking.',379,11.5,15)
t(19,153,'How long to allow',15,'H');lines(19,132,'Start the rice first. Cook chicken in one layer per load, about 12–16 min each. Two loads take 24–32 min of air-fryer time; three take 36–48 min. Allow another 10–20 min for cutting and boxing. The rice cooks alongside.',379,11,14)
button(18,42,215,'Store your 3- or 4-day batch  →','store');foot(44);c.showPage()
bg(cream);mark('timing','Time for every meal');check(678,green);t(18,634,'How long will it take?',24,'H')
lines(19,606,'Estimated elapsed time for one serving. “Ready” means the main components are cooked or purchased. Tap a row for the recipe.',380,11.4,15)
t(20,553,'MEAL',9,'B');t(170,553,'FROM START',9,'B');t(304,553,'READY',9,'B')
for j,name in enumerate(names):
 yy=531-j*25;rect(16,yy-6,388,24,pal[j%8][0] if j%2==0 else cream)
 start,end=times[j];start=start.replace(', no cooking','').replace(', canned lentils','').replace(', canned beans','').replace('overnight chill','overnight');end=end.replace(' to serve','').replace(' to reheat','')
 t(20,yy,name,9.5,'B');t(171,yy,start,9.7);t(305,yy,end,9.7);c.linkRect(name,'r'+str(j),(16,yy-6,404,yy+18),thickness=0)
lines(20,74,'Scale ingredient weights for extra servings. Cooking time depends on the number of pan or fryer loads.',380,10.5,14)
foot(45);c.showPage()
bg(cream);mark('store','How long components keep');check(678,green);t(18,634,'Pack it for later',28,'H');lines(20,601,'Planning four meals ahead? Label each box with the day you cooked it. Store the hot and cold components separately.',376,12,16)
for j,(title,body,ix) in enumerate([
 ('Rice  /  24 hours in the fridge','Cool quickly in shallow portions, ideally within one hour. Refrigerate the next serving. Freeze portions you will eat more than 24 hours later. Thaw in the fridge and reheat once until steaming throughout.',10),
 ('Chicken, kofta, plain pasta and potatoes','Divide into shallow containers. Refrigerate within two hours, or within one hour if the room is hotter than 32°C. Keep the fridge at 4°C or colder. Use cooked leftovers within 3–4 days, or freeze earlier.',7),
 ('Yogurt, hummus, beans and lentils','Follow the package’s after-opening time. Write the opening date on the lid. Refrigerate unused beans in a clean covered container. For a mixed meal, follow the shortest storage window of its ingredients.',28),
 ('Wraps, salads and sauces','Keep yogurt sauce in a small sealed cup. Pat greens dry and refrigerate them separately. Roll tortillas on the day you eat them to keep them from getting soggy.',5),
 ('Reheating one box','Thaw frozen portions in the fridge. Cover loosely, heat, stir and check several spots. Hot leftovers should reach 74°C. Add cold greens or yogurt after heating.',21)]):
 y=495-j*88;art(ings[ix],19,y+7,55,62);t(85,y+60,title,12,'B',green);lines(85,y+43,body,312,10.6,13)
t(18,88,'Sources: USDA FSIS leftover guidance and UK Food Standards Agency rice guidance.',8.3)
button(18,40,205,'Back to the batch example  →','batchmath');foot(46);c.showPage();c.save()

