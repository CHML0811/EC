#!/usr/bin/env python3
"""
Build the internal registry page — the whole product line on one page, so it can be
looked at rather than described.

Reads the manifests so the page can't drift from the artwork, embeds the previews as
data URIs so the published page needs no external hosts.

    python3 design/build_registry_page.py <preview-dir> <output.html>

<preview-dir> holds web-sized renders: <slug>.png for each design, plus
fmt-{1-framed,2-hook,3-detail,4-sizes,5-info,6-pin}.png for the format strip.
"""

import base64
import html
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from generate_mockups import PIN_PHRASE  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent
OUT_DIR = ROOT / "out"

PRICES = [("8 × 10", "$32", "~$10", "$7.36", "$14.64", "46%"),
          ("11 × 14", "$42", "~$14", "$9.66", "$18.34", "44%"),
          ("8 × 10 framed", "$58", "~$25", "$13.34", "$19.66", "34%")]

FORMATS = [
    ("1-framed", "Framed", "2000²", "The grid thumbnail. A buyer picturing it on a wall."),
    ("2-hook", "Hook", "2000²", "The joke at 200px. The only image that survives the search grid."),
    ("3-detail", "Detail", "2000²", "Seal and serial. Proof it isn't clip art."),
    ("4-sizes", "Sizes", "2000²", "Both sizes at true scale. Answers the question before it's asked."),
    ("5-info", "Specification", "2000²", "Stock, shipping, personalization, mailer."),
    ("6-pin", "Pin", "1000×1500", "Pinterest only. The banner carries the search phrase."),
]

MINE = [
    ("Certificate artwork", "16 designs, 2400×3000 at 300dpi, print-ready."),
    ("Listing images", "96 renders — six per design, no Printify account required."),
    ("Listing copy", "32 listings: titles, 13 tags each, descriptions, all inside Etsy's limits."),
    ("Store policies", "Returns, shipping, privacy, terms — written, validated, queued to push."),
    ("Shipping zones", "Live on Shopify. US $5.95, free over $60. Rest of world $14.95."),
]

YOURS = [
    ("Printify account", "Free. Connect it to the Shopify store, add a card so orders don't stall.",
     "~10 min"),
    ("Build the 16 products", "Matte vertical poster, US provider, 8×10 and 11×14 only. Spec is written.",
     "~40 min"),
    ("Etsy seller account", "Needs your ID and bank details. Nothing else can happen before this.",
     "~15 min"),
    ("Publish cohort 1", "Eight listings. Every field is in the paste sheet with a copy button.",
     "~30 min"),
    ("Downgrade Shopify", "Advanced $399 → Basic $39. Saves $360 every month you don't need it.",
     "~2 min"),
]


def data_uri(path: pathlib.Path) -> str:
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


def card(c: dict, web: pathlib.Path) -> str:
    return f"""
<figure class="card">
  <div class="shot"><img src="{data_uri(web / (c['slug'] + '.png'))}"
       alt="{html.escape(c['title'])}, framed" loading="lazy"></div>
  <figcaption>
    <h3>{html.escape(c['title'])}</h3>
    <p class="sub">{html.escape(c['subject'])}</p>
    <p class="dept">{html.escape(c['department'])}</p>
    <div class="meta">
      <span class="ref">{c['ref']}</span>
      <span class="tag t-{c['pattern']}">{c['pattern']}</span>
    </div>
    <p class="query"><span>searches for</span>{html.escape(PIN_PHRASE[c['slug']])}</p>
  </figcaption>
</figure>"""


def build(web: pathlib.Path) -> str:
    c1 = json.loads((OUT_DIR / "manifest.json").read_text(encoding="utf-8"))
    c2 = json.loads((OUT_DIR / "manifest-christmas.json").read_text(encoding="utf-8"))

    grid1 = "".join(card(c, web) for c in c1)
    grid2 = "".join(card(c, web) for c in c2)

    fmts = "".join(f"""
<figure class="fmt">
  <div class="fshot {'tall' if k == '6-pin' else ''}">
    <img src="{data_uri(web / f'fmt-{k}.png')}" alt="{n} format" loading="lazy"></div>
  <figcaption><h4>{n}<span>{px}</span></h4><p>{d}</p></figcaption>
</figure>""" for k, n, px, d in FORMATS)

    prices = "".join(
        f"<tr><td>{s}</td><td class='n'>{r}</td><td class='n dim'>{b}</td>"
        f"<td class='n dim'>{f}</td><td class='n'>{k}</td><td class='n pct'>{p}</td></tr>"
        for s, r, b, f, k, p in PRICES)

    mine = "".join(f"<li><h4>{t}</h4><p>{d}</p></li>" for t, d in MINE)
    yours = "".join(
        f"<li><div class='step'>{i}</div><div><h4>{t}</h4><p>{d}</p></div>"
        f"<div class='mins'>{m}</div></li>"
        for i, (t, d, m) in enumerate(YOURS, 1))

    page = TEMPLATE
    for token, value in [("GRID1", grid1), ("GRID2", grid2), ("FORMATS", fmts),
                         ("PRICES", prices), ("DONE", mine), ("TODO", yours)]:
        page = page.replace(f"<!--{token}-->", value)
    return page


TEMPLATE = """<title>Bureau of Minor Achievements</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{
  --ground:#E3E1D8; --surface:#F1F0EA; --raise:#FAF9F5;
  --ink:#1D2018; --muted:#6B6F62; --rule:#C2C1B5; --rule-soft:#D5D4C9;
  --accent:#7C2E1D; --stamp:#4C5A3F;
  --mono:"Liberation Mono","DejaVu Sans Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --serif:Georgia,"Liberation Serif","Times New Roman",serif;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --ground:#15170F; --surface:#1E2118; --raise:#252921;
    --ink:#E7E5DA; --muted:#99A18D; --rule:#343A2C; --rule-soft:#282E22;
    --accent:#C86A50; --stamp:#8A9A78;
  }
}
:root[data-theme="dark"]{
  --ground:#15170F; --surface:#1E2118; --raise:#252921;
  --ink:#E7E5DA; --muted:#99A18D; --rule:#343A2C; --rule-soft:#282E22;
  --accent:#C86A50; --stamp:#8A9A78;
}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--serif);
  font-size:17px;line-height:1.65;-webkit-font-smoothing:antialiased}
.wrap{max-width:1160px;margin:0 auto;padding:0 28px 120px}
img{max-width:100%;display:block}
h1,h2,h3,h4{font-family:var(--mono);font-weight:600;text-wrap:balance;margin:0}
p{margin:0}
a{color:var(--accent)}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}

/* ---- masthead: a received form ---- */
.mast{position:relative;margin-top:56px;padding:38px 34px 30px;background:var(--surface);
  border:2px solid var(--ink);box-shadow:7px 7px 0 var(--rule-soft)}
.mast .org{font-family:var(--mono);font-size:12px;letter-spacing:.34em;
  text-transform:uppercase;color:var(--accent)}
.mast h1{margin-top:20px;font-size:clamp(30px,5.2vw,50px);line-height:1.1;letter-spacing:-.5px}
.mast .lede{margin-top:20px;max-width:60ch;color:var(--muted);font-size:18px}
.stamp{position:absolute;top:26px;right:26px;transform:rotate(-8deg);
  border:3px double var(--accent);color:var(--accent);padding:7px 15px;
  font-family:var(--mono);font-size:13px;letter-spacing:.22em;font-weight:700;
  text-transform:uppercase;opacity:.9}
@media (max-width:620px){.stamp{position:static;transform:none;display:inline-block;
  margin-bottom:6px}}

.docket{display:grid;grid-template-columns:repeat(auto-fit,minmax(128px,1fr));
  margin-top:32px;border-top:1px solid var(--rule)}
.docket div{padding:16px 18px 14px;border-bottom:1px solid var(--rule);
  border-right:1px solid var(--rule)}
.docket div:last-child{border-right:0}
.docket dt{font-family:var(--mono);font-size:10.5px;letter-spacing:.2em;
  text-transform:uppercase;color:var(--muted)}
.docket dd{margin:6px 0 0;font-family:var(--mono);font-size:23px;font-weight:600;
  font-variant-numeric:tabular-nums}
.docket .word{font-size:15px;line-height:1.4;font-weight:500}

/* ---- sections ---- */
section{margin-top:82px}
.shead{display:flex;align-items:baseline;justify-content:space-between;gap:20px;
  flex-wrap:wrap;padding-bottom:14px;border-bottom:2px solid var(--ink)}
.shead h2{font-size:14px;letter-spacing:.24em;text-transform:uppercase}
.shead .note{font-family:var(--mono);font-size:12px;letter-spacing:.08em;color:var(--muted)}
.shead .flag{color:var(--accent);font-weight:700}
.intro{margin-top:24px;max-width:66ch;color:var(--muted)}

/* ---- design grid ---- */
.grid{display:grid;gap:26px;margin-top:32px;
  grid-template-columns:repeat(auto-fill,minmax(238px,1fr))}
.card{margin:0;background:var(--surface);border:1px solid var(--rule);
  display:flex;flex-direction:column}
.shot{background:var(--raise);border-bottom:1px solid var(--rule)}
.card figcaption{padding:18px 18px 20px;display:flex;flex-direction:column;gap:7px;flex:1}
.card h3{font-size:15.5px;line-height:1.32}
.sub{font-family:var(--mono);font-size:10.5px;letter-spacing:.18em;color:var(--stamp)}
.dept{font-size:13.5px;color:var(--muted);font-style:italic;line-height:1.4}
.meta{display:flex;align-items:center;justify-content:space-between;gap:10px;
  margin-top:auto;padding-top:12px}
.ref{font-family:var(--mono);font-size:10.5px;color:var(--muted);
  font-variant-numeric:tabular-nums}
.tag{font-family:var(--mono);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;
  padding:3px 8px;border:1px solid currentColor;border-radius:2px}
.t-occasion{color:var(--stamp)} .t-recipient{color:var(--accent)}
.t-personalised,.t-personalized{color:var(--muted)}
.query{font-family:var(--mono);font-size:11.5px;line-height:1.5;padding-top:11px;
  border-top:1px dashed var(--rule)}
.query span{display:block;font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;
  color:var(--muted);margin-bottom:3px}

/* ---- format strip ---- */
.fmts{display:grid;gap:24px;margin-top:32px;
  grid-template-columns:repeat(auto-fill,minmax(210px,1fr))}
.fmt{margin:0}
.fshot{background:var(--raise);border:1px solid var(--rule);aspect-ratio:1;
  display:flex;align-items:center;justify-content:center;overflow:hidden}
.fshot.tall img{height:100%;width:auto;object-fit:contain}
.fmt h4{margin-top:13px;font-size:13px;letter-spacing:.1em;text-transform:uppercase;
  display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.fmt h4 span{font-size:10px;color:var(--muted);letter-spacing:.06em;text-transform:none}
.fmt p{margin-top:6px;font-size:14px;line-height:1.5;color:var(--muted)}

/* ---- pricing ---- */
.tablewrap{overflow-x:auto;margin-top:28px;border:1px solid var(--rule);background:var(--surface)}
table{width:100%;border-collapse:collapse;font-family:var(--mono);font-size:14px;
  min-width:560px}
th,td{padding:14px 18px;text-align:left;border-bottom:1px solid var(--rule-soft)}
th{font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);
  border-bottom:1px solid var(--rule)}
tbody tr:last-child td{border-bottom:0}
.n{text-align:right;font-variant-numeric:tabular-nums}
.dim{color:var(--muted)}
.pct{color:var(--accent);font-weight:600}
.tnote{margin-top:14px;font-size:14.5px;color:var(--muted);max-width:66ch}

/* ---- ledgers ---- */
.cols{display:grid;gap:44px;margin-top:32px;grid-template-columns:repeat(auto-fit,minmax(310px,1fr))}
.cols h3{font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--muted);
  padding-bottom:11px;border-bottom:1px solid var(--rule)}
ul{list-style:none;margin:0;padding:0}
.done li{padding:16px 0 16px 30px;border-bottom:1px solid var(--rule-soft);position:relative}
.done li::before{content:"✓";position:absolute;left:0;top:16px;color:var(--stamp);
  font-family:var(--mono);font-weight:700}
.todo li{display:grid;grid-template-columns:auto 1fr auto;gap:16px;align-items:start;
  padding:16px 0;border-bottom:1px solid var(--rule-soft)}
.step{font-family:var(--mono);font-size:12px;font-weight:700;color:var(--accent);
  border:1px solid var(--accent);width:26px;height:26px;display:flex;
  align-items:center;justify-content:center;border-radius:50%;flex:0 0 26px}
.mins{font-family:var(--mono);font-size:11px;color:var(--muted);white-space:nowrap;
  padding-top:5px}
.cols h4{font-size:14.5px;letter-spacing:.01em}
.cols p{margin-top:4px;font-size:14.5px;line-height:1.5;color:var(--muted)}

.foot{margin-top:88px;padding-top:26px;border-top:2px solid var(--ink);
  font-family:var(--mono);font-size:11.5px;letter-spacing:.1em;color:var(--muted);
  display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
</style>

<div class="wrap">

<header class="mast">
  <div class="stamp">Rendered</div>
  <div class="org">The Bureau of Minor Achievements</div>
  <h1>Sixteen certificates,<br>ready to list.</h1>
  <p class="lede">A fictional agency issuing official recognition for things that don't
    deserve any. Every design, every listing image, and every word of copy below was
    generated — no camera, no photo studio, no stock to buy.</p>
  <dl class="docket">
    <div><dt>Designs</dt><dd>16</dd></div>
    <div><dt>Listing images</dt><dd>96</dd></div>
    <div><dt>Cohorts</dt><dd>2</dd></div>
    <div><dt>Channel</dt><dd class="word">Etsy, then Pinterest</dd></div>
    <div><dt>Blocked on</dt><dd class="word">Two free accounts</dd></div>
  </dl>
</header>

<section>
  <div class="shead"><h2>Cohort I · General occasions</h2>
    <span class="note">8 designs · list first</span></div>
  <p class="intro">Deliberately spread across three title patterns — named by
    <em>occasion</em>, by <em>recipient</em>, or by the joke itself. Whichever pattern
    converts best in the first month decides how cohort 2 gets titled. The cohort is an
    experiment, not just a product line.</p>
  <div class="grid"><!--GRID1--></div>
</section>

<section>
  <div class="shead"><h2>Cohort II · Christmas &amp; the office exchange</h2>
    <span class="note flag">must be live by Oct 1</span></div>
  <p class="intro">Secret Santa and white elephant are peak season for exactly this
    product. Etsy takes 30–90 days to rank a listing, and Christmas buying peaks between
    late November and mid-December. Live in October means ranked when the money arrives.
    Live in December means invisible.</p>
  <div class="grid"><!--GRID2--></div>
</section>

<section>
  <div class="shead"><h2>Six images per design</h2>
    <span class="note">shown: Retirement</span></div>
  <p class="intro">Etsy ranks on conversion, and conversion is decided in the search grid
    before anyone reads a word. Both normal routes to product photos were closed — Printify's
    mockup generator needs an account, a camera needs stock — so these are rendered the same
    way the artwork is. Upload the first five in order; the sixth is for Pinterest.</p>
  <div class="fmts"><!--FORMATS--></div>
</section>

<section>
  <div class="shead"><h2>Unit economics</h2><span class="note">after Etsy's ~23% all-in</span></div>
  <div class="tablewrap"><table>
    <thead><tr><th>Size</th><th class="n">Retail</th><th class="n">Print</th>
      <th class="n">Etsy</th><th class="n">You keep</th><th class="n">Margin</th></tr></thead>
    <tbody><!--PRICES--></tbody>
  </table></div>
  <p class="tnote">Etsy's headline fee is 6.5%. The real number, once payment processing,
    listing fees and offsite ads are counted, is 20–25% — which is why this is paper and not
    apparel. The same brand on t-shirts keeps 14%.</p>
</section>

<section>
  <div class="shead"><h2>Where this actually stands</h2>
    <span class="note">honest version</span></div>
  <div class="cols">
    <div>
      <h3>Done</h3>
      <ul class="done"><!--DONE--></ul>
    </div>
    <div>
      <h3>Needs you — about 1½ hours, once</h3>
      <ul class="todo"><!--TODO--></ul>
    </div>
  </div>
</section>

<div class="foot">
  <span>Bureau of Minor Achievements · internal registry</span>
  <span>No revenue yet. Nothing sells until step 4.</span>
</div>

</div>
"""


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    web, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    out.write_text(build(web), encoding="utf-8")
    print(f"{out}  {out.stat().st_size/1024/1024:.2f} MB")


if __name__ == "__main__":
    main()
