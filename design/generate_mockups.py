#!/usr/bin/env python3
"""
Listing imagery for all 16 Bureau certificates — generated, not photographed.

Etsy ranks on conversion and conversion is decided by the image grid, but Printify
mockups need a Printify account and photos need a camera. This renders the whole set
with headless Chromium instead: six images per certificate, no account, no credits.

    python3 design/generate_mockups.py

Output: design/mockups/<slug>-{1..6}-*.png

  1 framed   2000x2000  framed on a wall — the buyer picturing it hung
  2 hook     2000x2000  the joke at thumbnail size — this one wins the search grid
  3 detail   2000x2000  seal and serial close up — proof it isn't clip art
  4 sizes    2000x2000  8x10 vs 11x14 drawn to scale — kills the "how big" question
  5 info     2000x2000  what actually arrives — handles the rest of the objections
  6 pin      1000x1500  Pinterest 2:3, search phrase banded across

Etsy wants image 1 first in the grid; upload in numeric order and that happens.
"""

import html
import json
import pathlib
import subprocess

import generate_certificates as g

ROOT = pathlib.Path(__file__).resolve().parent
CERTS = ROOT / "out"
OUT = ROOT / "mockups"
TMP = ROOT / ".build-mockups"

SQ = 2000          # Etsy listing images
PW, PH = 1000, 1500  # Pinterest 2:3

PAPER, INK, RED, OLIVE, FAINT = g.PAPER, g.INK, g.RED, g.OLIVE, g.FAINT
WALL_A, WALL_B, WALL_C = "#EDE9E1", "#DCD7CC", "#C9C3B6"

# What a US buyer actually types into the search bar. Not the joke — the query.
PIN_PHRASE = {
    "retirement":       "Funny Retirement Gift",
    "coworker":         "Funny Coworker Gift",
    "uncle":            "Funny Gift for Uncle",
    "boss":             "Funny Boss Gift",
    "new-home":         "Funny Housewarming Gift",
    "new-parent":       "Funny New Parent Gift",
    "graduation":       "Funny Graduation Gift",
    "left-on-read":     "Funny Gift for a Friend",
    "x-secret-santa":   "Secret Santa Gift Idea",
    "x-white-elephant": "White Elephant Gift",
    "x-survived-year":  "Funny Office Christmas Gift",
    "x-office-party":   "Office Party Gift Idea",
    "x-okayest-gift":   "Funny Christmas Gift",
    "x-mom":            "Funny Gift for Mom",
    "x-dad":            "Funny Gift for Dad",
    "x-stocking":       "Funny Stocking Stuffer",
}

BASE_CSS = f"""
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:"Liberation Serif","Times New Roman",serif;color:{INK};
    -webkit-font-smoothing:antialiased}}
  .eyebrow{{font-size:30px;letter-spacing:11px;color:{RED};text-transform:uppercase}}
  .mono{{font-family:"Liberation Mono",monospace}}
"""


def band(width: int) -> str:
    """The engine-turned wave band, reused from the certificate plate."""
    return f"""
<svg viewBox="0 0 1200 40" preserveAspectRatio="none" width="{width}" height="34"
     xmlns="http://www.w3.org/2000/svg">
  <defs><pattern id="wv{width}" width="60" height="40" patternUnits="userSpaceOnUse">
    <path d="M0,20 C15,2 15,38 30,20 C45,2 45,38 60,20" fill="none" stroke="{FAINT}" stroke-width="1.6"/>
    <path d="M0,20 C15,38 15,2 30,20 C45,38 45,2 60,20" fill="none" stroke="{FAINT}" stroke-width="1.6"/>
  </pattern></defs>
  <rect width="1200" height="40" fill="url(#wv{width})"/>
</svg>"""


def page(w: int, h: int, css: str, body: str) -> str:
    return f"""<!doctype html>
<meta charset="utf-8">
<style>{BASE_CSS}
  html,body{{width:{w}px;height:{h}px;overflow:hidden}}
  {css}
</style>
{body}"""


# --- 1 · framed on a wall ------------------------------------------------------
def scene_framed(c: dict) -> str:
    css = f"""
  body{{background:radial-gradient(ellipse at 40% 32%, {WALL_A} 0%, {WALL_B} 58%, {WALL_C} 100%);
    display:flex;align-items:center;justify-content:center}}
  .frame{{position:relative;padding:34px;border-radius:3px;
    background:linear-gradient(148deg,#3B342A 0%,#211C15 42%,#2E281F 70%,#161209 100%);
    box-shadow:44px 56px 92px rgba(28,24,16,.34), 8px 10px 22px rgba(28,24,16,.22),
               inset 0 0 0 2px rgba(255,255,255,.06)}}
  .mat{{padding:92px;background:#FBFAF6;
    box-shadow:inset 0 0 0 1px rgba(0,0,0,.14), inset 2px 3px 9px rgba(0,0,0,.13)}}
  .art{{position:relative;display:block;width:1050px;height:1312px;object-fit:cover}}
  /* glass, kept faint so the type stays legible */
  .sheen{{position:absolute;inset:34px;pointer-events:none;
    background:linear-gradient(116deg,rgba(255,255,255,.20) 0%,rgba(255,255,255,0) 34%,
      rgba(255,255,255,0) 62%,rgba(255,255,255,.11) 100%)}}
"""
    body = f"""
<div class="frame">
  <div class="mat"><img class="art" src="../out/bma-{c['slug']}.png"></div>
  <div class="sheen"></div>
</div>"""
    return page(SQ, SQ, css, body)


# --- 2 · the hook --------------------------------------------------------------
def scene_hook(c: dict) -> str:
    n = len(c["title"])
    size = 250 if n <= 18 else 206 if n <= 26 else 172 if n <= 34 else 146
    css = f"""
  body{{background:{PAPER};padding:150px 160px;display:flex;flex-direction:column;
    align-items:center;justify-content:space-between;text-align:center}}
  .title{{font-size:{size}px;line-height:1.03;font-weight:700;text-transform:uppercase;
    letter-spacing:-2px;text-wrap:balance}}
  .subject{{margin-top:52px;font-size:60px;letter-spacing:18px;color:{OLIVE};
    text-transform:uppercase}}
  .rule{{width:300px;height:3px;background:{RED};margin:56px auto 0}}
  .foot{{font-size:34px;letter-spacing:6px;text-transform:uppercase;opacity:.66}}
"""
    body = f"""
<div class="eyebrow">The Bureau of Minor Achievements</div>
<div>
  <div class="title">{html.escape(c['title'])}</div>
  <div class="subject">{html.escape(c['subject'])}</div>
  <div class="rule"></div>
</div>
<div class="foot">Personalized with any name</div>"""
    return page(SQ, SQ, css, body)


# --- 3 · seal and serial -------------------------------------------------------
def scene_detail(c: dict) -> str:
    css = f"""
  body{{background:{PAPER};padding:130px 160px;display:flex;flex-direction:column;
    align-items:center;justify-content:space-between;text-align:center}}
  .seal{{width:820px;height:820px}}
  .caption{{font-size:52px;line-height:1.5;width:1560px}}
  .ref{{margin-top:40px;font-size:31px;letter-spacing:4px;line-height:2;opacity:.6}}
  .waves{{opacity:.85;line-height:0}}
"""
    body = f"""
<div class="waves">{band(1680)}</div>
{g.seal_svg(c['seal'])}
<div>
  <div class="caption">Embossed-look seal, hand-drawn laurel,<br>and a serial number that means nothing.</div>
  <div class="ref mono">REF&nbsp; {c['ref']} &nbsp;&middot;&nbsp; STATUS&nbsp; IRREVOCABLE</div>
</div>
<div class="waves">{band(1680)}</div>"""
    return page(SQ, SQ, css, body)


# --- 4 · sizes, drawn to scale -------------------------------------------------
def scene_sizes(c: dict) -> str:
    ppi = 74  # px per inch on this canvas — the two blocks are truly proportional
    css = f"""
  body{{background:{PAPER};padding:120px 100px;display:flex;flex-direction:column;
    align-items:center;justify-content:space-between;text-align:center}}
  .row{{display:flex;align-items:flex-end;gap:120px}}
  .item{{display:flex;flex-direction:column;align-items:center}}
  .plate{{background:#fff;box-shadow:0 0 0 2px {INK}, 18px 22px 40px rgba(30,26,18,.20)}}
  .plate img{{display:block;width:100%;height:100%;object-fit:cover}}
  .s8{{width:{8*ppi}px;height:{10*ppi}px}}
  .s11{{width:{11*ppi}px;height:{14*ppi}px}}
  .label{{margin-top:38px;font-size:56px;letter-spacing:4px}}
  .sub{{margin-top:10px;font-size:29px;letter-spacing:6px;text-transform:uppercase;opacity:.55}}
  .foot{{font-size:34px;line-height:1.6;opacity:.72}}
"""
    img = f'<img src="../out/bma-{c["slug"]}.png">'
    body = f"""
<div class="eyebrow">Shown actual proportions</div>
<div class="row">
  <div class="item">
    <div class="plate s8">{img}</div>
    <div class="label">8&Prime; &times; 10&Prime;</div><div class="sub">$32</div>
  </div>
  <div class="item">
    <div class="plate s11">{img}</div>
    <div class="label">11&Prime; &times; 14&Prime;</div><div class="sub">$42</div>
  </div>
</div>
<div class="foot">Fits any standard frame &middot; framed option available at checkout</div>"""
    return page(SQ, SQ, css, body)


# --- 5 · what arrives ----------------------------------------------------------
FACTS = [
    ("Printed in the USA", "Dispatched in 2–3 business days, delivered in 3–5."),
    ("Heavy matte poster stock", "No glare, no shine. It reads as a document, which is the joke."),
    ("Personalized with any name", "Type it at checkout. We print it exactly as typed."),
    ("Two sizes, framed if you want", "8×10 or 11×14. Fits standard frames."),
    ("Ships flat in a rigid mailer", "Arrives uncreased, or we replace it."),
]


def scene_info(c: dict) -> str:
    css = f"""
  body{{background:{PAPER};padding:120px 130px;display:flex;flex-direction:column;
    justify-content:space-between}}
  .head{{text-align:center}}
  .rule{{width:240px;height:3px;background:{RED};margin:34px auto 0}}
  .fact{{display:flex;gap:44px;align-items:flex-start;padding:36px 0;
    border-bottom:2px solid rgba(23,21,15,.13)}}
  .fact:last-child{{border-bottom:0}}
  .num{{flex:0 0 76px;height:76px;border:3px solid {RED};color:{RED};border-radius:50%;
    display:flex;align-items:center;justify-content:center;font-size:38px}}
  .ft{{font-size:52px;line-height:1.22}}
  .fd{{margin-top:12px;font-size:35px;line-height:1.45;opacity:.68}}
  .foot{{text-align:center;font-size:31px;letter-spacing:7px;text-transform:uppercase;
    color:{RED}}}
"""
    rows = "".join(
        f'<div class="fact"><div class="num">{i}</div><div>'
        f'<div class="ft">{t}</div><div class="fd">{d}</div></div></div>'
        for i, (t, d) in enumerate(FACTS, 1)
    )
    body = f"""
<div class="head">
  <div class="eyebrow">What arrives</div>
  <div class="rule"></div>
</div>
<div>{rows}</div>
<div class="foot">The Bureau of Minor Achievements</div>"""
    return page(SQ, SQ, css, body)


# --- 6 · Pinterest -------------------------------------------------------------
def scene_pin(c: dict) -> str:
    phrase = PIN_PHRASE[c["slug"]]
    size = 58 if len(phrase) <= 20 else 50 if len(phrase) <= 26 else 43
    css = f"""
  body{{background:radial-gradient(ellipse at 42% 30%, {WALL_A} 0%, {WALL_B} 60%, {WALL_C} 100%);
    padding:64px 62px;display:flex;flex-direction:column;align-items:center;
    justify-content:space-between;text-align:center}}
  .eyebrow{{font-size:21px;letter-spacing:7px}}
  .art{{display:block;width:660px;height:825px;object-fit:cover;
    box-shadow:22px 28px 52px rgba(28,24,16,.30);border:1px solid rgba(0,0,0,.16)}}
  .banner{{width:100%;background:{RED};color:#FBFAF6;padding:32px 30px;
    font-size:{size}px;letter-spacing:3px;text-transform:uppercase;line-height:1.2;
    text-wrap:balance;box-shadow:10px 12px 26px rgba(28,24,16,.26)}}
  .sub{{font-size:27px;line-height:1.5;opacity:.76}}
"""
    body = f"""
<div class="eyebrow">The Bureau of Minor Achievements</div>
<img class="art" src="../out/bma-{c['slug']}.png">
<div class="banner">{html.escape(phrase)}</div>
<div class="sub">Personalized with any name<br>Printed in the USA &middot; arrives in 3&ndash;5 days</div>"""
    return page(PW, PH, css, body)


SCENES = [
    ("1-framed", scene_framed, SQ, SQ),
    ("2-hook", scene_hook, SQ, SQ),
    ("3-detail", scene_detail, SQ, SQ),
    ("4-sizes", scene_sizes, SQ, SQ),
    ("5-info", scene_info, SQ, SQ),
    ("6-pin", scene_pin, PW, PH),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    chrome = g.find_chrome()

    certs = []
    for m in ("manifest.json", "manifest-christmas.json"):
        certs += json.loads((CERTS / m).read_text(encoding="utf-8"))

    total = 0
    index = {}
    for c in certs:
        files = []
        for name, fn, w, h in SCENES:
            src = TMP / f"{c['slug']}-{name}.html"
            png = OUT / f"{c['slug']}-{name}.png"
            src.write_text(fn(c), encoding="utf-8")
            subprocess.run(
                [chrome, "--headless", "--disable-gpu", "--no-sandbox",
                 "--hide-scrollbars", "--force-device-scale-factor=1",
                 "--allow-file-access-from-files",
                 f"--window-size={w},{h}", f"--screenshot={png}", src.as_uri()],
                check=True, capture_output=True,
            )
            files.append(png.name)
            total += 1
        index[c["slug"]] = {"phrase": PIN_PHRASE[c["slug"]], "files": files}
        kb = sum((OUT / f).stat().st_size for f in files) / 1024
        print(f"  {c['slug']:<18} {len(files)} images  {kb:7.0f} KB")

    (OUT / "index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"\n{total} images -> {OUT}")


if __name__ == "__main__":
    main()
