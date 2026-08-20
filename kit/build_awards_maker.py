#!/usr/bin/env python3
"""
Build AwardsMaker.html — the offline certificate maker that ships inside the kit.

    python3 kit/build_awards_maker.py kit/dist/AwardsMaker.html

One self-contained HTML file. The buyer opens it in any browser, types names, and prints.
No account, no software, no internet — which is the whole pitch against a Canva template.

The certificates are drawn live in HTML/CSS rather than embedded as images. That decision
carries the product:

  * the file is ~200 KB instead of ~13 MB of base64 PNGs
  * the recipient name is real text, so it typesets properly at any length
  * printing goes at printer resolution rather than resampling a 300dpi raster
  * every field is editable, so "editable template" is literally true

Certificate data is read from the design manifests, so the maker always carries exactly
the designs that exist.
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DESIGN = ROOT.parent / "design"
MANIFESTS = ["manifest.json", "manifest-christmas.json", "manifest-office.json"]

# The sheet is authored at 300dpi (2400x3000 = 8x10in) to match the print artwork, then
# scaled down for both screen and paper. 8in at 96 CSS dpi is 768px, so 768/2400 = 0.32.
PRINT_SCALE = 0.32


def collect() -> list:
    out = []
    for m in MANIFESTS:
        p = DESIGN / "out" / m
        if not p.exists():
            continue
        for c in json.loads(p.read_text(encoding="utf-8")):
            out.append({k: c[k] for k in
                        ("slug", "title", "subject", "department", "citation", "seal", "ref")})
    return out


def build() -> str:
    certs = collect()
    groups = {"": "General occasions", "x-": "Christmas & gift exchange", "o-": "Office awards"}
    for c in certs:
        c["group"] = ("x-" if c["slug"].startswith("x-")
                      else "o-" if c["slug"].startswith("o-") else "")
    return (TEMPLATE
            .replace("/*DATA*/", json.dumps(certs, ensure_ascii=False))
            .replace("/*GROUPS*/", json.dumps(groups, ensure_ascii=False))
            .replace("/*SCALE*/", str(PRINT_SCALE))
            .replace("<!--COUNT-->", str(len(certs))))


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Awards Maker — The Bureau of Minor Achievements</title>
<style>
:root{
  --paper:#F2EFE4; --ink:#17150F; --red:#B4321F; --olive:#565E42; --faint:#B9B3A0;
  --ui-bg:#E3E1D8; --ui-card:#FBFAF5; --ui-line:#C6C2B4; --ui-muted:#6B6658;
  --serif:"Liberation Serif",Georgia,"Times New Roman",serif;
  --mono:"Liberation Mono","DejaVu Sans Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
}
*{box-sizing:border-box}
body{margin:0;background:var(--ui-bg);color:var(--ink);font-family:var(--serif);
  font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
h1,h2,h3{margin:0;line-height:1.2}
button,input,select,textarea{font:inherit;color:inherit}
:focus-visible{outline:2px solid var(--red);outline-offset:2px}

.app{display:grid;grid-template-columns:352px 1fr;min-height:100vh}
@media (max-width:900px){.app{grid-template-columns:1fr}}

/* ---------- control panel ---------- */
.panel{background:var(--ui-card);border-right:1px solid var(--ui-line);padding:24px;
  display:flex;flex-direction:column;gap:22px;overflow-y:auto;max-height:100vh;
  position:sticky;top:0}
@media (max-width:900px){.panel{position:static;max-height:none;border-right:0;
  border-bottom:1px solid var(--ui-line)}}
.brand{font-family:var(--mono);font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;
  color:var(--red)}
.panel h1{font-size:23px;margin-top:6px}
.hint{font-size:13.5px;color:var(--ui-muted)}

fieldset{border:0;padding:0;margin:0;display:flex;flex-direction:column;gap:10px}
/* an author display rule beats the UA stylesheet's [hidden], so restate it */
[hidden]{display:none !important}
legend{font-family:var(--mono);font-size:10px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--ui-muted);padding:0 0 8px;border-bottom:1px solid var(--ui-line);width:100%;
  margin-bottom:4px}
label{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--ui-muted);display:block;margin-bottom:5px}
input[type=text],select,textarea{width:100%;padding:9px 11px;background:#fff;
  border:1px solid var(--ui-line);border-radius:2px;font-size:14.5px}
textarea{min-height:132px;resize:vertical;font-family:var(--mono);font-size:13px;
  line-height:1.7}
.row{display:flex;gap:10px}.row>*{flex:1}

.tabs{display:flex;border:1px solid var(--ink)}
.tabs button{flex:1;padding:10px;background:transparent;border:0;cursor:pointer;
  font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase}
.tabs button[aria-selected=true]{background:var(--ink);color:var(--paper)}

.btn{width:100%;padding:13px;background:var(--ink);color:var(--paper);border:0;cursor:pointer;
  font-family:var(--mono);font-size:12px;letter-spacing:.15em;text-transform:uppercase}
.btn:hover{background:var(--red)}
.btn.sec{background:transparent;color:var(--ink);border:1.5px solid var(--ink)}
.btn.sec:hover{background:var(--ink);color:var(--paper)}
.count{font-family:var(--mono);font-size:11.5px;color:var(--ui-muted);text-align:center}

/* ---------- preview stage ---------- */
.stage{padding:30px;display:flex;flex-direction:column;align-items:center;gap:26px}
.page{width:768px;height:960px;overflow:hidden;background:var(--paper);
  box-shadow:0 8px 30px rgba(28,24,16,.22);flex:0 0 auto}
@media (max-width:900px){
  .stage{padding:16px}
  .page{width:100%;max-width:768px;height:auto;aspect-ratio:768/960}
}

/* ---------- the certificate itself (authored at 2400x3000) ---------- */
.scaler{width:2400px;height:3000px;transform:scale(/*SCALE*/);transform-origin:0 0}
@media (max-width:900px){.scaler{transform:scale(calc(var(--fit,.32)))}}
.sheet{position:relative;width:2400px;height:3000px;background:var(--paper);
  padding:250px 190px 500px;display:flex;flex-direction:column;align-items:center;
  text-align:center;justify-content:center;font-family:var(--serif);color:var(--ink)}
.sheet .block{width:100%;display:flex;flex-direction:column;align-items:center}
.sheet .block+.block{margin-top:190px}
.frame-outer{position:absolute;inset:78px;border:7px solid var(--ink)}
.frame-inner{position:absolute;inset:104px;border:2px solid var(--ink)}
.corner{position:absolute;width:64px;height:64px;border:5px solid var(--red)}
.c-tl{top:118px;left:118px;border-right:0;border-bottom:0}
.c-tr{top:118px;right:118px;border-left:0;border-bottom:0}
.c-bl{bottom:118px;left:118px;border-right:0;border-top:0}
.c-br{bottom:118px;right:118px;border-left:0;border-top:0}
/* preserveAspectRatio="none" needs an explicit width or the band stops short */
.guilloche{position:absolute;left:126px;right:126px;width:calc(100% - 252px);height:40px;
  opacity:.85}
.guilloche.top{top:132px}.guilloche.bottom{bottom:132px}
.agency{font-size:42px;letter-spacing:16px;color:var(--red);text-transform:uppercase}
.rule{width:360px;height:2px;background:var(--ink);margin:34px auto 0;opacity:.5}
.title{margin-top:62px;font-size:132px;line-height:1.04;font-weight:700;letter-spacing:-1px;
  text-transform:uppercase;text-wrap:balance}
.subject{margin-top:34px;font-size:46px;letter-spacing:14px;color:var(--olive);
  text-transform:uppercase}
.presented{font-size:38px;font-style:italic;opacity:.72}
.nameline{margin-top:30px;width:1640px;border-bottom:3px solid var(--ink);padding-bottom:18px}
.name{font-size:112px;font-style:italic;line-height:1.1}
.citation{margin-top:100px;width:1640px;font-size:44px;line-height:1.62}
.dept{margin-top:58px;font-size:33px;letter-spacing:9px;color:var(--red);text-transform:uppercase}
.footer{position:absolute;left:190px;right:190px;bottom:250px;display:flex;
  align-items:flex-end;justify-content:space-between}
.seal{width:330px;height:330px}
.sigblock{width:560px;text-align:center}
.sigline{border-bottom:2px solid var(--ink);height:96px;display:flex;align-items:flex-end;
  justify-content:center;padding-bottom:8px;font-size:56px;font-style:italic}
.siglabel{margin-top:14px;font-size:26px;letter-spacing:5px;opacity:.62;text-transform:uppercase}
.refblock{width:420px;text-align:left;font-family:var(--mono);font-size:24px;line-height:1.9;
  opacity:.6}

/* ---------- print ---------- */
@page{size:Letter portrait;margin:0.25in}
@media print{
  body{background:#fff}
  .panel,.noprint{display:none !important}
  .app{display:block}
  .stage{padding:0;gap:0;display:block}
  .page{width:768px;height:960px;box-shadow:none;break-after:page;page-break-after:always}
  .page:last-child{break-after:auto;page-break-after:auto}
  .scaler{transform:scale(/*SCALE*/) !important}
}
</style>
</head>
<body>
<div class="app">

  <aside class="panel noprint">
    <div>
      <div class="brand">The Bureau of Minor Achievements</div>
      <h1>Awards Maker</h1>
      <p class="hint"><!--COUNT--> certificates. Type a name, print. Nothing is uploaded
        anywhere — this file works with the internet switched off.</p>
    </div>

    <div class="tabs" role="tablist">
      <button role="tab" id="tab-one" aria-selected="true" aria-controls="p-one">One award</button>
      <button role="tab" id="tab-many" aria-selected="false" aria-controls="p-many">Whole team</button>
    </div>

    <fieldset id="p-one">
      <legend>Single certificate</legend>
      <div>
        <label for="design">Award</label>
        <select id="design"></select>
      </div>
      <div>
        <label for="name">Recipient name</label>
        <input type="text" id="name" value="Jordan Ellis" placeholder="Name as it should print">
      </div>
    </fieldset>

    <fieldset id="p-many" hidden>
      <legend>The whole team</legend>
      <p class="hint">One name per line. Awards are handed out in order and start again from
        the top once they run out — reorder the lines to change who gets what.</p>
      <textarea id="names" spellcheck="false">Jordan Ellis
Priya Raman
Marcus Webb
Ana Sofia Reyes
Tom Okafor</textarea>
      <div>
        <label for="startat">Start from award</label>
        <select id="startat"></select>
      </div>
    </fieldset>

    <fieldset>
      <legend>On every certificate</legend>
      <div class="row">
        <div>
          <label for="date">Date</label>
          <input type="text" id="date" placeholder="December 2026">
        </div>
        <div>
          <label for="signer">Signed by</label>
          <input type="text" id="signer" placeholder="(leave blank to sign by hand)">
        </div>
      </div>
      <div>
        <label for="registrar">Signature line reads</label>
        <input type="text" id="registrar" value="Registrar, B.M.A.">
      </div>
    </fieldset>

    <fieldset>
      <legend>Rewrite this award</legend>
      <p class="hint">Only affects the award selected above. Reload the file to undo.</p>
      <div><label for="e-title">Title</label><input type="text" id="e-title"></div>
      <div><label for="e-subject">Subtitle</label><input type="text" id="e-subject"></div>
      <div><label for="e-dept">Department</label><input type="text" id="e-dept"></div>
      <div><label for="e-cit">Citation</label><textarea id="e-cit" style="min-height:88px"></textarea></div>
    </fieldset>

    <div>
      <button class="btn" id="print">Print / Save as PDF</button>
      <p class="count" id="count" style="margin-top:10px"></p>
    </div>
    <p class="hint">In the print dialog choose <b>Letter</b>, portrait, and set Margins to
      <b>Default</b>. To make a PDF, pick “Save as PDF” as the destination.</p>
  </aside>

  <main class="stage" id="stage"></main>
</div>

<script>
const CERTS = /*DATA*/;
const GROUPS = /*GROUPS*/;

const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"]/g, c =>
  ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

/* the Bureau seal, drawn rather than embedded so it prints sharp */
const seal = () => `
<svg viewBox="0 0 400 400" class="seal" xmlns="http://www.w3.org/2000/svg">
  <defs><path id="rim" d="M200,200 m-148,0 a148,148 0 1,1 296,0 a148,148 0 1,1 -296,0"/></defs>
  <circle cx="200" cy="200" r="180" fill="none" stroke="#B4321F" stroke-width="5"/>
  <circle cx="200" cy="200" r="168" fill="none" stroke="#B4321F" stroke-width="2"/>
  <circle cx="200" cy="200" r="120" fill="none" stroke="#B4321F" stroke-width="2"/>
  <text font-family="Liberation Serif, Times New Roman, serif" font-size="26"
        letter-spacing="5" fill="#B4321F">
    <textPath href="#rim" startOffset="50%" text-anchor="middle">
      &#9733; BUREAU OF MINOR ACHIEVEMENTS &#9733;</textPath></text>
  <g transform="translate(200,208) rotate(-6)" fill="none" stroke="#B4321F" stroke-width="4.5"
     stroke-linecap="round">
    <path d="M-52,26 C-64,-10 -44,-44 -12,-56"/><path d="M52,26 C64,-10 44,-44 12,-56"/>
    <path d="M-44,10 l-19,-9 M-38,-8 l-20,-7 M-28,-26 l-19,-4 M-14,-42 l-16,2
             M44,10 l19,-9 M38,-8 l20,-7 M28,-26 l19,-4 M14,-42 l16,2"/></g>
  <text x="200" y="272" text-anchor="middle" font-family="Liberation Serif, serif"
        font-size="25" letter-spacing="6" fill="#B4321F">EST. 1997</text>
</svg>`;

const wave = pos => `
<svg class="guilloche ${pos}" viewBox="0 0 1200 40" preserveAspectRatio="none"
     xmlns="http://www.w3.org/2000/svg">
  <defs><pattern id="w${pos}" width="60" height="40" patternUnits="userSpaceOnUse">
    <path d="M0,20 C15,2 15,38 30,20 C45,2 45,38 60,20" fill="none" stroke="#B9B3A0" stroke-width="1.6"/>
    <path d="M0,20 C15,38 15,2 30,20 C45,38 45,2 60,20" fill="none" stroke="#B9B3A0" stroke-width="1.6"/>
  </pattern></defs><rect width="1200" height="40" fill="url(#w${pos})"/></svg>`;

/* long names have to shrink or they collide with the ruled line */
const nameSize = n => n.length <= 18 ? 112 : n.length <= 26 ? 92 : n.length <= 34 ? 74 : 60;

function sheet(c, who) {
  const signer = $('signer').value.trim();
  const date = $('date').value.trim();
  return `<div class="page"><div class="scaler"><div class="sheet">
    <div class="frame-outer"></div><div class="frame-inner"></div>
    <div class="corner c-tl"></div><div class="corner c-tr"></div>
    <div class="corner c-bl"></div><div class="corner c-br"></div>
    ${wave('top')}${wave('bottom')}
    <div class="block">
      <div class="agency">The Bureau of Minor Achievements</div>
      <div class="rule"></div>
      <div class="title">${esc(c.title)}</div>
      <div class="subject">${esc(c.subject)}</div>
    </div>
    <div class="block">
      <div class="presented">This is to certify that</div>
      <div class="nameline"><div class="name" style="font-size:${nameSize(who)}px">${esc(who)}</div></div>
      <div class="citation">${esc(c.citation)}</div>
      <div class="dept">${esc(c.department)}</div>
    </div>
    <div class="footer">
      ${seal()}
      <div class="refblock">REF&nbsp; ${esc(c.ref)}<br>ISSUED&nbsp; ${esc(date || '—')}<br>
        STATUS&nbsp; IRREVOCABLE</div>
      <div class="sigblock">
        <div class="sigline">${esc(signer)}</div>
        <div class="siglabel">${esc($('registrar').value)}</div>
      </div>
    </div>
  </div></div></div>`;
}

const mode = () => $('tab-one').getAttribute('aria-selected') === 'true' ? 'one' : 'many';

function current() {
  const c = {...CERTS[+$('design').value]};
  // the rewrite fields override the stored copy, but only for the selected award
  if ($('e-title').value.trim()) c.title = $('e-title').value;
  if ($('e-subject').value.trim()) c.subject = $('e-subject').value;
  if ($('e-dept').value.trim()) c.department = $('e-dept').value;
  if ($('e-cit').value.trim()) c.citation = $('e-cit').value;
  return c;
}

function render() {
  let html = '', n = 0;
  if (mode() === 'one') {
    html = sheet(current(), $('name').value || '{ Recipient Name }');
    n = 1;
  } else {
    const people = $('names').value.split('\n').map(s => s.trim()).filter(Boolean);
    const start = +$('startat').value;
    html = people.map((p, i) => sheet(CERTS[(start + i) % CERTS.length], p)).join('');
    n = people.length;
  }
  $('stage').innerHTML = html || '';
  $('count').textContent = n === 1 ? '1 certificate ready' : `${n} certificates ready`;
  fit();
}

/* on narrow screens the sheet scales to whatever width is left */
function fit() {
  const p = document.querySelector('.page');
  if (!p) return;
  document.documentElement.style.setProperty('--fit', (p.clientWidth / 2400).toFixed(4));
}

function fillSelects() {
  const opts = CERTS.map((c, i) =>
    `<option value="${i}">${esc(c.title)} — ${esc(c.subject.toLowerCase())}</option>`);
  const grouped = Object.keys(GROUPS).map(g => {
    const inner = CERTS.map((c, i) => [c, i]).filter(([c]) => c.group === g)
      .map(([c, i]) => opts[i]).join('');
    return inner ? `<optgroup label="${esc(GROUPS[g])}">${inner}</optgroup>` : '';
  }).join('');
  $('design').innerHTML = grouped;
  $('startat').innerHTML = grouped;
}

function syncEditors() {
  const c = CERTS[+$('design').value];
  $('e-title').value = c.title; $('e-subject').value = c.subject;
  $('e-dept').value = c.department; $('e-cit').value = c.citation;
}

for (const t of ['tab-one', 'tab-many']) {
  $(t).addEventListener('click', () => {
    const one = t === 'tab-one';
    $('tab-one').setAttribute('aria-selected', one);
    $('tab-many').setAttribute('aria-selected', !one);
    $('p-one').hidden = !one; $('p-many').hidden = one;
    render();
  });
}
$('design').addEventListener('change', () => { syncEditors(); render(); });
for (const id of ['name','names','date','signer','registrar','startat',
                  'e-title','e-subject','e-dept','e-cit']) {
  $(id).addEventListener('input', render);
}
$('print').addEventListener('click', () => window.print());
addEventListener('resize', fit);

fillSelects();
syncEditors();
$('date').value = new Date().toLocaleDateString('en-US', {month:'long', year:'numeric'});
render();
</script>
</body>
</html>
"""


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out = pathlib.Path(sys.argv[1])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(), encoding="utf-8")
    print(f"{out}  {out.stat().st_size/1024:.0f} KB  ({len(collect())} designs)")


if __name__ == "__main__":
    main()
