from pathlib import Path
from PIL import Image,ImageOps
import json,io,shutil
base=Path('tmp/waifu'); asset=base/'assets';spec=json.loads((base/'spec.json').read_text()); root=base/'png';root.mkdir(exist_ok=True)
def png(im,path,lim):
 im=im.convert('RGB');im.thumbnail((lim,lim),Image.Resampling.LANCZOS)
 path.parent.mkdir(parents=True, exist_ok=True)
 im.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.FLOYDSTEINBERG).save(path,optimize=True)
def clean(s):return s.replace(' • ',' - ').replace('/','-').strip()
for id,r in spec['recipes'].items():
 name=clean(r['title']);dest=root/('01 - الوصفات')/(id+' - '+name)
 png(Image.open(asset/f'meal{id}.png'),dest/'00 - الطبق.png',840)
 im=Image.open(asset/f'steps{id}.png').convert('RGB');cols=2 if len(r['steps'])<=4 else 3;rows=(len(r['steps'])+cols-1)//cols
 for j,step in enumerate(r['steps']):
  x=j%cols;y=j//cols;w,h=im.size
  bb=(round(x*w/cols)+2,round(y*h/rows)+2,round((x+1)*w/cols)-2,round((y+1)*h/rows)-2)
  png(im.crop(bb),dest/f'{j+1:02} - {clean(step)[:53]}.png',520)
for eng,key in spec['ingkey'].items():png(Image.open(asset/f'{key}.png'),root/'02 - المكونات'/(spec['ing'][eng]+'.png'),500)
other={p.stem for p in asset.glob('*.png') if not p.stem.startswith(('meal','steps'))}-set(spec['ingkey'].values())
for key in other:png(Image.open(asset/f'{key}.png'),root/'03 - مهارات المطبخ'/(key+'.png'),600)
png(Image.open('generated_images/exec-9b50adac-6612-46d7-981e-87bfaca80d78.png'),root/'الغلاف.png',1200)
