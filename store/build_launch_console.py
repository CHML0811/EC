#!/usr/bin/env python3
"""
Build the Etsy launch console from the listing docs.

    python3 store/build_launch_console.py

The console used to hardcode listing #1's title, tags, description and price. That copy also
lives in marketing/*.md, and the two drifted: the published console still carried an old
comma-separated title, an old tag set, a price that had been changed twice and a fee figure
that had been corrected. Nothing failed, because nothing was checking.

So the docs are the source of truth and this generates the console from them. A title that
changes in the doc changes here on the next build, and the character counts are measured
rather than asserted by hand — all three were wrong before this existed.

Output: store/etsy-launch-console.html
"""

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "store" / "etsy-launch-console.html"
CSS = (ROOT / "store" / "_console_css.txt").read_text(encoding="utf-8")

# Per-listing facts that aren't in the copy docs: what to build, what to upload, and the
# order the images go up in. Everything else is parsed.
LISTINGS = [
    {
        "key": "office",
        "tab": "1 · Office",
        "doc": "marketing/etsy-office-awards-kit.md",
        "price": "14.99",
        "price_note": "<b>If the top organic row is $5–$8 with 400+ reviews, drop to "
                      "$9.99</b> — the premium needs a visible reason. If it's $15–$25 "
                      "Canva bundles, hold or raise.",
        "build": "python3 kit/build_kit.py",
        "zip": ("kit/Office-Awards-Kit.zip", "8.2 MB · cap is 20 MB"),
        "build_note": "Produces <b>kit/Office-Awards-Kit.zip</b> — 38 certificates, 5 PDFs "
                      "and the Awards Maker, 8.2 MB.",
        "images": [
            ("kit/listing/kit-1-hero.png", "printed, on a desk, DIGITAL DOWNLOAD"),
            ("kit/listing/kit-3-maker.png", "the maker — nobody else has this"),
            ("kit/listing/kit-2-grid.png", "all 38 at once"),
            ("kit/listing/kit-4-promise.png", "kills the objections"),
        ],
        "when": "Publish first. It's finished, and one live listing teaches more than four "
                "unpublished ones.",
    },
    {
        "key": "christmas",
        "tab": "2 · Christmas",
        "doc": "marketing/etsy-christmas-awards-kit.md",
        "price": "12.99",
        "price_note": "Same zip as listing #1 — no new product, no new fulfilment. Priced "
                      "just under the office listing because the seasonal buyer is "
                      "comparing against cheaper single-use party printables.",
        "build": "python3 kit/build_listing_images.py --christmas",
        "zip": ("kit/Office-Awards-Kit.zip", "the same file as listing #1"),
        "build_note": "The zip already exists — the eight Christmas certificates are inside "
                      "it. This command only builds the seasonal hero image.",
        "images": [
            ("kit/listing/kit-x1-hero.png", "Christmas-specific thumbnail"),
            ("kit/listing/kit-3-maker.png", "the maker"),
            ("kit/listing/kit-2-grid.png", "all 38 at once"),
            ("kit/listing/kit-4-promise.png", "kills the objections"),
        ],
        "when": "<b>This week.</b> Seasonal printables need 6–8 weeks to index and office "
                "parties are booked through November. Mid-October is the last responsible "
                "date, not the target.",
    },
    {
        "key": "school",
        "tab": "3 · Classroom",
        "doc": "marketing/etsy-teacher-awards-kit.md",
        "price": None,
        "price_note": "<b>Not set on purpose.</b> The educational band runs $3–20 and skews "
                      "low. Read the top row of <b>funny teacher awards printable</b> — "
                      "price and file count — and set it against that. Lead with the "
                      "teacher's script, not with the number twelve.",
        "build": "python3 kit/build_kit.py --school",
        "zip": ("kit/Classroom-Awards-Kit.zip", "2.8 MB · cap is 20 MB"),
        "build_note": "Produces <b>kit/Classroom-Awards-Kit.zip</b> — 12 certificates, 3 "
                      "PDFs and its own Awards Maker, 2.8 MB.",
        "images": [
            ("kit/listing/kit-s1-hero.png", "printed, on a desk, DIGITAL DOWNLOAD"),
            ("kit/listing/kit-s3-maker.png", "the maker"),
            ("kit/listing/kit-s2-grid.png", "all 12, titles legible"),
            ("kit/listing/kit-s4-promise.png", "safe to read out loud"),
        ],
        "when": "Last. End-of-year awards sell in May and June, so this wants to be live "
                "around March. Publishing early costs nothing, but it must not delay "
                "Christmas.",
    },
]


# ----------------------------------------------------------------- parsing
def section(text: str, heading: str) -> str:
    m = re.search(rf"^## {heading}.*?$(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        raise SystemExit(f"no '## {heading}' section found")
    return m.group(1)


def fenced(block: str) -> str:
    m = re.search(r"```\n(.*?)\n```", block, re.S)
    if not m:
        raise SystemExit("expected a fenced code block")
    return m.group(1).strip()


def blockquote(block: str) -> str:
    """The description is a markdown blockquote; Etsy wants plain text with blank lines."""
    out = []
    for ln in block.splitlines():
        if ln.startswith("> "):
            out.append(ln[2:].rstrip())
        elif ln.strip() == ">":
            out.append("")
    # unwrap hard-wrapped paragraphs; a bullet or a blank line ends one
    paras, buf = [], []
    for ln in out:
        if not ln:
            if buf:
                paras.append(" ".join(buf))
                buf = []
            paras.append("")
        elif ln.startswith(("✦", "1.", "2.", "3.")):
            if buf:
                paras.append(" ".join(buf))
                buf = []
            paras.append(ln)
        else:
            buf.append(ln)
    if buf:
        paras.append(" ".join(buf))
    text = "\n".join(paras)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)       # Etsy renders no markdown
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def load(spec: dict) -> dict:
    doc = (ROOT / spec["doc"]).read_text(encoding="utf-8")
    title = fenced(section(doc, "Title"))
    tags = [t.strip() for t in fenced(section(doc, "Tags")).split("·")]
    desc = blockquote(section(doc, "Description"))

    if len(tags) != 13:
        raise SystemExit(f"{spec['doc']}: {len(tags)} tags, Etsy wants exactly 13")
    over = [t for t in tags if len(t) > 20]
    if over:
        raise SystemExit(f"{spec['doc']}: tags over 20 chars: {over}")
    if len(title) > 140:
        raise SystemExit(f"{spec['doc']}: title is {len(title)} chars, Etsy's cap is 140")

    return {**spec, "title": title, "tags": tags, "desc": desc}


def main() -> None:
    data = [load(s) for s in LISTINGS]

    # Two listings sharing a primary keyword means Etsy buries one of them.
    for i, a in enumerate(data):
        for b in data[i + 1:]:
            shared = set(a["tags"]) & set(b["tags"])
            if shared:
                raise SystemExit(f"{a['key']} and {b['key']} share tags: {sorted(shared)}")

    payload = [{
        "key": d["key"], "tab": d["tab"], "title": d["title"], "tags": d["tags"],
        "desc": d["desc"], "price": d["price"], "priceNote": d["price_note"],
        "build": d["build"], "buildNote": d["build_note"], "when": d["when"],
        "zip": list(d["zip"]), "images": [list(i) for i in d["images"]],
        "titleLen": len(d["title"]),
    } for d in data]

    OUT.write_text(TEMPLATE.replace("/*CSS*/", CSS)
                           .replace("/*DATA*/", json.dumps(payload, ensure_ascii=False)),
                   encoding="utf-8")
    kb = OUT.stat().st_size / 1024
    print(f"{OUT.relative_to(ROOT)}  {kb:.0f} KB  ({len(data)} listings)")
    for d in payload:
        price = f"${d['price']}" if d["price"] else "price unset"
        print(f"  {d['key']:<10} {d['titleLen']:3} chars · {len(d['tags'])} tags · {price}")


TEMPLATE = r"""<title>Etsy Launch Console</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
/*CSS*/
/* ---- listing switcher ---- */
.tabs{display:flex;gap:8px;flex-wrap:wrap}
.tab{background:var(--sunk);border:1px solid var(--rule);color:var(--muted);
  padding:7px 14px;font-family:var(--mono);font-size:11px;letter-spacing:.1em;
  text-transform:uppercase}
.tab[aria-selected="true"]{background:var(--ink);border-color:var(--ink);color:var(--ground)}
.tab:hover{border-color:var(--accent);color:var(--accent)}
.tab[aria-selected="true"]:hover{color:var(--ground)}
.when{border-left:3px solid var(--done);padding:11px 14px;background:var(--sunk);
  font-size:14.5px;color:var(--muted);margin-top:14px}
.when b{color:var(--ink);font-weight:400}
</style>

<div class="bar"><div class="wrap barin">
  <h1>Etsy Launch</h1>
  <div class="track"><div class="fill" id="fill"></div></div>
  <span class="tally" id="tally">0 of 9</span>
  <button class="reset" id="reset">Reset</button>
</div></div>

<div class="wrap">
  <div class="intro">
    <div class="eyebrow">The Bureau of Minor Achievements</div>
    <h2>Three listings. Nine steps each.</h2>
    <p>Every field is here in the order Etsy asks for it, with a copy button. Keep this open
      beside the Etsy tab. Progress is saved per listing in this browser, so you can stop
      halfway and come back.</p>
    <div class="tabs" id="tabs" role="tablist"></div>
    <div class="when" id="when"></div>
  </div>

  <div class="steps" id="steps"></div>

  <div class="after">
    <h2>The first 48 hours</h2>
    <ul>
      <li><b>Don't touch the listing.</b> Etsy gives new listings a boost for 14–21 days.
        Editing resets how it's being measured.</li>
      <li><b>Watch impressions, not views.</b> Etsy Stats → Search. No impressions means the
        title doesn't match how people search — that's the only thing worth changing early.</li>
      <li><b>Expect nothing for two weeks.</b> Ranking takes 30–90 days. Silence in week one
        is normal, not a verdict.</li>
      <li><b>Pin every listing the day you publish it.</b> Pinterest is the main free traffic
        source for printables after Etsy search. One vertical pin using the exact title
        keyword, then three variants. No ads until a listing converts.</li>
      <li><b>The tags don't overlap between listings</b>, and that's deliberate — two
        listings competing for the same primary keyword means Etsy buries one of them.</li>
    </ul>
  </div>
</div>

<script>
const LISTINGS = /*DATA*/;

const esc = s => String(s).replace(/[&<>"]/g, c =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

let current = 0;
const keyFor = i => "bma-etsy-launch-" + LISTINGS[i].key;
let done = new Set();

function loadProgress() {
  try { done = new Set(JSON.parse(localStorage.getItem(keyFor(current)) || "[]")); }
  catch (e) { done = new Set(); }          // private mode, or storage blocked
}
function save() {
  try { localStorage.setItem(keyFor(current), JSON.stringify([...done])); } catch (e) {}
}

function steps(L) {
  const price = L.price
    ? [["Price (USD)", L.price, "code"]]
    : [["Price (USD)", "— read the live grid first —", "text"]];
  return [
    { t: "Create the Etsy seller account", m: "~15 min",
      p: "Needs your ID and bank details, which is why nobody can do this part for you. Everything after it is copy and paste. Already done? Tick it and move on.",
      link: ["https://www.etsy.com/sell", "Open Etsy seller signup"],
      fields: [["Shop name", "BureauOfMinorAchievements", "text"]],
      note: "If the name is taken, drop a word — <b>MinorAchievements</b> — rather than adding numbers. A number reads as spam to buyers." },

    { t: "Build the file you'll upload", m: "~90 sec",
      p: "A fresh clone has the source but not the built product. One command creates it.",
      fields: [["Run in the project folder", L.build, "code"]],
      note: L.buildNote + " If it can't find Chrome, install it or set <b>CHROME</b> to its path." },

    { t: "Start a new listing — Digital", m: "~1 min",
      p: "Shop Manager → Listings → Add a listing. Set the type to Digital straight away: it removes shipping entirely, which is the whole reason these go first.",
      note: "Category: <b>Paper &amp; Party Supplies → Paper → Stationery</b>. Renewal: automatic. No production partner." },

    { t: "Title", m: "~30 sec",
      p: `Front-loaded with the phrase that carries buying intent. ${L.titleLen} characters, inside Etsy's 140 limit.`,
      fields: [["Listing title", L.title, "text"]] },

    { t: "Description", m: "~1 min",
      p: "Paste as-is. Etsy renders plain text, so the line breaks are the formatting.",
      fields: [["Description", L.desc, "text"]] },

    { t: "The 13 tags", m: "~3 min",
      p: "Etsy allows exactly 13 and silently rejects any tag over 20 characters. These are all checked, and none of them are used by the other two listings.",
      tags: true,
      note: "Add them one at a time. If Etsy rejects one, it's a duplicate of a word already in your title — swap it rather than dropping to 12." },

    { t: "Price and settings", m: "~1 min",
      p: "Live party-award listings cluster at $6–$12, not the $12–$40 business-template band. Check the top organic row before you publish.",
      fields: price,
      note: "Quantity: <b>999</b>. Personalization: <b>off</b> — the buyer types the names, that's the product. " + L.priceNote },

    { t: "Upload the file and the images", m: "~4 min",
      p: "Images first, in this exact order. Etsy uses the first as your search-grid thumbnail. Note image 2 is the maker, not the grid — competitors sell packs of 50 to 101 certificates, so the count is not the argument. Working software is.",
      files: true },

    { t: "Publish", m: "~10 sec",
      p: "That's the whole thing. From here it's Etsy's search that does the selling.",
      note: L.price
        ? `At $${L.price} Etsy takes roughly <b>11%</b> on an organic sale — $0.20 listing, 6.5% transaction, 3% + $0.25 processing — and there is no cost of goods at all.`
        : "Set the price before you publish this one." }
  ];
}

function field([label, value, kind], id) {
  return `<div class="field">
    <div class="flabel"><span>${esc(label)}</span>
      <button class="copy" data-copy="${id}">Copy</button></div>
    <div class="fval ${kind === "code" ? "code" : ""}" id="v${id}">${esc(value)}</div>
  </div>`;
}

function render() {
  const L = LISTINGS[current];
  const S = steps(L);

  document.getElementById("tabs").innerHTML = LISTINGS.map((x, i) =>
    `<button class="tab" role="tab" data-tab="${i}"
       aria-selected="${i === current}">${esc(x.tab)}</button>`).join("");
  document.getElementById("when").innerHTML = L.when;

  document.getElementById("steps").innerHTML = S.map((s, i) => {
    const isDone = done.has(i);
    let inner = s.p ? `<p>${s.p}</p>` : "";
    if (s.link) inner += `<a class="go" href="${s.link[0]}" target="_blank" rel="noopener">${s.link[1]} →</a>`;
    (s.fields || []).forEach((f, j) => { inner += field(f, `${i}-${j}`); });
    if (s.tags) inner += `<div class="field"><div class="flabel">
        <span>13 tags · comma separated</span>
        <button class="copy" data-copy="tags">Copy all</button></div>
      <div class="tags">${L.tags.map(t =>
        `<span class="tag ${t.length > 17 ? "tight" : ""}"><b>${esc(t)}</b><i>${t.length}</i></span>`).join("")}
      </div><div class="fval code" id="vtags" hidden>${esc(L.tags.join(", "))}</div></div>`;
    if (s.files) {
      const rows = L.images.map(([p, w], n) =>
        `<div class="file"><i>Image ${n + 1}</i><b>${esc(p)}</b><em>${w}</em></div>`).join("")
        + `<div class="file"><i>The file</i><b>${esc(L.zip[0])}</b><em>${esc(L.zip[1])}</em></div>`;
      inner += `<div class="files">${rows}</div>`;
    }
    if (s.note) inner += `<div class="note">${s.note}</div>`;

    return `<section class="step ${isDone ? "done" : ""}">
      <button class="tick" data-step="${i}" aria-pressed="${isDone}"
        aria-label="Mark step ${i + 1} done">${isDone ? "✓" : i + 1}</button>
      <div class="head"><h3>${esc(s.t)}</h3><span class="mins">${s.m}</span></div>
      <div class="body">${inner}</div>
    </section>`;
  }).join("");

  const n = done.size, total = S.length;
  document.getElementById("fill").style.width = (n / total * 100) + "%";
  document.getElementById("tally").textContent =
    n === total ? `${L.tab} done` : `${n} of ${total}`;
}

document.addEventListener("click", e => {
  const tab = e.target.closest(".tab");
  if (tab) {
    current = +tab.dataset.tab;
    loadProgress(); render();
    return;
  }
  const tick = e.target.closest(".tick");
  if (tick) {
    const i = +tick.dataset.step;
    done.has(i) ? done.delete(i) : done.add(i);
    save(); render(); return;
  }
  const btn = e.target.closest(".copy");
  if (!btn) return;
  const src = document.getElementById("v" + btn.dataset.copy);
  if (!src) return;
  navigator.clipboard.writeText(src.textContent).then(() => {
    btn.textContent = "Copied"; btn.classList.add("ok");
    setTimeout(() => { btn.textContent = btn.dataset.copy === "tags" ? "Copy all" : "Copy";
                       btn.classList.remove("ok"); }, 1400);
  }).catch(() => { btn.textContent = "Select it"; });
});

document.getElementById("reset").addEventListener("click", () => {
  done = new Set(); save(); render();
});

loadProgress();
render();
</script>
"""


if __name__ == "__main__":
    main()
