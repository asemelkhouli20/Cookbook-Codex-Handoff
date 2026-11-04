from pathlib import Path
from PIL import Image,ImageDraw
sources=sorted(Path('tmp/waifu/assets').glob('steps*.png'),key=lambda p:int(p.stem[5:]))
for m in range(0,len(sources),9):
 subset=sources[m:m+9];sheet=Image.new('RGB',(1080,330*((len(subset)+2)//3)),'#fff');dr=ImageDraw.Draw(sheet)
 for i,p in enumerate(subset):
  im=Image.open(p);im.thumbnail((345,296));x=360*(i%3);y=(i//3)*330;sheet.paste(im,(x,y));dr.text((x+3,y+299),p.stem,fill='#211')
 sheet.save(f'tmp/waifu/proof-{m}.jpg',quality=83)
