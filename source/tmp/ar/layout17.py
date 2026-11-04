from pathlib import Path
s=Path('tmp/ar/edition16.py').read_text()
start=s.index('pageid=');end=s.index('src=open',start)
s=s[:start]+'''from steps17 import steps as actiondata,art
def portions(n):
 total=len(actiondata[n])
 if n==42:return [(0,total)]
 # Start beside the ingredients, then balance subsequent pages at legible size.
 first=3
 rem=total-first;cnt=(rem+5)//6
 q,r=divmod(rem,cnt)
 size=[first]+[q+int(j<r) for j in range(cnt)]
 return [(sum(size[:j]),sum(size[:j+1])) for j in range(len(size))]
pages=[(n,k) for n in kept for k in range(len(portions(n)) if n in actiondata else 1)]
pageid={n:pages.index((n,0))+1 for n in kept}
for i in pages:out.new_page(width=450,height=890)
'''+s[end:]
s=s.replace('str(pageid[n]),12','str(physical),12')
a=s.index('def recipe():');b=s.index(" nums=re.findall",a)
s=s[:a]+'''def actioncards(st,en,top,bottom,rows,ims):
 height=(bottom-top)/(en-st)
 for ix in range(st,en):
  key,word=actiondata[n][ix];y=top+(ix-st)*height
  rect(16,y,434,y+height-7,'#ffffff',.10,'#e4d8cd')
  half=min(53,(height-15)/2);cy=y+(height-7)/2;box=(321,cy-half,423,cy+half)
  if key.startswith('@'):
   ingr=key[1:];ref=ims[1+[r[0] for r in rows].index(ingr)]
   pic(ref,*box)
  elif key=='=':pic(ims[0],*box)
  else:p.insert_image(box,stream=art[key])
  rect(284,y+10,313,y+37,light,.30)
  tx(284,y+10,313,y+37,str(ix+1),13,True,ac,'center')
  tx(25,y+5,277,y+height-12,word,15)
  assert scales[-1][0]>=.92,(n,ix,word,scales[-1])
  seen.append((n,ix))
def recipe():
 a=src[n-1];name,*_,batch=D[n]; ims=imgs(n);kcal,tm=values(n);j=chapter(n)
 idx=sum(1 for i in D if chapter(i)==j and i<=n and i not in removed)
 chunks=portions(n);st,en=chunks[part];last=part==len(chunks)-1
 tag=ch[j]+'   •   وصفة '+str(idx)
 if part:tag+='   •   تابع التحضير'
 header(name,tag,ims[0], ('الخطوات '+str(st+1)+' إلى '+str(en)+' من '+str(len(actiondata[n]))) if part else kcal+' سعرة تقريبًا للحصة   •   '+tm)
'''+s[b:]
a=s.index(' nums=re.findall');b=s.index(' bt=timear',a)
old=s[a:b]
rows=old[old.index(' rows=re.findall'):old.index(' tx(217,263')]
nut=old[:old.index(' rows=re.findall')]+old[old.index(' tx(217,263'):old.index(" bar(y,'طريقة التحضير'")]
s=s[:a]+rows+' if part==0:\n'+''.join(' '+l+'\n' for l in nut.splitlines())+'''  tools='، '.join(uten[v.strip().lower()] for v in a.split('Make one')[1].split('\\n')[0].strip().split(','))
  bar(y,'طريقة التحضير  •  '+str(len(actiondata[n]))+' خطوات')
  tx(20,y+30,425,y+55,'الأدوات: '+tools,11,False,muted)
  if n==45:
   tx(18,y+55,430,y+81,'افتح دليل شواء الدجاجة الكاملة',12,True,ac);link(18,y+55,430,y+81,61);y+=28
  top=y+58
 else:
  bar(163,'طريقة التحضير  •  تابع من الخطوة '+str(st+1))
  top=203
 actioncards(st,en,top,665 if last else 797,rows,ims)
 if not last:
  rect(17,802,433,841,ac,.20);tx(22,802,428,841,'تابع إلى الخطوة '+str(en+1)+'   ←',14,True,'#ffffff','center')
  p.insert_link({'kind':1,'from':fitz.Rect(17,802,433,841),'page':physical})
  foot(starts[j]);return
'''+s[b:]
s=s.replace('for n in kept:\n p=out[pageid[n]-1];','seen=[]\nfor physical,(n,part) in enumerate(pages,1):\n p=out[physical-1];')
s=s.replace('assert len(textlayer)==len(out)==67','assert len(textlayer)==len(out)==len(pages)\nassert seen==[(i,k) for i in kept if i in actiondata for k in range(len(actiondata[i]))]')
s=s.replace("out.save('tmp/ar/revised.pdf'","out.save('tmp/ar/steps_complete.pdf'")
Path('tmp/ar/edition17.py').write_text(s)
