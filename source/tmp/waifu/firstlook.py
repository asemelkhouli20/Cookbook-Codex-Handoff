from pathlib import Path
s=Path('tmp/ar/newedition.py').read_text()
import sys
sys.path.insert(0,'tmp/ar')
exec(s[:s.index("meta=json.loads")])
n=8; part=1;physical=pages.index((n,1))+1;seen=[];p=out[physical-1];ac=accents[0];light=tints[0]
import json,io
spec=json.loads(Path('tmp/waifu/spec.json').read_text())
im=Image.open('tmp/waifu/assets/steps8.png');w,h=im.size
def buff(im):
 b=io.BytesIO();im.save(b,'JPEG',quality=76);return b.getvalue()
stepart={(8,j):buff(im.crop((int(j%3*w/3)+2,int(j//3*h/4)+2,int((j%3+1)*w/3)-2,int((j//3+1)*h/4)-2))) for j in range(10)}
portraits={8:buff(Image.open('tmp/waifu/assets/meal8.png').convert('RGB'))};actiondata[8]=[('single',v) for v in spec['recipes']['8']['steps']]
rect(0,0,450,890,paper);recipe();rtl.showpage(rtl.cr);rtl.finish(rtl.surf)
t=fitz.open('tmp/ar/text.pdf');p.show_pdf_page(p.rect,t,0);p.get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save('/mnt/data/How-To-Banana-Oats.png')
