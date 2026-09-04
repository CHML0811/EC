# Handoff — pick this up in Cursor

Everything is built and pushed. This is the order to do things in and the exact prompts to
paste. `AGENTS.md` carries the project rules; Cursor loads it automatically.

**Total time to first listing live: about 45 minutes.** None of it needs an AI.

---

## 0 · Check the project is healthy, then build it — ~2 minutes

```bash
python3 verify.py            # 13 checks: Chrome, sources, Etsy tag limits, doc links
python3 kit/build_kit.py     # → kit/Office-Awards-Kit.zip, the file you upload to Etsy
```

`verify.py` is the thing to run whenever you come back to this after a break, or after an
assistant changes something. It catches what actually rots: a missing Chrome, an Etsy tag
that grew past 20 characters, a British spelling in buyer-facing copy, a doc link pointing
at a renamed file. It exits non-zero on failure, so Cursor can run it too.

Needs Python 3 and Chrome, nothing else. If it says "No Chrome or Chromium found", install
Chrome or point at it — `export CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'`
on macOS.

Verified working from a clean clone: 38 certificates, 5 PDFs, the maker, 8.2 MB.

---

## Do these yourself. No AI required.

### 1 · Check the demand is real — ~15 min, free, do this FIRST
**I never got this number and it's the biggest gap in the work.** I verified the category has
~500 competing listings with real sales volume, but never how many people search for it.

Sign up for [eRank](https://erank.com) free — 100 keyword lookups a day. Check
`office awards`, `funny awards`, `employee awards`, `printable awards`.

| Monthly searches | Verdict |
|---|---|
| Under ~1,000 | Too thin. Don't spend the $20 — pick a different niche with the same machinery. |
| 1,000–20,000 | Normal and workable. Continue. |
| Over 20,000 | Good, but competition will be tougher than 500 listings suggests. |

Also open the top 3 listings for "funny office awards" and read their review counts.
Reviews ≈ 5–10% of sales, so 200 reviews ≈ 2,000–4,000 units sold. That tells you the
ceiling better than any tool. Full reasoning: [`playbooks/will-this-sell.md`](playbooks/will-this-sell.md).

### 2 · Etsy seller account — ~15 min
[etsy.com/sell](https://www.etsy.com/sell). Needs your ID and bank details, which is why
nobody else can do it for you. Shop name: **Bureau of Minor Achievements** (or
`BureauOfMinorAchievements` if taken — don't add numbers, it reads as spam).

### 3 · Publish the Office Awards Kit — ~20 min
**Open [`store/etsy-launch-console.html`](store/etsy-launch-console.html) in a browser and
work down it beside the Etsy tab.** Nine steps, every field with a copy button, in the order
Etsy asks for them. Progress saves in the browser so you can stop halfway.

The same content in plain markdown: **`marketing/etsy-office-awards-kit.md`**.

- Listing type: **Digital**
- Upload: **`kit/Office-Awards-Kit.zip`** (8.2 MB, under Etsy's 20 MB cap)
- Images: **`kit/listing/kit-1` … `kit-4`**, in that order
- Price: **$14.99** — provisional. If the top organic row is $5–$8 with 400+ reviews, drop to $9.99
- Personalization: **off**

### 4 · List it again for Christmas — ~1 hour, **this week**
**The same zip, a second listing.** The eight Christmas certificates are already inside it,
so this needs no new product — just a seasonal title, 13 different tags and one new image.
Etsy ranks listings, not shops, so two listings is two chances to be found on searches that
don't compete with each other.

**Not October.** Seasonal printables need 6–8 weeks to index and office parties are booked
through November. Today is 3 September; mid-October is the last responsible date, not the
target. Every week of delay is indexing lost from a season that comes once a year.

Copy is written: **[`marketing/etsy-christmas-awards-kit.md`](marketing/etsy-christmas-awards-kit.md)**
— $12.99, its own 13 tags with zero overlap so the two listings don't bury each other. The
seasonal hero is built at `kit/listing/kit-x1-hero.png`.

Then **pin both listings the same day**. Pinterest is the main free traffic source for
printables after Etsy search — one vertical pin per listing using the exact title keyword,
then three variants. No ads until a listing converts.

### 5 · Downgrade Shopify — ~2 min
Advanced $399 → Basic $39. **Saves $360 every month.** Nothing in this project uses an
Advanced feature.

### 6 · Finish the Shopify store — ~10 min, optional

**Mostly done already.** The catalog was pushed to `fbapgj-si.myshopify.com` through the
Shopify connector: **17 products** (the Office Awards Kit plus all 16 certificate prints),
each with images on Shopify's CDN and three priced variants ($32 / $42 / $58), plus the
**About** and **FAQ** pages, **four collections** (Digital Downloads · Office & Coworkers ·
Christmas & Secret Santa · Family & Milestones) and both **navigation menus**. Everything is
**DRAFT** — nothing is buyable yet, on purpose.

Two settings that only bite once a real order arrives were also fixed, because the defaults
are wrong for this catalog: the kit variant no longer **requires shipping** (it's a file), and
all 32 print variants created in the second API call had come back **inventory-tracked at
quantity zero**, which would have shown 11x14 and Framed as sold out on every product.

Three things are left, and they all need you:

1. **Policies.** The connector's token lacks `write_legal_policies`, so the four policies
   were rejected. Paste them from `store/policies-and-pages.md` into **Settings → Policies**
   (about 4 minutes), or create a custom app token and run
   `python3 store/upload_to_shopify.py --policies --execute`.
2. **Digital delivery.** Shopify does not deliver files on its own. Install the free
   first-party **Digital Downloads** app and attach `kit/Office-Awards-Kit.zip` to the kit
   product. **Until you do this, activating that product means a buyer pays and gets
   nothing.**
3. **Shop name.** The store is still called "My Store" in **Settings → Store details**.
   There is no API for this. Rename it to *The Bureau of Minor Achievements*.

Then flip products from Draft to Active when you're ready to sell.

There are also **8 leftover DRAFT products from the archived "Deadpan Goods" direction**
(inflatable shark suit, camo shorts, window silhouettes). They're invisible to customers.
Delete them when convenient — that was left to you rather than done automatically.

To re-run or extend the catalog from scratch, one command still does the whole thing:

```bash
# Shopify admin → Settings → Apps and sales channels → Develop apps → Create an app
#   → Admin API scopes: write_products, write_files, write_legal_policies,
#     write_online_store_pages → Install → reveal the token
export SHOPIFY_STORE=fbapgj-si.myshopify.com
export SHOPIFY_TOKEN=shpat_...
export SHOPIFY_SUPPORT_EMAIL=your-real@email.com   # policies name an address

python3 store/upload_to_shopify.py --all                       # dry run first
python3 store/upload_to_shopify.py --products --limit 1 --execute   # one product, check it
python3 store/upload_to_shopify.py --all --execute             # the rest
```

Products are created as **DRAFT** and matched on handle, so re-running is safe. The script
refuses to publish policies while they still name the placeholder support address — set
`SHOPIFY_SUPPORT_EMAIL` or pass `--allow-placeholder-email` if you genuinely don't care yet.

**It has never been run against a live store**, because no API token existed while it was
written. Hence the `--limit 1` step: create one product, look at it in admin, then continue.

---

## Then hand these to Cursor

Paste each prompt as-is. They assume `AGENTS.md` is loaded.

### Prompt A — get oriented
```
Read AGENTS.md, then playbooks/first-seller-strategy.md and
marketing/etsy-office-awards-kit.md.

Summarize in 10 lines: what this business sells, which product is the priority and why,
and what the single blocking step is. Then tell me the one thing you'd do next and why.
Don't write any code yet.
```

### Prompt B — verify the project is healthy
```
Run `python3 verify.py --full` and report the result.

If anything fails, fix only what failed and re-run until it passes. Do not refactor
anything, do not "improve" any copy, and do not touch a design — this is a check, not a
cleanup. Show me the final output.
```

### Prompt C — the second listing
```
Create a second Etsy listing for the SAME kit aimed at teachers instead of offices:
end-of-year classroom awards. Follow the exact structure of
marketing/etsy-office-awards-kit.md.

Rules from AGENTS.md apply: US English, exactly 13 tags, every tag 20 characters or fewer,
no invented numbers.

Write 12 new classroom certificates into design/certs_school.py, following the pattern in
design/certs_office.py exactly. Keep the deadpan voice — dry and specific, never zany.
Then run it and show me the new PNGs.

Do not touch the existing cohorts.
```

*Why this one: the kit is already built. A second audience is a second listing for a few
hours of work, and Etsy ranks listings, not shops — two listings is two chances to be found.*

### Prompt D — after the first sale
```
The first sale came in. Read marketing/etsy-metrics-brief.md and workflow/growth-loop.md,
then tell me:

1. Which metric decides whether to make more of this, and what the threshold is
2. Whether to add mugs yet (check playbooks/product-decision.md for the gate)
3. What to publish next

Give me a recommendation, not options.
```

### Prompt E — if nothing sells in 30 days
```
30 days, no sales. Before changing anything, diagnose in this order:

1. Is the listing getting IMPRESSIONS? (Etsy Stats → Search)
   - No impressions  = the title/tags don't match how people search. Rewrite the title.
   - Impressions, no clicks = image 1 is losing the grid. Remake it.
   - Clicks, no sales = the description or price. Fix in that order.

2. Do NOT cut the price first. Price is almost never why a new digital listing fails —
   being unfindable is.

Tell me which of the three it is, with the numbers you used, then fix that one thing only.
```

---

## The video, when you get to it

Read **`marketing/video-playbook.md`** first. It has the diagnosis of why the last one came
out badly, and the exact Grok prompts.

The three things that matter most:

1. **The best video for this product uses no AI at all** — screen-record the Awards Maker.
   Paste ten names, press print, watch ten certificates appear. That's the #1 performing hook
   type (product/outcome showcase) by definition, and it has zero uncanny-valley risk.
2. **In Grok, use image-to-video, never text-to-video**, starting from a real PNG in this
   repo. Text-to-video will melt the typography, and this product *is* typography. Every
   prompt in the playbook carries the clause that stops the model rewriting the text.
3. **Ship ten hooks, not one video.** That's the only real advantage AI gives you. The
   playbook has all ten written out.

Judge on **3-second retention**, not likes. Under 50% kill it, over 70% make five more.

---

## What's done, so you don't rebuild it

| | |
|---|---|
| Certificates | 38 designs, 2400×3000 @ 300dpi, print-ready |
| Listing images | 96 mockups + 82 channel crops + 4 kit images |
| The kit | Maker + 5 PDFs + 38 certificates, zipped at 8.2 MB |
| Copy | 32 physical listings + the kit listing, all inside Etsy's limits |
| Storefront | `site/index.html`, catalog built from the manifests |
| Shopify | USD, shipping zones live (US $5.95, free over $60) |

## What's genuinely unfinished

- **Etsy account and the listing.** The only thing standing between this and revenue.
- **Shopify policies, digital delivery, and the shop name.** The catalog and pages are done;
  see step 6. The kit product must not go Active before the Digital Downloads app is wired
  up, or a buyer pays and receives nothing.
- **Printify.** Not started. Not needed until the physical line goes live.
- **Bulk shipping math.** The departmental tiers on the storefront assume one parcel.
  Printify bills per item. **Verify in their calculator before promoting those tiers.**

---

## If you only remember one thing

The work is done. **The bottleneck is not more work — it's an Etsy account.**

Resist the urge to have Cursor build more. The temptation will be strong because building is
easy and listing is boring. Publish first, then build.
