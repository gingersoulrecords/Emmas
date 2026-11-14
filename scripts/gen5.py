import json, re
exec(open('/home/claude/scripts/gen3.py').read().split("# ---------- F:")[0])
eggs = [
 ("the classic","22","Two eggs any style and bacon, sausage, or griddled tomato, with a buttermilk biscuit or toasted rye bun.",None,False),
 ("Emma's benny","26","Two poached eggs on a split biscuit with bacon, sausage, griddled tomato, or arugula, finished with mousseline.",None,False),
 ("daily omelette","21","Changes daily, always vegetarian, with a biscuit or toasted rye bun.",None,False),
 ("the beltbuster","38","Three eggs, three bacon, sausage, or griddled tomato, a biscuit, and any two pancakes. Bring your appetite.",None,False),
 ("biscuits and gravy","17","A split biscuit smothered in creamy sage and onion sausage gravy, with two eggs any style and our house hot sauce.","swap eggs for home fries, fruit salad, green salad, or baked beans 4",True),
 ("brunch poutine","18","Crispy russet home fries under cheddar, Swiss, sausage gravy, and an over-easy egg.",None,True),
 ("the breakwich","11","One egg on a biscuit with cheddar, Swiss, or spicy pimento cheese, and bacon, sausage, griddled tomato, or arugula.",None,False),
 ("Emma's BLT","13","Two slices of bacon with baby arugula, tomato, and roasted garlic mayo on a biscuit or toasted rye bun.","add cheddar, Swiss, or spicy pimento cheese 2  ·  add an egg 2",False),
]
pancakes = [
 ("buttermilk pancakes","20","Fluffy pancakes with whipped citrus butter. Better than your mum's.","side of two 12  ·  make them chocolate 22, side 13  ·  add raspberry sauce 3",False),
 ("cinnamon bun pancakes","24","Swirled with butter, brown sugar, and cinnamon, topped with whipped brown butter.","side of two 14",False),
 ("gingerbread pancakes","24","Molasses, brown sugar, and warm winter spices, topped with whipped brown butter.","side of two 14",False),
]
small = [
 ("buttermilk biscuit","5","Warm, with citrus butter and blueberry jam.",None,False),
 ("Deb's bran muffin","7","Baked to order and topped with brown butter and honey.",None,False),
 ("yogurt parfait","12","Fresh raspberry compote and pumpkin seed granola.",None,False),
 ("baked oatmeal","16","Creamy baked oatmeal over warm apple cinnamon compote, with brûléed brown sugar, walnuts, and vanilla anglaise.",None,False),
]
greens = [("winter cobb salad","22","Baby arugula with free range chicken, roasted sweet potato, goat cheese, pumpkin seeds, dried cranberries, and honey Dijon.",None,False)]
table = [
 ("the full English","50","Two buttermilk biscuits, four sunny eggs, sausage, bacon, griddled tomato, baked beans, home fries, portobello, and HP sauce.",None,True),
 ("pancake party pack","45","Short stacks (2) of buttermilk, cinnamon bun, gingerbread, and dark chocolate raspberry, with all the fixins.",None,False),
]
side_cols = [
 [("glazed donuts (4)","8",0),("apple fritters (6)","8",0),("lazy daisy oatmeal cake","3",0)],
 [("eggs (2)","4",0),("home fries","9",0),("peppy baked beans","9",0),("green salad","9",0),("fruit salad","9",0)],
 [("side omelette","8",0),("bacon (3)","9",0),("sausage (3)","9",0),("griddled tomato (3)","9",0),("portobello","9",0)],
 [("sausage gravy","6",0),("maple syrup","3",0),("mousseline","3",0),("house hot sauce","2",0),("garlic mayo","1",0)],
]
PORKC="#A89C8E"
def tagspan(font, sz=12, ml=7): return ""
T="'Alegreya Sans SC', sans-serif"
N="font-family: 'Alegreya Sans', sans-serif; font-weight: 400; font-size: 18px"
P="font-family: 'Alegreya', serif; font-weight: 400; font-size: 17px"
D_SERIF="font-family: 'Alegreya', serif; font-style: italic; font-weight: 400; font-size: 14px"
D_SANS="font-family: 'Alegreya Sans', sans-serif; font-style: italic; font-weight: 300; font-size: 13.5px"
def hd(l, note=None):
    h=f'<div style="font-family: \'Alegreya Sans SC\', sans-serif; font-weight: 500; font-size: 13px; letter-spacing: 0.1em; color: {LABEL}; margin: 0 0 11px; padding-bottom: 5px; border-bottom: 0.5px solid #E0D8C9">{l}</div>'
    if note: h+=f'<div style="font-size: 13px; color: {MUTE}; line-height: 1.4; margin: -3px 0 10px">{note}</div>'
    return h
def col(*secs): return '<div style="display: flex; flex-direction: column; gap: 32px">' + "".join(secs) + '</div>'
favourites, rest = eggs[:4], eggs[4:]
def item(n,p,d,a,pk, N,P,D,T, pr=30, meta_color=MUTE):
    s=f'<div><div style="display: flex; justify-content: space-between; align-items: baseline; gap: 16px"><div style="{N}; line-height: 1.2">{E(n)}{tagspan(T) if pk else ""}</div><div style="{P}">{p}</div></div>'
    dd = re.sub(r'\[\[(.+?)\]\]', r'\1', E(d))
    s+=f'<div style="{D}; line-height: 1.38; margin-top: 2px; padding-right: {pr}px">{dd}</div>'
    if a:
        meta = re.sub(r'(?<![(\d.])(\d+(?:\.\d+)?)(?!\s*oz|\.\d|\s*mL|\s*%|\))', f'<span style="font-family: \'Alegreya\', serif; font-size: 13.5px; color: {INK}">\\1</span>', E(a))
        s+=f'<div style="font-size: 12.5px; color: {meta_color}; margin-top: 2px; white-space: pre">{meta}</div>'
    return s+'</div>'
def build(D, desc_color=None):
    DD = D + f"; color: {desc_color or MUTE}"
    MC = desc_color or MUTE
    def sec(l, items, note=None): return '<div>'+hd(l, note)+'<div style="display: flex; flex-direction: column; gap: 10px">'+"".join(item(*i,N,P,DD,T,meta_color=MC) for i in items)+'</div></div>'
    sn = "Served with your choice of: crispy russet home fries, baked beans, green salad, or fruit salad.<br>Citrus butter and blueberry jam available upon request."
    return f'''<header style="margin-bottom: 22px; display: flex; justify-content: flex-start"><img src="/_blob/8dc715ad13fee4de10e3c902a1da3dda" alt="Emma's" style="width: 108px; height: 40px; display: block"></header>
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 44px">
{col(sec("brunch favourites", favourites, sn), sec("more from the kitchen", rest))}
{col(sec("pancakes", pancakes, "Stacks of four, served with Jakeman's maple syrup (2 oz)."), sec("small plates", small), sec("greens", greens))}
</div>
<div style="margin-top: 32px">{hd("for the table")}<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 44px">{"".join(item(*i,N,P,DD,T,meta_color=MC) for i in table)}</div></div>
<div style="margin-top: 32px">{hd("add-ons")}{sides("font-family: 'Alegreya Sans', sans-serif; font-weight: 400; font-size: 13.5px", "font-family: 'Alegreya', serif; font-size: 13.5px", T)}</div>
<div style="margin-top: auto; display: flex; justify-content: space-between; align-items: baseline; gap: 24px; font-size: 12px; color: {LABEL}; line-height: 1.5; padding-top: 10px">
<div style="font-family: 'Alegreya', serif; font-style: italic; font-size: 13px; color: {MUTE}"><svg aria-hidden="true" viewBox="0 0 512 512" width="16" height="16" style="vertical-align: -4px; margin-right: 6px; opacity: 0.6" fill="#7A6E63"><path  d="m213.705 344.935l2.7 53.87h-26.24l-19.46-55.41zm150.56.33l-.34 4.38l18.15 49.16h24.44l-5.66-56.51a326 326 0 0 1-36.57 2.97zm32.79-164.08a90 90 0 0 0 13.05-1.12c51.2-7.62 36.49-49.56 36.49-49.56s-40.36 9-52.83 23.42c.02 0-28.12 27.26 3.31 27.26zm81.85-25.33s-6.81 0-15.92.82a47 47 0 0 1-13.28 22.9a117 117 0 0 1 7.44 14.09c25.25-9.43 21.79-37.81 21.79-37.81zm11.8 100.18v41.49s-53.15 31.9-134.5 31.9c-2.19 0-4.44-.15-6.67-.2l-5.48 69.58h-19l-24.45-66.86l-162.59-5.87l-9.4 72.73h-22.63s-48.15-101.58-23.18-182.06c-5.55-3.84-11.38-8.17-16.73-12.7c-5.13 2.65-10.26 4.11-15 3.85c-15.76-.85-28.37-12.73-29.78-14.09l11.16-11.46c2.6 2.5 11.21 9.13 19.48 9.57a8 8 0 0 0 1.7-.11a46.4 46.4 0 0 1-4.59-6.47c-5.65-9.83-7-20.32-3.84-28.79a25.1 25.1 0 0 1 15.94-14.87c11.29-3.81 26.85-3.35 34.75 4.9c2.94 3.07 7.24 9.84 3 20.7c-3.59 9.29-10.85 19.34-19.36 27.12c2.87 2.3 5.94 4.61 9.09 6.87c9.46-20.85 24.84-39.58 48.52-53.76a238.9 238.9 0 0 1 124-34.31a259.14 259.14 0 0 1 120.54 30.12a81 81 0 0 0-7.77 9.25c-7.6 10.67-9.67 20.49-6.15 29.19c2.85 7 10.23 15.42 29.24 15.42a105 105 0 0 0 15.41-1.3a80.5 80.5 0 0 0 24-7.18c15.75 25.72 17.22 58.67 28 61c12.79 2.72 26.29 6.34 26.29 6.34m-406.69-94.52c.43-1.12 1.05-3.11.32-3.87c-1.32-1.38-4.81-2.26-8.92-2.26a29.2 29.2 0 0 0-9.16 1.42c-3.13 1.05-5.12 2.81-6.09 5.38c-1.46 3.95-.46 9.62 2.75 15.19a36.3 36.3 0 0 0 4.79 6.25c6.66-5.82 13.19-14.04 16.31-22.11m331.14 81.55a9.05 9.05 0 1 0-9.05 9.05a9.05 9.05 0 0 0 9.05-9.05"/></svg>our baked beans, sausage gravy, sausage, and bacon are made with pork</div>
<div style="font-family: 'Alegreya', serif; font-style: italic; font-size: 13px; color: {MUTE}">a living wage employer · livingwage.ca</div>
</div>'''
out="/home/claude/eck/project/"
open(out+"LowerSerif.dc.html","w").write(page("Option F1: serif italic body", "#FBF8F1", build(D_SERIF, desc_color="#7A6E63")))

print("ok")
