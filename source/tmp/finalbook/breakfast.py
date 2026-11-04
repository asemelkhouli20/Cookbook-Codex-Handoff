def add(name,food,time,tools,steps,batch,prep,serve):
 i=len(meals);recipe(name,food,time,tools,[(h,d,'') for h,d in steps]);notes[i]=(batch,prep,serve)
add('Banana-oat breakfast squares','O50 N100 Z150','25–30 min','Oven, small baking dish, fork',[
 ('Mash the banana','Heat the oven to 180°C. Mash the peeled banana with a fork until there are only tiny lumps.'),
 ('Press into a dish','Mix in the oats and a spoonful of yogurt. Press the mixture 1.5 cm thick in a small dish lined with baking paper.'),
 ('Bake and slice','Bake for 18–22 minutes, until firm at the edges. Cool, cut into two squares and serve with the remaining yogurt.')],
 '30–35 min','Spread the batch 1.5 cm thick in one lined dish. Bake until set. Cool, then cut 6 squares for 3 breakfasts or 8 for 4.','Pack two squares and one yogurt cup per breakfast. Eat cold or warm the squares separately.')
add('Warm carrot oats','O40 A45 N75 Z170','8–10 min','Small pot, grater, spoon',[
 ('Grate the carrot','Wash the carrot. Grate it finely, stopping before your fingers reach the grater.'),
 ('Simmer the oats','Put oats, carrot and 150 ml water in a small pot. Bring to a gentle bubble. Stir for 5–7 minutes, until the oats are soft.'),
 ('Top your bowl','Take the pot off the heat. Spoon yogurt on top. Slice the banana over the bowl.')],
 '15–20 min','Use 450 ml water for 3 breakfasts or 600 ml for 4. Simmer oats and grated carrot together, stirring until soft. Divide into shallow boxes.','Warm one portion to 74°C with a splash of water. Add the cold yogurt and freshly sliced banana.')
add('Hummus breakfast box','H55 X45 U80 A60 Z120','5–8 min','Board, knife, snack box',[
 ('Cut the sticks','Wash the cucumber and carrot. Cut both into finger-length sticks.'),
 ('Make the scoops','Cut the soft tortilla into triangles. Put hummus in a small cup and plain yogurt in a second cup.'),
 ('Pack and dip','Put vegetable sticks beside the dips. Keep tortilla triangles dry in their own bag. Scoop hummus with either.')],
 '12–15 min','Line up 3 or 4 boxes. Slice the vegetables once. Weigh the dips into small cups and count out one tortilla portion per box.','Keep the dip and vegetables cold. Leave tortillas sealed and dry until breakfast.')
add('Lemon white-bean roll','W100 X50 U50 A35 J8 I3 Z50','7–10 min','Fork, grater, board',[
 ('Make the spread','Rinse and drain canned beans. Mash with lemon juice and olive oil. Add a teaspoon of water if too thick to spread.'),
 ('Add the crunch','Grate the carrot. Slice the cucumber into thin sticks. Spread the mashed beans along the middle of the tortilla.'),
 ('Roll it up','Lay carrot and cucumber over the beans. Fold in the sides and roll tightly. Serve yogurt on the side for dipping.')],
 '15–20 min','Mash the full batch of beans, lemon and oil together. Divide among covered cups. Grate the carrots and cut cucumber separately.','Keep fillings chilled. Roll one tortilla before work to keep it from getting soggy.')
add('Creamy banana rice bowl','R110 N90 Z180','3–5 min','Bowl, fork, spoon',[
 ('Loosen the rice','Use freshly cooked rice that has been chilled promptly. Separate the grains with a fork.'),
 ('Make it creamy','Mash half the banana with the yogurt. Fold in the cold rice. Add a teaspoon of water if you like it looser.'),
 ('Add banana coins','Slice the remaining banana over the top. Eat cold, straight from the bowl.')],
 '10–15 min with cooked rice','Weigh cold cooked rice into 3 or 4 portions. Refrigerate only rice you will eat within 3–4 days; freeze later portions. Keep yogurt separate and bananas whole.','Thaw one rice portion in the fridge. Add yogurt and banana just before breakfast. Eat within 24 hours of thawing.')
add('Chickpea & corn cakes','K110 S45 O18 G65 I3','15–20 min','Fork, nonstick pan, spatula',[
 ('Mash and mix','Rinse and drain chickpeas. Mash well. Mix in drained corn and oats. Add 1–2 teaspoons of water so the mixture holds together.'),
 ('Shape three cakes','Rest for 3 minutes. Divide into three balls. Press flat with your palm until each is about 1 cm thick.'),
 ('Cook both sides','Warm the oil over medium heat. Cook 3–4 minutes per side until golden. Turn gently and serve with the garlic yogurt.')],
 '25–40 min','Shape 9 cakes for 3 mornings or 12 for 4. Cook in a single layer per load, sharing the total oil between loads. Cool in shallow boxes.','Pack three cakes and one dip cup per meal. Reheat the cakes to 74°C and add the cold dip.')
