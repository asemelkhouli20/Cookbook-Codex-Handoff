from pathlib import Path
s=Path('tmp/ar/build.py').read_text()
s=s.replace('for i in range(74):','removed={18,21,22,31,32,50,51}\nkept=[i for i in range(1,75) if i not in removed]\npageid={i:j+1 for j,i in enumerate(kept)}\nfor i in kept:')
s=s[:s.index('def tx(')]+'''import rtl
def tx(x,y,X,Y,s,size=13,b=False,col=ink,align='right'):
 if s:
  actual=rtl.put(x,y,X,Y,num(s),size,b,rgb(col),align)
  scales.append((actual/size,n,s[:22]))
'''+s[s.index('def pic('):]
s=s.replace('page=dest-1','page=pageid[dest]-1')
a=s.index(' toc[n]=title;');b=s.index('def recipe():',a)
s=s[:a]+''' toc[n]=title
 rect(0,0,450,148,light)
 rect(418,18,432,34,ac,.28)
 tx(112,12,409,39,tag,11,True,ac)
 tx(137 if ref else 20,42,430,106,title,24,True,ink)
 tx(18,111,429,145,subtitle,12,False,ac)
 if ref:
  rect(16,12,123,106,'#ffffff',.15)
  pic(ref,22,16,117,102)
def foot(dest=2):
 rect(0,850,450,890,'#f2eade')
 tx(17,854,60,886,str(pageid[n]),12,True,ac,'center')
 tx(277,854,426,886,'فهرس الوجبات',11,True,ac,'right');link(269,851,434,889,2)
 if dest!=2:
  tx(75,854,258,886,'دليل الحفظ' if dest==64 else 'دليل الطبخ' if dest==56 else 'خيارات هذا الفصل',11,True,ac,'right');link(70,851,265,889,dest)
def bar(y,s):
 rect(16,y,434,y+27,light,.12);rect(427,y+5,431,y+22,ac,.30);tx(24,y,418,y+27,s,13,True,ac)
'''+s[b:]
s=s.replace("idx=re.search('OPTION (\\d+)',a)[1]","idx=sum(1 for i in D if chapter(i)==j and i<=n and i not in removed)")
s=s.replace("'   /   الوصفة '","'    •    وصفة '")
s=s.replace("top=start+rh*k;pic","top=start+rh*k;rect(17,top,433,top+rh-3,'#ffffff',.09,'#ede3d9');pic")
s=s.replace("tx(22,top+4,367,top+rh-4,str(k+1)+'  •  '+st,12.8)","rect(348,top+5,369,top+26,light,.3);tx(348,top+5,369,top+26,str(k+1),10,True,ac,'center');tx(25,top+2,342,top+rh-5,st,12.4)")
s=s.replace("٧١", "٧١").replace("٤٢ وصفة مصوّرة   •   ١٧ خيارًا للفطور","٣٥ وصفة مصوّرة   •   ١٤ خيارًا للفطور").replace("[17,11,2,1,11]","[14,9,2,1,9]").replace("سبع أفكار أخرى للفطور","أربع أفكار أخرى للفطور").replace("صفحة 61","صفحة 54")
s=s.replace('for n in range(1,75):','for n in kept:').replace('p=out[n-1];','p=out[pageid[n]-1];')
s=s.replace('selected=galleries[n];','selected=[i for i in galleries[n] if i not in removed];')
s=s.replace('def btn(','''# Balance each illustrated index across its two facing grids.
galleries[25]=[27,28,29,30,33];galleries[26]=[34,35,36,37]
galleries[43]=[45,46,47,48,49];galleries[44]=[52,53,54,55]
D[45][1]=D[45][1].replace('صفحة 61','صفحة 54')
groups[-1][1].pop();storage[-1]='\\n'.join(storage[-1].splitlines()[:-1])
def btn(''')
s=s.replace('height=min(194,630/math.ceil(len(selected)/2))','height=min(259,625/math.ceil(len(selected)/2))').replace('x=230 if k%2==0 else 18;', 'x=125 if k==len(selected)-1 and len(selected)%2 else 230 if k%2==0 else 18;')
s=s.replace("rect(x,y,x+w,y+height-8,'#ffffff',.10,'#ebdbd0');pic","rect(x,y,x+w,y+height-8,'#ffffff',.10,'#ebdbd0');rect(x+8,y+8,x+34,y+32,light,.30);tx(x+8,y+8,x+34,y+32,str(sum(1 for a in D if a<=i and a not in removed and chapter(a)==j)),10,True,ac,'center');pic")
s=s.replace("tx(97,yy+10,417,yy+h-11,label,16,True,ac)","tx(97,yy+3,413,yy+h-32 if sub else yy+h-9,label,17,True,ac)")
s=s.replace('else:raise ValueError(n)\nout.set_toc','else:raise ValueError(n)\n rtl.showpage(rtl.cr)\nrtl.finish(rtl.surf)\ntextlayer=fitz.open("tmp/ar/text.pdf")\nassert len(textlayer)==len(out)==67\nfor i in range(len(out)):out[i].show_pdf_page(out[i].rect,textlayer,i)\nout.set_toc').replace('else 2,v,i]','else 2,v,pageid[i]]')
s=s.replace("out.subset_fonts();out.save('output/pdf/Weekly_Meal_Cards.pdf'","out.save('tmp/ar/revised.pdf'")
Path('tmp/ar/edition16.py').write_text(s)
