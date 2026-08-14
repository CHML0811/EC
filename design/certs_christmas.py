#!/usr/bin/env python3
"""
Cohort 2 — Christmas / Secret Santa / office gifting.

Christmas is the real revenue target: Secret Santa and white-elephant exchanges are
peak season for exactly this product. Etsy needs 30-90 days to rank, so these must be
live by early October to be ranked when the money arrives.

    python3 design/certs_christmas.py

Reuses the cohort-1 renderer. Output: design/out/bma-x*.png
"""

import generate_certificates as g

CERTS = [
    {
        "slug": "x-secret-santa",
        "pattern": "occasion",
        "title": "Certificate of Obligatory Festivity",
        "subject": "SECRET SANTA",
        "department": "Office of Mandatory Fun",
        "citation": "for drawing a name at random, spending precisely the agreed limit, "
                    "and feigning surprise with a conviction bordering on the professional.",
        "seal": "MANDATORY FUN",
        "ref": "BMA-2026-1201-S",
    },
    {
        "slug": "x-white-elephant",
        "pattern": "occasion",
        "title": "White Elephant Champion",
        "subject": "UNDISPUTED",
        "department": "Bureau of Strategic Regifting",
        "citation": "for identifying the one desirable item in the pile and taking it "
                    "from a colleague without visible remorse. A tactical masterclass.",
        "seal": "STRATEGIC REGIFTING",
        "ref": "BMA-2026-1202-W",
    },
    {
        "slug": "x-survived-year",
        "pattern": "occasion",
        "title": "Certificate of Surviving Another Year",
        "subject": "ANNUAL RENEWAL",
        "department": "Division of Diminishing Returns",
        "citation": "for remaining employed, largely upright, and only moderately worse "
                    "than at the start of the period under review.",
        "seal": "DIMINISHING RETURNS",
        "ref": "BMA-2026-1203-Y",
    },
    {
        "slug": "x-office-party",
        "pattern": "occasion",
        "title": "Certificate of Attendance",
        "subject": "THE OFFICE PARTY",
        "department": "Office of Mandatory Fun",
        "citation": "for arriving, standing near the food, speaking to three people, "
                    "and leaving at the earliest defensible moment.",
        "seal": "MANDATORY FUN",
        "ref": "BMA-2026-1204-P",
    },
    {
        "slug": "x-okayest-gift",
        "pattern": "recipient",
        "title": "World's Okayest Gift Giver",
        "subject": "CERTIFIED",
        "department": "Division of Adequate Thoughtfulness",
        "citation": "for a gift that was purchased, wrapped, and delivered on time. "
                    "Thoughtfulness was attempted. The receipt has been retained.",
        "seal": "ADEQUATE THOUGHTFULNESS",
        "ref": "BMA-2026-1205-G",
    },
    {
        "slug": "x-mom",
        "pattern": "recipient",
        "title": "Certified Mom",
        "subject": "FULLY ACCREDITED",
        "department": "Office of Unread Advice",
        "citation": "for advice dispensed regardless of demand, a freezer of "
                    "unidentifiable containers, and being right an insufferable amount of the time.",
        "seal": "UNREAD ADVICE",
        "ref": "BMA-2026-1206-M",
    },
    {
        "slug": "x-dad",
        "pattern": "recipient",
        "title": "Certified Dad",
        "subject": "FULLY ACCREDITED",
        "department": "Bureau of Thermostat Enforcement",
        "citation": "for jokes of consistent quality, lights switched off in unoccupied "
                    "rooms, and an encyclopedic knowledge of alternative routes.",
        "seal": "THERMOSTAT ENFORCEMENT",
        "ref": "BMA-2026-1207-D",
    },
    {
        "slug": "x-stocking",
        "pattern": "personalised",
        "title": "Certificate of Marginal Improvement",
        "subject": "YEAR IN REVIEW",
        "department": "Office of Modest Expectations",
        "citation": "for measurable progress in at least one area, offset almost entirely "
                    "by regression in several others. On balance: encouraging.",
        "seal": "MODEST EXPECTATIONS",
        "ref": "BMA-2026-1208-I",
    },
]


def main() -> None:
    g.OUT.mkdir(parents=True, exist_ok=True)
    g.TMP.mkdir(parents=True, exist_ok=True)
    chrome = g.find_chrome()
    import subprocess, json

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
        manifest.append({**c, "file": png.name, "cohort": 2})

    (g.OUT / "manifest-christmas.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\n{len(CERTS)} Christmas certificates -> {g.OUT}")


if __name__ == "__main__":
    main()
