import sys,json
sys.path.insert(0,'tmp/ar')
ns={}
exec(open('tmp/ar/edition22.py').read().split('seen=[]')[0],ns)
rows={}
for k in sorted(ns['actiondata']):
 s=ns['src'][k-1].split('4 MEALS')[1].split('Make one')[0]
 import re
 rows[str(k)]={'title':ns['D'][k][0],'steps':[w for _,w in ns['actiondata'][k]],'ing':[v[0] for v in re.findall(r'^\s*(\S.*?)\s{2,}(\d+)\s*g\s+(\d+)\s*g\s+(\d+)\s*g\s*$',s,re.M)]}
json.dump({'recipes':rows,'ing':ns['ingredient'],'guidekeys':ns['guidekeys'],'storeart':ns['storeart'],'ingkey':ns['ingkey']},open('tmp/waifu/spec.json','w'),ensure_ascii=False)
