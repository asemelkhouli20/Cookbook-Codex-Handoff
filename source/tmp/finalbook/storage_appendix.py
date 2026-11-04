from pathlib import Path
import io,math
src=Path('tmp/finalbook/oatsbook.py').read_text()
exec(src[:src.rindex('cover();menu();starter();nutritionguide()')])
# Author appendix separately, then append it so existing pages retain their exact content.
from reportlab.pdfgen.canvas import Canvas
from pypdf import PdfReader,PdfWriter
from storage_data import groups
base=Path('output/pdf/Weekly_Meal_Cards.pdf')
import fitz
doc=fitz.open(base);assert len(doc) in (63,74)
if len(doc)>63:doc.delete_pages(63,len(doc)-1)
original=doc.tobytes();original_n=63
Path('tmp/cutebook/recipe_pages_before_storage_fix.pdf').write_bytes(original)
c=Canvas('tmp/cutebook/Component_storage_appendix.pdf',pagesize=(450,890))
c.setTitle('Component fridge guide')
def footer():
 line(19,29,412,'#D9C3C4');t(19,12,'Fork, Spoon & Go!',10,'H',RED);t(184,12,'Storage key  ↑',9,'B',BLUE);c.linkRect('Storage key','storage0',(168,2,309,28),thickness=0);t(397,11,str(original_n+c.getPageNumber()),11,'H',RED);c.showPage()
def opening(dest,title,sub,pic):
 bg(dest,title);rect(0,731,450,159,'#F7E1E5');scallop(732,'#F7E1E5')
 t(20,863,'THE COMPONENT NOTEBOOK   /   FRIDGE AT 4°C OR COLDER',9.3,'B',RED)
 lines(19,820,title,281,29,31,'H',INK);lines(20,757,sub,280,11.7,15,'S',RED);img(pic,323,753,112,107)
def symbol(x,y,status,r=10):
 if status=='S':
  c.setFillColor(HexColor('#F4CA69'));c.setStrokeColor(HexColor('#A47832'));c.setLineWidth(.65);p=c.beginPath()
  for k in range(10):
   a=math.pi/2+k*math.pi/5;rr=r if k%2==0 else r*.49;xx=x+math.cos(a)*rr;yy=y+math.sin(a)*rr
   (p.moveTo if k==0 else p.lineTo)(xx,yy)
  p.close();c.drawPath(p,fill=1,stroke=1)
  circ(x-2.7,y+1,1,'#6C4C2B');circ(x+2.7,y+1,1,'#6C4C2B')
  c.setStrokeColor(HexColor('#6C4C2B'));c.arc(x-3,y-4,x+3,y+1,190,160)
 elif status=='M':
  circ(x,y,r,'#D8C9ED');circ(x+r*.43,y+r*.32,r*.83,'#FFFFFF')
  circ(x-r*.4,y,1,'#756084')
 elif status=='D':
  circ(x,y,r*.92,'#4D475E');circ(x-3,y+1,1,'#FFF9EF');circ(x+3,y+1,1,'#FFF9EF')
  c.setStrokeColor(HexColor('#FFF9EF'));c.setLineWidth(.75);c.line(x-2,y-4,x+2,y-4)
 else:
  circ(x,y,r,'#F9DFDF');c.setStrokeColor(HexColor('#AB4353'));c.setLineWidth(2.2);c.line(x-3.5,y-3.5,x+3.5,y+3.5);c.line(x-3.5,y+3.5,x+3.5,y-3.5)
def legendline(y,s,hd,txt):
 rect(19,y-74,412,70,WHITE,12);symbol(47,y-36,s,17);t(80,y-27,hd,17,'H',RED);lines(80,y-47,txt,338,12,15)
opening('storage0','How long will it last?','Read the state of the food first: cooked, opened or cut.',art[12])
for y,s,hd,txt in [
 (707,'S','Happy star • good quality','Usually tasty and pleasant in this part of the storage window.'),
 (629,'M','Pale moon • flavor fading','May start to lose crunch, freshness or aroma.'),
 (551,'D','Dark moon • lower quality','Still within this guide’s planned window, but may be softer, drier or less tasty.'),
 (473,'X','X mark • stop','Past this guide’s storage window. Discard or use an earlier-frozen portion instead.')]:legendline(y,s,hd,txt)
rect(19,254,412,131,'#E7E2F6',12);t(31,361,'Count from preparation',20,'H',BLUE)
lines(31,338,'Day 0 = just prepared. Day 1 = 24 hours later, Day 2 = 48 hours, then 72, 96, 120 and 144 hours. Use a 3–4-day food by 72–96 hours from preparation. Day 4 shows the 96-hour cutoff, not a whole extra day.',387,13,18)
rect(19,112,412,130,'#E4EEDF',12);t(31,218,'Everything here is refrigerated',20,'H','#42634D')
lines(31,194,'Every row assumes continuous storage at 4°C or colder, in a clean covered container. Star and moon timing is an estimated quality guide. Use the written storage limit and any earlier package instructions. Discard spoiled or mishandled food sooner.',387,12.6,17)
t(23,79,'* A conservative planning limit chosen for this cookbook.',11.2,'B',RED)
t(23,59,'Raw meat rows mean time before cooking, not permission to eat it raw.',10.5,'B',RED);footer()
for gi,(heading,rows) in enumerate(groups):
 opening('store'+str(gi),heading,'Day-by-day quality at the ages shown. Earlier package limits win.',icons[rows[0][0]])
 # Compact legend repeats on every chart.
 for k,(s,lab) in enumerate([('S','Good'),('M','Fading'),('D','Lower quality'),('X','Stop')]):
  x=30+k*104;symbol(x,707,s,9);t(x+14,703,lab,10,'B',BLUE)
 rect(19,660,412,28,BLUE,7);t(27,670,'COMPONENT + STATE',9,'B',WHITE)
 for k in range(7):
  x=186+k*35;t(x+3,677,str(k)+' day',8.8,'B',WHITE);t(x+4,665,str(k*24)+' h',7.8,'S',WHITE)
 for n,(key,name,state,limit,seq,note) in enumerate(rows):
  yy=654-n*85
  rect(19,yy-83,412,82,WHITE if n%2==0 else '#F9EEE8',9);img(icons[key],24,yy-46,39,41)
  ss=12.1
  while len(simpleSplit(name,'B',ss,114))>2:ss-=.2
  lines(68,yy-17,name,114,ss,ss+1,'B',INK);lines(68,yy-46,state,113,9.5,11,'S',RED)
  for k,status in enumerate(seq):symbol(201+k*35,yy-23,status,9.2)
  t(186,yy-45,'LIMIT  '+limit,9.5,'B',BLUE)
  lines(26,yy-68,note,398,9.9,11.5,'S',INK)
 base_y=654-len(rows)*85-20
 if gi==0:txt='Cooked meat has a 3–4-day fridge window. Raw poultry and raw mince stay at 1–2 days. Freeze cooked portions for days 5–6.'
 elif gi==1:txt='Cooked rice and pasta use the same 3–4-day refrigerated range in this guide. Freeze portions for later days.'
 elif gi==3:txt='* Cut-produce plan: use within 3–4 days. The quality symbols are estimates for fresh, carefully handled vegetables.'
 elif gi==4:txt='* Cut-fruit plan: use within 3–4 days, sooner if freshness declines. Peel bananas and wash fragile berries close to eating.'
 elif gi==5:txt='† These published ranges assume suitable handling and freshness. Any shorter use-by or after-opening instruction overrides the row.'
 elif gi==6:txt='All these items are also shown REFRIGERATED. Keep dry products airtight to avoid condensation. A six-day row is not a promise beyond the package instructions.'
 else:txt='Day 0 starts when cooked, opened, cut or mixed. Adding a sauce or reheating an ingredient never restarts its earlier clock.'
 rect(19,max(65,base_y-73),412,77,'#E7E2F6',10);lines(31,max(65,base_y-73)+55,txt,388,12.5,17,'S',BLUE)
 footer()
opening('storageplan','What can I prep ahead?','Choose your next prep day by the most perishable component.',art[10])
plans=[
 ('Same day / next morning','Slice banana, prepare delicate berries, roll the wrap and add dressing. A jar made the night before has the freshest fruit texture. Keep crunchy salad and dips separate.',new[0]),
 ('Two-day batches','Cook chicken, beef, pasta and beans. Mix two oat bases and chill. Add fragile fruit near serving. Chill rice promptly and use within 3–4 days; freeze later portions.',art[10]),
 ('Three- and four-day batches','Cooked protein, pasta and canned beans can fit this plan. Use before the fourth-day cutoff. Cook raw poultry or mince first. Keep sauces within their shorter label or prep limits.',art[8]),
 ('Five- and six-day meals','Freeze cooked protein, rice and pasta in individual boxes promptly. Keep dry oats portioned and sealed in the fridge. Prepare fresh fruit and salad near eating time. Check yogurt and dip labels.',art[13])]
for n,(hd,txt,im) in enumerate(plans):
 y=713-n*132;rect(19,y-119,412,113,WHITE,12);img(im,24,y-99,75,82);t(108,y-26,hd,17,'H',RED);lines(108,y-48,txt,309,12.2,16.5)
lines(23,151,'Label every box with the original cooking or opening time. Example: chicken cooked Monday at 7 pm reaches its four-day cutoff Friday at 7 pm.',403,12.5,17)
lines(23,91,'Cool in shallow boxes within 2 hours, or 1 hour in heat above 32°C. Refrigerate rice promptly in shallow boxes. Thaw frozen portions in the fridge. Reheat hot meals to 74°C.',403,12,16);footer()
opening('storagesources','A few rules to keep','Use the written limits with the picture symbols.',art[15])
for n,(hd,txt) in enumerate([
 ('Cool first, count from the original prep','Refrigerate promptly in shallow containers. The clock starts at the original cooking, cutting or opening time. Buying a ready-cooked item does not create a fresh clock.'),
 ('Use the shortest component window','A bowl containing rice follows the rice window. A wrap with an older filling follows that filling. Label dates and opening instructions can be shorter than this guide.'),
 ('Freeze early for later days','Use clean single-portion boxes. Freeze while the food is still within its fridge window. Thaw in the fridge. Freezing does not make spoiled food safe.'),
 ('Source notes','Storage ranges use US household guidance from USDA and university extension services. Star and moon timing is an estimated quality guide. Asterisks mark shorter cookbook planning choices; they are not exact spoilage deadlines.')]):
 y=704-n*106;rect(19,y-99,412,93,WHITE,10);t(31,y-25,hd,16,'H',BLUE);lines(31,y-47,txt,387,12,16)
refs=[
 ('Montana State • yogurt-oat base: up to 3 days','https://www.montana.edu/extension/buyeatlivebetter/recipes/makeaheadbreakfastparfaits/'),
 ('FoodSafety.gov • cold storage and leftovers','https://www.foodsafety.gov/food-safety-charts/cold-food-storage-charts'),
 ('USDA FSIS • safe leftover handling','https://ask.fsis.usda.gov/article/How-do-I-handle-leftovers-safely'),
 ('Nebraska Extension • cooked rice: 3–4 days','https://food.unl.edu/article/freezing-rice-and-pasta/'),
 ('University of Maine • cut produce: 3–4 days','https://extension.umaine.edu/food-health/2025/05/29/storing-and-washing-fresh-fruits-and-vegetables/'),
 ('University of Nebraska • opened foods and condiments','https://food.unl.edu/free-resource/food-storage/')]
t(22,250,'Tap a source',17,'H',RED)
for n,(lab,url) in enumerate(refs):
 y=221-29*n;t(23,y,lab,11,'B',BLUE);c.linkURL(url,(22,y-4,431,y+14),relative=0)
lines(23,54,'No smell or taste check can confirm food safety. Do not taste food to test it.',402,11,14,'B',RED);footer()
c.save()
merged=fitz.open(stream=original,filetype='pdf')
appendix=fitz.open('tmp/cutebook/Component_storage_appendix.pdf')
toc=merged.get_toc()
merged.insert_pdf(appendix)
merged.set_toc(toc+[[1,'Component fridge guide',64]]+[[2,t,p+63] for level,t,p in appendix.get_toc()])
merged.save('tmp/cutebook/fridge_fixed.pdf',garbage=3,deflate=True)
Path('tmp/cutebook/fridge_fixed.pdf').replace(base)
print('Replaced storage pages. Total',len(merged))
