"""Validate generated PNGs and package an honest resumable production checkpoint."""
from pathlib import Path
import json,struct,zlib,zipfile
ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'assets/visuals'
brief=json.loads((ROOT/'visual-rebuild/asset-manifest.json').read_text())
def inspect_png(path):
 data=path.read_bytes(); assert data[:8]==b'\x89PNG\r\n\x1a\n'; offset=8; packed=[]; dimensions=None; end=False
 while offset<len(data):
  size=struct.unpack('>I',data[offset:offset+4])[0];tag=data[offset+4:offset+8];payload=data[offset+8:offset+8+size];crc=struct.unpack('>I',data[offset+8+size:offset+12+size])[0]
  assert zlib.crc32(tag+payload)&0xffffffff==crc,(path,tag)
  if tag==b'IHDR':
   w,h,depth,color,_,_,interlace=struct.unpack('>IIBBBBB',payload);dimensions=(w,h,depth,color,interlace)
  if tag==b'IDAT':packed.append(payload)
  if tag==b'IEND':end=True
  offset+=size+12
 assert end and dimensions
 decoded=zlib.decompress(b''.join(packed));assert decoded
 return dimensions
manifest=[]
for entry in brief:
 path=folder/entry['file'];record=dict(entry,status='pending',width=None,height=None,mode=None,recipe_id=None,step_number=None,notes='Not generated yet.')
 parts=Path(entry['file']).parts
 if parts[0]=='recipes':
  record['recipe_id']=int(parts[1]);record['step_number']=int(Path(parts[2]).stem.split('-')[1]) if parts[2].startswith('step-') else None
 if path.exists():
  w,h,depth,color,interlace=inspect_png(path)
  record.update(status='generated',width=w,height=h,mode={2:'RGB',6:'RGBA',0:'L',4:'LA',3:'P'}[color],notes=f'Generated individually using built-in image_gen; visual QA remains provisional. Actual native output {w}×{h}; no upscaling. PNG chunk CRCs and compressed pixel data validated.')
 manifest.append(record)
(folder/'asset-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
done=[r for r in manifest if r['status']=='generated']
readme=f'''# Cozy anime cookbook — production checkpoint — usage limit

PARTIAL COLLECTION: {len(done)} of {len(manifest)} PNGs generated; {len(manifest)-len(done)} pending. This archive is not the complete visual rebuild.

## Art direction and identity

Soft painterly slice-of-life anime, warm oat paper, terracotta apron, sage/olive accents, soft window light. The canonical chef is an adult woman age 25, chestnut low ponytail with olive ribbon, brown eyes, cream rolled sleeves, terracotta apron, olive skirt and brown flats. Reuse character/chef-front.png as the actual identity reference for later generations.

## Completed files and native dimensions

'''+''.join(f'- `{r["file"]}` — {r["width"]} × {r["height"]}, {r["mode"]}\n' for r in done)+'''
Image color modes are listed above; RGBA assets preserve their generated alpha channel. They were generated separately with the built-in image_gen tool, not extracted from a grid, and were not upscaled. Output resolution follows actual generator results rather than requested target dimensions. Textures and decorative cutouts are included. Texture repeat seams and actual alpha coverage still need final QA.

## Validation

Images were reviewed during production, but final visual QA is incomplete. Known corrections: remove unlisted breakfast toppings from site/breakfast.png; correct extra hands or floating pouring bowls in recipes/11/step-03.png and recipes/27/step-05.png. These remain generated drafts until corrected. PNG signatures, every chunk CRC, IHDR dimensions, IEND marker, and zlib pixel-data decoding were checked. Keep checking identity, hands, ingredients and continuity in future batches. The manifest records all 356 expected paths with honest status.

## Website integration

Files are retained at assets/visuals/ in the project. The homepage asset is site/home-hero.png; it has the chef/food at left and a quiet right-hand region. The existing website has not yet been switched to this new image set. Preserve recipe text and quantities. Later recipe covers map to source/book.json recipes[].hero; steps map to steps[].img; guides map to guides[].img. Paths should begin assets/visuals/ when installed. Then rebuild with python3 scripts/build.py and run python3 scripts/check.py.

## Resume

Follow visual-rebuild/prompt.md and this manifest. The exact remaining asset briefs are saved in pending-assets.json. Generation stopped at the built-in account usage limit, reported to reset on 2026-11-05 at 14:03:22 Asia/Riyadh. Do not regenerate completed character references unnecessarily. Finish the remaining site illustrations, textures, decorative assets, recipe covers and 288 step images, then the ten kitchen guides. Perform final texture tiling, alpha, ingredient, anatomy, and recipe continuity checks. A final consolidated ZIP is still required after production is complete.

The precise prompt set is preserved in visual-rebuild/prompt.md and visual-rebuild/asset-manifest.json.
'''
(folder/'README.md').write_text(readme)
(folder/'pending-assets.json').write_text(json.dumps([r for r in manifest if r['status']=='pending'],ensure_ascii=False,indent=2))
archive=ROOT/'cozy-anime-cookbook-checkpoint.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for r in done:z.write(folder/r['file'],r['file'])
 for name in ['README.md','asset-manifest.json','pending-assets.json']:z.write(folder/name,name)
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(f'Validated and packaged {len(done)} PNGs; {len(manifest)-len(done)} pending: {archive.name}')
