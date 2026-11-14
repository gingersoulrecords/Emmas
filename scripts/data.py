import json, html
E = lambda s: html.escape(s, quote=False)
LOGO="/_blob/1518580469b252f3644d0fd3731bbc68"
INK="#2E2620"; MUTE="#5E534A"; LABEL="#6E6257"; RULE="#CFC6B8"
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alegreya:ital,wght@0,500;0,700;0,800;1,500&amp;family=Alegreya+SC:wght@500;700&amp;family=Alegreya+Sans:ital,wght@0,400;0,500;1,400&amp;family=Alegreya+Sans+SC:wght@500;700&amp;display=swap">'
INTRO = "Every biscuit here comes from [Grandmother's name]'s recipe, the same one she baked every Sunday. We cure our own bacon, grind our own sausage, and bake everything else fresh each morning."
eggs = [
 ("the classic","22","Two eggs any style with bacon, sausage, or griddled tomato, a buttermilk biscuit or toasted rye bun, and your choice of side.","citrus butter and blueberry jam on request",False),
 ("Emma's benny","26","Two poached eggs on a split biscuit with bacon, sausage, griddled tomato, or arugula, finished with mousseline. Choice of side.",None,False),
 ("biscuits and gravy","17","A biscuit smothered in creamy sage and onion sausage gravy, with two eggs any style and our house hot sauce.","swap the eggs for a side 4",True),
 ("the beltbuster","38","Three eggs, three bacon, sausage, or tomato, a biscuit, two pancakes with whipped butter and maple syrup, and a side. Bring your appetite.",None,False),
 ("daily omelette","21","A two-egg omelette with whatever vegetables are good today, with a biscuit or rye bun and a side.",None,False),
 ("brunch poutine","18","Crispy russet home fries under cheddar, Swiss, sausage gravy, and an over-easy egg.",None,True),
 ("the breakwich","11","One egg on a biscuit with cheddar, Swiss, or spicy pimento cheese, and bacon, sausage, tomato, or arugula.",None,False),
 ("Emma's BLT","13","Two slices of our bacon with baby arugula, tomato, and roasted garlic mayo on a biscuit or rye bun.","add cheese 2  ·  add an egg 2",False),
]
small = [
 ("buttermilk biscuit","5","Warm, with citrus butter and blueberry jam.",None,False),
 ("yogurt parfait","12","Honey yogurt, fresh raspberry compote, and pumpkin seed granola.",None,False),
 ("Deb's bran muffin","7","Baked to order and topped with honey and brown butter.",None,False),
]
griddle = [
 ("buttermilk pancakes","20","Four fluffy pancakes, whipped citrus butter, real maple syrup. Better than your mum's.","side of two 12  ·  make them chocolate 22, side 13",False),
 ("cinnamon bun pancakes","24","Swirled with butter, brown sugar, and cinnamon, topped with whipped brown butter.","side of two 14",False),
 ("gingerbread pancakes","24","Molasses, brown sugar, and warm winter spices, topped with whipped brown butter.","side of two 14",False),
 ("baked oatmeal","16","Creamy baked oatmeal over warm apple cinnamon compote, with brûléed brown sugar, walnuts, and vanilla anglaise.",None,False),
]
greens = [("winter cobb salad","22","Baby arugula with free range chicken, roasted sweet potato, goat cheese, pumpkin seeds, dried cranberries, and honey Dijon.",None,False)]
table = [
 ("the full English","50","For two. Biscuits, four sunny eggs, sausage, bacon, griddled tomato, baked beans, home fries, portobello, and HP sauce.",None,False),
 ("pancake party pack","45","Short stacks of buttermilk, cinnamon bun, gingerbread, and dark chocolate raspberry, with all the fixings and real maple syrup.",None,False),
]
side_cols = [
 [("eggs (2)","4",0),("daily omelette","8",0),("home fries","9",0),("baked beans","9",1),("green salad","9",0),("fruit salad","9",0)],
 [("bacon (3)","9",0),("sausage (3)","9",0),("sausage gravy","6",1),("griddled tomato (3)","9",0),("portobello","9",0)],
 [("rye bun and jam","5",0),("glazed donuts (4)","8",0),("apple fritters (6)","8",0),("lazy daisy cake","3",0)],
 [("maple syrup","3",0),("mousseline","3",0),("house hot sauce","2",0),("garlic mayo","1",0)],
]
