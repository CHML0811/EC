#!/usr/bin/env python3
"""
Build the printable documents that ship alongside the certificates.

    python3 kit/build_documents.py kit/dist

Produces, as both PDF and HTML:

  Start-Here.pdf     what's in the box and the ten-minute path to a finished ceremony
  Hosts-Script.pdf   what to actually say, word for word, with timings
  Ballot.pdf         nomination sheet — turns one buyer into a whole-office activity
  Name-Tents.pdf     fold-over table tents, four per sheet
  Announcement.pdf   the emails: announce, remind, follow up

The host's script is the real product. Anyone can make a certificate; the buyer's actual
problem is standing up in front of forty colleagues without dying, and nothing else on
the market solves that.
"""

import html
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "design"))
import generate_certificates as g  # noqa: E402

PAPER, INK, RED, OLIVE, FAINT = g.PAPER, g.INK, g.RED, g.OLIVE, g.FAINT

CSS = f"""
@page{{size:Letter portrait;margin:0.7in}}
*{{box-sizing:border-box}}
body{{margin:0;background:#fff;color:{INK};
  font-family:"Liberation Serif",Georgia,"Times New Roman",serif;font-size:11.5pt;
  line-height:1.55}}
h1,h2,h3{{margin:0;line-height:1.18;text-wrap:balance}}
p{{margin:0}}
.mono{{font-family:"Liberation Mono","DejaVu Sans Mono",monospace}}
.eyebrow{{font-family:"Liberation Mono",monospace;font-size:8pt;letter-spacing:.24em;
  text-transform:uppercase;color:{RED}}}
.mast{{border-bottom:2.5pt solid {INK};padding-bottom:14pt;margin-bottom:22pt}}
.mast h1{{font-size:26pt;margin-top:9pt}}
.mast .sub{{margin-top:9pt;color:#5C5749;font-size:11pt;max-width:60ch}}
h2{{font-size:9pt;font-family:"Liberation Mono",monospace;letter-spacing:.2em;
  text-transform:uppercase;color:{RED};margin-top:22pt;padding-bottom:6pt;
  border-bottom:.6pt solid #C9C4B3}}
h3{{font-size:13pt;margin-top:15pt}}
p+p{{margin-top:8pt}}
ul,ol{{margin:9pt 0 0;padding-left:19pt}}
li{{margin-bottom:6pt}}
.say{{background:#F4F2EA;border-left:3pt solid {RED};padding:11pt 14pt;margin-top:10pt;
  font-size:11.5pt}}
.say b{{display:block;font-family:"Liberation Mono",monospace;font-size:7.5pt;
  letter-spacing:.2em;text-transform:uppercase;color:{RED};margin-bottom:6pt}}
.tip{{margin-top:9pt;font-size:10pt;color:#5C5749;font-style:italic}}
table{{width:100%;border-collapse:collapse;margin-top:11pt;font-size:10.5pt}}
th,td{{text-align:left;padding:7pt 9pt;border-bottom:.6pt solid #D5D0C0;vertical-align:top}}
th{{font-family:"Liberation Mono",monospace;font-size:7.5pt;letter-spacing:.16em;
  text-transform:uppercase;color:#5C5749;border-bottom:.9pt solid {INK}}}
.t{{white-space:nowrap;font-family:"Liberation Mono",monospace;font-size:9.5pt;color:{RED}}}
.page-break{{break-before:page;page-break-before:always}}
.foot{{margin-top:26pt;padding-top:10pt;border-top:.6pt solid #C9C4B3;
  font-family:"Liberation Mono",monospace;font-size:7.5pt;letter-spacing:.14em;color:#7A7565}}
"""


def doc(title: str, body: str, extra: str = "") -> str:
    return (f'<!doctype html><meta charset="utf-8"><title>{html.escape(title)}</title>'
            f"<style>{CSS}{extra}</style>{body}")


def mast(eyebrow: str, title: str, sub: str) -> str:
    return (f'<div class="mast"><div class="eyebrow">{eyebrow}</div><h1>{title}</h1>'
            f'<p class="sub">{sub}</p></div>')


FOOT = ('<div class="foot">The Bureau of Minor Achievements &middot; '
        'Office Awards Kit</div>')


# ---------------------------------------------------------------- start here
START = doc("Start Here", mast(
    "Office Awards Kit", "Start here.",
    "A complete awards ceremony in an envelope. Ten minutes of setup, twenty minutes on "
    "the day, and a room full of people who feel seen.") + f"""
<h2>What's in the box</h2>
<table>
  <tr><th>File</th><th>What it's for</th></tr>
  <tr><td><b>AwardsMaker.html</b></td><td>Open it in any browser. Pick an award, type a
    name, print. 38 awards. Works offline — nothing is uploaded anywhere.</td></tr>
  <tr><td><b>Hosts-Script.pdf</b></td><td>What to actually say, word for word, with
    timings. Read it off the page if you want to.</td></tr>
  <tr><td><b>Ballot.pdf</b></td><td>Nomination sheet. Print one per person and let the
    office decide who gets what.</td></tr>
  <tr><td><b>Name-Tents.pdf</b></td><td>Fold-over table tents, four to a sheet.</td></tr>
  <tr><td><b>Announcement.pdf</b></td><td>Three emails: announce it, remind people, follow
    up afterwards. Copy and paste.</td></tr>
  <tr><td><b>certificates/</b></td><td>All 38 as print-ready images, if you'd rather skip
    the maker and print directly.</td></tr>
</table>

<h2>The ten-minute version</h2>
<ol>
  <li><b>Send the announcement email</b> (Announcement.pdf, email 1). Do this a week out.</li>
  <li><b>Print the ballots</b> and leave a stack in the kitchen, or paste the list into a
    form. Give people three days.</li>
  <li><b>Open AwardsMaker.html</b>, click <b>Whole team</b>, paste your names in the order
    the awards should be handed out, and print.</li>
  <li><b>Skim the host's script</b> once. Don't rehearse it. It reads better slightly
    under-prepared.</li>
  <li><b>Run it.</b> Twenty minutes, standing up, at the end of a Friday.</li>
</ol>

<h2>Three things that decide whether this lands</h2>
<h3>Everybody gets one</h3>
<p>The fastest way to ruin this is to give awards to five people in a team of twelve. The
seven without one will notice before the second award is read out. There are 38 in here for
exactly this reason — print one for every single person.</p>

<h3>Read the citation, don't summarise it</h3>
<p>The small print under the name is where the joke actually is. Read it out in full, in a
flat voice, as though you're reading a legal finding. Do not add "because, you know, he's
always late" afterwards. Explaining it kills it.</p>

<h3>Punch sideways, never down</h3>
<p>Awards about someone's habits are funny. Awards about someone's performance are a
disciplinary meeting with a certificate. Skip anyone having a hard year, and never give a
negative award to the most junior person in the room.</p>
{FOOT}""")


# ---------------------------------------------------------------- host script
SCRIPT = doc("Host's Script", mast(
    "Office Awards Kit", "The host's script.",
    "Twenty minutes, start to finish. Square brackets are yours to fill in. Everything else "
    "can be read exactly as written — it's built to survive being read off the page.") + f"""
<h2>Before you stand up</h2>
<ul>
  <li>Certificates stacked <b>in running order</b>, face down. Nothing kills momentum like
    shuffling paper.</li>
  <li>Know your <b>first sentence</b> by heart. Only the first one. After that the room is
    with you.</li>
  <li><b>Stand up.</b> Sitting down turns a ceremony back into a meeting.</li>
  <li>Have <b>somebody hand them over</b> while you read. Two people is a ceremony; one
    person is an announcement.</li>
</ul>

<h2>1 · Opening <span class="t">— 60 seconds</span></h2>
<div class="say"><b>Say this</b>
Right — before anyone escapes. Every year this company hands out awards for revenue, and
targets, and quarterly performance. Nobody ever gets an award for the things they're
<i>actually</i> known for. So we fixed that.<br><br>
The Bureau of Minor Achievements has reviewed the year. Its findings are final and cannot
be appealed.</div>
<p class="tip">Then pick up the first certificate immediately. Don't pause for laughs — if
they come, they'll come over the top of you, which is what you want.</p>

<h2>2 · Each award <span class="t">— 40 seconds each</span></h2>
<p>Same four beats every time. The rhythm is what makes it feel like an event rather than a
list.</p>
<table>
  <tr><th>Beat</th><th>What you do</th></tr>
  <tr><td class="t">1. Department</td><td>Read the department name first, deadpan.
    <i>"From the Office of Elastic Timekeeping…"</i></td></tr>
  <tr><td class="t">2. Award</td><td>Read the title. <i>"…the Certificate of Approximate
    Punctuality."</i></td></tr>
  <tr><td class="t">3. Citation</td><td>Read the small print in full. This is the joke.
    Flat voice. No editorialising.</td></tr>
  <tr><td class="t">4. Name</td><td>Name last, always. <i>"Awarded to — Marcus."</i>
    Hand it over, shake hands, move on.</td></tr>
</table>
<p class="tip">Name last. Every time. If you open with the name, everyone watches them
instead of listening, and the citation lands on nobody.</p>

<h2>3 · The three you plan for</h2>
<h3>The one who isn't there</h3>
<div class="say"><b>Say this</b>
[Name] can't be with us, which — given the award — is thematically perfect.</div>

<h3>The one who wants to say something</h3>
<p>Let them, but cap it. Hand the certificate over <i>while</i> they're talking; it signals
the segment is closing without you having to say so.</p>

<h3>The one that lands wrong</h3>
<p>It happens once. Don't explain it and don't apologise twice.</p>
<div class="say"><b>Say this</b>
That one's on the Bureau, not on me. Moving swiftly.</div>

<h2>4 · The last award</h2>
<p>Save a good one for last — the person the whole room likes, or the one with the biggest
laugh. Never end on a flat one.</p>

<h2>5 · Closing <span class="t">— 30 seconds</span></h2>
<div class="say"><b>Say this</b>
That's the lot. Nobody asked for these, none of them mean anything, and I fully expect to
see at least three of them still stuck to a monitor in March.<br><br>
Thanks for a [year / quarter / genuinely strange nine months]. Go home.</div>

<h2>Timing</h2>
<table>
  <tr><th>Team size</th><th>Runs for</th><th>Note</th></tr>
  <tr><td>Up to 10</td><td class="t">~9 min</td><td>Do every person. No exceptions.</td></tr>
  <tr><td>10–25</td><td class="t">~18 min</td><td>Still do everyone. Keep the pace up.</td></tr>
  <tr><td>25–40</td><td class="t">~28 min</td><td>Split by team, two hosts, halfway swap.</td></tr>
  <tr><td>40+</td><td class="t">—</td><td>Per-team ceremonies. One long one loses the room.</td></tr>
</table>
{FOOT}""")


# ---------------------------------------------------------------- ballot
BALLOT_CSS = """
.slot{border:.9pt solid #17150F;padding:11pt 13pt;margin-top:9pt}
.slot .q{font-family:"Liberation Mono",monospace;font-size:8pt;letter-spacing:.13em;
  text-transform:uppercase;color:#B4321F}
.line{border-bottom:.6pt solid #8E8877;height:20pt;margin-top:7pt}
.two{display:grid;grid-template-columns:1fr 1fr;gap:9pt}
"""

BALLOT = doc("Nomination Ballot", mast(
    "Form 3A — Nomination", "Nomination ballot.",
    "One per person. Fold once and put it in the box by the kettle. Nominations close "
    "[date]. The Bureau's decisions are final and mildly arbitrary.") + f"""
<div class="two">
  <div class="slot"><div class="q">Most likely to reply "will do" and not</div><div class="line"></div></div>
  <div class="slot"><div class="q">Best snack contribution</div><div class="line"></div></div>
  <div class="slot"><div class="q">Loudest keyboard</div><div class="line"></div></div>
  <div class="slot"><div class="q">Camera permanently off</div><div class="line"></div></div>
  <div class="slot"><div class="q">Most calendar chaos</div><div class="line"></div></div>
  <div class="slot"><div class="q">Fixes the printer</div><div class="line"></div></div>
  <div class="slot"><div class="q">Best under actual pressure</div><div class="line"></div></div>
  <div class="slot"><div class="q">Worst offender: meetings that were emails</div><div class="line"></div></div>
</div>

<div class="slot" style="margin-top:13pt">
  <div class="q">Invent an award. Who, and what for?</div>
  <div class="line"></div><div class="line"></div>
</div>

<div class="slot">
  <div class="q">Anyone who should be left out this year? (No reason needed.)</div>
  <div class="line"></div>
</div>

<p class="tip">Ballots are anonymous. That last question is real — if someone is having a
rough year, say so here and the Bureau will quietly skip them.</p>
{FOOT}""", BALLOT_CSS)


# ---------------------------------------------------------------- name tents
TENT_CSS = """
@page{size:Letter portrait;margin:0.4in}
body{font-size:10pt}
.tent{height:2.3in;border:.6pt dashed #A9A392;display:grid;grid-template-rows:1fr 1fr;
  margin-bottom:.12in}
.half{display:flex;align-items:center;justify-content:center;text-align:center;padding:8pt}
.half.up{transform:rotate(180deg);border-bottom:.9pt solid #B4321F}
.nm{font-size:21pt;font-weight:700}
.rl{font-family:"Liberation Mono",monospace;font-size:7.5pt;letter-spacing:.18em;
  text-transform:uppercase;color:#B4321F;margin-top:5pt}
"""

TENTS = doc("Name Tents", mast(
    "Office Awards Kit", "Table name tents.",
    "Four per sheet. Cut along the dashes, fold along the red line, and it stands up on "
    "its own. Write the name in, or type it in the maker first.") +
    ("".join("""
<div class="tent">
  <div class="half up"><div><div class="nm">&nbsp;</div><div class="rl">Bureau of Minor Achievements</div></div></div>
  <div class="half"><div><div class="nm">&nbsp;</div><div class="rl">Bureau of Minor Achievements</div></div></div>
</div>""" for _ in range(4))) + FOOT, TENT_CSS)


# ---------------------------------------------------------------- emails
EMAILS = doc("Announcement Emails", mast(
    "Office Awards Kit", "The three emails.",
    "Copy, paste, replace the brackets. Written to sound like a person, because an "
    "announcement that reads like HR gets the participation of one.") + f"""
<h2>Email 1 · A week out</h2>
<p><b>Subject:</b> Nominations are open, and they are not serious</p>
<div class="say">
Team —<br><br>
We're doing awards this year. Not the real kind. There will be a Certificate of Approximate
Punctuality and somebody is going to receive it.<br><br>
Ballots are in the kitchen / at [link]. Nominate whoever you like, for whatever you like.
Nominations close [day] at [time].<br><br>
Ceremony is [date] at [time] in [place]. It takes twenty minutes and there will be [drinks
/ cake / nothing, just this].<br><br>
[Your name]
</div>

<h2>Email 2 · Two days before nominations close</h2>
<p><b>Subject:</b> Six of you have nominated. There are [N] of us.</p>
<div class="say">
A reminder that nominations close [day].<br><br>
So far the leading category is "loudest keyboard" and the results are, frankly, not close.
If you have opinions — and you do — the ballots are [where].<br><br>
[Your name]
</div>
<p class="tip">This one does most of the work. Naming a real, funny early result makes it
feel already underway.</p>

<h2>Email 3 · The morning after</h2>
<p><b>Subject:</b> The findings of the Bureau are final</p>
<div class="say">
Thanks for yesterday — that was genuinely good fun.<br><br>
Photos are [link]. Certificates are yours to keep, frame, or quietly recycle. The Bureau
notes that [name]'s acceptance speech ran considerably over.<br><br>
Same time next year.<br><br>
[Your name]
</div>

<h2>If you're remote</h2>
<ul>
  <li>Post the certificate image in the channel <b>as you read each one</b>. The reveal is
    the whole mechanic.</li>
  <li>Ask people to <b>put reactions on the award, not the person</b> — it keeps the thread
    readable.</li>
  <li>Mail the paper copies afterwards. It costs almost nothing and it's the part people
    remember.</li>
</ul>
{FOOT}""")


DOCS = [("Start-Here", START), ("Hosts-Script", SCRIPT), ("Ballot", BALLOT),
        ("Name-Tents", TENTS), ("Announcement", EMAILS)]


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out = pathlib.Path(sys.argv[1]).resolve()  # Chrome needs an absolute file:// URI
    out.mkdir(parents=True, exist_ok=True)
    chrome = g.find_chrome()

    for name, content in DOCS:
        src = out / f"{name}.html"
        src.write_text(content, encoding="utf-8")
        subprocess.run(
            [chrome, "--headless", "--disable-gpu", "--no-sandbox",
             "--virtual-time-budget=3000", "--no-pdf-header-footer",
             f"--print-to-pdf={out / (name + '.pdf')}", src.as_uri()],
            check=True, capture_output=True)
        src.unlink()  # the PDF is the deliverable; the HTML was scaffolding
        kb = (out / f"{name}.pdf").stat().st_size / 1024
        print(f"  {name + '.pdf':<22} {kb:6.0f} KB")

    print(f"\n{len(DOCS)} documents -> {out}")


if __name__ == "__main__":
    main()
