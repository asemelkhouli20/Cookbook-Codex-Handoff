# Supplements the existing USDA-based ingredient lookup.
extrafoods={'apple':171688,'strawberry':167762,'blueberry':171711,'mango':169910,'raspberry':167755,'cinnamon':171320,'vanilla':173471}
ex={v:{} for v in extrafoods.values()}
for row in csv.DictReader(next(Path('tmp/food-nutrients').rglob('food_nutrient.csv')).open()):
 f,n=int(row['fdc_id']),int(row['nutrient_id'])
 if f in ex and n in NID.values():ex[f][n]=float(row['amount'])
for k,f in extrafoods.items():
 data[k]={key:ex[f].get(n,0) for key,n in NID.items()}
data['water']={key:0 for key in NID}
F.update({'apple':('Apple, cored',data['apple']['kcal']),'strawberry':('Strawberries, trimmed',data['strawberry']['kcal']),'blueberry':('Blueberries',data['blueberry']['kcal']),'mango':('Mango flesh',data['mango']['kcal']),'raspberry':('Raspberries',data['raspberry']['kcal']),'cinnamon':('Ground cinnamon',data['cinnamon']['kcal']),'vanilla':('Vanilla extract',data['vanilla']['kcal']),'water':('Drinking water',0)})
# All recipes use rolled oats, plain low-fat yogurt and water.
specs=[
 ('Banana vanilla overnight oats',[('N',100)],('vanilla',1),'Peel the banana. Mash half with a fork and cut the rest into rounds.','banana'),
 ('Apple cinnamon overnight oats',[('apple',100)],('cinnamon',1),'Wash the apple and cut away the core. Grate half and dice the rest into tiny pieces. Leave the skin on.','apple'),
 ('Strawberry vanilla overnight oats',[('strawberry',120)],('vanilla',1),'Rinse strawberries under running water. Remove the green tops. Mash half with a fork and slice the rest.','strawberry'),
 ('Blueberry vanilla overnight oats',[('blueberry',100)],('vanilla',1),'Rinse and drain the blueberries. Crush half with a fork to release their juice. Keep the rest whole.','blueberry'),
 ('Mango vanilla overnight oats',[('mango',100)],('vanilla',1),'Use peeled mango flesh with the stone removed. Mash half with a fork and dice the rest into small cubes.','mango'),
 ('Banana strawberry overnight oats',[('N',50),('strawberry',70)],('vanilla',1),'Peel and mash the banana. Rinse the strawberries, remove the green tops and cut into small pieces.','strawberry'),
 ('Apple blueberry overnight oats',[('apple',60),('blueberry',60)],('vanilla',1),'Wash both fruits. Core and finely grate the apple. Gently crush half the blueberries with a fork.','apple'),
 ('Mango strawberry overnight oats',[('mango',60),('strawberry',60)],('vanilla',1),'Dice peeled mango flesh. Rinse the strawberries, remove their green tops and chop into small pieces.','mango'),
 ('Banana cinnamon overnight oats',[('N',100)],('cinnamon',1),'Peel the banana. Mash half until soft and cut the rest into rounds.','banana'),
 ('Mixed berry overnight oats',[('strawberry',40),('blueberry',40),('raspberry',40)],('vanilla',1),'Rinse and drain all berries. Remove strawberry tops and chop. Gently crush the raspberries with a fork.','raspberry')]
oatids=[]
for n,(name,fruit,flavor,prep,hero) in enumerate(specs):
 i=0 if n==0 else len(meals);oatids.append(i)
 q=[('O',50),('Z',200),('water',50),*fruit,flavor]
 # Flavor amounts are per jar. Vanilla and cinnamon are also included in nutrition.
 fword='vanilla' if flavor[0]=='vanilla' else 'cinnamon'
 steps=[('Prepare the fruit',prep,''),('Stir the base',f'In a clean 500 ml jar, stir oats, yogurt, water and {fword} until no dry oat flakes remain. Stir in the mashed or grated fruit, then fold in the pieces.',''),('Chill overnight','Close the lid and refrigerate at 4°C or colder for at least 8 hours. In the morning, stir well. Add a spoonful of water if too thick. Eat cold.','')]
 entry=(name,q,'5–8 min + overnight','500 ml jar, fork, spoon',steps)
 if n==0:meals[0]=entry
 else:meals.append(entry);new.append(oatart[n])
 new[i]=oatart[n]
 # Keep the fruit separate for storage and make the final jar the night before.
 notes[i]=('12–18 min + overnight','Put 50 g dry oats into each of 3 or 4 jars. Portion yogurt separately. Keep fruit whole, or use ready-cut fruit within its package date. Use the 3- or 4-meal column for your shopping totals.','Each night, add one yogurt portion, 50 g water, fruit and flavor to one oat jar. Stir, close and chill for 8 hours. Eat the next morning. Keep yogurt and ready-cut fruit at 4°C or colder.')
 storyboard[i]=[icons['N'] if hero=='banana' else icons[hero],art[2],art[12]]
chapters[0]=('Breakfast','Morning','10 overnight oat jars and 7 other easy breakfasts.',oatids+[27,29,1,28,30,31,32])
