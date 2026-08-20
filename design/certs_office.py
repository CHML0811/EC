#!/usr/bin/env python3
"""
Cohort 3 — the office awards ceremony.

Written for the Office Awards Kit rather than for single-print listings. An awards
ceremony needs enough categories that everyone in the room gets one and nobody feels
singled out, so these cover the recognisable office archetypes rather than occasions.

    python3 design/certs_office.py

Reuses the cohort-1 renderer. Output: design/out/bma-o-*.png
"""

import json
import subprocess

import generate_certificates as g

CERTS = [
    {
        "slug": "o-punctuality",
        "pattern": "recipient",
        "title": "Certificate of Approximate Punctuality",
        "subject": "HABITUAL LATENESS",
        "department": "Office of Elastic Timekeeping",
        "citation": "for arriving at 9:14 every morning with the consistency of a scheduled "
                    "service, and for a different and compelling reason each time.",
        "seal": "ELASTIC TIMEKEEPING",
        "ref": "BMA-2026-0901-T",
    },
    {
        "slug": "o-email-meeting",
        "pattern": "occasion",
        "title": "Certificate of Meetings That Were Emails",
        "subject": "THIRTY MINUTES",
        "department": "Department of Recoverable Time",
        "citation": "for convening nine people to communicate a single sentence that would "
                    "have survived transmission in written form.",
        "seal": "RECOVERABLE TIME",
        "ref": "BMA-2026-0902-M",
    },
    {
        "slug": "o-camera-off",
        "pattern": "recipient",
        "title": "Certificate of Permanent Audio Only",
        "subject": "CAMERA STATUS: OFF",
        "department": "Bureau of Unverified Presence",
        "citation": "for two years of attendance confirmed by voice alone, and for connection "
                    "difficulties of remarkable and consistent specificity.",
        "seal": "UNVERIFIED PRESENCE",
        "ref": "BMA-2026-0903-C",
    },
    {
        "slug": "o-unmute",
        "pattern": "recipient",
        "title": "Certificate of Delayed Unmuting",
        "subject": "YOU'RE ON MUTE",
        "department": "Division of Silent Contribution",
        "citation": "for delivering the first four seconds of every observation directly into "
                    "a muted microphone. Without fail. Without learning.",
        "seal": "SILENT CONTRIBUTION",
        "ref": "BMA-2026-0904-U",
    },
    {
        "slug": "o-reply-all",
        "pattern": "recipient",
        "title": "Certificate of Reply All",
        "subject": "DISTRIBUTION: EVERYONE",
        "department": "Office of Unnecessary Inclusion",
        "citation": "for informing four hundred colleagues of a lunch preference, and for the "
                    "subsequent apology, sent by the same method.",
        "seal": "UNNECESSARY INCLUSION",
        "ref": "BMA-2026-0905-R",
    },
    {
        "slug": "o-coffee",
        "pattern": "recipient",
        "title": "Certificate of Caffeine Dependency",
        "subject": "SUSTAINED INTAKE",
        "department": "Bureau of Chemical Support",
        "citation": "for a personality that does not commence until the second cup, and for "
                    "treating the office machine as a life support system.",
        "seal": "CHEMICAL SUPPORT",
        "ref": "BMA-2026-0906-K",
    },
    {
        "slug": "o-snacks",
        "pattern": "recipient",
        "title": "Certificate of Snack Provision",
        "subject": "UNPAID, UNPROMPTED",
        "department": "Division of Morale Logistics",
        "citation": "for the unexplained appearance of pastries on difficult mornings, funded "
                    "personally, and never once mentioned by the provider.",
        "seal": "MORALE LOGISTICS",
        "ref": "BMA-2026-0907-S",
    },
    {
        "slug": "o-fridge",
        "pattern": "occasion",
        "title": "Certificate of Refrigerator Archaeology",
        "subject": "CONTENTS UNIDENTIFIED",
        "department": "Office of Deferred Disposal",
        "citation": "for a container of considerable age bearing a date that no longer holds "
                    "meaning, and for the bravery of whoever finally removed it.",
        "seal": "DEFERRED DISPOSAL",
        "ref": "BMA-2026-0908-F",
    },
    {
        "slug": "o-printer",
        "pattern": "recipient",
        "title": "Certificate of Printer Diplomacy",
        "subject": "MECHANICAL WHISPERER",
        "department": "Bureau of Percussive Maintenance",
        "citation": "for restoring function to a device that responds to no one else, by means "
                    "that have never been successfully documented.",
        "seal": "PERCUSSIVE MAINTENANCE",
        "ref": "BMA-2026-0909-P",
    },
    {
        "slug": "o-jargon",
        "pattern": "recipient",
        "title": "Certificate of Advanced Jargon",
        "subject": "SYNERGY ACHIEVED",
        "department": "Department of Circling Back",
        "citation": "for leveraging bandwidth, touching base offline, and taking it away as an "
                    "action item — all within a single unbroken sentence.",
        "seal": "CIRCLING BACK",
        "ref": "BMA-2026-0910-J",
    },
    {
        "slug": "o-spreadsheet",
        "pattern": "recipient",
        "title": "Certificate of Spreadsheet Sorcery",
        "subject": "PIVOT TABLE CLASS",
        "department": "Division of Unreadable Formulas",
        "citation": "for a workbook that runs the department, that exactly one person "
                    "understands, and that must never be opened on a Friday.",
        "seal": "UNREADABLE FORMULAS",
        "ref": "BMA-2026-0911-X",
    },
    {
        "slug": "o-notes",
        "pattern": "occasion",
        "title": "Certificate of Passive Aggression",
        "subject": "KITCHEN CORRESPONDENCE",
        "department": "Office of Anonymous Signage",
        "citation": "for notices affixed to the microwave in a tone of steadily escalating "
                    "politeness, signed only: The Team.",
        "seal": "ANONYMOUS SIGNAGE",
        "ref": "BMA-2026-0912-N",
    },
    {
        "slug": "o-firefighter",
        "pattern": "recipient",
        "title": "Certificate of Crisis Response",
        "subject": "FIRST ON SCENE",
        "department": "Bureau of Predictable Emergencies",
        "citation": "for solving, at 4:55pm on a Friday, a problem that had been raised, "
                    "ignored, and raised again since Tuesday morning.",
        "seal": "PREDICTABLE EMERGENCIES",
        "ref": "BMA-2026-0913-E",
    },
    {
        "slug": "o-notetaker",
        "pattern": "recipient",
        "title": "Certificate of Minutes Taken",
        "subject": "SOLE WITNESS",
        "department": "Office of Institutional Memory",
        "citation": "for maintaining the only written record of what was actually agreed, and "
                    "for producing it whenever anyone claims otherwise.",
        "seal": "INSTITUTIONAL MEMORY",
        "ref": "BMA-2026-0914-W",
    },
    {
        "slug": "o-calendar",
        "pattern": "recipient",
        "title": "Certificate of Calendar Tetris",
        "subject": "FULLY BOOKED",
        "department": "Division of Scheduling Warfare",
        "citation": "for a calendar so densely packed that lunch now appears as a recurring "
                    "conflict, automatically declined.",
        "seal": "SCHEDULING WARFARE",
        "ref": "BMA-2026-0915-D",
    },
    {
        "slug": "o-newhire",
        "pattern": "occasion",
        "title": "Certificate of Successful Onboarding",
        "subject": "PROBATION SURVIVED",
        "department": "Bureau of Gradual Assimilation",
        "citation": "for learning the passwords, the acronyms, and which printer to avoid — "
                    "in that order, over the course of nine months.",
        "seal": "GRADUAL ASSIMILATION",
        "ref": "BMA-2026-0916-O",
    },
    {
        "slug": "o-tenure",
        "pattern": "occasion",
        "title": "Certificate of Extended Service",
        "subject": "STILL HERE",
        "department": "Office of Institutional Furniture",
        "citation": "for outlasting four managers, three restructures and two relocations, "
                    "without displaying a visible reaction to any of them.",
        "seal": "INSTITUTIONAL FURNITURE",
        "ref": "BMA-2026-0917-L",
    },
    {
        "slug": "o-weekend",
        "pattern": "recipient",
        "title": "Certificate of Unrequested Availability",
        "subject": "SENT 23:47, SUNDAY",
        "department": "Department of Boundaries Not Observed",
        "citation": "for correspondence timestamped at hours suggesting either exceptional "
                    "dedication or a situation that should be discussed.",
        "seal": "BOUNDARIES NOT OBSERVED",
        "ref": "BMA-2026-0918-B",
    },
    {
        "slug": "o-typing",
        "pattern": "recipient",
        "title": "Certificate of Percussive Typing",
        "subject": "AUDIBLE FROM RECEPTION",
        "department": "Division of Mechanical Enthusiasm",
        "citation": "for a keyboard technique that conveys tremendous urgency to the entire "
                    "floor, regardless of what is being written.",
        "seal": "MECHANICAL ENTHUSIASM",
        "ref": "BMA-2026-0919-Y",
    },
    {
        "slug": "o-question",
        "pattern": "recipient",
        "title": "Certificate of the Final Question",
        "subject": "ASKED AT 4:58PM",
        "department": "Bureau of Extended Meetings",
        "citation": "for raising, in the closing two minutes, the one consideration that adds "
                    "forty minutes and cannot reasonably be dismissed.",
        "seal": "EXTENDED MEETINGS",
        "ref": "BMA-2026-0920-Q",
    },
    {
        "slug": "o-plant",
        "pattern": "recipient",
        "title": "Certificate of Botanical Stewardship",
        "subject": "SOLE SURVIVOR",
        "department": "Office of Departmental Greenery",
        "citation": "for the continued survival of the one plant, watered by one person, in an "
                    "environment engineered entirely against it.",
        "seal": "DEPARTMENTAL GREENERY",
        "ref": "BMA-2026-0921-G",
    },
    {
        "slug": "o-dresscode",
        "pattern": "recipient",
        "title": "Certificate of Interpretive Dress Code",
        "subject": "BUSINESS ADJACENT",
        "department": "Division of Flexible Standards",
        "citation": "for an interpretation of business casual that has never been formally "
                    "challenged, and at this point never will be.",
        "seal": "FLEXIBLE STANDARDS",
        "ref": "BMA-2026-0922-A",
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
        manifest.append({**c, "file": png.name, "cohort": 3})

    (g.OUT / "manifest-office.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\n{len(CERTS)} office certificates -> {g.OUT}")


if __name__ == "__main__":
    main()
