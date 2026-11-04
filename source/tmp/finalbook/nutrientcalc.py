from pathlib import Path
import csv
NID=dict(kcal=1008,protein=1003,carbs=1005,fat=1004,fiber=1079,calcium=1087,iron=1089,potassium=1092,vitc=1162)
foods=dict(C=171477,B=171790,T=173709,K=173801,W=175203,D=173735,R=168878,P=169737,X=167535,O=173904,U=168409,L=169249,A=170393,E=170108,S=169214,H=174289,Z=170886,J=167747,I=171413,M=172234,Y=174277,N=173944,V=171450,Q=172796,garlic=169230)
hits={n:{} for n in foods.values()}
for row in csv.DictReader(next(Path('tmp/food-nutrients').rglob('food_nutrient.csv')).open()):
 f,n=int(row['fdc_id']),int(row['nutrient_id'])
 if f in hits and n in NID.values():hits[f][n]=float(row['amount'])
for k,v in foods.items():
 miss=set(NID.values())-hits[v].keys()
 if miss:print('nutrient unavailable',k,miss)
data={k:{key:hits[f].get(n) for key,n in NID.items()} for k,f in foods.items()}
data['G']={key:(data['Z'][key]*.98+data['garlic'][key]*.02) for key in NID}
def nutr(q):
 return {n:sum(data[k][n]*w/100 for k,w in q) if all(data[k][n] is not None for k,w in q) else None for n in NID}
def cal(q):return int(round(nutr(q)['kcal']/5)*5)
