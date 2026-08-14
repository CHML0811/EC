# Listing images — 96 of them, generated

`python3 design/generate_mockups.py` → `design/mockups/`

Six images per certificate, all 16 designs. No Printify account, no camera, no image
credits — same headless-Chromium trick as the artwork itself.

**Why this existed as a blocker:** Etsy ranks on conversion, and conversion is decided in
the search grid before anyone reads a word. A listing with no images doesn't convert, and
the two normal ways to get product photos — Printify's mockup generator, or a camera —
both needed something we don't have yet. So the images are rendered instead.

---

## The set

| # | File | Size | Job |
|---|---|---|---|
| 1 | `<slug>-1-framed.png` | 2000² | Framed on a wall. The buyer picturing it hung. **This is the thumbnail.** |
| 2 | `<slug>-2-hook.png` | 2000² | The joke at thumbnail size — the only image that survives being 200px wide |
| 3 | `<slug>-3-detail.png` | 2000² | Seal and serial, close. Proof it isn't clip art |
| 4 | `<slug>-4-sizes.png` | 2000² | 8×10 vs 11×14 drawn to true scale. Kills the "how big is it" message |
| 5 | `<slug>-5-info.png` | 2000² | What actually arrives — stock, shipping, personalization, mailer |
| 6 | `<slug>-6-pin.png` | 1000×1500 | Pinterest 2:3, search phrase banded across |

Images 1–5 go on the Etsy listing **in that order**. Etsy uses the first as the grid
thumbnail, so 1 must be the framed shot — it's the one that reads as a real product.

Image 6 is Pinterest only. Don't upload it to Etsy; the banner text looks like an ad in a
product grid and Etsy shoppers scroll past ads.

## The banner phrases

Image 6 carries the phrase a US buyer actually types, not the joke title. `Certified Uncle`
is the product; `Funny Gift for Uncle` is the search. The full map is in
`generate_mockups.py` → `PIN_PHRASE`, and mirrored into `mockups/index.json` after a run.

## Replacing these with Printify mockups

Once Printify exists, its generated mockups are *better for image 1* — real paper, real
frame, real room. Swap image 1, keep 2–6. Images 2, 3 and 5 are typographic and Printify
has no equivalent; image 4 is drawn to scale and Printify's size charts are worse.

So: **Printify replaces one of the six, not all six.**

## Changing them

Everything is in `generate_mockups.py`. One function per scene, plain HTML and CSS.
Re-render the whole set in about 40 seconds:

```bash
python3 design/generate_certificates.py   # cohort 1 artwork
python3 design/certs_christmas.py         # cohort 2 artwork
python3 design/generate_mockups.py        # all 96 listing images
```

The artwork must be regenerated first — the framed, sizes and pin scenes load the PNGs
from `design/out/`.
