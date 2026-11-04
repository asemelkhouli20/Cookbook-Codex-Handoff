from pathlib import Path
p=Path('tmp/ar/edition20.py');s=p.read_text()
a=s.index('ink=');b=s.index('def rect',a)
s=s[:a]+"""ink='#362840';plum='#704174';muted='#66566d';paper='#fffaf6';accents=['#a42659','#137369','#865421','#67519d','#376897','#23675e'];tints=['#ffdae5','#c9efe2','#ffebac','#e5d9ff','#d3eafa','#d3f1e9']
"""+s[b:]
s=s.replace("'#f2eade'","'#e5f4e9'").replace("'#fff1df'","'#fff0bc'").replace("'#faf0e6'","'#f1faef'").replace("'#f4f0e3'","'#e8f6eb'").replace("'#eaded4'","'#ddc8db'").replace("'#ebdbd0'","'#e4bfd0'")
a=s.index('def actioncards');b=s.index('def portrait',a)
s=s[:a]+"""def scene(key,box):
 p.insert_image(box,stream=art[key])
def actioncards(st,en,top,bottom,rows,ims):
 count=en-st
 linecount=(count+1)//2
 height=min(188,(bottom-top)/linecount)
 for ix in range(st,en):
  pos=ix-st;key,word=actiondata[n][ix]
  x=229 if pos%2==0 else 16
  y=top+(pos//2)*height;w=205
  rect(x,y,x+w,y+height-5,'#ffffff',.07,'#dabdd1')
  caption=min(57,height*.43)
  picbox=(x+19,y+3,x+w-19,y+height-caption-6)
  if key.startswith('@'):scene(ingkey[key[1:]],picbox)
  elif key=='=':portrait(n,picbox)
  else:scene(key,picbox)
  rect(x+w-32,y+5,x+w-6,y+30,ac,.39);tx(x+w-32,y+5,x+w-6,y+30,str(ix+1),13,True,'#ffffff','center')
  tx(x+8,y+height-caption-4,x+w-8,y+height-8,word,14,False,ink,'center')
  assert scales[-1][0]>.78,(n,ix,scales[-1])
  seen.append((n,ix))
"""+s[b:]
s=s.replace("pic(ims[1+k],399,y+2,428,y+23)","scene(ingkey[ingredient_key],(386,y+1,431,y+29))").replace('y=285+k*26','y=281+k*30').replace("433,y+25,","433,y+29,").replace('212,y+1,393,y+24','210,y+1,382,y+28').replace('x+66,y+25,v','x+66,y+29,v').replace('293+len(rows)*26','286+len(rows)*30')
s=s.replace("'اتبع الخطوات من ١ إلى '+str(en)","'ابدأ من اليمين   •   '+str(en)+' مشاهد مصوّرة'").replace("rect(0,0,450,98,light)","rect(0,0,450,98,light);portrait(n,(8,5,92,90))").replace('tx(18,34,431,89,name','tx(96,34,431,89,name')
s=s.replace("'المقادير بالجرام'","'جهّز المكوّنات   •   الوزن بالجرام'").replace("'الأدوات: '+tools","tools").replace("tx(18,106,432,188,'شوكة وملعقة',38","tx(18,90,432,174,'شوكة وملعقة',38").replace("'كتاب الطبخ المصوّر للمبتدئين'","'مطبخ الأنمي المصوّر'").replace("'وجبات سهلة من الفطور إلى ما بعد التمرين'","'اطبخ معي خطوة بخطوة'").replace("tx(30,192,420,239","tx(30,172,420,211").replace("tx(30,245,420,285","tx(30,218,420,257")
s=s.replace("coverdoc=fitz.open('tmp/ar/anime.pdf');p.insert_image(p.rect,stream=coverdoc.extract_image(coverdoc[0].get_images()[0][0])['image'],keep_proportion=False)","p.insert_image(p.rect,stream=coverbytes,keep_proportion=False)")
s=s.replace("pic(ref,22,16,117,102)","scene(guidekeys.get(n,['ref8'])[0],(22,16,117,102))")
s=s.replace('if k<len(refs):pic(refs[k],20,top+12,94,top+ht-20)','if k<len(refs):scene(guidekeys[n][k],(20,top+12,94,top+ht-20))')
s=s.replace("pic(ref,23,yy+3,90,yy+h-8);","(portrait([8,27,39,42,45][k],(23,yy+3,90,yy+h-8)) if n==2 else scene(guidekeys[dest][0],(23,yy+3,90,yy+h-8)));")
s=s.replace("pic(imgs(n)[k+1],396,y+5,429,y+38)","scene(storeart[gi][k],(394,y+4,430,y+40))")
s=s.replace("rect(16,y,434,y+27,light,.12);rect(427,y+5,431,y+22,ac,.30);tx(24,y,418,y+27,s,13,True,ac)","rect(16,y,434,y+27,ac,.25);tx(24,y,424,y+27,s,13,True,'#ffffff')")
a=s.index("with ZipFile(");b=s.index("seen=[]",a)
s=s[:a]+"""for i in sorted(actiondata):
 im=Image.open(f'tmp/ar/mealart/{i}.png').convert('RGBA');im=im.crop(im.getchannel('A').getbbox());im.thumbnail((330,330));buf=io.BytesIO();im.save(buf,'PNG');portraits[i]=buf.getvalue()
exec(Path('tmp/ar/manga/assets.py').read_text())
"""+s[b:]
s=s.replace('tmp/ar/meal_cute.pdf','tmp/ar/manga/big.pdf')
Path('tmp/ar/edition22.py').write_text(s)
