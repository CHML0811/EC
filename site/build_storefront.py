#!/usr/bin/env python3
"""
Build the storefront.

    python3 site/build_storefront.py <preview-dir> --local  site/index.html
    python3 site/build_storefront.py <preview-dir> --inline out.html

--local  writes relative <img> paths, for serving the repo as a static site.
--inline embeds every image as a data URI, for publishing as a single file.

The catalog is read from the design manifests, so a new certificate appears in the
shop the moment it is rendered — the storefront can't fall out of sync with the line.
"""

import base64
import html
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DESIGN = ROOT.parent / "design"
sys.path.insert(0, str(DESIGN))
from generate_mockups import PIN_PHRASE  # noqa: E402

SHOP = "https://fbapgj-si.myshopify.com"

# Bulk tiers. Sold direct through Shopify, so Etsy's ~23% never applies — which is why
# $23/unit here still beats $32/unit through Etsy on money actually kept.
BULK = [("5", "$135", "$27", "16%"), ("10", "$250", "$25", "22%"), ("25", "$575", "$23", "28%")]

STEPS = [
    ("Pick the certificate", "Sixteen of them. One will be uncomfortably accurate."),
    ("Type the name", "Exactly as it should be printed. We don't autocorrect it."),
    ("It prints in the USA", "Dispatched in 2–3 business days, on your wall in 3–5."),
]

FAQS = [
    ("Is this actually funny or is it just a certificate?",
     "It's a real certificate, printed properly, that says something absurd with a completely "
     "straight face. The joke only works because the object is serious. A cheap print of a "
     "joke is just a cheap print."),
    ("Can I put any name on it?",
     "Any name, up to 40 characters. We print it exactly as you type it, including the "
     "spelling you chose. Check it twice."),
    ("How big is it?",
     "8×10 or 11×14 inches. Both fit standard frames you can buy anywhere, or add the framed "
     "option and skip that errand."),
    ("Will it arrive creased?",
     "It ships flat in a rigid mailer. If it arrives damaged, send a photo and we replace it. "
     "You don't have to send the damaged one back."),
    ("Do you do custom text?",
     "Not yet. The wording is what makes them work, and we'd rather write it well than let "
     "you write it at 11pm. Departmental orders are the exception — ask."),
]


def data_uri(p: pathlib.Path) -> str:
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()


def build(web: pathlib.Path, inline: bool) -> str:
    def img(name: str) -> str:
        return data_uri(web / f"{name}.png") if inline else f"../design/mockups/{name}-1-framed.png"

    def art(name: str) -> str:
        if inline:
            return data_uri(web / f"{name}.png")
        return {"hero-wide": "../design/crops/hero-wide.png",
                "hero-mobile": "../design/crops/hero-mobile.png",
                "seal": "../design/crops/retirement-crop-seal.png"}[name]

    certs = []
    for man, season in (("manifest.json", False), ("manifest-christmas.json", True)):
        for c in json.loads((DESIGN / "out" / man).read_text(encoding="utf-8")):
            certs.append({**c, "season": season})

    cards = "".join(f"""
<article class="item">
  <a class="shot" href="{SHOP}" aria-label="{html.escape(c['title'])}">
    <img src="{img(c['slug'])}" alt="{html.escape(c['title'])}, framed" loading="lazy">
    {'<span class="flag">Holiday</span>' if c['season'] else ''}
  </a>
  <div class="body">
    <h3>{html.escape(c['title'])}</h3>
    <p class="dept">{html.escape(c['department'])}</p>
    <div class="foot">
      <span class="code">{c['ref']}</span>
      <span class="price">from $32</span>
    </div>
  </div>
</article>""" for c in certs)

    tiers = "".join(
        f"<tr><td>{n} certificates</td><td class='n'>{t}</td>"
        f"<td class='n'>{u} each</td><td class='n save'>save {s}</td></tr>"
        for n, t, u, s in BULK)

    steps = "".join(
        f"<li><span class='no'>{i}</span><div><h4>{t}</h4><p>{d}</p></div></li>"
        for i, (t, d) in enumerate(STEPS, 1))

    faqs = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>"
                   for q, a in FAQS)

    return TEMPLATE.replace("<!--HERO-->", art("hero-wide")) \
                   .replace("<!--HEROM-->", art("hero-mobile")) \
                   .replace("<!--SEAL-->", art("seal")) \
                   .replace("<!--CARDS-->", cards).replace("<!--TIERS-->", tiers) \
                   .replace("<!--STEPS-->", steps).replace("<!--FAQS-->", faqs) \
                   .replace("<!--SHOP-->", SHOP).replace("<!--COUNT-->", str(len(certs)))


TEMPLATE = """<title>The Bureau of Minor Achievements</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Personalized certificates recognizing things that don't deserve recognition. Printed in the USA, delivered in 3-5 days.">
<style>
:root{
  --paper:#F2EFE4; --card:#FBFAF5; --deep:#E7E3D5;
  --ink:#17150F; --muted:#6A6558; --line:#CFC9B8; --hair:#E0DBCB;
  --red:#B4321F; --olive:#565E42;
  --serif:"Liberation Serif",Georgia,"Times New Roman",serif;
  --mono:"Liberation Mono","DejaVu Sans Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --paper:#14130E; --card:#1D1B15; --deep:#100F0B;
    --ink:#EFECE1; --muted:#9A9484; --line:#332F26; --hair:#262319;
    --red:#D2603F; --olive:#8B9673;
  }
}
:root[data-theme="dark"]{
  --paper:#14130E; --card:#1D1B15; --deep:#100F0B;
  --ink:#EFECE1; --muted:#9A9484; --line:#332F26; --hair:#262319;
  --red:#D2603F; --olive:#8B9673;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--serif);
  font-size:17px;line-height:1.62;-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
h1,h2,h3,h4{margin:0;text-wrap:balance;line-height:1.14}
p{margin:0}
a{color:inherit;text-decoration:none}
:focus-visible{outline:2px solid var(--red);outline-offset:3px}
/* padding-inline, not padding: .wrap is also on <section>, and a class beats an element
   selector — plain `padding` here silently cancels the sections' vertical rhythm */
.wrap{max-width:1200px;margin:0 auto;padding-inline:26px}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.28em;text-transform:uppercase;
  color:var(--red)}

/* ---- masthead ---- */
.top{border-bottom:1px solid var(--line);background:var(--paper);position:sticky;top:0;z-index:9}
.topin{display:flex;align-items:center;justify-content:space-between;gap:18px;
  padding:13px 0;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:12px}
.brand img{width:38px;height:38px}
.brand b{font-family:var(--mono);font-size:12.5px;letter-spacing:.17em;text-transform:uppercase;
  font-weight:600;line-height:1.35}
.btn{font-family:var(--mono);font-size:12px;letter-spacing:.13em;text-transform:uppercase;
  padding:11px 20px;border:1.5px solid var(--ink);background:var(--ink);color:var(--paper)}
.btn.ghost{background:transparent;color:var(--ink)}
.btn:hover{background:var(--red);border-color:var(--red);color:#FBFAF5}

/* ---- hero ---- */
.hero img{width:100%}
.hero .m{display:none}
@media (max-width:860px){.hero .w{display:none}.hero .m{display:block}}

.strip{border-top:1px solid var(--line);border-bottom:1px solid var(--line);
  background:var(--deep)}
.strip ul{list-style:none;margin:0;padding:0;display:grid;
  grid-template-columns:repeat(auto-fit,minmax(190px,1fr))}
.strip li{padding:18px 22px;border-right:1px solid var(--line);font-family:var(--mono);
  font-size:11.5px;letter-spacing:.13em;text-transform:uppercase;text-align:center}
.strip li:last-child{border-right:0}

/* ---- sections ---- */
section{padding-block:76px}
.shead{display:flex;align-items:baseline;justify-content:space-between;gap:18px;
  flex-wrap:wrap;padding-bottom:15px;border-bottom:2px solid var(--ink);margin-bottom:34px}
.shead h2{font-size:15px;font-family:var(--mono);letter-spacing:.24em;text-transform:uppercase}
.shead span{font-family:var(--mono);font-size:11.5px;color:var(--muted);letter-spacing:.08em}

/* ---- catalog ---- */
.grid{display:grid;gap:26px;grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}
.item{background:var(--card);border:1px solid var(--line);display:flex;flex-direction:column}
.shot{position:relative;display:block;border-bottom:1px solid var(--line)}
.shot img{transition:transform .35s ease}
.item:hover .shot img{transform:scale(1.03)}
@media (prefers-reduced-motion:reduce){.shot img{transition:none}
  .item:hover .shot img{transform:none}}
.flag{position:absolute;top:12px;right:12px;background:var(--red);color:#FBFAF5;
  font-family:var(--mono);font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;
  padding:5px 9px}
.item .body{padding:18px 18px 19px;display:flex;flex-direction:column;gap:8px;flex:1}
.item h3{font-size:18px}
.dept{font-size:14px;color:var(--muted);font-style:italic}
.item .foot{margin-top:auto;padding-top:13px;border-top:1px dashed var(--line);
  display:flex;align-items:baseline;justify-content:space-between;gap:10px}
.code{font-family:var(--mono);font-size:10.5px;color:var(--muted)}
.price{font-family:var(--mono);font-size:13px;font-weight:600}

/* ---- requisition ---- */
.req{background:var(--card);border:2px solid var(--ink);padding:44px 40px;
  box-shadow:8px 8px 0 var(--hair)}
.req h3{font-size:clamp(27px,4vw,40px);margin-top:16px}
.req .lede{margin-top:18px;max-width:62ch;color:var(--muted);font-size:17.5px}
.tablewrap{overflow-x:auto;margin-top:30px}
table{width:100%;border-collapse:collapse;font-family:var(--mono);font-size:14px;min-width:460px}
td{padding:14px 16px;border-bottom:1px solid var(--hair)}
tr:last-child td{border-bottom:0}
.n{text-align:right;font-variant-numeric:tabular-nums}
.save{color:var(--red)}
.reqfoot{margin-top:26px;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
.note{font-size:14.5px;color:var(--muted);max-width:56ch}

/* ---- steps ---- */
.steps{list-style:none;margin:0;padding:0;display:grid;gap:30px;
  grid-template-columns:repeat(auto-fit,minmax(270px,1fr))}
.steps li{display:flex;gap:18px;align-items:flex-start}
.no{flex:0 0 40px;height:40px;border:2px solid var(--red);color:var(--red);border-radius:50%;
  display:flex;align-items:center;justify-content:center;font-family:var(--mono);font-size:16px}
.steps h4{font-size:19px}
.steps p{margin-top:7px;color:var(--muted);font-size:15.5px}

/* ---- story ---- */
.story{display:grid;gap:52px;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));
  align-items:center}
.story h3{font-size:clamp(28px,4vw,42px)}
.story p{margin-top:20px;color:var(--muted);max-width:58ch}
/* the seal PNG carries its own paper ground, so frame it as a stamped card — otherwise
   it reads as a transparency bug against the dark theme */
.story .seal{width:100%;max-width:300px;margin:0 auto;padding:34px;background:#F2EFE4;
  border:1px solid var(--line);box-shadow:10px 12px 0 var(--hair)}

/* ---- faq ---- */
details{border-bottom:1px solid var(--line);padding:19px 0}
summary{cursor:pointer;font-size:18.5px;list-style:none;display:flex;justify-content:space-between;
  gap:18px;align-items:baseline}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";font-family:var(--mono);color:var(--red);font-size:21px;flex:0 0 auto}
details[open] summary::after{content:"–"}
details p{margin-top:13px;color:var(--muted);max-width:70ch}

/* ---- footer ---- */
footer{border-top:2px solid var(--ink);padding:40px 0 64px;margin-top:40px}
.fin{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;
  font-family:var(--mono);font-size:11.5px;letter-spacing:.1em;color:var(--muted)}
</style>

<header class="top"><div class="wrap topin">
  <a class="brand" href="#top">
    <img src="<!--SEAL-->" alt="">
    <b>The Bureau of<br>Minor Achievements</b>
  </a>
  <a class="btn" href="<!--SHOP-->">Shop all <!--COUNT--></a>
</div></header>

<div class="hero" id="top">
  <img class="w" src="<!--HERO-->" alt="Three personalized certificates from the Bureau of Minor Achievements">
  <img class="m" src="<!--HEROM-->" alt="Three personalized certificates from the Bureau of Minor Achievements">
</div>

<div class="strip"><div class="wrap"><ul>
  <li>Personalized with any name</li>
  <li>Printed in the USA</li>
  <li>Delivered in 3–5 days</li>
  <li>Heavy matte stock</li>
</ul></div></div>

<section class="wrap">
  <div class="shead"><h2>The catalog</h2><span>16 certifications currently issued</span></div>
  <div class="grid"><!--CARDS--></div>
</section>

<section class="wrap">
  <div class="req">
    <div class="eyebrow">Form 7B — Departmental Requisition</div>
    <h3>Recognize an entire team at once.</h3>
    <p class="lede">Offices order these for reviews, farewells, and the holiday party — a
      certificate for every person, each one specific enough to be read aloud. Every name is
      printed individually. Nobody gets a blank.</p>
    <div class="tablewrap"><table><!--TIERS--></table></div>
    <div class="reqfoot">
      <a class="btn" href="<!--SHOP-->">Request a departmental quote</a>
      <p class="note">Mixed designs are fine — the point is that they're different. Send the
        list of names and what each person is guilty of.</p>
    </div>
  </div>
</section>

<section class="wrap">
  <div class="shead"><h2>How it works</h2><span>three steps, no account</span></div>
  <ul class="steps"><!--STEPS--></ul>
</section>

<section class="wrap">
  <div class="shead"><h2>The Bureau</h2><span>est. 1997, allegedly</span></div>
  <div class="story">
    <div>
      <h3>Official recognition, deployed against things that don't deserve any.</h3>
      <p>Most gag gifts announce themselves. Novelty fonts, bright colors, a punchline you
        can read from across the room. They get one laugh and then they get thrown away.</p>
      <p>These don't. Each one is a properly set document — engine-turned border, embossed-look
        seal, serial number, a registrar's signature line — that happens to certify that
        someone stands near a grill without ever cooking anything. The joke lands because the
        object refuses to admit there is one.</p>
      <p>That's why they end up framed instead of binned. It's a real thing on real paper, and
        it has that person's name on it.</p>
    </div>
    <img class="seal" src="<!--SEAL-->" alt="Seal of the Bureau of Minor Achievements">
  </div>
</section>

<section class="wrap">
  <div class="shead"><h2>Questions</h2><span>answered plainly</span></div>
  <!--FAQS-->
</section>

<footer><div class="wrap fin">
  <span>The Bureau of Minor Achievements</span>
  <span>Printed in the USA · Ships flat · Replaced if damaged</span>
</div></footer>
"""


def main() -> None:
    if len(sys.argv) != 4 or sys.argv[2] not in ("--local", "--inline"):
        sys.exit(__doc__)
    web, mode, out = pathlib.Path(sys.argv[1]), sys.argv[2], pathlib.Path(sys.argv[3])
    out.write_text(build(web, mode == "--inline"), encoding="utf-8")
    print(f"{out}  {out.stat().st_size/1024:.0f} KB")


if __name__ == "__main__":
    main()
