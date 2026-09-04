#!/usr/bin/env python3
"""
Build the printable documents that ship with the Classroom Awards Kit.

    python3 kit/build_school_documents.py kit/dist-school

Produces:

  Start-Here.pdf         what's in the folder and the ten-minute path to the last day
  Teachers-Script.pdf    what to say for each award, in a classroom, in front of parents
  Blank-Certificate.pdf  for the award only this class would understand

The teacher's script is the real product, for the same reason the host's script is in the
office kit: anyone can sell twelve PNGs. The buyer's actual problem is standing at the front
on the last day, with parents at the back of the room, reading something out loud that has
to land as warm rather than as a joke at a child's expense.

Shares the stylesheet and helpers with kit/build_documents.py so both kits look like they
came from the same agency.
"""

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent / "design"))

import build_documents as d  # noqa: E402
import generate_certificates as g  # noqa: E402

doc, mast = d.doc, d.mast
INK, RED = g.INK, g.RED

FOOT = ('<div class="foot">The Bureau of Minor Achievements &middot; '
        'Classroom Awards Kit</div>')


# ---------------------------------------------------------------- start here
START = doc("Start Here", mast(
    "Classroom Awards Kit", "Start here.",
    "Twelve awards for the last day of the year. Ten minutes to set up, fifteen minutes to "
    "hand out, and a class that goes home feeling noticed.") + f"""
<h2>What's in the folder</h2>
<table>
  <tr><th>File</th><th>What it's for</th></tr>
  <tr><td><b>AwardsMaker.html</b></td><td>Open it in any browser. Pick an award, type a
    name, press print. No account, no software, works offline.</td></tr>
  <tr><td><b>Teachers-Script.pdf</b></td><td>What to say for each award. Read it off the
    page if you want to.</td></tr>
  <tr><td><b>Blank-Certificate.pdf</b></td><td>For the award only your class would
    understand. There is always one.</td></tr>
  <tr><td><b>certificates/</b></td><td>All twelve as ready-to-print images, if you'd
    rather skip the maker.</td></tr>
</table>

<h2>The ten-minute path</h2>
<ol>
  <li><b>Read the twelve titles</b> and match them to your class. Most will be obvious
    within about four seconds. That's the point of the set.</li>
  <li><b>Anyone left over gets the blank one.</b> The awards a class remembers are usually
    the ones about a thing that only happened in that room.</li>
  <li><b>Type the names into the maker</b> and print. Plain paper is fine; card is better
    if the office has any.</li>
  <li><b>Skim the script once.</b> Not to memorize — just so the order doesn't surprise
    you on the day.</li>
</ol>

<h2>One rule, and it matters more than the rest</h2>
<p>Every award here is about a <b>situation</b> — a habit, a running joke the class already
shares. None of them are about how clever, how quick, how well-behaved or how well-liked a
child is. That isn't squeamishness; it's what makes the set safe to hand out in front of
parents.</p>
<p class="tip">If you write your own on the blank certificate, hold it to the same test:
would you hand this to a nine-year-old with their family watching, and would they still be
pleased about it in September?</p>

<h2>Timing</h2>
<table>
  <tr><th>When</th><th>What</th></tr>
  <tr><td class="t">A week before</td><td>Match awards to names. Print. Ten minutes.</td></tr>
  <tr><td class="t">The morning of</td><td>Stack them in running order, face down.</td></tr>
  <tr><td class="t">On the day</td><td>Fifteen minutes for a class of thirty.</td></tr>
</table>
{FOOT}""")


# ---------------------------------------------------------------- the script
SCRIPT = doc("Teacher's Script", mast(
    "Classroom Awards Kit", "The teacher's script.",
    "Fifteen minutes for a class of thirty. Square brackets are yours to fill in. "
    "Everything else can be read exactly as written.") + f"""
<h2>Before you start</h2>
<ul>
  <li>Certificates <b>in running order</b>, face down. Shuffling paper is what turns a
    ceremony back into admin.</li>
  <li><b>Every child gets one.</b> Not most. If the set doesn't cover someone, the blank
    certificate does — write it the night before, not on the spot.</li>
  <li><b>Save the quietest child for the middle</b>, never last. Last is the loudest
    position in the room and not everyone wants it.</li>
  <li>If parents are in, say the sentence in section 1 out loud. It tells them how to
    listen, which is most of the job.</li>
</ul>

<h2>1 · Opening <span class="t">— 45 seconds</span></h2>
<div class="say"><b>Say this</b>
Before we go — there's one more thing. All year, this class has been handing out awards for
reading, and for effort, and for attendance. Which is fine. But nobody has ever been given
an award for the thing they're <i>actually</i> famous for in this room.<br><br>
So the Bureau of Minor Achievements has reviewed the year. Its findings are final and cannot
be appealed.</div>
<p class="tip">If parents are present, add: <i>"These are all about something the class
finds funny about each other, in a nice way. Nothing in here is about marks."</i> Say it
once, at the start. It stops anyone reading a joke the wrong way.</p>

<h2>2 · Each award <span class="t">— 25 seconds each</span></h2>
<p>Four beats, the same every time. The rhythm is what makes it feel like an occasion
instead of a list being read out.</p>
<table>
  <tr><th>Beat</th><th>What you do</th></tr>
  <tr><td class="t">1. Department</td><td>Read the department, deadpan.
    <i>"From the Office of Vanished Stationery&hellip;"</i></td></tr>
  <tr><td class="t">2. Award</td><td>Read the title. <i>"&hellip;the Certificate of
    Recurring Pencil Loss."</i></td></tr>
  <tr><td class="t">3. Citation</td><td>Read the small print in full, flat. This is the
    joke. Don't explain it and don't add to it.</td></tr>
  <tr><td class="t">4. Name</td><td>Name last, always. <i>"Awarded to &mdash; [name]."</i>
    Hand it over, and move on.</td></tr>
</table>
<p class="tip">Name last, every time. If you open with the name, the room watches the child
instead of listening, and the citation lands on nobody.</p>

<h2>3 · Worked example <span class="t">— read this one as written</span></h2>
<div class="say"><b>Say this</b>
From the Office of Quiet Decency &mdash; the Certificate of Unprompted Assistance.<br><br>
For noticing that someone needed help before anyone said so, and for not mentioning it
afterwards. Repeatedly. Without being told.<br><br>
Awarded to &mdash; [name].</div>
<p class="tip">That one usually gets the biggest reaction of the twelve, and it's worth
placing about two-thirds of the way through.</p>

<h2>4 · The things that go wrong</h2>
<table>
  <tr><th>What happens</th><th>What to do</th></tr>
  <tr><td>A child is <b>absent</b></td><td>Read it anyway, to the room, and say you'll
    give it to them in September. Skipping it is worse — everyone notices.</td></tr>
  <tr><td>Somebody says <b>"that's not fair"</b></td><td>Agree cheerfully. <i>"It isn't.
    The Bureau is famously unfair."</i> Then keep going.</td></tr>
  <tr><td>A joke <b>doesn't land</b></td><td>Don't rescue it. Move to the next name. The
    rhythm carries it and nobody remembers by award four.</td></tr>
  <tr><td>A child looks <b>upset</b></td><td>Stop the bit. <i>"And genuinely — this class
    was better with you in it."</i> Straight, no joke. Then carry on.</td></tr>
  <tr><td>Parents <b>filming</b></td><td>Fine, and it's why the citations avoid anything
    about ability. Nothing here is embarrassing out of context.</td></tr>
</table>

<h2>5 · Closing <span class="t">— 30 seconds</span></h2>
<div class="say"><b>Say this</b>
That's the lot. Everyone in this room got one, because everyone in this room did something
this year that only this room would understand.<br><br>
The Bureau wishes you a restful summer, and reminds you that none of these certificates
are valid anywhere. Go on.</div>
<p class="tip">Then stop talking. Don't add a moral. The last line is the last line.</p>
{FOOT}""")


# ---------------------------------------------------------------- blank cert
BLANK_CSS = f"""
@page{{size:Letter landscape;margin:0}}
body{{font-size:11pt;background:{g.PAPER}}}
.cert{{position:relative;width:11in;height:8.5in;padding:0.9in 1.1in;background:{g.PAPER};
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  text-align:center}}
.seal{{position:absolute;bottom:0.72in;left:50%;transform:translateX(-50%);
  width:1.15in;height:1.15in;opacity:.9}}
.f-out{{position:absolute;inset:0.34in;border:3.4pt solid {INK}}}
.f-in{{position:absolute;inset:0.46in;border:.9pt solid {INK}}}
.cnr{{position:absolute;width:0.30in;height:0.30in;border:2.4pt solid {RED}}}
.tl{{top:0.52in;left:0.52in;border-right:0;border-bottom:0}}
.tr{{top:0.52in;right:0.52in;border-left:0;border-bottom:0}}
.bl{{bottom:0.52in;left:0.52in;border-right:0;border-top:0}}
.br{{bottom:0.52in;right:0.52in;border-left:0;border-top:0}}
.ag{{font-size:13pt;letter-spacing:.42em;color:{RED};text-transform:uppercase}}
.fill{{border-bottom:1.1pt solid {INK};width:7.4in;height:0.46in;margin:0 auto}}
.fill.short{{width:5.2in}}
.hint{{font-family:"Liberation Mono",monospace;font-size:7pt;letter-spacing:.17em;
  text-transform:uppercase;color:#9A9484;margin-top:4pt;max-width:5.6in;
  margin-left:auto;margin-right:auto;line-height:1.5}}
.lbl{{font-size:11.5pt;font-style:italic;color:#5C5749;margin-top:20pt}}
.meta{{position:absolute;bottom:0.85in;left:1.15in;font-family:"Liberation Mono",monospace;
  font-size:7.5pt;letter-spacing:.13em;color:#7A7565;text-align:left}}
.sig{{position:absolute;bottom:0.95in;right:1.15in;width:2.5in;
  border-top:.9pt solid {INK};padding-top:5pt;font-family:"Liberation Mono",monospace;
  font-size:7pt;letter-spacing:.15em;text-transform:uppercase;color:#7A7565}}
"""

BLANK = doc("Blank Certificate", f"""
<div class="cert">
  <div class="f-out"></div><div class="f-in"></div>
  <div class="cnr tl"></div><div class="cnr tr"></div>
  <div class="cnr bl"></div><div class="cnr br"></div>

  <div class="ag">The Bureau of Minor Achievements</div>

  <div class="lbl">hereby issues the</div>
  <div class="fill"></div>
  <div class="hint">Certificate of &mdash; write the award here</div>

  <div class="lbl">to</div>
  <div class="fill short"></div>
  <div class="hint">Name</div>

  <div class="lbl">for</div>
  <div class="fill"></div>
  <div class="fill"></div>
  <div class="hint">The citation &mdash; dry, specific, and about a thing that
    happened rather than about them</div>

  {g.seal_svg("MINOR ACHIEVEMENTS")}

  <div class="meta">REF &nbsp;BMA-____-____<br>ISSUED &nbsp;____________<br>
    STATUS &nbsp;IRREVOCABLE</div>
  <div class="sig">Registrar, B.M.A.</div>
</div>""", BLANK_CSS)


DOCS = [("Start-Here", START), ("Teachers-Script", SCRIPT),
        ("Blank-Certificate", BLANK)]


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    out = pathlib.Path(sys.argv[1]).resolve()   # Chrome needs an absolute file:// URI
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
        src.unlink()   # the PDF is the deliverable; the HTML was scaffolding
        kb = (out / f"{name}.pdf").stat().st_size / 1024
        print(f"  {name + '.pdf':<24} {kb:6.0f} KB")

    print(f"\n{len(DOCS)} classroom documents -> {out}")


if __name__ == "__main__":
    main()
