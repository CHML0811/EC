#!/usr/bin/env python3
"""
Listing images for the Office Awards Kit.

    python3 kit/build_listing_images.py

Output: kit/listing/kit-{1..5}-*.png at 2000x2000

A digital product has no photograph, so the images have to do the explaining: what you
get, how many, and — the objection that actually blocks the sale — whether you'll be able
to use it. Image 3 exists purely to prove the maker is real software and not a promise.
"""

import base64
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
sys.path.insert(0, str(REPO / "design"))
import generate_certificates as g  # noqa: E402
import generate_mockups as m  # noqa: E402

OUT = ROOT / "listing"
TMP = ROOT / ".build-listing"
SQ = 2000
PAPER, INK, RED, OLIVE, FAINT = g.PAPER, g.INK, g.RED, g.OLIVE, g.FAINT

CONTENTS = [
    ("38", "personalized award certificates"),
    ("1", "certificate maker — type a name, print"),
    ("1", "host's script, word for word"),
    ("1", "nomination ballot for the office"),
    ("1", "set of fold-over name tents"),
    ("3", "announcement emails, ready to send"),
]


def page(w, h, css, body):
    return m.page(w, h, css, body)


def scene_hero() -> str:
    css = f"""
  body{{background:{PAPER};padding:140px 150px;display:flex;flex-direction:column;
    justify-content:space-between}}
  .top{{text-align:center}}
  .eyebrow{{font-size:30px;letter-spacing:12px;color:{RED};text-transform:uppercase}}
  h1{{margin-top:44px;font-size:158px;line-height:1.02;font-weight:700;
    text-transform:uppercase;letter-spacing:-3px;text-wrap:balance}}
  .rule{{width:280px;height:4px;background:{RED};margin:46px auto 0}}
  .list{{display:flex;flex-direction:column;gap:0}}
  .row{{display:flex;align-items:baseline;gap:34px;padding:26px 0;
    border-bottom:2px solid rgba(23,21,15,.13)}}
  .row:last-child{{border-bottom:0}}
  .q{{flex:0 0 130px;text-align:right;font-size:62px;font-weight:700;color:{RED};
    font-family:"Liberation Mono",monospace}}
  .w{{font-size:46px;line-height:1.3}}
  .foot{{text-align:center;font-size:34px;letter-spacing:6px;text-transform:uppercase;
    opacity:.66}}
"""
    rows = "".join(f'<div class="row"><div class="q">{q}</div><div class="w">{w}</div></div>'
                   for q, w in CONTENTS)
    body = f"""
<div class="top">
  <div class="eyebrow">The Bureau of Minor Achievements</div>
  <h1>The Office<br>Awards Kit</h1>
  <div class="rule"></div>
</div>
<div class="list">{rows}</div>
<div class="foot">Instant download &middot; nothing to install</div>"""
    return page(SQ, SQ, css, body)


def scene_grid(slugs) -> str:
    css = f"""
  body{{background:{PAPER};padding:120px 110px;display:flex;flex-direction:column;
    justify-content:space-between;text-align:center}}
  .eyebrow{{font-size:30px;letter-spacing:12px;color:{RED};text-transform:uppercase}}
  h2{{margin-top:22px;font-size:104px;font-weight:700;text-transform:uppercase;
    letter-spacing:-2px}}
  /* 8 wide fits 38 tiles in 5 rows; 7 wide needs 6 and the last row falls off the sheet */
  .grid{{display:grid;grid-template-columns:repeat(8,1fr);gap:18px;justify-items:center}}
  .grid img{{width:100%;aspect-ratio:4/5;object-fit:cover;border:1px solid rgba(0,0,0,.2);
    box-shadow:5px 6px 14px rgba(28,24,16,.16)}}
  .foot{{font-size:36px;line-height:1.45;opacity:.72}}
"""
    # absolute file:// URIs — the build dir is kit/.build-listing, not alongside design/
    tiles = "".join(f'<img src="{(REPO / "design" / "out" / f"bma-{s}.png").as_uri()}">'
                    for s in slugs)
    body = f"""
<div>
  <div class="eyebrow">Enough for everyone</div>
  <h2>38 different awards</h2>
</div>
<div class="grid">{tiles}</div>
<div class="foot">Nobody has to be left out — which is the one thing<br>
  that ruins an office awards ceremony.</div>"""
    return page(SQ, SQ, css, body)


def scene_shot(img_b64: str, eyebrow: str, head: str, sub: str) -> str:
    css = f"""
  body{{background:{PAPER};padding:120px 110px;display:flex;flex-direction:column;
    justify-content:space-between;text-align:center}}
  .eyebrow{{font-size:30px;letter-spacing:12px;color:{RED};text-transform:uppercase}}
  h2{{margin-top:22px;font-size:96px;font-weight:700;text-transform:uppercase;
    letter-spacing:-2px;text-wrap:balance;line-height:1.05}}
  .shot{{border:2px solid {INK};box-shadow:20px 24px 48px rgba(28,24,16,.24);
    max-height:900px;overflow:hidden}}
  .shot img{{width:100%;display:block}}
  .foot{{font-size:38px;line-height:1.45;opacity:.74}}
"""
    body = f"""
<div><div class="eyebrow">{eyebrow}</div><h2>{head}</h2></div>
<div class="shot"><img src="data:image/png;base64,{img_b64}"></div>
<div class="foot">{sub}</div>"""
    return page(SQ, SQ, css, body)


def scene_promise() -> str:
    items = [
        ("Instant download", "Files arrive the moment you pay. No shipping, no waiting."),
        ("Works offline", "The maker is one HTML file. No account, no subscription, no app."),
        ("Print at home", "Any printer, any paper. Or send the PDF to a print shop."),
        ("Use it every year", "Yours forever. Rename the awards, change the citations."),
    ]
    css = f"""
  body{{background:{PAPER};padding:150px 140px;display:flex;flex-direction:column;
    justify-content:space-between}}
  .top{{text-align:center}}
  .eyebrow{{font-size:30px;letter-spacing:12px;color:{RED};text-transform:uppercase}}
  h2{{margin-top:30px;font-size:112px;font-weight:700;text-transform:uppercase;
    letter-spacing:-2px}}
  .items{{display:flex;flex-direction:column;gap:52px}}
  .it{{display:flex;gap:44px;align-items:flex-start}}
  .tick{{flex:0 0 78px;height:78px;border:4px solid {RED};border-radius:50%;color:{RED};
    display:flex;align-items:center;justify-content:center;font-size:44px}}
  .ih{{font-size:56px;line-height:1.15}}
  .ip{{margin-top:12px;font-size:37px;line-height:1.42;opacity:.7}}
  .foot{{text-align:center;font-size:32px;letter-spacing:7px;text-transform:uppercase;
    color:{RED}}}
"""
    rows = "".join(f'<div class="it"><div class="tick">&#10003;</div><div>'
                   f'<div class="ih">{h}</div><div class="ip">{p}</div></div></div>'
                   for h, p in items)
    body = f"""
<div class="top"><div class="eyebrow">What you get</div><h2>No catch</h2></div>
<div class="items">{rows}</div>
<div class="foot">The Bureau of Minor Achievements</div>"""
    return page(SQ, SQ, css, body)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    chrome = g.find_chrome()

    def shot(html_text: str, name: str, w=SQ, h=SQ) -> None:
        src = TMP / f"{name}.html"
        src.write_text(html_text, encoding="utf-8")
        subprocess.run(
            [chrome, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
             "--allow-file-access-from-files", "--force-device-scale-factor=1",
             "--virtual-time-budget=4000",
             f"--window-size={w},{h}", f"--screenshot={OUT / (name + '.png')}", src.as_uri()],
            check=True, capture_output=True)

    slugs = []
    for man in ("manifest.json", "manifest-christmas.json", "manifest-office.json"):
        p = REPO / "design" / "out" / man
        if p.exists():
            slugs += [c["slug"] for c in json.loads(p.read_text(encoding="utf-8"))]

    # screenshots of the real thing — the maker, and the script
    maker = TMP / "_maker.png"
    subprocess.run(
        [chrome, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
         "--virtual-time-budget=4000", "--window-size=1500,1000",
         f"--screenshot={maker}", (ROOT / "dist" / "AwardsMaker.html").resolve().as_uri()],
        check=True, capture_output=True)

    shot(scene_hero(), "kit-1-hero")
    shot(scene_grid(slugs), "kit-2-grid")
    shot(scene_shot(base64.b64encode(maker.read_bytes()).decode(),
                    "Included: the maker",
                    "Type a name.<br>Press print.",
                    "38 awards, any name, any number of people. Works in any browser."),
         "kit-3-maker")
    shot(scene_promise(), "kit-4-promise")

    for p in sorted(OUT.glob("*.png")):
        print(f"  {p.name:<22} {p.stat().st_size/1024:6.0f} KB")
    print(f"\n{len(list(OUT.glob('*.png')))} listing images -> {OUT}")


if __name__ == "__main__":
    main()
