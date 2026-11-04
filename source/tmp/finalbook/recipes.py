# All quantities in grams per serving; energy estimates per 100 g as used.
F={
'C':('Cooked chicken',165),'B':('Raw lean beef, 5% fat',137),'T':('Tuna in water, drained',116),'K':('Chickpeas, drained',155),'W':('White beans, drained',120),'D':('Black beans, drained',132),'R':('Cooked rice',130),'P':('Cooked egg-free pasta',155),'X':('Flour tortilla',310),'O':('Rolled oats',380),'U':('Cucumber',15),'L':('Lettuce',15),'A':('Carrot',41),'E':('Bell pepper',31),'S':('Sweetcorn, drained',86),'H':('Hummus',180),'G':('Garlic yogurt',75),'J':('Lemon juice',22),'I':('Olive oil',884),'M':('Mustard',65),'Y':('Soy sauce',53),'N':('Banana, peeled',89),'Z':('Plain low-fat yogurt',70)}
# Each card starts with one serving. Keep batch directions in the final chapter.
meals=[]
def recipe(name,food,tm,tool,steps):
 q=[(p[0],int(p[1:])) for p in food.split()];meals.append((name,q,tm,tool,steps))
recipe('Banana overnight oats','O50 Z200 N100','5 min + overnight','Jar, fork, spoon',[
('Mash half','Peel the banana. Mash half in a jar with a fork. Slice the rest.','banana'),
('Stir','Stir in the yogurt and dry oats. Add a spoonful of water if the mixture feels stiff.','mix'),
('Chill','Place the banana slices on top. Close the jar and refrigerate overnight. The oats will be soft by breakfast.','chill')])
recipe('Banana breakfast fold','X50 O30 N100 Z100','8–10 min','Fork, bowl, nonstick pan',[
('Soften the oats','Stir the oats and 2 spoonfuls of yogurt together. Leave for 3 minutes while you mash the banana with a fork.','mix'),
('Fold','Mix the banana into the oats. Spread over one half of the tortilla and fold the empty half over it.','fold'),
('Toast','Set in a dry pan over medium-low heat. Toast for 2 minutes on each side until golden. Dip in the remaining yogurt.','pan')])
recipe('Little chicken wrap','X25 C60 G15 U20 L10','3–5 min','Knife, board, lunch box',[
('Slice','Cut ready-cooked chicken and cucumber into thin sticks. Pat lettuce dry.','slice'),
('Fill','Lay the tortilla flat. Spread garlic yogurt in a strip down the middle. Layer lettuce, cucumber and chicken on top.','spread'),
('Roll','Fold in both sides. Lift the bottom edge over the filling and roll away from you. Keep cold until your 7 pm break.','fold')])
recipe('Chicken & pepper rice bowl','C140 R160 E100 G50 I4','10–12 min','Pan, spoon, bowl',[
('Cut','Cut out the pepper stem, shake out the seeds and cut the pepper into thin strips. Slice the cooked chicken.','slice'),
('Soften','Heat the oil in a pan over medium heat. Stir the pepper for 4–5 minutes, until it bends easily.','pan'),
('Heat & serve','Add rice, chicken and a spoonful of water. Cover and stir occasionally until hot throughout. Spoon into a bowl and add garlic yogurt.','bowl')])
recipe('Mustard chicken pasta salad','C125 P145 U80 A50 M12 Z45','8–10 min','Bowl, grater, fork',[
('Chop cold ingredients','Use chilled cooked chicken and pasta. Dice the cucumber and chicken. Grate the carrot.','slice'),
('Dress','Stir mustard into the yogurt. Add a spoonful of water and stir until the dressing falls from a spoon.','mix'),
('Toss','Add pasta, chicken, cucumber and carrot. Turn gently with a spoon until coated. Eat cold.','bowl')])
recipe('Chicken hummus pinwheels','C115 X65 H50 A50 L15','8–10 min','Board, knife, spoon',[
('Prepare','Grate the carrot. Cut the cooked chicken into small pieces. Pat the lettuce dry.','slice'),
('Spread','Spread hummus over the whole tortilla, right up to the edge. Place lettuce, carrot and chicken in a thin layer.','spread'),
('Roll & slice','Roll the tortilla tightly from one edge. Set the seam underneath. Cut across into four thick rounds.','fold')])
recipe('Soy chicken & corn rice','C130 R160 S70 Y10 I4','8–12 min','Wide pan, spoon',[
('Warm the corn','Drain the corn. Warm oil in a pan on medium heat. Stir corn for 2 minutes.','pan'),
('Break up the rice','Add rice and diced cooked chicken. Press any rice clumps apart with the back of a spoon.','bowl'),
('Finish','Mix soy sauce with a spoonful of water and pour it around the pan. Stir until every bite is hot.','pan')])
recipe('White bean chicken penne','C110 P140 W75 G40 J8','10–12 min','Fork, bowl, pan',[
('Mash','Rinse and drain the beans. Mash with lemon and 2 spoonfuls of water until mostly smooth.','mash'),
('Heat','Put the mash, cooked pasta and sliced cooked chicken in a pan. Stir over medium heat until hot throughout. Add water if it sticks.','pan'),
('Make it creamy','Turn off the heat. Stir in the garlic yogurt. The sauce should cling lightly to the pasta.','mix')])
recipe('Kofta rice plate','B155 R150 U80 G65 I3','18–24 min','Air fryer, tongs, thermometer',[
('Shape','With clean hands divide raw lean beef into three pieces. Roll into short logs about 2 cm thick. Wash hands and the work surface.','shape'),
('Air-fry','Brush the logs with oil. Place in one layer at 190°C for 10–15 minutes. Turn halfway. A thermometer in the center must read 71°C.','air'),
('Plate','Heat the rice. Dice cucumber into the garlic yogurt. Set kofta beside the rice and serve the cool dip on the side.','bowl')])
recipe('Beef & pepper soy pasta','B145 P150 E100 Y12 I4','15–20 min','Pan, spatula, thermometer',[
('Slice','Remove the pepper stem and seeds. Cut into thin strips.','slice'),
('Brown','Heat oil in a pan on medium. Add beef and break it into small crumbs. Add pepper and stir until soft and the beef reaches 71°C.','pan'),
('Toss','Add cooked pasta, soy sauce and a spoonful of water. Stir until hot. The sauce should lightly coat the pasta.','mix')])
recipe('Beef-stuffed pepper boats','B130 R120 E180 H35 I3','22–28 min','Microwave, pan, thermometer',[
('Soften the pepper','Halve the pepper from stem to base. Remove seeds. Put halves cut-side up in a microwave-safe dish with a spoonful of water. Cover loosely. Heat 3–5 minutes until tender.','slice'),
('Cook the filling','Heat oil in a pan over medium heat. Add beef and break up with a spoon. Cook to 71°C, then stir in the rice and heat throughout.','pan'),
('Fill the boats','Lift pepper halves onto a plate. Spoon hummus inside, then mound the beef and rice on top. Eat any extra filling alongside.','fill')])
recipe('Beef & black bean lettuce cups','B120 D90 S55 L70 X45 M10 I3','15–20 min','Pan, spatula, thermometer',[
('Make the cups','Pull off the largest lettuce leaves. Rinse and pat dry. Cut the tortilla into wedges to serve alongside.','slice'),
('Brown the beef','Heat oil on medium. Break beef up in the pan with a spatula. Cook until it reaches 71°C.','pan'),
('Spoon and eat','Drain beans and corn. Add them to the pan with mustard and a splash of water. Stir until hot. Spoon small amounts into each leaf.','fill')])
recipe('Mustard beef patties & pasta salad','B145 P135 U80 M12 Z50 I3','18–24 min','Pan, bowl, thermometer',[
('Shape','Divide raw beef into two balls. Flatten to patties about 1.5 cm thick. Wash hands and the work surface.','shape'),
('Pan-cook','Warm oil over medium heat. Cook patties about 5–6 minutes on each side. Check the center reaches 71°C. Brush with half the mustard.','pan'),
('Make the side','Mix the rest of the mustard into yogurt. Dice cucumber and toss with chilled cooked pasta and dressing. Serve beside the patties.','mix')])
recipe('Crisp beef & bean pockets','B115 D80 X60 S50 I3','18–23 min','Pan, fork, thermometer',[
('Brown','Break raw beef into crumbs in a nonstick pan over medium heat. Cook to 71°C. Transfer to a bowl.','pan'),
('Mash & fill','Mash drained black beans with a spoonful of water. Spread on one half of the tortilla. Add beef and drained corn. Fold it closed.','fold'),
('Toast','Brush the pan with the oil. Toast the folded tortilla on medium-low for 2–3 minutes per side. Cut into wedges.','pan')])
recipe('Tuna & sweetcorn pasta salad','T120 P155 S65 M12 Z50 U50','7–10 min','Sieve, bowl, fork',[
('Drain','Tip canned tuna and corn into a sieve. Shake off the liquid. Dice the cucumber.','flake'),
('Make dressing','Stir mustard and yogurt together in a bowl. Break the tuna into small flakes with a fork.','mix'),
('Combine','Add chilled cooked pasta, tuna, cucumber and corn. Fold through the dressing and eat cold.','bowl')])
recipe('Tuna cucumber boats','T130 U180 H65 X65 A40','10–12 min','Knife, spoon, bowl',[
('Hollow the cucumber','Cut the cucumber lengthwise. Run a teaspoon down the middle to scoop out the soft seeds. Leave thick sides.','slice'),
('Mix','Drain tuna. Grate the carrot. Mix both with hummus until the filling holds together.','flake'),
('Fill','Spoon filling into both cucumber halves. Cut the tortilla into wedges for scooping up any filling left in the bowl.','fill')])
recipe('Tuna rice & carrot ribbons','T125 R170 U80 A70 Y10 I4','8–10 min','Peeler, bowl, fork',[
('Cut ribbons','Rinse the carrot. Use a peeler to shave long ribbons, working away from your fingers. Cut cucumber into small sticks.','slice'),
('Season the tuna','Drain and flake the tuna. Mix soy sauce, oil and a teaspoon of water in a small cup.','flake'),
('Build','Put freshly cooked or safely chilled rice in a bowl. Arrange tuna and vegetables on top. Drizzle with the soy dressing.','bowl')])
recipe('Open tuna & white bean tortilla','T110 W100 X60 E70 J12 I3','10–12 min','Pan, fork, plate',[
('Mash','Rinse and drain beans. Mash with lemon, oil and a spoonful of water to make a thick spread.','mash'),
('Toast','Place the tortilla in a dry pan over medium heat for 1 minute per side. Remove to a plate. Slice the pepper into thin strips.','pan'),
('Top','Spread bean mash over the tortilla. Scatter drained tuna flakes and pepper strips over it. Cut into wedges.','spread')])
recipe('Chickpea oat patty wrap','K140 O20 X50 L25 G45 I4','18–22 min','Fork, bowl, nonstick pan',[
('Mash','Rinse chickpeas and pat dry. Mash thoroughly with a fork. Stir in oats and a teaspoon of water. Rest 3 minutes.','mash'),
('Shape & toast','Press into three small, flat patties. Heat oil in a nonstick pan on medium. Cook 3–4 minutes per side until golden. Turn gently with a flat spatula.','shape'),
('Wrap','Spread garlic yogurt on the tortilla. Add lettuce and the patties. Fold the sides inward and roll.','fold')])
recipe('Hummus penne with carrot','P160 K90 H45 A60 J10','8–10 min','Grater, fork, pan',[
('Thin the hummus','Stir hummus, lemon juice and 2 spoonfuls of warm water in a cup until smooth enough to pour.','mix'),
('Warm the base','Grate carrot. Add it to a pan with drained chickpeas, cooked penne and a splash of water. Stir over medium heat until hot.','pan'),
('Coat','Turn the heat off. Fold in the hummus mixture until it coats the pasta. Add a little water if needed.','bowl')])
recipe('Black bean & corn burrito','D120 R80 X60 S50 E50 G25','10–14 min','Pan, board, fork',[
('Soften the pepper','Dice the pepper. Put it in a pan with a spoonful of water. Cover over medium heat for 3–4 minutes.','slice'),
('Warm the filling','Add drained beans, corn and cooked rice. Mash some beans and stir until the filling is hot and holds together.','mash'),
('Fold','Spread garlic yogurt on the tortilla. Add as much filling as fits. Fold in both sides and roll. Serve remaining filling beside it.','fold')])
recipe('Carrot & white bean dip plate','W180 A100 X65 I5 J12 U80','12–16 min','Microwave, bowl, fork',[
('Soften the carrot','Grate the carrot into a microwave-safe bowl with a spoonful of water. Cover loosely and heat 2–3 minutes until a fork presses through easily.','slice'),
('Mash','Add rinsed white beans. Heat another minute, then mash with lemon and oil. Add a little water for a soft dip.','mash'),
('Scoop','Toast the tortilla in a dry pan over medium heat for 1 minute per side. Cut into strips. Serve with the dip and cucumber sticks.','pan')])
recipe('Two-bean crunch salad','D95 W95 S55 U80 L40 X45 J15 I5','10–12 min','Sieve, board, bowl',[
('Drain & chop','Rinse both beans in a sieve. Drain corn. Dice cucumber and tear the lettuce into small pieces.','slice'),
('Dress','Mix lemon and oil in a bowl. Toss in beans, corn and cucumber. Add lettuce just before eating.','mix'),
('Make the crunch','Toast the tortilla in a dry pan for 1 minute per side. Cut into small triangles and serve beside the salad.','pan')])
recipe('Roast pepper & chickpea rice','K140 R140 E120 H40 J12 I4','18–24 min','Air fryer, bowl, spoon',[
('Prepare','Rinse chickpeas and pat dry. Remove pepper seeds and cut the pepper into short strips. Toss both with oil.','slice'),
('Air-fry','Spread in one layer. Cook at 190°C for 12–16 minutes. Shake halfway. Stop when peppers are soft and chickpeas start to turn golden.','air'),
('Serve','Mix hummus and lemon with a spoonful of water. Put the hot peppers and chickpeas on warm rice and spoon the dressing over them.','bowl')])
F['V']=('Carved roast chicken',255)
recipe('Whole roast chicken dinner','V150 R145 U80 G55 J10','5–8 min if roasted','Board, scale, bowl',[
('Choose a cut','Roast one whole bird using the illustrated guide at the back, or buy a plain whole roast chicken. Choose breast, thigh, drumstick or a mix.','bird'),
('Weigh the meat','Take the meat off the bone. Weigh 150 g of edible chicken, including any skin you plan to eat. The bones do not count.','carve'),
('Make your plate','Spoon warm rice onto the plate and add the chicken. Slice cucumber. Mix lemon into garlic yogurt for dipping. Reheat chilled chicken to 74°C.','bowl')])
F['Q']=('Small plain burger bun',280)
recipe('Little mustard beef burger','B75 Q35 M5 L10 U15','12–16 min','Nonstick pan, spatula, thermometer',[
('Shape one patty','Roll the raw beef into a ball. Flatten it to about 1 cm thick and a little wider than the bun. Wash your hands and the plate.','press'),
('Cook both sides','Heat a nonstick pan on medium. Add the patty. Cook about 3–4 minutes per side. Probe the center from the side. Continue cooking until it reads 71°C.','burgerpan'),
('Build your burger','Split the bun and spread mustard inside. Stack lettuce, the cooked patty and thin cucumber slices. Serve at 7 pm in place of the chicken wrap.','burger')])
