# Emma's brand files

## Logo kit

`emmas-logo-kit/` is the client set, made from the owner's original 2013 vector rather than a trace. Its `README.txt` is written for the client.

- Three layouts: `emmas-logo-box` (the full logo), `emmas-logo-no-box` (the lettering and the two rules, without the frame) and `emmas-wordmark` ("Emma's").
- Three colors each: `ink` (`#2E2620`, the menu ink), `black` and `white`.
- Each as SVG, PDF and EPS, plus a 4800px PNG with a transparent background.

`emmas-logo-original.eps` is the source, as supplied: gray `#6C6867` on an off-white background, with the letter counters drawn as off-white shapes.

`../scripts/export_logo.py` builds the kit from it (needs `pip install skia-pathops pyclipper` and ImageMagick). On the way it:

- cuts the off-white counters and specks out as real holes and drops the background;
- fills two blemishes, the crack through the E's middle bar and the ink trap where the a's bowl meets its stem (`PATCHES`);
- fills the cracks and pinholes inside every stroke so the letters read solid while the edges stay rough (`SOLID_R` 1.75 pt, `MIN_HOLE` 60 pt²). The outline comes out as fine straight segments, accurate to 0.02 pt.

## Scan traces

Older vector traces of "Emma's" from the logo scan. The kit's wordmark replaces them, except where a job needs simpler edges.

- `emmas-wordmark-textured.svg` keeps the stamped, rough edge of the scan.
- `emmas-wordmark-smooth.svg` has simplified edges. Use it for embroidery, vinyl cutting, engraving, or anything that struggles with fine detail.
- `*-white.svg` are the same shapes filled white, `*.pdf` vector PDFs of the ink versions, and `*-4800px.png` transparent exports at 4800 px wide (about 16 in at 300 dpi).

Sources: `emmas-wordmark-scan-transparent.png` (the crop the traces were made from) and `emmas-logo-full-transparent.png` (the whole logo, cleaned, on transparency). The original scan is in `../source/`.
