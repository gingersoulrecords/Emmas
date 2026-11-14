# Emma's Country Kitchen menu

Menu redesign for Emma's Country Kitchen: a two-sided legal sheet (8.5 x 14), food on one side and drinks on the other, set in Alegreya, Alegreya Sans, and their small caps.

## Layout

- `project/` — the design canvas files as published to Claude. `LowerSerif.dc.html` is the food side, `Drinks.dc.html` the drinks side; the other `.dc.html` files are earlier explorations kept for reference. `canvas.json` is the canvas index.
- `scripts/` — the Python that generates the two live artboards from the menu data. `gen5.py` holds the food menu (items, prices, copy) and builds the food side; `gen6.py` holds the drinks menu and builds the drinks side (it runs gen5 first). `gen3.py` and `data.py` are shared helpers. Run `python3 scripts/gen6.py` from `scripts/` to regenerate both pages into `project/`. `export_logo.py` builds the client logo kit in `brand/emmas-logo-kit/` from the original EPS.
- `brand/` — the logo kit for the client (full logo, logo without the box, and "Emma's", in vector and raster), the original EPS, and older scan traces. See `brand/README.md`.
- `source/` — the owner's menus and the logo scan the work started from.

## Type and color

- Dish names: Alegreya Sans 400, lowercase.
- Section heads: Alegreya Sans SC 500, 13 px, 0.1em tracking, with a 0.5 px rule beneath.
- Descriptions: Alegreya italic 400, 14 px, `#7A6E63`.
- Prices: Alegreya 400, old-style figures.
- Ink `#2E2620`, paper `#FBF8F1`.

## Pig icon

The pork note on the food side uses the "pig" icon by Delapouite from game-icons.net, CC BY 3.0. It needs a credit line if the menu is distributed; the Health Icons pig (MIT) is a drop-in alternative that does not.

## Open questions for the owner

See the end of the working conversation; at last check: whether the benny's biscuit is split, bleed and fold requirements from the printer, and the pig icon credit.
