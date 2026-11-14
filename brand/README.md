# Emma's wordmark

Vector traces of the hand-lettered "Emma's" from the original logo scan, for merch and large-format use.

- `emmas-wordmark-textured.svg` — keeps the stamped, rough edge of the original. Use for screen printing, paper, signage.
- `emmas-wordmark-smooth.svg` — edges simplified. Use for embroidery, vinyl cutting, engraving, or anything that struggles with fine detail.
- `*-white.svg` — same shapes filled white, for dark garments and backgrounds.
- `*.pdf` — vector PDFs of the ink versions for printers that want PDF.
- `*-4800px.png` — raster exports at 4800 px wide with transparent background (about 16 in at 300 dpi).

Ink color on the menu is `#2E2620`.

Sources: `emmas-wordmark-scan-transparent.png` (the crop the traces were made from) and `emmas-logo-full-transparent.png` (the whole logo, cleaned, on transparency). The original scan is in `../source/`.

## Full logo

The whole boxed logo ("Emma's / Country / Kitchen"), from the owner's original 2013 vector rather than a trace.

- `emmas-logo-original.eps` — the original EPS, as supplied. Gray `#6C6867` on an off-white background, with letter counters drawn as off-white shapes.
- `emmas-logo.svg` — the same artwork as one compound path in menu ink, counters cut out, background removed, cropped to the box.
- `emmas-logo-white.svg` — same shape filled white.
- `emmas-logo.pdf` — vector PDF of the ink version.
- `emmas-logo-4800px.png`, `emmas-logo-white-4800px.png` — raster exports at 4800 px wide with transparent background.

The "Emma's" from that same vector, cropped tight, comes in the same set: `emmas-wordmark.svg`, `emmas-wordmark-white.svg`, `emmas-wordmark.pdf`, `emmas-wordmark-4800px.png`, `emmas-wordmark-white-4800px.png`. It is the original artwork, so prefer it to the scan traces above; keep the smooth trace for embroidery and other jobs that need simpler edges.

All ten files are generated from the EPS by `../scripts/export_logo.py` (needs `pip install skia-pathops` and ImageMagick).
