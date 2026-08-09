# Deadpan Goods — AI-Run Print-on-Demand Gift Brand

Personalised joke certificates from **The Bureau of Minor Achievements** — a fictional agency
issuing official certifications for things that don't deserve them. Deadpan voice, real
quality, sold where gift buyers already search.

Stack: **Claude** (research, design, listings, analysis) → **Printify** (US printing, free
auto-generated mockups) → **Etsy** (primary channel) + **Shopify** (brand home) → Pinterest
and TikTok Shop affiliate.

▶ **START HERE:** [`workflow/30-day-plan.md`](workflow/30-day-plan.md) — the dated plan,
Aug 9 → Sep 8: what ships each week, the gates, the honest revenue target, and the budget.

▶ **This week's cohort:** [`marketing/etsy-cohort-1.md`](marketing/etsy-cohort-1.md) — 8
Etsy listings with titles, 13 tags each, descriptions, and the pricing ladder.
Artwork: `design/out/` · generator: `design/generate_certificates.py`.

▶ The weekly loop: [`workflow/growth-loop.md`](workflow/growth-loop.md) — scorecard, metric
gates, targeting matrix. Runs automatically every Monday.

▶ ⭐ **READ FIRST:** [`playbooks/beginner-fit-strategy.md`](playbooks/beginner-fit-strategy.md)
— the corrected plan for a beginner with no product and no content ability: switch goods to
print-on-demand (free auto-generated photos) and lead with Etsy, not TikTok organic.

▶ 📊 **The numbers:** [`marketing/etsy-metrics-brief.html`](marketing/etsy-metrics-brief.html)
— which metric actually decides Etsy ranking, the threshold bands, the four listings not worth
making, and the 30-day no-touch rule.

▶ 🚀 **Go live:** [`store/go-live-checklist.md`](store/go-live-checklist.md) — sell-first,
no samples. What's done, what's blocking the first sale, and the launch sequence.

▶ 🚨 **Fix first:** [`store/us-market-setup.md`](store/us-market-setup.md) — currency to USD,
US shipping zone, timezone. The store carries Brazilian demo defaults that charge US buyers
~$18 shipping. Validated mutation ready to run:
[`store/shipping-fix-mutation.md`](store/shipping-fix-mutation.md).

▶ **The moat:** [`playbooks/original-design-line.md`](playbooks/original-design-line.md)
— The Bureau of Minor Achievements: your first owned IP, 70–80% margin, no supplier risk.

▶ **Long term:** [`playbooks/long-term-brand-strategy.md`](playbooks/long-term-brand-strategy.md)
— three horizons, the goods ladder, the retention product, and the four things worth owning.

▶ Parked (needs sourced stock): [`marketing/halloween-launch-plan.md`](marketing/halloween-launch-plan.md)
— dated Halloween plan for the window silhouettes: hooks, posting schedule, bundle
economics, gates, and the Oct 10 cutoff.

Playbooks:
> - [`playbooks/gag-gift-playbook.md`](playbooks/gag-gift-playbook.md)
>   — **the active build**: novelty/gag-gift brand — two fulfilment lanes (POD vs
>   sourced), product shortlist, decoded viral mechanics, and auto-DM automation.
> - [`marketing/poster-system.html`](marketing/poster-system.html)
>   — the "Deadpan Luxury" poster system: 6 formats, house rules, image/video prompts.
> - [`store/shopify-setup.md`](store/shopify-setup.md)
>   — **the click-path**: Shopify store, theme colors, products, fulfilment, payments.
> - [`store/storefront.html`](store/storefront.html)
>   — the Deadpan Goods storefront (deployable, or lift the copy into Shopify).
> - [`playbooks/sleepmaxxing-brand-horizontal-club.md`](playbooks/sleepmaxxing-brand-horizontal-club.md)
>   — **the active build**: a premium rest-identity brand ("Horizontal Club") with
>   positioning, palette, product line, pricing, and a brand-locked prompt library.
> - [`playbooks/trending-products-2026.md`](playbooks/trending-products-2026.md)
>   — ranked trend research: POD lane (do today) vs. gadget lane, and IP traps.
> - [`playbooks/fifa-football-pod-playbook.md`](playbooks/fifa-football-pod-playbook.md)
>   — the FIFA research, legal design rules, and 10 product concepts.
> - [`prompts/design-and-marketing-prompts.md`](prompts/design-and-marketing-prompts.md)
>   — the general copy-paste prompt library (design, video, website, retargeting).

Store & automation (deploy-ready):
> - [`workflow/automation-blueprint.md`](workflow/automation-blueprint.md)
>   — Shopify ↔ Printful ↔ PayPal connection steps + marketing automation + costs.
> - [`store/product-listings.md`](store/product-listings.md)
>   — 7 listings in brand voice, Printful setup, premium prices, email flows.
> - [`store/landing-page.html`](store/landing-page.html)
>   — deployable on-brand landing page (Vercel-ready).
> - [`marketing/content-calendar.md`](marketing/content-calendar.md)
>   — 14 days of ready-to-post hooks + captions for TikTok / Reels.

---

## The three decisions that matter (July 2026)

1. **The World Cup is over (Spain beat Argentina 1–0 on July 19).** The *live-tournament*
   hype window has passed its peak. Do **not** build a "World Cup 2026 merch" store —
   you'd be late *and* illegal. Pivot to **football-culture streetwear**, which is a
   rising, evergreen trend (soccer jerseys +527% on TikTok Shop), not a tournament spike.

2. **Never touch FIFA IP.** "FIFA", "World Cup", "WC26", the logo, mascot, trophy,
   official typeface, club crests, and player names/faces are aggressively enforced —
   this is the single worst month of the year for POD takedowns. Printify *will* remove
   listings and can freeze payouts / close your store. Win with **original cultural
   designs** (heritage patterns, flag colours, city pride, retro/blokecore aesthetics).

3. **The demand is in cultural design, not replicas.** The current #1 soccer product on
   TikTok Shop US is a *Mexico "Chichén Itzá / Aztec"* graphic jersey (6,195 orders,
   +1,229% in 7 days) — a **cultural design, not an official kit**. That is your exact
   legal + profitable lane.

---

## The evidence-gated pipeline

AI should not go idea → product. It goes:

```
Trend signal → cultural angle → IP clearance → design → sample QA → offer test → scale
```

| # | Stage | Tool | Gate to pass |
|---|-------|------|--------------|
| 1 | Trend scan | Google Trends, TikTok Creative Center, vidIQ | Rising 3-yr trend + generic (brand-blind) language |
| 2 | Angle | Claude | A cultural/identity hook, not a replica |
| 3 | **IP clearance** | Human + checklist | Zero FIFA marks, crests, names, faces, kits |
| 4 | Design | Higgsfield / image gen | Print-ready, original, on-brand |
| 5 | Sample QA | Printify sample order | Colour, print, fabric acceptable |
| 6 | Offer test | TikTok/Shopify + ads | Cold CVR ≥ 1.5%, CPA ≤ contribution margin |
| 7 | Scale | Printify + Claude + Higgsfield | 10+ clean paid orders before you automate wider |

---

## Realistic cost to launch (first 30 days)

| Item | Cost |
|------|------|
| Printify | Free (or $29/mo Premium for better margins once selling) |
| Storefront | TikTok Shop = free · Shopify = $5–39/mo · Vercel landing = free |
| Higgsfield | ~$17–49/mo |
| Domain | Free Vercel subdomain, or ~$12/yr custom |
| Sample orders (3–5 SKUs) | ~$60–120 |
| **Ad spend to get first signal** | **$300–1,000** ← the real cost |
| **Total to a real test** | **~$400–1,200, mostly ad spend** |

## What is automated vs. human

- **Automated / fast (Claude + Higgsfield):** trend synthesis, cultural angles, design
  generation, product mockups, listing titles/descriptions, ad scripts, video creative,
  landing-page copy, retargeting audiences.
- **Human, do not skip:** the **IP clearance check**, the "does this design actually
  resonate" gut call, sample-order QA, and ad-account / TikTok Shop approval.

See the playbook for the **3-hour launch timeline**.
