# Builds the Emma's logo kit in brand/emmas-logo-kit/ from brand/emmas-logo-original.eps:
# three layouts (boxed logo, logo without the box, "Emma's" alone), each in ink, black and white,
# as SVG, PDF and EPS, plus 4800px transparent PNGs.
# Needs skia-pathops and pyclipper (pip install skia-pathops pyclipper) and ImageMagick (`magick`) for the PNGs.
# Run from anywhere: python3 scripts/export_logo.py
import math, os, shutil, subprocess, zlib
import pathops, pyclipper

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.join(HERE, '..', 'brand')
KIT = os.path.join(BRAND, 'emmas-logo-kit')
COLORS = {  # name: (hex, rgb 0-1)
    'ink': ('#2E2620', (0.180, 0.149, 0.125)),
    'black': ('#000000', (0, 0, 0)),
    'white': ('#FFFFFF', (1, 1, 1)),
}
# Each layout keeps the contours whose bounds fall inside its window (EPS points from the top).
LAYOUTS = {
    'emmas-logo-box': None,                       # everything
    'emmas-logo-no-box': (150, 100, 1000, 800),   # lettering and the two rules, without the frame
    'emmas-wordmark': (190, 115, 970, 410),       # "Emma's"
}
# Blemishes filled by a local close (grow the ink by r, shrink it back): (x0, y0, x1, y1), r in points.
PATCHES = [
    ((214, 236, 256, 262), 2.5),  # crack through the E's middle bar, and the bites under it
    ((788, 318, 812, 350), 4.5),  # ink trap where the a's bowl meets its stem
]
# Then the same close over the whole mark: fills cracks narrower than 2 * SOLID_R inside the strokes
# and pinholes smaller than MIN_HOLE square points, so the letters read solid and keep their rough edge.
SOLID_R, MIN_HOLE = 1.75, 60
SCALE = 100  # pyclipper works in integers: hundredths of a point

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

def rect(box):
    x0, y0, x1, y1 = box
    r = pathops.Path(); pen = r.getPen()
    pen.moveTo((x0, y0)); pen.lineTo((x1, y0)); pen.lineTo((x1, y1)); pen.lineTo((x0, y1)); pen.closePath()
    return r

def clip(path, box):
    return pathops.op(path, rect(box), pathops.PathOp.INTERSECTION)

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

def to_polys(path, steps=16):
    # Curves flattened to integer polygons for pyclipper.
    polys = []
    for c, pts in segments(path):
        if c == 'M': polys.append([pts[0]])
        elif c == 'L': polys[-1].append(pts[0])
        elif c == 'C':
            p0, (p1, p2, p3) = polys[-1][-1], pts
            for i in range(1, steps + 1):
                t = i / steps; u = 1 - t
                polys[-1].append(tuple(u**3*a + 3*u*u*t*b + 3*u*t*t*c_ + t**3*d for a, b, c_, d in zip(p0, p1, p2, p3)))
    return pyclipper.SimplifyPolygons([[(round(x * SCALE), round(y * SCALE)) for x, y in p] for p in polys if len(p) > 2], pyclipper.PFT_NONZERO)

def from_polys(polys):
    out = pathops.Path(); pen = out.getPen()
    for p in polys:
        if len(p) < 3: continue
        pen.moveTo((p[0][0] / SCALE, p[0][1] / SCALE))
        for x, y in p[1:]: pen.lineTo((x / SCALE, y / SCALE))
        pen.closePath()
    return out

def morph_close(polys, r):
    for delta in (r, -r):
        co = pyclipper.PyclipperOffset(); co.ArcTolerance = 0.01 * SCALE
        co.AddPaths(polys, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
        polys = co.Execute(delta * SCALE)
    return polys

def close_region(path, box, r):
    # Close only inside box. Works on a margin around it so the box's own edges don't count as ink edges.
    x0, y0, x1, y1 = box; m = 2 * r + 2
    fill = from_polys(morph_close(to_polys(clip(path, (x0 - m, y0 - m, x1 + m, y1 + m)), steps=12), r))
    return pathops.op(path, clip(fill, box), pathops.PathOp.UNION)

def solidify(path, r, min_hole):
    # Close over the whole mark, all in pyclipper (merging its straight-edged result back into the
    # curved outline makes pathops fail on near-coincident edges), then drop the small holes.
    pc = pyclipper.Pyclipper(); pc.AddPaths(morph_close(to_polys(path), r), pyclipper.PT_SUBJECT, True)
    tree = pc.Execute2(pyclipper.CT_UNION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
    keep = []
    def walk(node):
        for ch in node.Childs:
            if ch.IsHole and abs(pyclipper.Area(ch.Contour)) < min_hole * SCALE * SCALE:
                continue  # a pinhole, and any speck inside it
            keep.append(pyclipper.CleanPolygon(ch.Contour, 0.02 * SCALE)); walk(ch)
    walk(tree)
    return from_polys(keep)

def within(path, box):
    # The contours (letters, their counters, specks) whose bounds sit inside box.
    out = pathops.Path()
    for c in path.contours:
        x0, y0, x1, y1 = c.bounds
        if x0 >= box[0] and y0 >= box[1] and x1 <= box[2] and y1 <= box[3]: out.addPath(c)
    return out

fmt = lambda v: ('%.2f' % v).rstrip('0').rstrip('.')

def write_svg(segs, box, color, out):
    x0, y0, x1, y1 = box
    d = ''.join(c + ' '.join(fmt(px - x0) + ' ' + fmt(py - y0) for px, py in pts) for c, pts in segs)
    open(out, 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(x1 - x0)} {fmt(y1 - y0)}" '
                         f'width="{fmt(x1 - x0)}pt" height="{fmt(y1 - y0)}pt"><path fill="{COLORS[color][0]}" d="{d}"/></svg>\n')

def ps_body(segs, box, ops):
    # Path operators with y flipped back to PostScript/PDF's bottom-up space.
    x0, y0, x1, y1 = box; H = y1 - y0
    out = []
    for c, pts in segs:
        out.append(ops['Z'] if c == 'Z' else ' '.join(fmt(px - x0) + ' ' + fmt(H - (py - y0)) for px, py in pts) + ' ' + ops[c])
    return out

def write_pdf(segs, box, color, out):
    x0, y0, x1, y1 = box; W, H = x1 - x0, y1 - y0
    cs = ['%.3f %.3f %.3f rg' % COLORS[color][1]] + ps_body(segs, box, {'M': 'm', 'L': 'l', 'C': 'c', 'Z': 'h'}) + ['f']
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

def write_eps(segs, box, color, out, title):
    x0, y0, x1, y1 = box; W, H = x1 - x0, y1 - y0
    head = ['%!PS-Adobe-3.0 EPSF-3.0', f'%%BoundingBox: 0 0 {math.ceil(W)} {math.ceil(H)}',
            f'%%HiResBoundingBox: 0 0 {fmt(W)} {fmt(H)}', f'%%Title: {title}', '%%LanguageLevel: 2', '%%EndComments',
            '%.3f %.3f %.3f setrgbcolor' % COLORS[color][1], 'newpath']
    body = ps_body(segs, box, {'M': 'moveto', 'L': 'lineto', 'C': 'curveto', 'Z': 'closepath'})
    open(out, 'w').write('\n'.join(head + body + ['fill', 'showpage', '%%EOF']) + '\n')

def write_png(svg, out):
    subprocess.run(['magick', '-background', 'none', '-density', '600', svg, '-resize', '4800x',
                    '-depth', '8', 'PNG32:' + out], check=True)

def export(path, name):
    segs = segments(path); box = path.bounds
    folder = os.path.join(KIT, name)
    for sub in ('svg', 'pdf', 'eps', 'png'): os.makedirs(os.path.join(folder, sub), exist_ok=True)
    for color in COLORS:
        base = f'{name}-{color}'
        write_svg(segs, box, color, os.path.join(folder, 'svg', base + '.svg'))
        write_pdf(segs, box, color, os.path.join(folder, 'pdf', base + '.pdf'))
        write_eps(segs, box, color, os.path.join(folder, 'eps', base + '.eps'), base)
        write_png(os.path.join(folder, 'svg', base + '.svg'), os.path.join(folder, 'png', base + '-4800px.png'))
    print(name, fmt(box[2] - box[0]), 'x', fmt(box[3] - box[1]), 'pt')

def build():
    logo = read_eps(os.path.join(BRAND, 'emmas-logo-original.eps'))
    for box, r in PATCHES:
        logo = close_region(logo, box, r)
    return solidify(logo, SOLID_R, MIN_HOLE)

if __name__ == '__main__':
    logo = build()
    for name in LAYOUTS:
        shutil.rmtree(os.path.join(KIT, name), ignore_errors=True)
    for name, window in LAYOUTS.items():
        export(logo if window is None else within(logo, window), name)
