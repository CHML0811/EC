# Who actually buys on Etsy, and what should we sell them

You spotted that Etsy skews female and asked what the best sellers look like. You're right,
and it changes what we should build next — though not what we should publish first.

> **A limit up front:** Etsy is blocked by this environment's network proxy, so I could not
> open the page you linked. Everything below comes from published category and demographic
> data. **You can see the live bestseller grid and I can't** — there's a short list at the
> bottom of exactly what to look for.

---

## The demographic

| | |
|---|---|
| Female buyers | **58%–80%** depending on source — every source agrees it's a clear majority ([Printful](https://www.printful.com/blog/etsy-statistics), [ElectroIQ](https://electroiq.com/stats/etsy-statistics/)) |
| Largest age group | **25–34** at 28.9% |
| Under 44 | **64.7%** |

So: mostly women, mostly under 45. Your read was correct.

## What actually earns

The top-earning digital categories, with the prices they sustain
([category data](https://mydesigns.io/blog/digital-products-to-sell-on-etsy/), [what sells](https://www.outfy.com/blog/top-selling-digital-products-on-etsy/)):

| Rank | Category | Price band | Note |
|---|---|---|---|
| 1 | Digital planners & organizers | $8–25 | ~95% margin |
| 2 | Printable wall art | $5–15 | High volume, high competition |
| 3 | **Wedding templates & printables** | **$15–50** | **Highest value orders on the platform** |
| 4 | **Business templates** | **$12–40** | B2B buyers |
| 5 | Educational printables for teachers | $3–20 | **Repeat customers** |
| — | **Party award certificates — our niche** | **$4–$12** | **$15–$30 only if huge + editable** |

Two other findings that matter more than the list:

- **Bundles beat single files.** Multi-file packs raise order value and climb the algorithm faster.
- **Specific problem for a defined audience beats generic design.** Every time.
- **Scale is listings, not products.** Sellers at $5K–50K/month run **200–1,000 listings**,
  built over 6–18 months.

---

## Where our product actually sits

**⚠️ Corrected.** I placed the kit in the business-template band ($12–40) by category
reasoning. Against **live listings in our actual niche** that's wrong: party award
certificates cluster at **$6–$12** — $6 for 47 office holiday awards, $6.50 for 24 funny
office awards, $8.25 for 200 Canva awards, $10 for 50 editable Christmas awards. A $30/150
listing exists and has almost no reviews.

$14.99 is above that cluster and defensible *only if the listing visibly shows* the script,
the ballot and the editor. A flat page-one screenshot at $14.99 loses to $6.99 every time.
Price against the live grid, not a category average.

And on your demographic point: **who buys office party supplies?** Office managers, HR, EAs,
team leads. Those roles skew female. The kit is not misaligned with Etsy's buyer — it's
aimed at exactly the person who gets handed "organise something for the team."

**So the product is fine. The problem is that we have one listing.**

The data says revenue comes from *many listings*, and Etsy **ranks listings, not shops**. One
listing is one lottery ticket.

---

## The cheapest expansions, ranked

Our generator makes a new certificate cohort in minutes. Every one of these is the **same
machinery, same file format, different audience** — not a new product line.

| # | Cohort | Category band | Buyer | Cost to build |
|---|---|---|---|---|
| 1 | **Christmas office party** | Business $12–40 | Office manager | **Almost zero — already built** |
| 2 | **Bridal shower games & awards** | **Wedding $15–50** | Bride, maid of honour | ~2 hours |
| 3 | **Teacher end-of-year awards** | Educational $3–20, **repeat** | Teachers (majority female) | ~2 hours |
| 4 | Baby shower awards | Wedding-adjacent $15–50 | Mum-to-be, friend | ~2 hours |
| 5 | **Nurse / unit awards** | $10–25 | Same buyer type, **less competition** | ~2 hours |
| 6 | Sports team / coach awards | $10–25 | Team parent | ~2 hours |

### 1. Christmas — do this **this week**, not October

Seasonal printables need **6–8 weeks to index** before the rush, and office parties are
booked through November. Today is 3 September; **mid-October is the last responsible date,
not the target.**


**The eight Christmas certificates are already in the zip.** A second listing titled for
"office christmas party awards" is the *same file* with a different title, tags and images.
That's legitimate on Etsy and it's the cheapest listing you will ever create — maybe an hour,
mostly image work.

### 2. Bridal shower — the highest-value match

Wedding is the **top price band on Etsy ($15–50)** and the buyer is overwhelmingly a woman
with a deadline and a budget who is *actively looking to spend*. "Awards for the bridal
party" is an established format. This is the single best fit between what Etsy buys and what
our generator makes.

### 3. Teachers — the volume and repeat play

Lower price band, but **repeat customers** and an enormous population. Already written up as
prompt C in `HANDOFF.md`.

---

## One design note, and it matters

Our certificates are **austere** — cream, oxblood, serif, institutional. That's exactly right
for the office, where the joke depends on looking like real paperwork.

It is **wrong for bridal and baby showers.** That end of Etsy runs warm and decorative —
soft palettes, script faces, florals. The joke structure travels; the aesthetic doesn't.

The generator makes this cheap: the palette is five constants at the top of
`design/generate_certificates.py`, and the frame is CSS. A bridal cohort should be its own
visual world — blush, gold, a script display face — while keeping the deadpan citations that
make it ours.

---

## The discipline this does not break

`playbooks/product-decision.md` says **don't add SKUs before 10 sales.** This doesn't
contradict it, and the distinction is worth being precise about:

| | |
|---|---|
| **More listings of the same product** to new audiences | ✅ Cheap, and it's literally how Etsy revenue scales |
| **New product types** — mugs, apparel, sourced goods | ❌ Still gated behind 10 sales |

Mugs need a new supply chain. A bridal cohort needs an afternoon and reuses everything.

**Still publish the office kit first.** Not because it's the best category, but because it's
*finished*, and one live listing teaches more than four more unpublished ones.

---

## Two more things that decide this

**Photo 1 must be the product, printed.** Buyers cannot hold a file. First image is a printed
certificate on a desk with **DIGITAL DOWNLOAD** on the image; second is a grid of every award
title. Flat page-one screenshots lose the click. *(Done — `kit/listing/kit-1-hero.png`.)*

**Pinterest the same day you publish.** For printables it's the main free traffic source after
Etsy search. One vertical pin using the exact title keyword, then three variants. No ads until
the listing converts.

**And what not to do:** don't start planners or wall art. They earn more in aggregate and are
far more flooded. Our edge is a joke structure that already exists. Don't buy a PLR dump.
Don't run ads. **The constraint is listing count against a product that is already built.**

## What to look at that I can't

Open the grid you linked and check four things. Ten minutes, and it's worth more than
everything above because it's live data:

1. **The Bestseller badges.** Which listings carry one, and what are they? That's Etsy telling
   you what sells.
2. **The price of the top row.** If the first screen is $3–8, this niche is a volume game and
   $18 is wrong. If it's $15–40, our pricing is right.
3. **Review counts on the top 3.** Reviews ≈ 5–10% of sales. 200 reviews ≈ 2,000–4,000 units.
4. **How many are bundles vs single files** — and how many files the bundles claim.

Tell me what you see and I'll adjust the positioning against it rather than against
published averages.
