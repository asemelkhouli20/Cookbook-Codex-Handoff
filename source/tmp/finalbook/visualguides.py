# All teaching cards share the headings, header band, picture steps and batch panel used on recipes.
def teaching(key,title,sub,hero,needs,steps,tag,tip,tipart,col=4):
 cl,ac=colors[col]
 page(key,title,ac)
 rect(0,600,W,118,cl)
 t(16,695,'KITCHEN BASICS' if key=='start' else 'WEEKLY PREP    /    PICTURE GUIDE',9.5,'B',ac)
 lines(16,663,title,261,22,26,'H');t(17,610,sub,10.5,'B',ac);image(hero,285,603,153,109)
 t(17,576,'What you need',17,'H',ac)
 for n,(im,caption) in enumerate(needs):
  x=16+140*n;rect(x,481,135,80,WHITE,5);image(im,x+8,503,119,56)
  w=pdfmetrics.stringWidth(caption,'B',10);t(x+(135-w)/2,488,caption,10,'B',ac)
 t(17,452,'Step by step',17,'H',ac)
 for n,(im,hd,txt) in enumerate(steps):
  y=435-n*91;rect(16,y-86,418,84,WHITE,5);image(im,20,y-83,78,76)
  t(105,y-22,str(n+1)+'   '+hd,13,'B',ac)
  bottom=lines(106,y-40,txt,319,11.2,14.4)
  assert bottom>y-98,(key,hd,bottom,y)
 rect(16,49,418,103,cl,8);image(tipart,22,63,75,73);t(106,128,tag,15,'H',ac);lines(106,107,tip,316,11.4,15)
 foot(c.getPageNumber())
def starter():
 teaching('start','Read your first card','Choose a recipe and a serving column.',new[25],
 [(art[0],'Kitchen scale'),(art[10],'Shallow boxes'),(art[15],'Thermometer')],
 [(new[25],'Pick your meal','Choose a chapter, then tap a dish. Each calorie estimate is for one serving, including the listed sauce and oil.'),
 (art[0],'Weigh one ingredient','Put a bowl on the scale and press zero. Add food until the grams match your column. Press zero before the next ingredient.'),
 (art[10],'Make three or four','Use that column for every ingredient. Follow the batch panel at the bottom and split the finished food equally.')],
 'Look at the food label','Cooked rice and cooked chicken are weighed after cooking. Weigh ground beef raw. Drain canned beans or tuna before weighing.',art[4],0)
def guides():
 teaching('bases','Rice in a cooker','Allow 25–40 min, depending on the cooker.',art[5],
 [(icons['R'],'Rice'),(art[5],'Rice cooker'),(art[0],'Kitchen scale')],
 [(art[5],'Add rice and water','Measure dry rice. Follow the water amount on the rice packet or the fill line for that amount in your cooker.'),
 (art[5],'Cook and rest','Close the lid and press Cook. When it switches to Warm, leave the lid closed for 5 minutes. Fluff with a fork.'),
 (art[10],'Weigh the cooked rice','Put a box on the scale. Press zero. Spoon in the cooked grams on your recipe card. Repeat for each portion.')],
 'Make 3 or 4','Chill rice promptly in shallow boxes at 4°C or colder. Use within 3–4 days. Freeze later portions and reheat only the portion you will eat.',art[13])
 teaching('pasta','Pasta in a pot','Allow 15–25 min, including time to boil.',art[6],
 [(icons['P'],'Egg-free pasta'),(art[6],'Large pot'),(art[4],'Colander')],
 [(art[6],'Bring water to a boil','Fill a large pot with water as directed on the packet. Heat until large bubbles rise continuously.'),
 (art[6],'Add pasta and stir','Set the packet timer. Stir occasionally. Taste one cooled piece when the timer rings. Drain when tender.'),
 (art[10],'Weigh each serving','Drain in a colander. Set a box on the scale and press zero. Add the cooked grams on your card.')],
 'Make 3 or 4','Cook the batch in one pot with room for the pasta to move. Portion it into shallow boxes. Keep dressing and crunchy vegetables separate.',art[11])
 teaching('chicken','Air-fryer chicken','About 12–16 min per load of chicken strips.',art[7],
 [(icons['C'],'Chicken'),(art[7],'Air fryer'),(art[15],'Thermometer')],
 [(art[7],'Cut even strips','Use a clean board. Cut raw chicken into strips about 2 cm thick. Wash hands, knife and board after touching raw chicken.'),
 (art[7],'Air-fry in one layer','Set to 190°C. Leave space between strips. Cook for about 12–16 minutes, turning halfway.'),
 (art[15],'Check the middle','Probe the thickest strip. Keep cooking until it reaches 74°C. If needed, cook 2 minutes longer and check again.')],
 'Make 3 or 4','Cook a second load if the basket is full. Weigh the cooked strips into boxes. Plain ready-cooked skinless chicken also works.',art[10])
 teaching('beef','Lean ground beef','Allow about 10–15 min per pan of crumbs.',art[8],
 [(icons['B'],'Lean ground beef'),(art[8],'Nonstick pan'),(art[15],'Thermometer')],
 [(icons['B'],'Weigh it raw','Use the grams in your chosen column. For a burger or kofta, shape the raw meat as shown on that recipe card.'),
 (art[8],'Make beef crumbs','Heat the pan over medium heat. Use the oil listed on the card. Add beef and break it into small pieces with a spatula.'),
 (burg[3],'Check the center','Cook ground beef to 71°C. Insert the thermometer sideways into patties. For crumbs, gather a mound around the probe to check.')],
 'Make 3 or 4','Cook in batches when the pan is crowded. Divide the cooked beef evenly. Store patties separately from buns, lettuce and sauce.',art[11])
 teaching('roast','Roast a whole chicken','1.4–1.8 kg bird   •   About 1¾–2 hr total',bird[0],
 [(bird[0],'Unstuffed chicken'),(bird[0],'Roasting pan'),(bird[2],'Thermometer')],
 [(bird[0],'Heat the oven to 177°C / 350°F','Remove the wrapping and any giblet bag. Pat the bird dry. Set it breast-side up on a rack in the pan, with the cavity empty. Wash hands and tools.'),
 (bird[2],'Roast and check three places','Roast for about 75–90 minutes. Check the thickest breast, inner thigh and inner wing away from bone. Keep roasting until all three reach 74°C.'),
 (bird[3],'Rest, carve and weigh','Rest 10 minutes. Cut legs at the joints and slice breast meat from the bone. Weigh edible meat, including any skin you will eat.')],
 'Make 3 or 4','For roast dinners, pack 150 g edible meat each. That is 450 g for three or 600 g for four. A plain rotisserie chicken is a shortcut.',bird[3])
 teaching('week','Three prep days','One example for six days of meals.',art[10],
 [(bird[0],'Chicken and rice'),(new[9],'Beef and pasta'),(new[14],'Tuna and beans')],
 [(bird[0],'Saturday • Chicken and rice','Roast the bird and start the rice cooker. Set aside portions for roast dinners and bowls. Use skinless meat for snack wraps.'),
 (new[25],'Monday • Beef and pasta','Boil pasta while the beef cooks. Shape a 75 g raw patty for each 7 pm burger. Pack buns separately. Allow about 35–60 minutes.'),
 (art[4],'Wednesday • Tuna and beans','Drain the cans. Choose a cold salad, then portion the dressing. Add chickpea patties if you want a hot option. Allow about 20–45 minutes.')],
 'Plan two portions at a time','Choose one lunch and one dinner for each pair of days. Check the batch panel on each card for what goes in the fridge or freezer.',art[11])
 teaching('boxes','Cool, store and reheat','Use a clean, shallow box for each portion.',art[11],
 [(art[10],'Shallow boxes'),(art[12],'Fridge at 4°C'),(art[15],'Thermometer')],
 [(art[12],'Chill promptly','Divide hot food into shallow boxes. Refrigerate within 2 hours, or 1 hour if the room is hotter than 32°C. Label with the day you cooked it.'),
 (art[13],'Freeze later portions','Most cooked leftovers keep 3–4 days at 4°C or colder. Chill rice promptly in shallow boxes. Eat within 3–4 days or freeze it promptly.'),
 (art[14],'Reheat one box','Thaw in the fridge. Cover loosely, heat and stir. Check several spots reach 74°C. Reheat rice once. Add cold salad and yogurt afterward.')],
 'Pack hot and cold apart','Keep lettuce, cucumber and cold yogurt in a separate tub. Put them on the meal after reheating. Follow shorter dates on food labels.',art[11])
