import json
exec(open('/home/claude/scripts/data.py').read())
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alegreya:ital,wght@0,400;0,500;1,400;1,500&amp;family=Alegreya+SC:wght@400;500&amp;family=Alegreya+Sans:ital,wght@0,300;0,400;0,500;1,300;1,400&amp;family=Alegreya+Sans+SC:wght@400;500&amp;display=swap">'
def page(title, paper, body, w=816, h=1344, pad="56px 64px 48px"):
    props = json.dumps({"$preview":{"width":w,"height":h}})
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS}
<style>
html,body{{margin:0;padding:0;background:{paper}}}
a{{color:{INK}}}a:hover{{color:#000}}
</style>
</helmet>
<div style="width: {w}px; height: {h}px; box-sizing: border-box; padding: {pad}; background: {paper}; color: {INK}; font-family: 'Alegreya Sans', sans-serif; display: flex; flex-direction: column">
{body}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{props}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
'''
def tagspan(font, sz=12, ml=7): return f'<span style="font-family: {font}; font-weight: 500; font-size: {sz}px; letter-spacing: 0.08em; color: {LABEL}; margin-left: {ml}px">pork</span>'
def item(n,p,d,a,pk, N,P,D,T, pr=30):
    s=f'<div><div style="display: flex; justify-content: space-between; align-items: baseline; gap: 16px"><div style="{N}; line-height: 1.2">{E(n)}{tagspan(T) if pk else ""}</div><div style="{P}">{p}</div></div>'
    s+=f'<div style="{D}; color: {MUTE}; line-height: 1.38; margin-top: 2px; padding-right: {pr}px">{E(d)}</div>'
    if a: s+=f'<div style="font-size: 12.5px; color: {LABEL}; margin-top: 2px; white-space: pre">{E(a)}</div>'
    return s+'</div>'
def sides(N,P,T, center=False):
    cols=[]
    for c in side_cols:
        rows="".join(f'<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 8px; font-size: 13px; line-height: 1.35"><div style="{N}">{E(n)}{tagspan(T,11.5,5) if pk else ""}</div><div style="{P}">{p}</div></div>' for n,p,pk in c)
        cols.append(f'<div style="display: flex; flex-direction: column; gap: 5px">{rows}</div>')
    return '<div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0 28px">' + "".join(cols) + '</div>'
def col(*secs): return '<div style="display: flex; flex-direction: column; gap: 22px">' + "".join(secs) + '</div>'
def footer(T, center=True):
    return f'<div style="margin-top: auto; text-align: {"center" if center else "left"}; font-size: 12px; color: {LABEL}; line-height: 1.5; padding-top: 14px">items marked {tagspan(T,12,0)} contain pork that can\'t be removed</div>'
def two_col(sec, a_items, b_items, cols=2, gap=44):
    return f'<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 {gap}px">{col(sec("eggs and biscuits", eggs))}{col(sec("small plates", small), sec("from the griddle", griddle), sec("greens", greens))}</div>'
def body(logo_w, head, sec, N,P,D,T, sidesN, sidesP, center_foot=True, gap=44, extra_head=""):
    lh=round(logo_w*774/930)
    return f'''<header style="display: flex; flex-direction: column; align-items: center; margin-bottom: 24px">
<img src="{LOGO}" alt="Emma's Country Kitchen" style="width: {logo_w}px; height: {lh}px; display: block">{extra_head}
</header>
{two_col(sec, eggs, None, gap=gap)}
<div style="margin-top: 18px">{head("for the table")}
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 {gap}px">{"".join(item(*i,N,P,D,T) for i in table)}</div>
</div>
<div style="margin-top: 16px">{head("on the side")}{sides(sidesN, sidesP, T)}</div>
{footer(T, center_foot)}'''

# ---------- F: all lowercase ----------
T6="'Alegreya Sans SC', sans-serif"
N6="font-family: 'Alegreya Sans', sans-serif; font-weight: 400; font-size: 18px"
P6="font-family: 'Alegreya', serif; font-weight: 400; font-size: 17px"
D6="font-family: 'Alegreya Sans', sans-serif; font-style: italic; font-weight: 300; font-size: 14px"
def h6(l): return f'<div style="display: flex; align-items: center; gap: 10px; margin: 0 0 11px"><div style="font-family: \'Alegreya Sans\', sans-serif; font-weight: 500; font-size: 12.5px; letter-spacing: 0.18em; color: {LABEL}">{l}</div><div style="flex: 1; height: 1px; background: {RULE}"></div></div>'
def s6(l, items): return '<div>'+h6(l)+'<div style="display: flex; flex-direction: column; gap: 11px">'+"".join(item(*i,N6,P6,D6,T6) for i in items)+'</div></div>'
F = body(150, h6, s6, N6,P6,D6,T6, "font-family: 'Alegreya Sans', sans-serif; font-weight: 400; font-size: 13.5px", "font-family: 'Alegreya', serif; font-size: 13.5px", center_foot=False)

# ---------- G: italic names, centered heads, one ornament ----------
T4="'Alegreya Sans SC', sans-serif"
N4="font-family: 'Alegreya', serif; font-style: italic; font-weight: 500; font-size: 19px"
P4="font-family: 'Alegreya Sans', sans-serif; font-weight: 400; font-size: 15px"
D4="font-family: 'Alegreya Sans', sans-serif; font-weight: 400; font-size: 13.5px"
def h4(l): return f'<div style="display: flex; align-items: center; justify-content: center; gap: 12px; margin: 0 0 12px"><div style="width: 26px; height: 1px; background: {RULE}"></div><div style="font-family: \'Alegreya Sans SC\', sans-serif; font-weight: 500; font-size: 13.5px; letter-spacing: 0.22em; color: {LABEL}">{l}</div><div style="width: 26px; height: 1px; background: {RULE}"></div></div>'
def s4(l, items): return '<div>'+h4(l)+'<div style="display: flex; flex-direction: column; gap: 11px">'+"".join(item(*i,N4,P4,D4,T4) for i in items)+'</div></div>'
DIA=f'<svg aria-hidden="true" width="9" height="9" viewBox="0 0 9 9" style="margin-top: 12px"><path d="M4.5 0l4.5 4.5-4.5 4.5L0 4.5z" fill="{LABEL}"/></svg>'
G = body(160, h4, s4, N4,P4,D4,T4, "font-family: 'Alegreya', serif; font-style: italic; font-weight: 500; font-size: 14px", "font-family: 'Alegreya Sans', sans-serif; font-size: 13px", extra_head=DIA)

# ---------- H: half-fold, cover + inside (sans small caps, one weight) ----------
T2="'Alegreya Sans SC', sans-serif"
N2="font-family: 'Alegreya Sans SC', sans-serif; font-weight: 500; font-size: 16.5px; letter-spacing: 0.03em"
P2="font-family: 'Alegreya Sans', sans-serif; font-weight: 400; font-size: 15px"
D2="font-family: 'Alegreya Sans', sans-serif; font-weight: 300; font-size: 14px"
def h2(l): return f'<div style="font-family: \'Alegreya Sans SC\', sans-serif; font-weight: 400; font-size: 13.5px; letter-spacing: 0.2em; color: {LABEL}; margin: 0 0 11px; padding-bottom: 6px; border-bottom: 1px solid {RULE}">{l}</div>'
def s2(l, items): return '<div>'+h2(l)+'<div style="display: flex; flex-direction: column; gap: 11px">'+"".join(item(*i,N2,P2,D2,T2) for i in items)+'</div></div>'
H_inside = f'''<header style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 22px">
<div style="font-family: 'Alegreya Sans SC', sans-serif; font-weight: 500; font-size: 15px; letter-spacing: 0.22em">brunch, all day</div>
<div style="font-family: 'Alegreya Sans', sans-serif; font-weight: 300; font-style: italic; font-size: 14px; color: {MUTE}">we're glad you're here</div>
</header>
{two_col(s2, eggs, None)}
<div style="margin-top: 18px">{h2("for the table")}
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 44px">{"".join(item(*i,N2,P2,D2,T2) for i in table)}</div>
</div>
<div style="margin-top: 16px">{h2("on the side")}{sides("font-family: 'Alegreya Sans SC', sans-serif; font-weight: 500; font-size: 13px; letter-spacing: 0.03em", "font-family: 'Alegreya Sans', sans-serif; font-size: 13px", T2)}</div>
{footer(T2, False)}'''
H_cover = f'''<div style="flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center">
<img src="{LOGO}" alt="Emma's Country Kitchen" style="width: 300px; height: 250px; display: block">
<div style="font-family: 'Alegreya', serif; font-style: italic; font-size: 17px; color: {MUTE}; margin-top: 28px">Biscuits from Grandma's recipe, bacon we cure ourselves, and everything else baked this morning.</div>
</div>
<div style="font-family: 'Alegreya Sans SC', sans-serif; font-weight: 400; font-size: 12.5px; letter-spacing: 0.22em; color: {LABEL}; text-align: center">brunch, all day</div>'''

out="/home/claude/eck/project/"
open(out+"Lowercase.dc.html","w").write(page("Option F: all lowercase", "#FBF8F1", F))
open(out+"Italic.dc.html","w").write(page("Option G: italic names", "#F6F1E7", G))
open(out+"FoldCover.dc.html","w").write(page("Option H: half-fold cover", "#F3EDE2", H_cover, w=816, h=672, pad="56px 64px 48px"))
open(out+"FoldInside.dc.html","w").write(page("Option H: half-fold inside", "#F3EDE2", H_inside))
c=json.load(open(out+"canvas.json"))
y=3400
c["boards"]["Lowercase.dc.html"]={"x":0,"y":y,"w":816,"h":1344,"title":"F · All lowercase"}
c["boards"]["Italic.dc.html"]={"x":896,"y":y,"w":816,"h":1344,"title":"G · Italic names, centered heads"}
c["boards"]["FoldCover.dc.html"]={"x":1792,"y":y,"w":816,"h":672,"title":"H · Half-fold, cover"}
c["boards"]["FoldInside.dc.html"]={"x":2688,"y":y,"w":816,"h":1344,"title":"H · Half-fold, inside"}
for f in ["Lowercase.dc.html","Italic.dc.html","FoldCover.dc.html","FoldInside.dc.html"]:
    if f not in c["order"]: c["order"].append(f)
c["notes"]["r3"]={"x":0,"y":y-260,"text":"Round 3: looks from the genre conventions","kind":"title1","maxW":3504}
json.dump(c,open(out+"canvas.json","w"))
print("ok")
