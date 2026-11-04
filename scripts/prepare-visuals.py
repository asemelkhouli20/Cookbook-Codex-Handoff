"""Create compact website copies; preserve original generated PNGs untouched."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'assets/visuals'
target=ROOT/'assets/web-visuals'
def convert(path):
 out=target/path.relative_to(source).with_suffix('.webp')
 if out.exists() and out.stat().st_mtime>=path.stat().st_mtime:return
 out.parent.mkdir(parents=True,exist_ok=True)
 subprocess.run(['cwebp','-quiet','-q','83','-resize','960','0',str(path),'-o',str(out)],check=True)
paths=list(source.rglob('*.png'))
with ThreadPoolExecutor(max_workers=5) as pool:list(pool.map(convert,paths))
print(f'Prepared {len(paths)} web images; original PNGs preserved.')
