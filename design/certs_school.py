#!/usr/bin/env python3
"""
Cohort 4 — end-of-year classroom awards.

The same machinery aimed at a different buyer. A teacher printing thirty of these at the end
of June has the same problem an office manager has in December: everyone in the room needs
one, and nobody should feel singled out.

That constraint bites harder here than it does in the office set. These go to children, so
every award is about a *situation* — a habit, a running joke, a thing the class already finds
funny — never about ability, effort, behaviour or appearance. Nothing here can be read as a
consolation prize, and nothing rewards a child for being worse at something than the others.
Test for any addition: would you hand it to a nine-year-old in front of their parents?

    python3 design/certs_school.py

Reuses the cohort-1 renderer. Output: design/out/bma-s-*.png
"""

import json
import subprocess

import generate_certificates as g

CERTS = [
    {
        "slug": "s-expertise",
        "pattern": "recipient",
        "title": "Certificate of Extremely Specific Expertise",
        "subject": "ONE SUBJECT, EXHAUSTIVELY",
        "department": "Bureau of Narrow Scholarship",
        "citation": "for a depth of knowledge on a single topic that exceeds that of every "
                    "adult in the building, and for sharing it without being asked.",
        "seal": "NARROW SCHOLARSHIP",
        "ref": "BMA-2026-0601-E",
    },
    {
        "slug": "s-questions",
        "pattern": "recipient",
        "title": "Certificate of Continuous Enquiry",
        "subject": "BUT WHY THOUGH",
        "department": "Office of Unresolved Questions",
        "citation": "for asking the question the rest of the room was also wondering about, "
                    "and for the follow-up question that nobody had prepared for.",
        "seal": "UNRESOLVED QUESTIONS",
        "ref": "BMA-2026-0602-Q",
    },
    {
        "slug": "s-longest-answer",
        "pattern": "recipient",
        "title": "Certificate of the Comprehensive Answer",
        "subject": "IT STARTED IN 1847",
        "department": "Division of Thorough Explanation",
        "citation": "for responding to a question requiring one word with an account that "
                    "began considerably earlier and covered substantially more ground.",
        "seal": "THOROUGH EXPLANATION",
        "ref": "BMA-2026-0603-A",
    },
    {
        "slug": "s-pencil",
        "pattern": "recipient",
        "title": "Certificate of Recurring Pencil Loss",
        "subject": "IT WAS HERE A MINUTE AGO",
        "department": "Office of Vanished Stationery",
        "citation": "for the disappearance of writing implements at a rate that has begun to "
                    "interest the school, and for locating each one eventually.",
        "seal": "VANISHED STATIONERY",
        "ref": "BMA-2026-0604-P",
    },
    {
        "slug": "s-snack",
        "pattern": "recipient",
        "title": "Certificate of Advanced Snack Diplomacy",
        "subject": "AN EVEN TRADE",
        "department": "Bureau of Lunchtime Commerce",
        "citation": "for negotiations conducted daily at the lunch table, and for a trading "
                    "record that has never once ended in an incident.",
        "seal": "LUNCHTIME COMMERCE",
        "ref": "BMA-2026-0605-S",
    },
    {
        "slug": "s-weather",
        "pattern": "recipient",
        "title": "Certificate of Meteorological Commentary",
        "subject": "IT'S RAINING AGAIN",
        "department": "Division of Window Observation",
        "citation": "for continuous reporting on conditions outside, delivered promptly and "
                    "without regard for whether the lesson had finished.",
        "seal": "WINDOW OBSERVATION",
        "ref": "BMA-2026-0606-W",
    },
    {
        "slug": "s-bookmark",
        "pattern": "recipient",
        "title": "Certificate of Steady Bookmark Advancement",
        "subject": "ONE MORE CHAPTER",
        "department": "Office of Deferred Bedtimes",
        "citation": "for reading past the point where reading was supposed to stop, and for "
                    "carrying the same book to places books do not need to go.",
        "seal": "DEFERRED BEDTIMES",
        "ref": "BMA-2026-0607-B",
    },
    {
        "slug": "s-line",
        "pattern": "recipient",
        "title": "Certificate of Distinguished Line Leadership",
        "subject": "AT THE FRONT, AGAIN",
        "department": "Bureau of Orderly Movement",
        "citation": "for arriving at the door before the instruction to line up had finished, "
                    "on every occasion, for an entire academic year.",
        "seal": "ORDERLY MOVEMENT",
        "ref": "BMA-2026-0608-L",
    },
    {
        "slug": "s-handwriting",
        "pattern": "recipient",
        "title": "Certificate of Handwriting Under Pressure",
        "subject": "THE LAST FOUR MINUTES",
        "department": "Division of Terminal Velocity",
        "citation": "for maintaining legibility through the closing stage of every written "
                    "task, at a speed the paper was not designed to accommodate.",
        "seal": "TERMINAL VELOCITY",
        "ref": "BMA-2026-0609-H",
    },
    {
        "slug": "s-kindness",
        "pattern": "recipient",
        "title": "Certificate of Unprompted Assistance",
        "subject": "NOBODY ASKED",
        "department": "Office of Quiet Decency",
        "citation": "for noticing that someone needed help before anyone said so, and for "
                    "not mentioning it afterwards. Repeatedly. Without being told.",
        "seal": "QUIET DECENCY",
        "ref": "BMA-2026-0610-K",
    },
    {
        "slug": "s-fact",
        "pattern": "recipient",
        "title": "Certificate of the Unscheduled Fact",
        "subject": "DID YOU KNOW",
        "department": "Bureau of Interrupting Information",
        "citation": "for the delivery of accurate and genuinely interesting information at "
                    "moments bearing no relationship whatsoever to the lesson in progress.",
        "seal": "INTERRUPTING INFORMATION",
        "ref": "BMA-2026-0611-F",
    },
    {
        "slug": "s-year",
        "pattern": "occasion",
        "title": "Certificate of Completing the Year",
        "subject": "ALL OF IT",
        "department": "Office of Accumulated Days",
        "citation": "for attending, participating, growing measurably taller, and reaching "
                    "the end of the year having made the room better by being in it.",
        "seal": "ACCUMULATED DAYS",
        "ref": "BMA-2026-0612-Y",
    },
]


def main() -> None:
    g.OUT.mkdir(parents=True, exist_ok=True)
    g.TMP.mkdir(parents=True, exist_ok=True)
    chrome = g.find_chrome()

    manifest = []
    for c in CERTS:
        src = g.TMP / f"{c['slug']}.html"
        png = g.OUT / f"bma-{c['slug']}.png"
        src.write_text(g.build_html(c), encoding="utf-8")
        subprocess.run(
            [chrome, "--headless", "--disable-gpu", "--no-sandbox",
             "--hide-scrollbars", "--force-device-scale-factor=1",
             f"--window-size={g.W},{g.H}", f"--screenshot={png}", src.as_uri()],
            check=True, capture_output=True,
        )
        print(f"  {png.name:<34} {png.stat().st_size/1024:8.0f} KB")
        manifest.append({**c, "file": png.name, "cohort": 4})

    (g.OUT / "manifest-school.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\n{len(CERTS)} classroom certificates -> {g.OUT}")


if __name__ == "__main__":
    main()
