# Builds the full logo and the "Emma's" wordmark from brand/emmas-logo-original.eps.
# Needs skia-pathops (pip install skia-pathops) and ImageMagick (`magick`) for the PNGs.
# Run from anywhere: python3 scripts/export_logo.py
import os, subprocess, zlib
import pathops

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.join(HERE, '..', 'brand')
INK, INK_RGB = '#2E2620', '0.180 0.149 0.125'
WORDMARK_CLIP = (190, 115, 970, 410)  # x0, y0, x1, y1 around "Emma's", in EPS points from the top

def read_eps(path):
    # The EPS is a flat list of filled paths, painted in order: gray ink, then off-white
    # counters and specks on top. Union the ink, subtract the off-white, skip the page background.
    H = None; acc = pathops.Path(); n = 0
    for ln in open(path, encoding='latin-1'):
        if ln.startswith('%%BoundingBox:'): H = float(ln.split()[4])
        t = ln.split()
        if not t or t[0].startswith('%'): continue
        op = t[-1]; a = [float(x) for x in t[:-1]]
        y = lambda v: H - v
        if op == 'setrgbcolor': light = a[0] > 0.9
        elif op == 'newpath': cur = pathops.Path(); pen = cur.getPen()
        elif op == 'moveto': pen.moveTo((a[0], y(a[1])))
        elif op == 'lineto': pen.lineTo((a[0], y(a[1])))
        elif op == 'curveto': pen.curveTo((a[0], y(a[1])), (a[2], y(a[3])), (a[4], y(a[5])))
        elif op == 'closepath': pen.closePath()
        elif op == 'fill':
            n += 1
            if n == 1: continue
            acc = pathops.op(acc, cur, pathops.PathOp.DIFFERENCE if light else pathops.PathOp.UNION)
    acc.simplify()
    return acc

def clip(path, box):
    x0, y0, x1, y1 = box
    r = pathops.Path(); pen = r.getPen()
    pen.moveTo((x0, y0)); pen.lineTo((x1, y0)); pen.lineTo((x1, y1)); pen.lineTo((x0, y1)); pen.closePath()
    return pathops.op(path, r, pathops.PathOp.INTERSECTION)

def segments(path):
    # Flatten to M/L/C/Z, turning any quadratics from the boolean ops into cubics.
    segs = []; st = {}
    class Pen:
        def moveTo(s, p): segs.append(('M', [p])); st['p'] = st['start'] = p
        def lineTo(s, p): segs.append(('L', [p])); st['p'] = p
        def curveTo(s, *p): segs.append(('C', list(p))); st['p'] = p[-1]
        def qCurveTo(s, *p):
            offs, end = list(p[:-1]), p[-1]
            ons = [((offs[i][0] + offs[i+1][0]) / 2, (offs[i][1] + offs[i+1][1]) / 2) for i in range(len(offs) - 1)] + [end]
            for q, e in zip(offs, ons):
                s0 = st['p']
                c1 = (s0[0] + 2/3 * (q[0] - s0[0]), s0[1] + 2/3 * (q[1] - s0[1]))
                c2 = (e[0] + 2/3 * (q[0] - e[0]), e[1] + 2/3 * (q[1] - e[1]))
                segs.append(('C', [c1, c2, e])); st['p'] = e
        def closePath(s): segs.append(('Z', [])); st['p'] = st['start']
        def endPath(s): pass
    path.draw(Pen())
    return segs

fmt = lambda v: ('%.2f' % v).rstrip('0').rstrip('.')

def write_svg(segs, box, fill, out):
    x0, y0, x1, y1 = box
    d = ''.join(c + ' '.join(fmt(px - x0) + ' ' + fmt(py - y0) for px, py in pts) for c, pts in segs)
    open(out, 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(x1 - x0)} {fmt(y1 - y0)}"><path fill="{fill}" d="{d}"/></svg>')

def write_pdf(segs, box, out):
    x0, y0, x1, y1 = box; W, H = x1 - x0, y1 - y0
    ops = {'M': 'm', 'L': 'l', 'C': 'c'}
    cs = [INK_RGB + ' rg']
    for c, pts in segs:
        cs.append('h' if c == 'Z' else ' '.join(fmt(px - x0) + ' ' + fmt(H - (py - y0)) for px, py in pts) + ' ' + ops[c])
    cs.append('f')
    body = zlib.compress('\n'.join(cs).encode())
    objs = [b'<</Type/Catalog/Pages 2 0 R>>', b'<</Type/Pages/Kids[3 0 R]/Count 1>>',
            f'<</Type/Page/Parent 2 0 R/MediaBox[0 0 {fmt(W)} {fmt(H)}]/Contents 4 0 R/Resources<<>>>>'.encode(),
            b'<</Length %d/Filter/FlateDecode>>stream\n' % len(body) + body + b'\nendstream']
    pdf = b'%PDF-1.4\n'; offs = []
    for i, o in enumerate(objs, 1):
        offs.append(len(pdf)); pdf += b'%d 0 obj\n' % i + o + b'\nendobj\n'
    x = len(pdf)
    pdf += b'xref\n0 %d\n0000000000 65535 f \n' % (len(objs) + 1) + b''.join(b'%010d 00000 n \n' % o for o in offs)
    pdf += b'trailer\n<</Size %d/Root 1 0 R>>\nstartxref\n%d\n%%%%EOF\n' % (len(objs) + 1, x)
    open(out, 'wb').write(pdf)

def write_png(svg, out):
    subprocess.run(['magick', '-background', 'none', '-density', '600', svg, '-resize', '4800x',
                    '-depth', '8', 'PNG32:' + out], check=True)

def export(path, name):
    segs = segments(path); box = path.bounds
    base = os.path.join(BRAND, name)
    write_svg(segs, box, INK, base + '.svg')
    write_svg(segs, box, '#FFFFFF', base + '-white.svg')
    write_pdf(segs, box, base + '.pdf')
    write_png(base + '.svg', base + '-4800px.png')
    write_png(base + '-white.svg', base + '-white-4800px.png')
    print(name, fmt(box[2] - box[0]), 'x', fmt(box[3] - box[1]))

logo = read_eps(os.path.join(BRAND, 'emmas-logo-original.eps'))
export(logo, 'emmas-logo')
export(clip(logo, WORDMARK_CLIP), 'emmas-wordmark')
