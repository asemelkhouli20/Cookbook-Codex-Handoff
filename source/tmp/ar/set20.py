from pathlib import Path
s=Path('tmp/ar/edition18.py').read_text()
pos=s.index('def recipe():')
s=s[:pos]+'''def portrait(i,box):
 p.insert_image(box,stream=portraits[i])
def mealheader(name,tag,kcal,tm):
 toc[n]=name
 rect(0,0,450,151,light)
 portrait(n,(4,3,157,146))
 tx(162,9,430,37,tag,11,True,ac)
 tx(162,38,430,108,name,22,True,ink)
 tx(161,109,429,145,kcal+' سعرة للحصة   •   '+tm,11.5,False,ac)
'''+s[pos:]
s=s.replace('else:header(name,tag,ims[0],kcal+\' سعرة تقريبًا للحصة   •   \'+tm)','else:mealheader(name,tag,kcal,tm)')
s=s.replace('pic(imgs(i)[0],x+12,y+4,x+w-12,y+height-67)','portrait(i,(x+29,y+4,x+w-29,y+height-67))')
s=s.replace("seen=[]","from PIL import Image,ImageOps\nfrom zipfile import ZipFile\nimport io\nportraits={}\nwith ZipFile('output/Meal_Illustrations_PNG.zip','w') as pack:\n for pos,i in enumerate(sorted(actiondata),1):\n  im=Image.open(f'tmp/ar/mealart/{i}.png').convert('RGBA'); bbox=im.getchannel('A').point(lambda v:255 if v>15 else 0).getbbox()\n  assert bbox is not None\n  im=im.crop(bbox);im.thumbnail((820,820),Image.Resampling.LANCZOS);im=ImageOps.expand(im,border=12,fill=(0,0,0,0))\n  buf=io.BytesIO();im.save(buf,'PNG',optimize=True);name=D[i][0].replace(' • ',' - ');pack.writestr(f'{pos:02d} - {name}.png',buf.getvalue())\n  im.thumbnail((500,500),Image.Resampling.LANCZOS);buf=io.BytesIO();im.save(buf,'PNG');portraits[i]=buf.getvalue()\nseen=[]")
s=s.replace("p.insert_image(p.rect,stream=d.extract_image(imgs(1)[0])['image'],keep_proportion=False)","coverdoc=fitz.open('tmp/ar/anime.pdf');p.insert_image(p.rect,stream=coverdoc.extract_image(coverdoc[0].get_images()[0][0])['image'],keep_proportion=False)")
s=s.replace("tmp/ar/layout_fixed.pdf","tmp/ar/meal_cute.pdf")
Path('tmp/ar/edition20.py').write_text(s)
