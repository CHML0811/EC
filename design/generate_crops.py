#!/usr/bin/env python3
"""
Channel crops — every aspect ratio the marketing plan actually needs.

    python3 design/generate_crops.py

Output: design/crops/

SCOPE: cohorts 1 and 2, matching generate_mockups.py — the designs sold as standalone
prints. Cohort 3 (office) ships inside the kit and is not listed individually.

Two different operations, because "crop it" only works some of the time:

  TRUE CROPS — a window onto the real artwork, measured in the browser rather than
  guessed. The certificate is flex-centred, so hard-coded pixel offsets drift the moment
  a citation runs to three lines. Instead the page is rendered, the target element is
  measured with getBoundingClientRect, and the sheet is transformed so that element
  fills the frame. Exact for every design, no per-design tuning.

    <slug>-crop-title.png   1600×900   the headline, for wide placements
    <slug>-crop-seal.png    1000×1000  the seal, for avatars and detail tiles

  RE-COMPOSITIONS — a 1:1 image cropped to 9:16 loses both sides and the joke with them,
  and cropped to a 3:1 banner loses everything. These are laid out fresh at the target
  ratio instead.

    <slug>-story.png   1080×1920  TikTok, Reels, IG Stories
    <slug>-feed.png    1080×1350  Instagram feed (4:5 — the tallest feed allows)
    <slug>-og.png      1200×630   link previews: iMessage, Slack, Facebook, X

Plus two brand-level banners for the storefront, which belong to no single design:

    hero-wide.png    2400×1000
    hero-mobile.png  1200×1200
"""

import html
import json
import pathlib
import subprocess

import generate_certificates as g
import generate_mockups as m

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "crops"
TMP = ROOT / ".build-crops"

PAPER, INK, RED, OLIVE, FAINT = g.PAPER, g.INK, g.RED, g.OLIVE, g.FAINT
WALL_A, WALL_B, WALL_C = m.WALL_A, m.WALL_B, m.WALL_C

# selector, what to blank out around it, padding, output size
TRUE_CROPS = [
    # the frame is wider than the crop, so hide it too or its edges cut through the type
    ("crop-title", ".block", ".block+.block,.footer,.frame-outer,.frame-inner,.corner,.guilloche",
     70, 1600, 900),
    ("crop-seal", "svg.seal", ".block,.refblock,.sigblock,.frame-outer,.frame-inner,"
     ".corner,.guilloche", 100, 1000, 1000),
]


def crop_page(c: dict, selector: str, hide: str, pad: int, w: int, h: int) -> str:
    """The certificate page, plus a script that frames one element and nothing else."""
    return g.build_html(c) + f"""
<script>
addEventListener("load", function () {{
  var el = document.querySelector({json.dumps(selector)});
  var r = el.getBoundingClientRect();               // measure before touching layout
  // visibility (not display) so hiding neighbours cannot shift what we just measured
  document.querySelectorAll({json.dumps(hide)}).forEach(function (n) {{
    n.style.visibility = "hidden";
  }});
  var W = {w}, H = {h}, PAD = {pad};
  var scale = Math.min(W / (r.width + 2 * PAD), H / (r.height + 2 * PAD));
  var cx = r.left + r.width / 2, cy = r.top + r.height / 2;
  var s = document.querySelector(".sheet");
  s.style.position = "absolute"; s.style.top = "0"; s.style.left = "0";
  s.style.transformOrigin = "0 0";
  s.style.transform = "translate(" + W / 2 + "px," + H / 2 + "px) scale(" + scale +
                      ") translate(" + -cx + "px," + -cy + "px)";
  [document.documentElement, document.body].forEach(function (e) {{
    e.style.width = W + "px"; e.style.height = H + "px"; e.style.overflow = "hidden";
  }});
}});
</script>"""


def scene_story(c: dict) -> str:
    """9:16. Vertical video platforms crop the top and bottom, so nothing vital goes there."""
    phrase = m.PIN_PHRASE[c["slug"]]
    size = 62 if len(phrase) <= 20 else 54 if len(phrase) <= 26 else 46
    css = f"""
  body{{background:radial-gradient(ellipse at 44% 26%, {WALL_A} 0%, {WALL_B} 58%, {WALL_C} 100%);
    padding:230px 70px 250px;display:flex;flex-direction:column;align-items:center;
    justify-content:space-between;text-align:center}}
  .eyebrow{{font-size:23px;letter-spacing:8px}}
  .art{{display:block;width:720px;height:900px;object-fit:cover;
    box-shadow:24px 30px 58px rgba(28,24,16,.32);border:1px solid rgba(0,0,0,.16)}}
  .banner{{width:100%;background:{RED};color:#FBFAF6;padding:34px 28px;
    font-size:{size}px;letter-spacing:3px;text-transform:uppercase;line-height:1.2;
    text-wrap:balance;box-shadow:10px 12px 26px rgba(28,24,16,.26)}}
  .sub{{font-size:29px;line-height:1.5;opacity:.78}}
"""
    body = f"""
<div class="eyebrow">The Bureau of Minor Achievements</div>
<img class="art" src="../out/bma-{c['slug']}.png">
<div class="banner">{html.escape(phrase)}</div>
<div class="sub">Personalized with any name<br>Printed in the USA &middot; arrives in 3&ndash;5 days</div>"""
    return m.page(1080, 1920, css, body)


def scene_feed(c: dict) -> str:
    """4:5. Instagram's tallest feed slot — the artwork sits beside the joke, not under it."""
    n = len(c["title"])
    size = 96 if n <= 20 else 80 if n <= 30 else 66
    css = f"""
  body{{background:{PAPER};padding:82px 76px;display:flex;gap:64px;align-items:center}}
  .left{{flex:0 0 400px}}
  .art{{display:block;width:400px;height:500px;object-fit:cover;
    box-shadow:16px 20px 40px rgba(28,24,16,.26);border:1px solid rgba(0,0,0,.16)}}
  .right{{flex:1;display:flex;flex-direction:column;justify-content:center;gap:26px}}
  .eyebrow{{font-size:19px;letter-spacing:6px;line-height:1.5}}
  .title{{font-size:{size}px;line-height:1.06;font-weight:700;text-transform:uppercase;
    letter-spacing:-1px;text-wrap:balance}}
  .subject{{font-size:27px;letter-spacing:9px;color:{OLIVE};text-transform:uppercase}}
  .rule{{width:150px;height:3px;background:{RED}}}
  .sub{{font-size:26px;line-height:1.5;opacity:.72}}
"""
    body = f"""
<div class="left"><img class="art" src="../out/bma-{c['slug']}.png"></div>
<div class="right">
  <div class="eyebrow">The Bureau of<br>Minor Achievements</div>
  <div class="title">{html.escape(c['title'])}</div>
  <div class="subject">{html.escape(c['subject'])}</div>
  <div class="rule"></div>
  <div class="sub">Personalized with any name.<br>Printed in the USA.</div>
</div>"""
    return m.page(1080, 1350, css, body)


def scene_og(c: dict) -> str:
    """1.91:1. Rendered small in a chat window, so the title carries it alone."""
    n = len(c["title"])
    size = 66 if n <= 22 else 56 if n <= 32 else 47
    css = f"""
  body{{background:{PAPER};padding:56px 64px;display:flex;gap:54px;align-items:center}}
  .art{{flex:0 0 auto;display:block;width:414px;height:518px;object-fit:cover;
    box-shadow:12px 15px 32px rgba(28,24,16,.24);border:1px solid rgba(0,0,0,.16)}}
  .right{{flex:1;display:flex;flex-direction:column;gap:20px}}
  .eyebrow{{font-size:17px;letter-spacing:6px}}
  .title{{font-size:{size}px;line-height:1.08;font-weight:700;text-transform:uppercase;
    letter-spacing:-1px;text-wrap:balance}}
  .rule{{width:130px;height:3px;background:{RED}}}
  .sub{{font-size:24px;line-height:1.5;opacity:.72}}
"""
    body = f"""
<img class="art" src="../out/bma-{c['slug']}.png">
<div class="right">
  <div class="eyebrow">The Bureau of Minor Achievements</div>
  <div class="title">{html.escape(c['title'])}</div>
  <div class="rule"></div>
  <div class="sub">Official recognition for things that don't deserve any.<br>
    Personalized, printed in the USA.</div>
</div>"""
    return m.page(1200, 630, css, body)


def hero(w: int, h: int, stack: bool) -> str:
    """Storefront banner. Three certificates overlapped, because the line is the product."""
    picks = ["bma-retirement.png", "bma-uncle.png", "bma-x-secret-santa.png"]
    css = f"""
  /* centred with a fixed gap — space-between strands the two halves at opposite edges */
  body{{background:radial-gradient(ellipse at 34% 26%, {WALL_A} 0%, {WALL_B} 60%, {WALL_C} 100%);
    display:flex;flex-direction:{'column' if stack else 'row'};align-items:center;
    justify-content:center;
    gap:{'56px' if stack else '110px'};padding:{'78px 70px' if stack else '90px 110px'};
    text-align:{'center' if stack else 'left'}}}
  .copy{{max-width:{'none' if stack else '780px'}}}
  .eyebrow{{font-size:{20 if stack else 22}px;letter-spacing:7px;color:{RED};
    text-transform:uppercase;white-space:nowrap}}
  h1{{margin-top:26px;font-size:{74 if stack else 90}px;line-height:1.04;font-weight:700;
    letter-spacing:-2px;text-wrap:balance}}
  .sub{{margin-top:26px;font-size:{29 if stack else 32}px;line-height:1.5;opacity:.74;
    max-width:{'none' if stack else '30ch'}}}
  /* height tracks the tallest card plus its offset, or the fan floats in dead space */
  .fan{{position:relative;flex:0 0 auto;width:{560 if stack else 820}px;
    height:{397 if stack else 613}px}}
  .fan img{{position:absolute;top:0;width:{300 if stack else 460}px;
    height:{375 if stack else 575}px;object-fit:cover;border:1px solid rgba(0,0,0,.18);
    box-shadow:16px 22px 44px rgba(28,24,16,.28)}}
  .f1{{left:0;transform:rotate(-7deg)}}
  .f2{{left:{130 if stack else 180}px;top:{22 if stack else 38}px;z-index:2}}
  .f3{{left:{260 if stack else 360}px;transform:rotate(6deg)}}
"""
    body = f"""
<div class="copy">
  <div class="eyebrow">The Bureau of Minor Achievements</div>
  <h1>Official recognition for things that don't deserve any.</h1>
  <div class="sub">Personalized certificates, printed in the USA, delivered in 3–5 days.</div>
</div>
<div class="fan">
  <img class="f1" src="../out/{picks[0]}">
  <img class="f2" src="../out/{picks[1]}">
  <img class="f3" src="../out/{picks[2]}">
</div>"""
    return m.page(w, h, css, body)


SCENES = [("story", scene_story, 1080, 1920),
          ("feed", scene_feed, 1080, 1350),
          ("og", scene_og, 1200, 630)]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    chrome = g.find_chrome()

    def shot(src: pathlib.Path, png: pathlib.Path, w: int, h: int) -> None:
        subprocess.run(
            [chrome, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
             "--allow-file-access-from-files", "--force-device-scale-factor=1",
             "--virtual-time-budget=3000",
             f"--window-size={w},{h}", f"--screenshot={png}", src.as_uri()],
            check=True, capture_output=True)

    certs = []
    for man in ("manifest.json", "manifest-christmas.json"):
        certs += json.loads((ROOT / "out" / man).read_text(encoding="utf-8"))

    total = 0
    for c in certs:
        for name, sel, hide, pad, w, h in TRUE_CROPS:
            src = TMP / f"{c['slug']}-{name}.html"
            src.write_text(crop_page(c, sel, hide, pad, w, h), encoding="utf-8")
            shot(src, OUT / f"{c['slug']}-{name}.png", w, h)
            total += 1
        for name, fn, w, h in SCENES:
            src = TMP / f"{c['slug']}-{name}.html"
            src.write_text(fn(c), encoding="utf-8")
            shot(src, OUT / f"{c['slug']}-{name}.png", w, h)
            total += 1
        print(f"  {c['slug']:<18} 5 crops")

    for name, w, h, stack in [("hero-wide", 2400, 1000, False),
                              ("hero-mobile", 1200, 1200, True)]:
        src = TMP / f"{name}.html"
        src.write_text(hero(w, h, stack), encoding="utf-8")
        shot(src, OUT / f"{name}.png", w, h)
        total += 1
    print(f"  {'storefront banners':<18} 2")

    print(f"\n{total} crops -> {OUT}")


if __name__ == "__main__":
    main()
