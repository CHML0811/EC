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

XMAS_CONTENTS = [
    ("38", "awards, including 8 for Christmas"),
    ("1", "certificate maker — type a name, print"),
    ("1", "host's script, word for word"),
    ("1", "nomination ballot for the office"),
    ("1", "set of fold-over name tents"),
    ("3", "announcement emails, ready to send"),
]

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


HEROES = {
    "office":    ("bma-o-punctuality.png", "bma-o-email-meeting.png",
                  "Funny Office<br>Awards", "38 printable award certificates"),
    "christmas": ("bma-x-secret-santa.png", "bma-x-office-party.png",
                  "Christmas Office<br>Party Awards",
                  "38 printable certificates &middot; 8 for Christmas"),
    "school":    ("bma-s-expertise.png", "bma-s-kindness.png",
                  "End of Year<br>Class Awards",
                  "12 printable certificates &middot; every child gets one"),
}


def scene_hero(variant: str = "office") -> str:
    """Photo 1. A printed certificate on a desk, not a flat page.

    Buyers can't hold a file. The listings that win the click show the thing printed and
    sitting somewhere real, with DIGITAL DOWNLOAD stated on the image so nobody expects a
    parcel. A screenshot of page one loses to that every time.
    """
    top, bottom, head, sub = HEROES[variant]
    art = (REPO / "design" / "out" / top).as_uri()
    under = (REPO / "design" / "out" / bottom).as_uri()
    css = f"""
  /* a desk, not a photo studio — a warm surface, real shadows, nothing pretending to be a
     photograph. The certificate is the only sharp thing on the page. */
  body{{background:
      radial-gradient(ellipse at 30% 18%, #C7B49A 0%, #AF9A7E 46%, #8E7A60 100%);
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    padding:110px 100px;position:relative;overflow:hidden}}
  .stack{{position:relative;width:1180px;height:1180px}}
  .stack img{{position:absolute;border:1px solid rgba(0,0,0,.22)}}
  .under{{width:820px;height:1025px;left:60px;top:96px;transform:rotate(-7deg);
    box-shadow:20px 26px 46px rgba(38,28,16,.34);filter:brightness(.97)}}
  .top{{width:880px;height:1100px;left:250px;top:40px;transform:rotate(3.5deg);
    box-shadow:30px 38px 66px rgba(38,28,16,.42)}}
  .badge{{position:absolute;top:74px;right:70px;background:{RED};color:#FBFAF5;
    padding:22px 40px;font-family:"Liberation Mono",monospace;font-size:40px;
    letter-spacing:9px;text-transform:uppercase;font-weight:700;
    box-shadow:10px 12px 26px rgba(38,28,16,.4);transform:rotate(3deg)}}
  .cap{{position:absolute;left:0;right:0;bottom:78px;text-align:center;color:#FBF8F1}}
  .cap h1{{font-size:118px;line-height:1.04;font-weight:700;text-transform:uppercase;
    letter-spacing:-2px;text-shadow:0 4px 26px rgba(38,28,16,.6)}}
  .cap p{{margin-top:26px;font-size:42px;letter-spacing:3px;
    text-shadow:0 3px 16px rgba(38,28,16,.6)}}
"""
    body = f"""
<div class="badge">Digital Download</div>
<div class="stack">
  <img class="under" src="{under}">
  <img class="top" src="{art}">
</div>
<div class="cap"><h1>{head}</h1><p>{sub}</p></div>"""
    return page(SQ, SQ, css, body)


def scene_grid(slugs, head: str = "38 different awards",
               foot: str = "Nobody has to be left out — which is the one thing<br>"
                           "that ruins an office awards ceremony.") -> str:
    # 4-across tiles are far taller than 8-across, so a 12-tile grid overflows the fixed
    # 2000px sheet and clips the footer. Cap its width so three rows fit with the caption.
    cols, gap, width = (8, 18, "100%") if len(slugs) > 20 else (4, 30, "1480px")
    css = f"""
  body{{background:{PAPER};padding:120px 110px;display:flex;flex-direction:column;
    justify-content:space-between;text-align:center}}
  .eyebrow{{font-size:30px;letter-spacing:12px;color:{RED};text-transform:uppercase}}
  h2{{margin-top:22px;font-size:104px;font-weight:700;text-transform:uppercase;
    letter-spacing:-2px}}
  /* 8 wide fits 38 tiles in 5 rows; 7 wide needs 6 and the last row falls off the sheet.
     A 12-tile set wants 4 across, or the tiles end up postage stamps in one thin band. */
  .grid{{display:grid;grid-template-columns:repeat({cols},1fr);gap:{gap}px;
    justify-items:center;width:{width};margin:0 auto}}
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
  <h2>{head}</h2>
</div>
<div class="grid">{tiles}</div>
<div class="foot">{foot}</div>"""
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


def scene_promise(last: tuple[str, str] | None = None) -> str:
    items = [
        ("Instant download", "Files arrive the moment you pay. No shipping, no waiting."),
        ("Works offline", "The maker is one HTML file. No account, no subscription, no app."),
        ("Print at home", "Any printer, any paper. Or send the PDF to a print shop."),
        last or ("Use it every year",
                 "Yours forever. Rename the awards, change the citations."),
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
    # --christmas builds only the seasonal hero for listing #2; everything else is shared
    # with listing #1. --school is a different product and needs its own four.
    xmas = "--christmas" in sys.argv
    school = "--school" in sys.argv
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

    mans = (["manifest-school.json"] if school else
            ["manifest.json", "manifest-christmas.json", "manifest-office.json"])
    slugs = []
    for man in mans:
        p = REPO / "design" / "out" / man
        if p.exists():
            slugs += [c["slug"] for c in json.loads(p.read_text(encoding="utf-8"))]

    # a screenshot of the real maker — each kit ships its own, carrying only its own designs
    maker_src = ROOT / ("dist-school" if school else "dist") / "AwardsMaker.html"
    if not maker_src.exists():
        raise SystemExit(f"{maker_src} not built — run: python3 kit/build_kit.py"
                         f"{' --school' if school else ''}")
    maker = TMP / "_maker.png"
    subprocess.run(
        [chrome, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
         "--virtual-time-budget=4000", "--window-size=1500,1000",
         f"--screenshot={maker}", maker_src.resolve().as_uri()],
        check=True, capture_output=True)

    if school:
        shot(scene_hero("school"), "kit-s1-hero")
        shot(scene_grid(slugs, head="12 different awards",
                        foot="Every child gets one — and none of them are<br>"
                             "about how clever, quick or well-behaved they are."),
             "kit-s2-grid")
        shot(scene_shot(base64.b64encode(maker.read_bytes()).decode(),
                        "Included: the maker",
                        "Type the names.<br>Press print.",
                        "12 awards, any class size. Works in any browser, offline."),
             "kit-s3-maker")
        shot(scene_promise(last=("Safe to read out loud",
                                 "Every award is about a situation, never about a "
                                 "child's ability, effort or behavior.")),
             "kit-s4-promise")
        for name in ("kit-s1-hero", "kit-s2-grid", "kit-s3-maker", "kit-s4-promise"):
            f = OUT / f"{name}.png"
            print(f"  {f.name:<22} {f.stat().st_size/1024:6.0f} KB")
        print("\n4 classroom listing images -> use in this order for listing #3")
        return

    if xmas:
        shot(scene_hero("christmas"), "kit-x1-hero")
        p = OUT / "kit-x1-hero.png"
        print(f"  {p.name:<22} {p.stat().st_size/1024:6.0f} KB")
        print("\nChristmas hero -> use as image 1 of listing #2")
        return

    shot(scene_hero(), "kit-1-hero")
    shot(scene_grid(slugs), "kit-2-grid")
    shot(scene_shot(base64.b64encode(maker.read_bytes()).decode(),
                    "Included: the maker",
                    "Type a name.<br>Press print.",
                    "38 awards, any name, any number of people. Works in any browser."),
         "kit-3-maker")
    shot(scene_promise(), "kit-4-promise")

    # report what this run built, not everything sitting in the directory — the school and
    # Christmas variants live here too, and counting them made an office run overstate itself
    built = ["kit-1-hero", "kit-2-grid", "kit-3-maker", "kit-4-promise"]
    for name in built:
        f = OUT / f"{name}.png"
        print(f"  {f.name:<22} {f.stat().st_size/1024:6.0f} KB")
    print(f"\n{len(built)} listing images -> {OUT}")


if __name__ == "__main__":
    main()
