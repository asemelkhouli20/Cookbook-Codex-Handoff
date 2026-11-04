from pathlib import Path
src=Path('tmp/finalbook/cute.py').read_text()
src=src[:src.index('cover();menu();starter();nutritionguide()')]
src=src.replace("'[active]","'[active]") # Preserve every existing recipe and hint.
src=src.replace("][active]","][active] if active<33 else 'Stir tonight. Breakfast is ready tomorrow.'")
# Existing first card receives the same practical oat reminder.
exec(src)
import csv
from nutrientcalc import data,NID
ASSETS.update(__import__('json').loads(Path('tmp/cutebook/oatassets.json').read_text()))
oatart=pieces('oats',5,2)
fruitart=pieces('fruit',3,3)
icons.update(dict(zip(['apple','strawberry','blueberry','mango','raspberry','cinnamon','vanilla','water','jar'],fruitart)))
exec(Path('tmp/finalbook/oatvariants.py').read_text())
# Amend the two cover count badges without changing the cover artwork.
cover_src=src[src.index('def cover():'):src.index('def nutritionguide():')]
cover_src=cover_src.replace('33 picture recipes','42 picture recipes').replace('8 breakfasts','17 breakfasts')
exec(cover_src)
def chapter(j):
 title,when,desc,ids=chapters[j];cl,ac=colors[j]
 if j==0:
  chunks=[oatids[:6],oatids[6:],ids[10:]]
 else:chunks=[ids] if len(ids)<=8 else [ids[:6],ids[6:]]
 for k,subset in enumerate(chunks):
  dest='ch'+str(j)+(str(k) if k else '')
  bg(dest,str(j+1)+'. '+title if not k else title+' • more options',int(k>0))
  rect(0,656,W,156,cl);t(20,778,f'CHAPTER 0{j+1}   /   {when.upper()}',10,'B',ac);line(20,762,407,ac)
  heading='Breakfast' if j!=0 or k!=2 else 'Other breakfasts'
  t(18,712,heading,37,'H',ac);star(390,736,8,ac);scallop(655,cl)
  caption=('Overnight oats 01–06  •  mix, chill, enjoy' if k==0 else 'Overnight oats 07–10  •  more fruit combinations') if j==0 and k<2 else desc
  t(20,678,caption,11.5,'S',ac)
  rows=(len(subset)+1)//2;rh=min(182,565/rows)
  for ni,i in enumerate(subset):
   x=18+210*(ni%2);top=641-int(ni/2)*rh;ww=203;hh=rh-7
   rect(x+1.5,top-hh-1.5,ww,hh,'#E7DCD3',12);rect(x,top-hh,ww,hh,WHITE,12);tape(x+8,top-8,cl)
   img(new[i],x+4,top-hh+48,ww-8,hh-53)
   name=meals[i][0].replace(' overnight oats','') if i in oatids else meals[i][0];ns=12
   while len(simpleSplit(name,'B',ns,ww-16))>2:ns-=.2
   lines(x+8,top-hh+35,name,ww-16,ns,13,'B',ac);t(x+8,top-hh+6,'~'+str(cal(meals[i][1]))+' kcal   /   '+meals[i][2],8.5,'S',INK)
   c.linkRect(name,'r'+str(i),(x,top-hh,x+ww,top),thickness=0)
  if k+1<len(chunks):link('More breakfast choices  →' if j==0 else 'More meal choices  →',18,38,230,'ch'+str(j)+str(k+1),ac)
  else:link('First choices  →',18,38,170,'ch'+str(j),ac)
  bottom('menu0','All chapters')
# Our nine additional oat cards are covered by the same layout.
# Original card draws the third row for storage when appropriate.
oat_original_card=card
def card(i,j):
 if i in oatids:
  oldnotes=notes[i]
  # The recipe's standard panel includes chilled storage. All preparation is done the night before eating.
  notes[i]=(oldnotes[0],oldnotes[1],oldnotes[2])
 oat_original_card(i,j)
cover();menu();starter();nutritionguide()
for j in range(5):
 chapter(j)
 for i in chapters[j][3]:
  active=i;card(i,j);active=None
guidemenu();guides();c.save()
