from PIL import ImageChops
for prefix,cols,nr in [('f',4,3),('v',4,3),('c',4,3),('h',4,3),('e',4,4),('ia',4,3),('ib',4,3),('ic',3,3),('ref',3,3)]:
 im=Image.open(f'tmp/ar/manga/{prefix}.png').convert('RGB');w,h=im.size
 for ix in range(cols*nr):
  x,y=ix%cols,ix//cols
  cell=im.crop((round(w*x/cols)+2,round(h*y/nr)+2,round(w*(x+1)/cols)-2,round(h*(y+1)/nr)-2))
  bb=ImageChops.difference(cell,Image.new('RGB',cell.size,'white')).convert('L').point(lambda v:255 if v>40 else 0).getbbox()
  if bb:cell=cell.crop(bb)
  cell.thumbnail((255,240));buf=io.BytesIO();cell.save(buf,'JPEG',quality=82,optimize=True);art[prefix+str(ix+1)]=buf.getvalue()
ingkey=dict(zip(ens.split('|'),[f'ia{i}' for i in range(1,13)]+[f'ib{i}' for i in range(1,13)]+['ic1','ic2','ic3','ic4','ic5','ic6','ic7','ic9','ic8']))
guidekeys={3:['ref1','ref1','ref2','ref1'],4:['ref1','ia6','ref2','ref1'],57:['ref4','ref4','ref1','ref2'],58:['ref5','ref5','ref1','ref2'],59:['e4','ref6','ref3','ref2'],60:['ref1','e11','ref3','ref2'],61:['ref7','ref3','h12','e9'],62:['ref7','ref5','c1','ref2'],63:['ref8','ref9','ref3','ref2'],73:['f8','ref2','ref8','ref9']}
storeart=[['ia11','ia7','e11','ic7','ref8','ic1'],['ia10','ia9','ic2','ib2','ic3'],['ia8','ic8','ia4','ic6'],['ia12','ib7','ia6','ia3','h2','e8'],['ia2','ia1','ic5','ia5','ib8','ib12'],['ib11','ib3','ib5','ib5','ib6','c5'],['ib9','ic4','ib10','ib4','ic9','ib1'],['f7','e3']]
for line in Path('tmp/ar/manga/short').read_text().splitlines():
 ns,ss=line.split(' ',1);i=int(ns);words=ss.split('|');assert len(words)==len(actiondata[i]);actiondata[i]=[(key,w) for (key,_),w in zip(actiondata[i],words)]
variants={9:['f2','f4','v10','f4'],10:['v1','v2','v3','v4'],11:['v5','v6'],12:['v7','v8','v9'],13:['f1','f5','v1','v4'],14:['v11','f4','v10','v6'],15:['v7','v9','v1','v4'],17:['v11','v4','v12']}
for i in range(8,18):
 front=actiondata[i][:-7]
 if i in variants:front=[(k,s) for k,(_,s) in zip(variants[i],front)]
 flavor='القرفة' if i in (9,16) else 'الفانيلا'
 actiondata[i]=front+list(zip(['f6','f7','f8','f9','f10','f7','f11'],['ضع الشوفان والزبادي والماء و'+flavor+' في مرطبان نظيف سعة 500 مل.','حرّك حتى يبتلّ الشوفان كله.','أضف الفاكهة وقلّب برفق.','أغلق الغطاء بإحكام.','برّد 8 ساعات على الأقل عند 4°م أو أقل.','قلّب الشوفان صباحًا.','إذا ثقل القوام، أضف ملعقة ماء. تناوله باردًا.']))
 D[i][-1]='لكل مرطبان 50 غ شوفان و50 غ ماء. أضف حصة الزبادي والفاكهة والنكهة، وبرّد 8 ساعات. تُحفظ القاعدة حتى 3 أيام؛ أضف الفاكهة عند الأكل لقوام أفضل.'.replace('؛','.')
cover=Image.open('tmp/ar/manga/cover.png').convert('RGB');cover=ImageOps.fit(cover,(760,1500));buf=io.BytesIO();cover.save(buf,'JPEG',quality=86);coverbytes=buf.getvalue()
