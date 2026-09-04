# Etsy listing #3 — End of Year Classroom Awards

**Status: built and ready to publish — except the price.**

| | |
|---|---|
| 12 classroom certificates | ✅ `design/certs_school.py` → `bma-s-*.png` |
| Classroom documents | ✅ Start Here, Teacher's Script, Blank Certificate |
| The packaged download | ✅ `python3 kit/build_kit.py --school` → **2.8 MB** |
| Listing images | ✅ `kit/listing/kit-s1…s4` |
| Listing copy | ✅ Below |
| Price | ❌ **Waiting on the live grid.** See below. |

Cohorts 1–3 are in `kit/Office-Awards-Kit.zip`; the classroom set is deliberately **not**,
because it's a different product for a different buyer. The two kits share no certificates
and each ships its own Awards Maker carrying only its own designs — a teacher scrolling past
"Permanent Audio Only" is a worse product, not a bigger one.

---

## Why this cohort, and why it's third

`playbooks/etsy-market-fit.md` ranks teachers third of six expansions: a lower price band
than office ($3–20 against $6–12 for party awards), but **repeat customers** and an enormous
population. It's also the expansion that most obviously reuses what exists — same renderer,
same frame, same voice.

It does **not** break the no-new-SKU rule. This is more listings of a product that already
exists, which is the thing that actually scales an Etsy shop. No supplier, no new format.

## The one rule that's different here

These go to children, in front of their parents.

Every award is about a **situation** — a habit, a running joke the class already shares —
never about ability, effort, behavior or appearance. Nothing here can read as a consolation
prize, and nothing rewards a child for being worse at something than everyone else. The test
for any addition: *would you hand it to a nine-year-old in front of their family?*

That constraint is written into the docstring of `design/certs_school.py` so it survives
whoever edits it next.

## Title

```
Classroom Awards Printable | 12 End of Year Student Certificates | Funny Class Superlatives | Instant Download
```

109 characters. Front-loaded with **classroom awards**; "end of year" and "last day of
school" are the seasonal phrases that carry intent in May and June.

## Tags — 13, none over 20 characters, zero overlap with listings #1 and #2

```
classroom awards · end of year awards · student awards · teacher printable · class superlatives · last day of school · student certificate · classroom printable · elementary awards · teacher gift idea · kids awards · school year end · funny class awards
```

Checked against both the office and Christmas tag sets. No string appears twice across the
three listings — if two listings share a primary keyword, Etsy buries one of them.

## Description

> **Twelve awards for the last day of school. Print them, sign them, hand them out.**
>
> Every class has the child who knows an unreasonable amount about one specific subject, the
> one who asks the question everybody else was thinking, and the one whose pencil has
> achieved a kind of independent life. None of that fits on a standard certificate.
>
> The Bureau of Minor Achievements issues official recognition for things that don't deserve
> any. The Certificate of Extremely Specific Expertise, for a depth of knowledge on a single
> topic exceeding that of every adult in the building. The Certificate of Recurring Pencil
> Loss. The Certificate of Unprompted Assistance, for noticing someone needed help before
> anyone said so, and not mentioning it afterwards.
>
> Properly typeset documents — guilloche border, embossed-look seal, serial number, a
> registrar's signature line — that happen to certify something gently absurd. The joke works
> because the paperwork refuses to admit there is one.
>
> **WHAT'S INCLUDED**
>
> ✦ **12 award certificates** — one for every recognizable character in a classroom
> ✦ **The Awards Maker** — open one file in your browser, type the names, press print. No
>   account, no software, no subscription. Works with the internet switched off.
> ✦ **A blank certificate** — for the award only you and your class would understand
>
> **WRITTEN TO BE SAFE TO HAND OUT**
>
> Every award is about a situation, never about a child's ability, effort or behavior.
> Nothing here is a consolation prize and nothing singles anybody out. They're meant to be
> read aloud, in front of parents, without anybody's stomach dropping.
>
> **HOW IT WORKS**
>
> 1. Download instantly after checkout
> 2. Open AwardsMaker.html in any browser
> 3. Type your class list, print the lot
>
> Print at home or in the staff room on plain paper or card. Yours to keep and reuse every
> year — rewrite the wording to suit your own class.
>
> **A note on the format.** The Awards Maker is a single HTML file — you open it in Chrome,
> Safari or Edge like a web page. There is nothing to install, no Canva account, and no
> subscription. Every certificate is also included as a ready-to-print image if you'd rather
> skip the maker entirely.
>
> **PLEASE NOTE**
>
> This is a digital download. No physical item is shipped. Because files can't be returned,
> digital purchases aren't refundable — but if anything doesn't open or print properly,
> message me and I'll sort it out the same day.

## Settings

Digital, automatic renewal, **Paper & Party Supplies → Paper → Stationery**, personalization
off, no production partner. Same as listings #1 and #2.

**File to upload:** `kit/Classroom-Awards-Kit.zip` — 2.8 MB, well inside Etsy's 20 MB cap.
Build it with `python3 kit/build_kit.py --school`.

## Listing images — `kit/listing/`

Upload in this order. Build with `python3 kit/build_listing_images.py --school`.

| # | File | Job |
|---|---|---|
| 1 | `kit-s1-hero.png` | Printed certificates on a desk with **DIGITAL DOWNLOAD** on the image |
| 2 | `kit-s3-maker.png` | The maker. The thing no competitor has — show it before the count |
| 3 | `kit-s2-grid.png` | All 12 at once, titles legible at full size |
| 4 | `kit-s4-promise.png` | Instant, offline, printable — and *safe to read out loud* |

## Price — decide it against the live grid, not this file

The educational band runs **$3–20** and skews low. Twelve certificates is fewer than the
office kit's thirty-eight, so this cannot carry the same price on count alone.

**I'm not setting a number here.** The office listing already has one provisional price
waiting on live-grid data; adding a second guess compounds the error. When you check
`funny teacher awards printable` — one of the four searches already on your list — read the
top row's price and file count, and price this against that.

What argues for the top of the band is the **teacher's script**, which is now in the zip:
what to say for each award, in a classroom, in front of parents, including the five things
that go wrong. That's the same thing that makes the office kit worth more than a folder of
PNGs — so lead the listing with it, not with the number twelve.

## Timing

**Not urgent, and that's the point.** End-of-year listings sell in May and June. Seasonal
printables need 6–8 weeks to index, so this wants to be live around **March**. Publishing it
now costs nothing and gains indexing time, but it must not delay the Christmas listing, which
is time-critical and ready.

Order: Christmas this week → office refresh → this, whenever there's a spare day.

## What's actually in the download

| File | What it's for |
|---|---|
| `AwardsMaker.html` | Type the names, press print. 12 designs, offline, no account |
| `Start-Here.pdf` | What's in the folder, and the ten-minute path to the last day |
| `Teachers-Script.pdf` | **The differentiator.** What to say for each award, in front of parents |
| `Blank-Certificate.pdf` | For the award only this class would understand |
| `certificates/` | All 12 as ready-to-print 300dpi images |

The teacher's script is the product, for the same reason the host's script is in the office
kit. Anyone can sell twelve PNGs. The buyer's real problem is standing at the front on the
last day and reading something out loud that lands as warm rather than as a joke at a child's
expense — including the five things that go wrong, which the script covers by name.

## The only thing left

**A price.** Everything else is built. Don't guess it — read the top row of
`funny teacher awards printable`, which is already on your list of four searches, and price
against what's actually there.
