#!/usr/bin/env python3
"""
The Bureau of Minor Achievements — certificate generator.

Renders print-ready certificate artwork (8x10in @ 300dpi = 2400x3000px) using
headless Chromium. Pure typography and vector shapes, so no image model needed.

    python3 design/generate_certificates.py

Output: design/out/*.png  (upload straight to Printify as poster artwork)
"""

import base64
import html
import json
import os
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "out"
TMP = ROOT / ".build"

W, H = 2400, 3000  # 8x10in @ 300dpi

# Every build script renders through Chrome, so this has to work on whatever machine the
# project is cloned onto. macOS and Windows both install Chrome somewhere that is NOT on
# PATH, which is the first thing that breaks for anyone picking this up.
CHROME_CANDIDATES = [
    # this container
    "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell",
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    # macOS
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    # Windows
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    # Linux
    "/usr/bin/google-chrome", "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium", "/usr/bin/chromium-browser",
    "/snap/bin/chromium",
]

PATH_NAMES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
              "chrome", "msedge"]

# --- palette -----------------------------------------------------------------
PAPER = "#F2EFE4"
INK = "#17150F"
RED = "#B4321F"
OLIVE = "#565E42"
FAINT = "#B9B3A0"

# --- the line-up -------------------------------------------------------------
# Each entry is one Etsy listing. `pattern` records which title pattern the
# listing tests, so the cohort can be read against the metrics brief.
CERTS = [
    {
        "slug": "retirement",
        "pattern": "occasion",
        "title": "Certificate of Minor Achievement",
        "subject": "RETIREMENT",
        "department": "Office of Sustained Mediocrity",
        "citation": "for arriving, more or less on time, for several decades, "
                    "and for leaving before anyone could ask them to learn a new system.",
        "seal": "SUSTAINED MEDIOCRITY",
        "ref": "BMA-2026-0117-R",
    },
    {
        "slug": "coworker",
        "pattern": "recipient",
        "title": "World's Okayest Coworker",
        "subject": "CERTIFIED",
        "department": "Division of Technically Correct",
        "citation": "for meeting expectations approximately, replying eventually, "
                    "and never once being the reason a meeting ran long.",
        "seal": "TECHNICALLY CORRECT",
        "ref": "BMA-2026-0208-C",
    },
    {
        "slug": "uncle",
        "pattern": "recipient",
        "title": "Certified Uncle",
        "subject": "FULLY LICENSED",
        "department": "Bureau of Unsolicited Advice",
        "citation": "for opinions delivered at volume, jokes repeated annually, "
                    "and an unbroken record of standing near the grill without cooking.",
        "seal": "UNSOLICITED ADVICE",
        "ref": "BMA-2026-0304-U",
    },
    {
        "slug": "boss",
        "pattern": "recipient",
        "title": "Certificate of Adequate Leadership",
        "subject": "MANAGEMENT",
        "department": "Department of Almost Trying",
        "citation": "for decisions made eventually, emails sent at unreasonable hours, "
                    "and saying “let’s circle back” with genuine conviction.",
        "seal": "ALMOST TRYING",
        "ref": "BMA-2026-0421-B",
    },
    {
        "slug": "new-home",
        "pattern": "occasion",
        "title": "Certificate of Structural Commitment",
        "subject": "HOMEOWNERSHIP",
        "department": "Office of Regrettable Purchases",
        "citation": "for signing a document of considerable length, and for discovering "
                    "what a load-bearing wall is under the least convenient circumstances.",
        "seal": "REGRETTABLE PURCHASES",
        "ref": "BMA-2026-0530-H",
    },
    {
        "slug": "new-parent",
        "pattern": "occasion",
        "title": "Certificate of Sustained Sleep Deprivation",
        "subject": "PARENTHOOD",
        "department": "Division of Diminishing Rest",
        "citation": "for remaining upright through hours that should not exist, "
                    "and for developing strong opinions about a stroller.",
        "seal": "DIMINISHING REST",
        "ref": "BMA-2026-0612-P",
    },
    {
        "slug": "graduation",
        "pattern": "occasion",
        "title": "Certificate of Technically Finishing",
        "subject": "GRADUATION",
        "department": "Bureau of Unfinished Projects",
        "citation": "for completing the required minimum, submitting at the final "
                    "permitted minute, and retaining approximately none of it.",
        "seal": "UNFINISHED PROJECTS",
        "ref": "BMA-2026-0708-G",
    },
    {
        "slug": "left-on-read",
        "pattern": "personalized",
        "title": "Certificate of Leaving On Read",
        "subject": "THE GROUP CHAT",
        "department": "Office of Deferred Replies",
        "citation": "for reading immediately, intending to reply thoroughly, "
                    "and then simply never doing so. Repeatedly. Without remorse.",
        "seal": "DEFERRED REPLIES",
        "ref": "BMA-2026-0822-L",
    },
]


def seal_svg(text: str) -> str:
    """Circular official seal with the department name set around the rim."""
    return f"""
<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg" class="seal">
  <defs>
    <path id="rim" d="M200,200 m-148,0 a148,148 0 1,1 296,0 a148,148 0 1,1 -296,0"/>
  </defs>
  <circle cx="200" cy="200" r="180" fill="none" stroke="{RED}" stroke-width="5"/>
  <circle cx="200" cy="200" r="168" fill="none" stroke="{RED}" stroke-width="2"/>
  <circle cx="200" cy="200" r="120" fill="none" stroke="{RED}" stroke-width="2"/>
  <text font-family="Liberation Serif, Times New Roman, serif" font-size="26"
        letter-spacing="5" fill="{RED}">
    <textPath href="#rim" startOffset="50%" text-anchor="middle">
      &#9733; BUREAU OF MINOR ACHIEVEMENTS &#9733;
    </textPath>
  </text>
  <!-- deliberately slightly crooked laurel -->
  <g transform="translate(200,208) rotate(-6)" fill="none" stroke="{RED}" stroke-width="4.5"
     stroke-linecap="round">
    <path d="M-52,26 C-64,-10 -44,-44 -12,-56"/>
    <path d="M52,26 C64,-10 44,-44 12,-56"/>
    <path d="M-44,10 l-19,-9 M-38,-8 l-20,-7 M-28,-26 l-19,-4
             M-14,-42 l-16,2 M44,10 l19,-9 M38,-8 l20,-7
             M28,-26 l19,-4 M14,-42 l16,2"/>
  </g>
  <text x="200" y="272" text-anchor="middle" font-family="Liberation Serif, serif"
        font-size="25" letter-spacing="6" fill="{RED}">EST. 1997</text>
</svg>"""


def guilloche(pos: str) -> str:
    """Repeating engine-turned wave band, the way real certificates fake security."""
    return f"""
<svg class="guilloche {pos}" viewBox="0 0 1200 40" preserveAspectRatio="none"
     xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="w{pos}" width="60" height="40" patternUnits="userSpaceOnUse">
      <path d="M0,20 C15,2 15,38 30,20 C45,2 45,38 60,20" fill="none"
            stroke="{FAINT}" stroke-width="1.6"/>
      <path d="M0,20 C15,38 15,2 30,20 C45,38 45,2 60,20" fill="none"
            stroke="{FAINT}" stroke-width="1.6"/>
    </pattern>
  </defs>
  <rect width="1200" height="40" fill="url(#w{pos})"/>
</svg>"""


def build_html(c: dict) -> str:
    return f"""<!doctype html>
<meta charset="utf-8">
<style>
  @page {{ margin:0 }}
  *{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{width:{W}px;height:{H}px;background:{PAPER};
    font-family:"Liberation Serif","Times New Roman",serif;color:{INK};
    -webkit-font-smoothing:antialiased}}
  /* three blocks, spread down the full sheet so there is no dead middle */
  .sheet{{position:relative;width:{W}px;height:{H}px;padding:250px 190px 500px;
    display:flex;flex-direction:column;align-items:center;text-align:center;
    justify-content:center}}
  .block{{width:100%;display:flex;flex-direction:column;align-items:center}}
  .block+.block{{margin-top:190px}}
  .frame-outer{{position:absolute;inset:78px;border:7px solid {INK}}}
  .frame-inner{{position:absolute;inset:104px;border:2px solid {INK}}}
  .corner{{position:absolute;width:64px;height:64px;border:5px solid {RED}}}
  .c-tl{{top:118px;left:118px;border-right:0;border-bottom:0}}
  .c-tr{{top:118px;right:118px;border-left:0;border-bottom:0}}
  .c-bl{{bottom:118px;left:118px;border-right:0;border-top:0}}
  .c-br{{bottom:118px;right:118px;border-left:0;border-top:0}}
  .guilloche{{position:absolute;left:126px;right:126px;width:calc(100% - 252px);height:40px;opacity:.85}}
  .guilloche.top{{top:132px}} .guilloche.bottom{{bottom:132px}}

  .agency{{font-size:42px;letter-spacing:16px;color:{RED};text-transform:uppercase}}
  .rule{{width:360px;height:2px;background:{INK};margin:34px auto 0;opacity:.5}}
  .title{{margin-top:62px;font-size:132px;line-height:1.04;font-weight:700;
    letter-spacing:-1px;text-transform:uppercase;text-wrap:balance}}
  .subject{{margin-top:34px;font-size:46px;letter-spacing:14px;color:{OLIVE};
    text-transform:uppercase}}

  .presented{{font-size:38px;font-style:italic;opacity:.72}}
  .nameline{{margin-top:30px;width:1640px;border-bottom:3px solid {INK};
    padding-bottom:18px}}
  .name{{font-size:112px;font-style:italic;line-height:1.1}}
  .namehint{{margin-top:18px;font-size:26px;letter-spacing:7px;opacity:.42;
    text-transform:uppercase}}
  .citation{{margin-top:100px;width:1640px;font-size:44px;line-height:1.62}}
  .dept{{margin-top:58px;font-size:33px;letter-spacing:9px;color:{RED};
    text-transform:uppercase}}

  .footer{{position:absolute;left:190px;right:190px;bottom:250px;
    display:flex;align-items:flex-end;justify-content:space-between}}
  .seal{{width:330px;height:330px}}
  .sigblock{{width:560px;text-align:center}}
  .sigline{{border-bottom:2px solid {INK};height:96px}}
  .siglabel{{margin-top:14px;font-size:26px;letter-spacing:5px;opacity:.62;
    text-transform:uppercase}}
  .refblock{{width:420px;text-align:left;font-family:"Liberation Mono",monospace;
    font-size:24px;line-height:1.9;opacity:.6}}
</style>
<div class="sheet">
  <div class="frame-outer"></div><div class="frame-inner"></div>
  <div class="corner c-tl"></div><div class="corner c-tr"></div>
  <div class="corner c-bl"></div><div class="corner c-br"></div>
  {guilloche('top')}{guilloche('bottom')}

  <div class="block">
    <div class="agency">The Bureau of Minor Achievements</div>
    <div class="rule"></div>
    <div class="title">{html.escape(c['title'])}</div>
    <div class="subject">{html.escape(c['subject'])}</div>
  </div>

  <div class="block">
    <div class="presented">This is to certify that</div>
    <div class="nameline"><div class="name">{{ Recipient Name }}</div></div>
    <div class="namehint">personalized at checkout</div>
    <div class="citation">{c['citation']}</div>
    <div class="dept">{html.escape(c['department'])}</div>
  </div>

  <div class="footer">
    {seal_svg(c['seal'])}
    <div class="refblock">
      REF &nbsp;{c['ref']}<br>
      ISSUED &nbsp;{{ DATE }}<br>
      STATUS &nbsp;IRREVOCABLE
    </div>
    <div class="sigblock">
      <div class="sigline"></div>
      <div class="siglabel">Registrar, B.M.A.</div>
    </div>
  </div>
</div>"""


def find_chrome() -> str:
    """Locate a Chrome/Chromium binary. Override with CHROME=/path/to/chrome."""
    override = os.environ.get("CHROME")
    if override:
        if pathlib.Path(override).exists():
            return override
        sys.exit(f"CHROME is set to {override!r} but nothing is there.")

    for p in CHROME_CANDIDATES:
        if pathlib.Path(p).exists():
            return p
    for name in PATH_NAMES:
        found = shutil.which(name)
        if found:
            return found

    sys.exit(
        "No Chrome or Chromium found.\n\n"
        "Everything in this project renders through headless Chrome. Install Google Chrome\n"
        "(google.com/chrome) — if it's already installed somewhere unusual, point at it:\n\n"
        "  macOS    export CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'\n"
        "  Linux    export CHROME=/usr/bin/google-chrome\n"
        "  Windows  set CHROME=C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\n"
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    chrome = find_chrome()

    manifest = []
    for c in CERTS:
        src = TMP / f"{c['slug']}.html"
        png = OUT / f"bma-{c['slug']}.png"
        src.write_text(build_html(c), encoding="utf-8")

        subprocess.run(
            [chrome, "--headless", "--disable-gpu", "--no-sandbox",
             "--hide-scrollbars", "--force-device-scale-factor=1",
             f"--window-size={W},{H}", f"--screenshot={png}", src.as_uri()],
            check=True, capture_output=True,
        )
        size = png.stat().st_size
        print(f"  {png.name:<34} {size/1024:8.0f} KB")
        manifest.append({**c, "file": png.name, "px": f"{W}x{H}", "dpi": 300})

    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\n{len(CERTS)} certificates -> {OUT}")


if __name__ == "__main__":
    main()
