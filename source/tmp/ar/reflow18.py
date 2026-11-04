from pathlib import Path
s=Path('tmp/ar/edition17.py').read_text()
a=s.index(' total=len(actiondata[n])');b=s.index('pages=[',a)
s=s[:a]+''' return [(0,len(actiondata[n]))] if n==42 else [(0,0),(0,len(actiondata[n]))]
'''+s[b:]
a=s.index('  half=min(');b=s.index('  if key.startswith',a)
s=s[:a]+'''  half=min(42,(height-16)/2);cy=y+(height-7)/2;box=(355,cy-half,423,cy+half)
'''+s[b:]
s=s.replace('rect(284,y+10,313,y+37,light,.30)','rect(319,cy-12,345,cy+12,light,.30)').replace('tx(284,y+10,313,y+37','tx(319,cy-12,345,cy+12').replace('tx(25,y+5,277,y+height-12,word,15)','tx(26,y+3,309,y+height-10,word,14.5)')
a=s.index(' if part:tag+=');b=s.index(' rows=re.findall',a)
s=s[:a]+''' if part:
  rect(0,0,450,98,light)
  tx(18,7,431,33,tag+'    /    طريقة التحضير',11,True,ac)
  tx(18,34,431,89,name,23,True,ink)
 else:header(name,tag,ims[0],kcal+' سعرة تقريبًا للحصة   •   '+tm)
'''+s[b:]
a=s.index("  bar(y,'طريقة التحضير");b=s.index(" bt=timear",a)
s=s[:a]+'''  if n==42:
   bar(y,'طريقة التحضير');actioncards(0,en,y+35,650,rows,ims)
  else:
   bar(y,'أدوات المطبخ')
   tx(22,y+30,430,y+70,tools,14)
   if n==45:
    tx(18,y+70,430,y+100,'افتح دليل شواء الدجاجة الكاملة',13,True,ac);link(18,y+70,430,y+100,61)
 else:
  tx(18,101,431,134,'اتبع الخطوات من ١ إلى '+str(en),13,True,ac)
  actioncards(st,en,138,803,rows,ims)
  rect(17,807,433,841,light,.19);tx(20,807,430,841,'العودة إلى المقادير والكميات',12,True,ac,'center')
  link(17,807,433,841,n)
  foot(starts[j]);return
'''+s[b:]
a=s.index(' bt=timear');b=s.index(' foot(starts[j])',a)
s=s[:a]+s[a:b].replace("bar(674,","bar(663 if n==42 else 559,").replace("tx(24,714,425,785,batch,12.5)","tx(24,694 if n==42 else 594,425,777 if n==42 else 687,batch,14)").replace("rect(18,792,432,842,'#f4f0e3',.14);tx(25,800,425,839,limit,11,False,muted)","""by=784 if n==42 else 696
 rect(18,by,432,by+59,'#f4f0e3',.14);tx(25,by+3,425,by+55,limit,12,False,muted)
 if n!=42:
  rect(17,784,433,838,ac,.15);tx(20,784,430,838,'افتح خطوات التحضير المصوّرة   ←',15,True,'#ffffff','center')
  p.insert_link({'kind':1,'from':fitz.Rect(17,784,433,838),'page':physical})""")+s[b:]
s=s.replace("tmp/ar/steps_complete.pdf","tmp/ar/layout_fixed.pdf")
Path('tmp/ar/edition18.py').write_text(s)
