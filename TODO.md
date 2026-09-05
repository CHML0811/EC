# TODO — in order

Everything below is either **yours** (needs an account, a card, or your identity) or
**Cursor's** (code and copy). They're interleaved because the order matters more than the
split: nothing Cursor builds earns anything until the listings are live.

Run `python3 verify.py` before and after any change. 15 checks, exits non-zero on failure.

**Legend:** 🙋 you only · 🤖 give to Cursor · ⛔ blocked, and by what

---

## Now — this week

### 1. 🙋 Create the Etsy seller account — ~15 min
[etsy.com/sell](https://www.etsy.com/sell). Needs your ID and bank details, which is why
nobody else can do it.

Shop name: **BureauOfMinorAchievements**. If it's taken, drop a word rather than adding
numbers — a number reads as spam to buyers.

> **This is the only thing blocking revenue.** Three listings are written and two are fully
> packaged. Every other task on this page is worth less than this one.

### 2. 🙋 Publish listing #1 — the Office Awards Kit — ~20 min
Open **`store/etsy-launch-console.html`** in a browser, tab **1 · Office**, and work down it
beside the Etsy tab. Nine steps, every field with a copy button.

- Build the file first: `python3 kit/build_kit.py` → `kit/Office-Awards-Kit.zip` (8.2 MB)
- Type: **Digital** · Personalization: **off** · Quantity: **999**
- Price **$14.99** — but see task 4 before you commit to it

**Done when:** the listing is live and you can find it in your shop.

### 3. 🙋 Publish listing #2 — Christmas — ~1 hour, same week
Console tab **2 · Christmas**. Same zip, different title, 13 different tags, one new hero
image. Etsy ranks listings, not shops, so this is a second chance to be found on searches
listing #1 doesn't target.

**Timing is the whole point.** Seasonal printables need 6–8 weeks to index and office parties
are booked through November. Mid-October is the last responsible date, not the target.

**Done when:** both listings are live and you've pinned each one to Pinterest the same day —
one vertical pin using the exact title keyword, then three variants. No ads.

### 4. 🙋 Send back four numbers from the live Etsy grid — ~10 min
This unblocks three separate decisions and I still don't have it. Search each of these and
report what you see:

- `office party awards printable`
- `christmas office awards printable`
- `funny teacher awards printable`
- `bridal shower awards printable`

For each, four things:

| # | What to look for | What it decides |
|---|---|---|
| 1 | Which listings carry a **Bestseller** badge, and what they are | What actually sells here |
| 2 | The **price** of rows 1–3 | Whether $14.99 holds or drops to $9.99 |
| 3 | **Review counts** on the top 3 | Reviews ≈ 5–10% of sales, so this is the ceiling |
| 4 | **Certificate count** per bundle, and Canva vs PDF | Whether 38 is competitive |

**Done when:** those numbers exist somewhere I can read them. Then the office price, the
classroom price and the bridal palette all get set against real listings instead of averages.

---

## Next — once the listings are live

### 5. 🙋 Downgrade Shopify — ~2 min
Advanced $399 → Basic $39. **Saves $360 every month.** Nothing in this project uses an
Advanced feature. This is the highest-value two minutes on the page.

### 6. 🙋 Finish the Shopify store — ~15 min
The catalog is already there: 17 products with images and priced variants, About and FAQ,
four collections, both menus. All **DRAFT**. Three things need you:

1. **Policies.** Paste the four from `store/policies-and-pages.md` into Settings → Policies.
   (The connector's token lacks `write_legal_policies`. Alternatively create a custom app
   token and run `SHOPIFY_SUPPORT_EMAIL=you@real.com python3 store/upload_to_shopify.py
   --policies --execute`.)
2. **Digital delivery.** Install the free first-party **Digital Downloads** app and attach
   `kit/Office-Awards-Kit.zip` to the kit product. ⚠️ **Until this is done, activating that
   product means a buyer pays and receives nothing.**
3. **Rename the shop.** It is still called "My Store" in Settings → Store details. There is
   no API for this.

Also: 8 leftover DRAFT products from the archived "Deadpan Goods" direction (inflatable shark
suit, camo shorts, window silhouettes) are still in the catalog. Invisible to customers.
Delete them when convenient.

### 7. ⛔🤖 Set the two open prices — blocked by task 4
Office is provisional at $14.99; classroom has no price at all. Both are deliberate.

```
Read marketing/etsy-office-awards-kit.md and marketing/etsy-teacher-awards-kit.md, then
set both prices against the live-grid numbers I'm pasting below.

[paste the four searches' results here]

Rules: if the top organic row for office party awards is $5–8 with 400+ reviews, drop the
office kit to $9.99 — the premium needs a visible reason we don't have yet. If it's $15–25
Canva bundles, hold $14.99 or go to $18.

Update the price in the marketing doc, then run python3 store/build_launch_console.py so
the console picks it up, then python3 verify.py.

Do not invent a number for anything the grid doesn't cover — say so instead.
```

---

## Then — growth, in value order

### 8. ⛔🤖 Bridal shower cohort — blocked by task 4 (palette)
`playbooks/etsy-market-fit.md` ranks this highest of six expansions: wedding is Etsy's top
price band ($15–50) and the buyer is actively looking to spend. **The palette decision needs
the live grid** — cream and oxblood is right for an office and wrong for a shower.

```
Read playbooks/etsy-market-fit.md and marketing/etsy-teacher-awards-kit.md, then build a
bridal shower cohort exactly the way the classroom one was built:

1. 12 certificates in design/certs_bridal.py, following design/certs_school.py.
2. A "bridal" entry in the KITS dict in kit/build_kit.py, with its own documents
   (build_school_documents.py is the pattern — a host's script for a shower, not an office).
3. A bridal variant in kit/build_listing_images.py.
4. Listing copy in marketing/etsy-bridal-awards-kit.md.
5. A "bridal" entry in LISTINGS in store/build_launch_console.py.

IMPORTANT — the palette is different. The colors are five constants at the top of
design/generate_certificates.py and the frame is CSS. Give this cohort its own visual world
while keeping the deadpan citations.

Rules from AGENTS.md apply: US English, exactly 13 tags, every tag 20 characters or fewer,
no tag shared with any existing listing, no invented numbers, no invented price.

Cohort selection is manifest-driven — do not go back to globbing design/out.
Run python3 verify.py when you're done.
```

### 9. 🤖 Nurse / unit awards cohort
Same machinery, and `etsy-market-fit.md` flags it as **less competitive** than the others.
Same prompt as task 8 with the audience swapped — the office palette is right for this one,
so no palette work.

### 10. 🤖 The marketing video
Read `marketing/video-playbook.md` first — it has the diagnosis of why the last one came out
badly and the exact Grok prompts.

Three things matter more than the rest:

1. **The best video for this product uses no AI at all.** Screen-record the Awards Maker:
   paste ten names, press print, watch ten certificates appear. That's the #1 performing hook
   type by definition, and it has zero uncanny-valley risk.
2. **In Grok, image-to-video only, never text-to-video**, starting from a real PNG in this
   repo. Text-to-video melts typography and this product *is* typography.
3. **Ship ten hooks, not one video.** That's the only real advantage AI gives you. All ten
   are written out in the playbook.

Judge on **3-second retention**, not likes. Under 50% kill it, over 70% make five more.

### 11. ⛔🙋 Printify — blocked until the physical line is worth starting
Not needed for any digital listing. `store/printify-setup-spec.md` has the exact blank,
provider, sizes and prices when you get there.

⚠️ **Bulk shipping math is unverified.** The departmental tiers on the storefront assume one
parcel; Printify bills per item. Check their calculator before promoting those tiers.

---

## Standing orders for Cursor

Paste this once at the start of a session:

```
Read AGENTS.md, then TODO.md. Tell me which task you're picking up and why, then do it.

Non-negotiable: never invent a number or a price. Two prices are deliberately unset pending
live Etsy data — leave them unset and say so rather than guessing.

Buyer-facing copy lives in marketing/*.md only. store/etsy-launch-console.html is generated;
edit the markdown and run python3 store/build_launch_console.py instead of touching the HTML.

Cohorts are named from manifests in the KITS dict in kit/build_kit.py, never globbed.

Run python3 verify.py before you start and before you tell me you're done. 15 checks.
```

### When something breaks

```
Run python3 verify.py --full and report the result.

If anything fails, fix only what failed and re-run until it passes. Do not refactor, do not
"improve" any copy, and do not touch a design — this is a check, not a cleanup.
Show me the final output.
```

### If nothing sells in 30 days

```
30 days, no sales. Before changing anything, diagnose in this order:

1. Is the listing getting IMPRESSIONS? (Etsy Stats → Search)
   - No impressions       = the title/tags don't match how people search. Rewrite the title.
   - Impressions, no clicks = image 1 is losing the grid. Remake it.
   - Clicks, no sales      = the description or price. Fix in that order.

2. Do NOT cut the price first. Price is almost never why a new digital listing fails —
   being unfindable is.

Tell me which of the three it is, with the numbers you used, then fix that one thing only.
```

---

## What is already done, so nobody rebuilds it

| | |
|---|---|
| Certificates | 50 designs across 4 cohorts, 2400×3000 @ 300dpi |
| Listing images | 96 mockups + 82 crops + 9 kit images |
| Office Awards Kit | maker + 5 PDFs + 38 certificates, 8.2 MB |
| Classroom Awards Kit | maker + 3 PDFs + 12 certificates, 2.8 MB |
| Copy | 3 kit listings + 16 print listings, all inside Etsy's limits |
| Launch console | All three listings, generated from the docs, drift-checked |
| Shopify | 17 products, 2 pages, 4 collections, both menus — all draft |
| Storefront | `site/index.html`, catalog built from the manifests |

**Resist the urge to build more.** The bottleneck is not work — it's an Etsy account.
