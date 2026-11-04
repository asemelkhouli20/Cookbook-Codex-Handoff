from pathlib import Path
old=Path('tmp/finalbook/illustrated.py').read_text()
exec(old[:old.index("page('cover',")])
exec(Path('tmp/finalbook/breakfast.py').read_text())
new.extend(grid('fd6e',3,2))
chapters[0]=('Breakfast','Morning','Sweet jars, warm bowls and savory breakfasts.',[0,27,2+27,1,28,30,31,32])
assert sorted(chapters[0][3])==[0,1,27,28,29,30,31,32]
W,H=450,812;c.setPageSize((W,H));c.setTitle('Fork, Spoon & Go! | The illustrated meal-prep cookbook')
PAPER='#FFFAEE';INK='#272437';BLUE='#253D76';RED='#B33D2C'
colors=[('#FFE8AA','#7E3F16'),('#DAEBD9','#225741'),('#FFE0CB','#873B26'),('#F5EAB3','#695117'),('#DEE9F7','#294A77')]
def line(x,y,w,col=INK):
 c.setStrokeColor(HexColor(col));c.setLineWidth(.65);c.line(x,y,x+w,y)
def pill(x,y,label,color=BLUE,bg=WHITE):
 ww=pdfmetrics.stringWidth(label,'B',9.5)+17;rect(x,y,ww,20,bg,9);t(x+8,y+6,label,9.5,'B',color);return ww
def img(im,x,y,w,h):
 c.saveState();c.setBlendMode('Multiply');image(im,x,y,w,h);c.restoreState()
def bg(dest,title,level=0):
 rect(0,0,W,H,PAPER);c.bookmarkPage(dest);c.addOutlineEntry(title,dest,level)
def bottom(dest,label='Chapter menu'):
 line(18,27,414,'#B9ADA2');t(18,12,'FORK, SPOON & GO!',8.4,'B',BLUE);t(181,12,label+'  ↑',8.9,'B',BLUE);c.linkRect(label,dest,(158,2,315,28),thickness=0);t(398,11,f'{c.getPageNumber():02}',10,'B',BLUE);c.showPage()
def titleband(cl,ac,eyebrow,name,meta,pic):
 rect(0,H-159,W,159,cl);rect(0,H-159,6,159,ac)
 t(18,H-22,eyebrow,9.2,'B',ac);line(18,H-31,239,ac)
 titlesize=23
 while len(simpleSplit(name,'H',titlesize,232))>3:titlesize-=1
 lines(17,H-61,name,232,titlesize,titlesize*1.12,'H',INK)
 pill(18,H-151,meta,ac,PAPER);img(pic,256,H-153,186,143)
def sec(y,n,txt,ac):
 rect(18,y-4,25,20,ac,9);t(24,y+2,n,9,'B',WHITE);t(50,y,txt,17,'H',ac);line(18,y-11,414,'#C5B9A7')
def cover():
 bg('cover','Fork, Spoon & Go!')
 im=load('943f');c.drawImage(ImageReader(im),0,0,W,H)
 t(23,773,'THE ILLUSTRATED MEAL-PREP COOKBOOK',10,'B',BLUE);line(23,759,402,BLUE)
 t(19,689,'Fork, Spoon',51,'H',BLUE);t(20,620,'& Go!',64,'H',BLUE)
 t(24,579,'Breakfast to dinner, in pictures.',17,'B',INK)
 pill(24,540,'33 OPTIONS',BLUE,PAPER);pill(120,540,'8 BREAKFASTS',RED,PAPER)
 link('Open the meal chapters   →',24,34,206,'menu0',BLUE);c.showPage()
def menu():
 bg('menu0','Contents');t(20,776,'FORK, SPOON & GO!     /     CONTENTS',10,'B',RED)
 t(18,724,'Your day at a glance',30,'H',BLUE);t(20,690,'Tap a meal time to see its picture menu.',12)
 for j,(name,when,desc,ids) in enumerate(chapters):
  y=585-88*j;cl,ac=colors[j];rect(18,y,414,78,cl,10);img(new[ids[0]],22,y+3,82,71);t(116,y+53,f'0{j+1}   /   {when.upper()}',9.5,'B',ac)
  t(115,y+23,name,19,'H',ac);t(330,y+29,str(len(ids))+' option'+('s' if len(ids)>1 else '')+'  →',10,'B',ac);c.linkRect(name,'ch'+str(j),(18,y,432,y+78),thickness=0)
 sec(199,'06','Kitchen notebook',BLUE)
 link('How to read a recipe  →',18,140,201,'start',BLUE);link('Prep & storage guide  →',229,140,203,'guidemenu',BLUE)
 lines(20,106,'Calories are estimates for one serving. Choosing one standard portion from each chapter gives less than your 2,600 kcal daily target.',406,11,15)
 bottom('menu0','Contents')
def chapter(j):
 title,when,desc,ids=chapters[j];cl,ac=colors[j];chunks=[ids] if len(ids)<=8 else [ids[:6],ids[6:]]
 for k,subset in enumerate(chunks):
  dest='ch'+str(j)+('b' if k else '');bg(dest,(str(j+1)+'. '+title) if not k else title+' • more options',int(k>0))
  rect(0,656,W,156,cl);t(20,778,f'CHAPTER 0{j+1}   /   {when.upper()}',10,'B',ac);line(20,762,407,ac)
  t(18,712,title,33,'H',ac);t(20,678,desc,11.6,'S',ac)
  if len(subset)>2:
   rows=(len(subset)+1)//2;rh=min(182,565/rows)
   for ni,i in enumerate(subset):
    x=18+210*(ni%2);top=641-int(ni/2)*rh;ww=203;hh=rh-7
    rect(x,top-hh,ww,hh,WHITE,8);img(new[i],x+4,top-hh+48,ww-8,hh-53)
    ns=12
    while len(simpleSplit(meals[i][0],'B',ns,ww-16))>2:ns-=.2
    lines(x+8,top-hh+35,meals[i][0],ww-16,ns,13,'B',ac)
    t(x+8,top-hh+6,'~'+str(cal(meals[i][1]))+' kcal   /   '+meals[i][2],8.5,'S',INK)
    c.linkRect(meals[i][0],'r'+str(i),(x,top-hh,x+ww,top),thickness=0)
  else:
   for ni,i in enumerate(subset):
    y=396-203*ni;rect(18,y,413,186,WHITE,10);img(new[i],23,y+8,175,172);lines(210,y+120,meals[i][0],209,18.3,23,'H',ac);t(210,y+52,'~'+str(cal(meals[i][1]))+' kcal   /   '+meals[i][2],10.7,'B');c.linkRect(meals[i][0],'r'+str(i),(18,y,431,y+186),thickness=0)
  if len(chunks)>1:link('More '+title.lower()+' options  →' if not k else 'First options  →',18,38,235,'ch'+str(j)+('b' if not k else ''),ac)
  bottom('menu0','All chapters')
storytext=old[old.index('  storyboard={')+2:old.index('  im=storyboard')]
exec(storytext)
storyboard.update({27:[icons['N'],icons['O'],new[27]],28:[icons['A'],icons['O'],new[28]],29:[art[1],icons['H'],new[29]],30:[art[3],art[1],new[30]],31:[art[5],icons['Z'],new[31]],32:[art[3],icons['K'],new[32]]})
def card(i,j):
 name,q,tm,tool,steps=meals[i];label,when,_,ids=chapters[j];cl,ac=colors[j]
 bg('r'+str(i),name,1);titleband(cl,ac,f'0{j+1}   /   {label.upper()}     •     OPTION {ids.index(i)+1:02}',name,'~'+str(cal(q))+' kcal   •   '+tm,new[i])
 sec(626,'01','What you need',ac)
 rect(18,588,414,20,ac,4)
 for x,s in [(25,'INGREDIENT'),(234,'1 MEAL'),(299,'3 MEALS'),(365,'4 MEALS')]:t(x,594,s,9,'B',WHITE)
 y=586
 for k,(f,g) in enumerate(q):
  rect(18,y-22,414,22,WHITE if k%2==0 else cl,3);img(icons[f],22,y-21,31,20);t(60,y-15,F[f][0],10.3,'B')
  for x,n in [(235,1),(300,3),(366,4)]:t(x,y-15,str(g*n)+' g',11,'B' if n==1 else 'S')
  y-=22
 y-=28;sec(y,'02','Make one',ac);t(163,y+1,tool,9.4,'S',ac);y-=17
 for k,(hd,body,_) in enumerate(steps):
  sz=11.15;ls=simpleSplit(body,'S',sz,330);bh=max(48,25+len(ls)*13.7)
  rect(18,y-bh,414,bh-2,WHITE,7);img(storyboard[i][k],23,y-bh+4,63,bh-10);t(93,y-16,str(k+1)+'. '+hd,12,'B',ac);lines(93,y-32,body,330,sz,13.7);y-=bh+2
 y-=7
 tm2,prep,serve=notes[i]; rice='R' in dict(q)
 store='Chill rice promptly in shallow boxes. Use within 3–4 days at 4°C or colder. Freeze later portions.' if rice else 'Chill at 4°C or colder. Eat within 3–4 days of the original cooking or prep.'
 rr=[('PREP',prep,art[10]),('SERVE',serve,new[i])]
 if i not in [0,26]:rr.append(('STORE',store,art[13] if rice else art[12]))
 sz=11
 while True:
  lead=sz*1.24;bh=34+sum(max(23,len(simpleSplit(txt,'S',sz,330))*lead)+5 for _,txt,_ in rr)
  if y-bh>=33 or sz<8.4:break
  sz-=.15
 assert y-bh>=30,(name,y,bh)
 rect(18,y-bh,414,bh,cl,9);t(29,y-21,'03   Make 3 or 4',15,'H',ac);t(231,y-19,'BATCH   /   '+tm2,9.1,'B',ac)
 top=y-30
 for lab,txt,im in rr:
  rh=max(23,len(simpleSplit(txt,'S',sz,330))*lead);img(im,24,top-rh,45,rh);lines(88,top-sz,txt,330,sz,lead);top-=rh+5
 if i==24 and y-bh>64:link('Whole chicken oven guide   →',18,35,209,'roast',ac)
 bottom('ch'+str(j),'Meal options')
def teaching(key,title,sub,hero,needs,steps,tag,tip,tipart,col=4):
 cl,ac=colors[col];bg(key,title,0 if key=='start' else 1);titleband(cl,ac,'KITCHEN NOTEBOOK   /   PICTURE GUIDE',title,sub,hero)
 sec(624,'01','What you need',ac)
 for n,(im,caption) in enumerate(needs):
  x=18+n*140;rect(x,493,134,108,WHITE,9);img(im,x+5,520,124,76);t(x+(134-pdfmetrics.stringWidth(caption,'B',10))/2,502,caption,10,'B',ac)
 sec(462,'02','Step by step',ac)
 for n,(im,hd,txt) in enumerate(steps):
  y=445-94*n;rect(18,y-89,414,87,WHITE,7);img(im,22,y-86,78,81);t(107,y-22,str(n+1)+'. '+hd,12.7,'B',ac);lines(107,y-42,txt,313,11.5,14.7)
 rect(18,50,414,104,cl,10);img(tipart,25,63,74,75);t(107,130,tag,14.5,'H',ac);lines(107,108,tip,312,11.3,14.5)
 bottom('menu0' if key=='start' else 'guidemenu','Contents' if key=='start' else 'Prep guide')
def guidemenu():
 bg('guidemenu','Kitchen notebook');t(18,773,'REFERENCE   /   THE PICTURE GUIDES',10,'B',BLUE);t(18,725,'Kitchen notebook',30,'H',BLUE);t(20,691,'Tap a skill when you need it on prep day.',12)
 for n,(name,im,dest) in enumerate([('Rice in a cooker',art[5],'bases'),('Pasta in a pot',art[6],'pasta'),('Air-fryer chicken',art[7],'chicken'),('Lean ground beef',art[8],'beef'),('Roast a whole chicken',bird[0],'roast'),('Three prep days',art[10],'week'),('Cool, store and reheat',art[12],'boxes')]):
  y=588-n*77;rect(18,y,413,66,WHITE,8);img(im,23,y+2,80,61);t(111,y+27,name,16,'H',BLUE);t(394,y+26,'→',14,'B',BLUE);c.linkRect(name,dest,(18,y,431,y+66),thickness=0)
 bottom('menu0','Contents')
cover();menu();starter()
for j in range(5):
 chapter(j)
 for i in chapters[j][3]:card(i,j)
guidemenu();guides();c.save()
