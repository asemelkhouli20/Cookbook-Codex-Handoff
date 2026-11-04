from pathlib import Path
source=Path('tmp/finalbook/build.py').read_text()
exec(source[:source.index('def group(i):')])
from batchnotes import notes
F['C']=('Cooked skinless chicken',165)
meals.append(('Pre-gym banana',[('N',120)],'1 min','Ready to eat',[('Pack','Take one whole banana with you. The peel keeps it easy to carry.','banana'),('Peel & eat','Peel the banana when you are ready for your pre-gym snack.','banana')]))
new.append(icons['N'])
chapters=[
 ('Breakfast','Morning','Two breakfasts you can prepare ahead.',[0,1]),
 ('Work lunch','3 pm','Pack a cold lunch or bring a box you can reheat.',[3,4,5,14,15,16,17,18,20,21,22]),
 ('Work snack','7 pm','Choose a chicken wrap or a little beef burger.',[2,25]),
 ('Before the gym','Pre-workout','Your usual banana, ready to grab.',[26]),
 ('Dinner','After the gym','Pick a dinner you can have ready when you get home.',[24,6,7,8,9,10,11,12,13,19,23])]
colors=[('#F9DEB9','#74421F'),('#D7EDDF','#245A46'),('#F5D9C9','#873E2A'),('#F8E5A7','#6E5314'),('#DFE8F3','#345574')]
page('cover','Fork, Spoon & Go!');rect(0,0,W,H,GOLD);t(22,670,'THE BEGINNER COOKBOOK   /   FIVE MEAL CHAPTERS',11,'B');t(19,591,'Fork, Spoon',53,'H');t(19,521,'& Go!',64,'H');t(24,472,'Cook for one, three or four.',19,'B')
image(bird[0],26,184,255,245);image(new[25],264,280,152,133);image(new[0],284,141,110,125)
rect(0,0,W,108,INK);link('Open the chapters  →',22,50,190,'menu0');link('See the prep guide  →',225,50,202,'bases');t(23,22,'Picture recipes for workdays and gym nights.',11,'S',WHITE);c.showPage()
page('menu0','Your meal chapters');t(18,672,'Your meal chapters',28,'H');t(19,642,'Tap a meal time, then choose a dish.',12)
for j,(label,when,desc,ids) in enumerate(chapters):
 y=543-86*j;cl,ac=colors[j];rect(16,y,418,77,cl,9);image(new[ids[0]],21,y+5,86,66);t(119,y+48,'0'+str(j+1)+'    '+when.upper(),10,'B',ac);t(118,y+21,label,20,'H',ac);t(370,y+29,'OPEN  ›',9,'B',ac);c.linkRect(label,'ch'+str(j),(16,y,434,y+77),thickness=0)
t(18,165,'How to read a card',17,'H');lines(18,141,'Choose one column for the whole recipe. For example, the burger column for 4 makes four separate burgers, one for each snack.',411,12.1,16)
lines(18,90,'Calories are estimates per serving. One standard option at each meal time adds up to less than your 2,600 kcal daily target.',412,11,15)
link('Kitchen basics  →',18,33,181,'start');link('Weekly prep guide  →',208,33,224,'week');foot(2)
# Preserve the introductory page and end-of-book component methods.
intro=source[source.index("page('start','Before"):source.index('for n,i in enumerate(order):')]
exec(intro.replace('foot(4)','foot(c.getPageNumber())').replace('Each card makes one meal.','Read the column for 1, 3 or 4 servings.').replace('Each card','Each option'))
def chapter(j):
 label,when,desc,ids=chapters[j];cl,ac=colors[j];page('ch'+str(j),str(j+1)+'. '+label,ac)
 rect(0,567,W,151,cl);t(20,678,'CHAPTER 0'+str(j+1)+'    /    '+when.upper(),11,'B',ac);t(18,623,label,34,'H',ac);t(20,588,desc,11.5)
 t(20,538,'Pick your option',18,'H',ac)
 if len(ids)>2:
  for n,i in enumerate(ids):
   y=485-40*n;rect(17,y,416,37,WHITE,5);image(new[i],19,y+1,53,35);t(79,y+18,meals[i][0],12.2,'B');t(80,y+4,'~'+str(cal(meals[i][1]))+' kcal    /    '+meals[i][2],9,'S',ac);c.linkRect(meals[i][0],'r'+str(i),(17,y,433,y+37),thickness=0)
 else:
  for n,i in enumerate(ids):
   y=340-165*n;rect(17,y,416,148,WHITE,9);image(new[i],20,y+8,142,130);lines(175,y+96,meals[i][0],245,18,23,'H',ac);t(176,y+37,'~'+str(cal(meals[i][1]))+' kcal    /    '+meals[i][2],10.8,'B');c.linkRect(meals[i][0],'r'+str(i),(17,y,433,y+148),thickness=0)
 foot(c.getPageNumber())
def recipe_card(i,j):
 name,q,tm,tool,steps=meals[i];label,when,_,_=chapters[j];cl,ac=colors[j];page('r'+str(i),name,ac);rect(0,600,W,118,cl)
 t(16,695,when.upper()+'    /    '+label.upper(),9.5,'B',ac);lines(16,663,name,263,22,26,'H');t(17,610,'~'+str(cal(q))+' kcal per serving   •   '+tm,10.7,'B',ac);image(new[i],285,603,153,109)
 t(17,576,'What you need',17,'H',ac);t(226,576,'Read down ONE column.',10.8,'B',ac)
 rect(16,548,417,19,ac,4)
 for x,txt in zip([23,239,304,370],['INGREDIENT','1 MEAL','3 MEALS','4 MEALS']):t(x,554,txt,8.8,'B',WHITE)
 y=547
 for k,(f,g) in enumerate(q):
  rect(16,y-20,417,20,WHITE if k%2==0 else '#F5EFDF',2);image(icons[f],20,y-19,30,18);t(56,y-14,F[f][0],10.7,'B');unit=' g'
  for x,n in [(240,1),(305,3),(371,4)]:t(x,y-14,str(g*n)+unit,10.4,'B' if n==1 else 'S')
  y-=20
 y-=24;t(17,y,'Make one',17,'H',ac);t(135,y+1,tool,10,'S',ac);y-=10
 for k,(hd,body,key) in enumerate(steps):
  ss=10.7; ls=simpleSplit(body,'S',ss,344);bh=23+len(ls)*13.5;rect(16,y-bh,418,bh-2,WHITE,5)
  im=actions[key]
  if key in ('slice','spread','mash','mix','chill','pan','fill','bowl') and i!=0:
   words={'U':'cucumber','A':'carrot','C':'chicken','B':'beef','E':'pepper','H':'hummus','O':'oats','M':'mustard','W':'beans','K':'chickpeas','D':'beans','P':'pasta','R':'rice','S':'corn','G':'yogurt','Z':'yogurt','X':'tortilla','L':'lettuce','N':'banana','T':'tuna'}
   candidates=[(body.lower().find(words[f]),f) for f,g in q if f in words and words[f] in body.lower()]
   im=icons[min(candidates)[1]] if candidates and k!=len(steps)-1 else new[i]
  im=im or new[i];image(im,20,y-bh+5,49,bh-10)
  t(78,y-16,str(k+1)+'   '+hd,12.1,'B',ac);lines(78,y-31,body,344,ss,13.5);y-=bh+2
 y-=7
 tm2,batch,serve=notes[i];rice=any(f=='R' for f,g in q)
 if rice:store='Cool rice within 1 hour. Fridge for 24 hours. Freeze later rice portions now.'
 elif i in (0,26):store=''
 else:store='Fridge at 4°C or colder. Eat within 3–4 days of the original cooking or prep.' if i!=1 else 'Fridge at 4°C or colder. Eat within 3–4 days.'
 batchrows=[('PREP',batch),('SERVE' if i!=26 else 'KEEP',serve)]
 if store:batchrows.append(('STORE',store))
 size=11
 while True:
  leading=size*1.26;height=32+sum(max(1,len(simpleSplit(txt,'S',size,339)))*leading+6 for _,txt in batchrows)
  if y-height>=35 or size<=9:break
  size-=.15
 assert y-height>=30,(i,y,height)
 rect(16,y-height,418,height,cl,8);t(27,y-20,'Make 3 or 4',15,'H',ac);t(192,y-19,'Batch time   '+tm2,10.6,'B',ac);pos=y-40
 for lab,txt in batchrows:
  t(25,pos,lab,8.5,'B',ac);pos=lines(79,pos,txt,339,size,leading)-6
 if i==24 and y-height>66:link('Whole bird oven guide  →',17,34,190,'roast',ac)
 if i==24:c.linkRect('Whole chicken oven guide','roast',(78,329,418,392),thickness=0)
 foot(c.getPageNumber(),'ch'+str(j))
for j in range(5):
 chapter(j)
 for i in chapters[j][3]:recipe_card(i,j)
back=source[source.index("page('bases','Rice"):source.index('# Final quantities only.')]
back=back.replace("Safety guidance: FoodSafety.gov, USDA FSIS and the UK Food Standards Agency.","Food safety sources: FoodSafety.gov cooking charts and UK FSA home food safety.")
for k in range(32,36):back=back.replace('foot('+str(k)+')','foot(c.getPageNumber())')
exec(back)
c.save()
