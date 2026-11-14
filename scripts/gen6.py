import os
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.join(HERE, '..', 'project') + os.sep
import json
exec(open(os.path.join(HERE,'gen5.py')).read())
cocktails = [
 ("Emma's Caesar","11","TAG No. 5 vodka, Clamato, horseradish, Worcestershire, and our house hot sauce, with a celery salt rim and a dill pickle.","1 oz",False),
 ("mimosa","11","Fresh squeezed orange juice topped with Montelliana prosecco.","4 oz",False),
 ("morning mule","11","TAG No. 5 vodka, Fever-Tree ginger beer, and fresh lime, topped with orange juice.","1 oz  ·  pitcher (5 oz) 45",False),
 ("spiked lemonade","11","House made blueberry lemonade with your choice of tequila, vodka, gin, or rum.","1 oz  ·  pitcher (5 oz) 45",False),
 ("paloma","11","El Jimador tequila, fresh lime and grapefruit juice, topped with soda, with a salted rim.","1 oz  ·  pitcher (5 oz) 45",False),
 ("Baileys latte","11","Baileys, Reunion Island espresso, and steamed milk with a light layer of foam.","1 oz",False),
 ("Earl Grey hot toddy","11","Jameson, honey, lemon, and cinnamon, steeped with Tea Squared Uncle Grey tea.","1 oz",False),
 ("spiked hot chocolate","11","Baileys and butter ripple in steamed chocolate milk, topped with house made marshmallow or whipped cream.","1.5 oz",False),
 ("hot shots","9","Hot apple cider with a shot of Jameson or brandy, or drip coffee with a shot of Baileys.","1 oz",False),
]
hot = [("coffee","4.5"),("americano / iced americano","5"),("cappuccino","5.5"),("latte / iced latte","5.5"),("mocha / iced mocha","5.5"),("tea","4.5"),("chai latte / iced chai latte","5.5"),("London fog","5.5"),("hot chocolate","5","add house made marshmallow 1")]
cold = [("fresh squeezed orange juice","6"),("fresh squeezed grapefruit juice","6"),("fresh pressed apple cider","5"),("house made blueberry lemonade","6"),("mango, strawberry, and orange smoothie","6"),("chocolate milk","4.5"),("Perrier","3"),("diet Coke","3"),("Cane Cola","3"),("ginger ale","3")]
beer = [("Beau's Lug-Tread lagered ale","6","355 mL · 5.2% ABV"),("Strongbow dry apple cider","7","440 mL · 5.3% ABV")]
NS="font-family: 'Alegreya Sans', sans-serif; font-weight: 400; font-size: 14px"
PS="font-family: 'Alegreya', serif; font-size: 14px"
def plain(items):
    rows=[]
    for n,p,*m in items:
        rows.append(f'<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 10px; line-height: 1.35"><div style="{NS}">{E(n)}</div><div style="{PS}">{p}</div></div>')
        if m:
            mm = re.sub(r'(?<![(\d.])(\d+)(?!\s*mL|\.\d|\s*%)', f'<span style="font-family: \'Alegreya\', serif; font-size: 13px; color: {INK}">\\1</span>', E(m[0]))
            rows.append(f'<div style="font-size: 12.5px; color: #7A6E63; margin-top: -4px; line-height: 1.35">{mm}</div>')
    return '<div style="display: flex; flex-direction: column; gap: 7px">'+"".join(rows)+'</div>'
def dsec(l, items, note=None): return '<div>'+hd(l, note)+'<div style="display: flex; flex-direction: column; gap: 10px">'+"".join(item(*i,N,P,D_SERIF+f"; color: #7A6E63",T,meta_color="#7A6E63") for i in items)+'</div></div>'
DR = f'''<header style="margin-bottom: 22px; display: flex; justify-content: flex-start"><img src="/_blob/8dc715ad13fee4de10e3c902a1da3dda" alt="Emma's" style="width: 108px; height: 40px; display: block"></header>
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 44px">
{col(dsec("cocktails", cocktails, "Available from 9 am."))}
{col('<div>'+hd("coffee and tea")+plain(hot)+'</div>', '<div>'+hd("juice, lemonade, and more")+plain(cold)+'</div>', '<div>'+hd("beer and cider")+plain(beer)+'</div>')}
</div>
<div style="margin-top: auto; display: flex; justify-content: flex-end; align-items: baseline; gap: 24px; font-size: 12px; color: {LABEL}; line-height: 1.5; padding-top: 10px">
<div style="font-family: 'Alegreya', serif; font-style: italic; font-size: 13px; color: {MUTE}">a living wage employer · livingwage.ca</div>
</div>'''
open(out+"Drinks.dc.html","w").write(page("Drinks side", "#FBF8F1", DR))
c=json.load(open(out+"canvas.json"))
c["boards"].pop("LowerSans.dc.html",None)
c["order"]=[o for o in c["order"] if o!="LowerSans.dc.html"]
c["boards"]["Drinks.dc.html"]={"x":896,"y":5100,"w":816,"h":1344,"title":"F1 · Drinks side","print":"fixed"}
c["boards"]["LowerSerif.dc.html"]["print"]="fixed"
c["notes"]["r4"]["text"]="Round 4: F1 food side and drinks side"
if "Drinks.dc.html" not in c["order"]: c["order"].append("Drinks.dc.html")
json.dump(c,open(out+"canvas.json","w")); print("ok")
