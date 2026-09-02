# The Bureau of Minor Achievements

A fictional government agency issuing official recognition for things that don't deserve
any. Personalized certificates and a complete office awards ceremony, sold where gift
buyers are already searching. Deadpan voice, real production quality.

> *"Recognition, finally, for meeting expectations approximately."*

**Two products.** The **Office Awards Kit** ($24 digital, $0 per sale, built and packaged)
and **38 certificates** as physical prints ($32–58 via Printify, built and waiting).

**Stack:** Claude for research, design, copy and code → **Etsy** as the sales channel →
**Shopify** as the brand home → Printify only when the physical line goes live.

**Built with:** Python 3 and headless Chromium. No dependencies, nothing to install.

---

## Start here

| | |
|---|---|
| ✅ **[verify.py](verify.py)** | `python3 verify.py` — 13 checks. **Run this first after any break.** |
| 🚀 **[HANDOFF.md](HANDOFF.md)** | **Read this first.** The 45-minute path to a live listing, plus ready-to-paste Cursor prompts. |
| 🤖 **[AGENTS.md](AGENTS.md)** | Project rules for any AI picking this up — voice, non-negotiables, and the bugs already fixed. |
| 🎬 **[Video playbook](marketing/video-playbook.md)** | Why the last video was trash, the 10 hooks to test, exact Grok prompts. |
| 🎯 **[30-day plan](workflow/30-day-plan.md)** | Weekly gates, honest revenue target, ~$34 budget |
| 📦 **[Etsy cohort 1](marketing/etsy-cohort-1.md)** | 8 listings — titles, 13 tags each, descriptions, pricing ladder |
| 🎄 **[Etsy cohort 2 — Christmas](marketing/etsy-cohort-2-christmas.md)** | 8 Secret Santa / gift-exchange listings. **Publish by Oct 1** to rank for December. |
| ⚡ **[Paste sheet](store/paste-sheet.html)** | Every field in the order Etsy asks, with copy buttons. **Open this while you set up.** |
| 🔧 **[Shopify uploader](store/upload_to_shopify.py)** | `python3 store/upload_to_shopify.py --all --execute` — 16 products, images, prices, policies, pages. One command, no connector. |
| 🖨️ **[Printify setup spec](store/printify-setup-spec.md)** | Exactly which blank, provider, sizes and prices. Only needed for the physical line. |
| 🎨 **[Certificate generators](design/generate_certificates.py)** | `generate_certificates` + `certs_christmas` + `certs_office` → 38 print-ready 300dpi designs |
| 🖼️ **[Listing images](design/listing-images.md)** | 96 mockups + 82 channel crops. Six per design, generated — no camera. **Upload 1–5 in order.** |
| 🎁 **[Office Awards Kit](marketing/etsy-office-awards-kit.md)** | **The lead product.** 38 awards, a working maker, a host's script. `python3 kit/build_kit.py` |
| 🧭 **[First-seller strategy](playbooks/first-seller-strategy.md)** | Impulse vs intent, necessity vs AOV, why the winners here sell digital kits. **Read before building anything new.** |
| 🧭 **[What to sell next](playbooks/product-decision.md)** | Market data, three candidates, the sequence. Bulk orders first — 20× the order value at $0 cost. |
| 🏛️ **[Storefront](site/index.html)** | `python3 site/build_storefront.py <previews> --local site/index.html` — catalog built from the manifests |
| 📌 **[Pinterest pins](marketing/pinterest-pins.md)** | 40 pins, 6 boards, image crops. Free traffic — a December play made in August. |
| 📊 **[Etsy metrics brief](marketing/etsy-metrics-brief.html)** | The metric that actually decides ranking, threshold bands, the 30-day no-touch rule |
| 🔁 **[Growth loop](workflow/growth-loop.md)** | The weekly review cycle. **You run it** — nothing is automated. |

## The strategy in five lines

1. **Digital first, physical second.** The $24 kit needs no Printify, no card on file and no
   shipping setup — it can list the hour the Etsy account exists, and costs $0 per sale.
2. **Paper and downloads, not apparel.** Etsy takes 20–25% all-in. The kit keeps 77%,
   certificates 34–46%; t-shirts keep 14%.
3. **Etsy, not TikTok organic.** Intent products are found by search. Impulse products need an
   audience, daily content, or ad budget — none of which exist here.
4. **Sell the ceremony, not the print.** The listings actually moving volume in this category
   are bundles sold to offices, not single art prints.
5. **Owned IP, not resold SKUs.** The Bureau is a world competitors can't clone, and the
   writing — not the layout — is the part that takes more than an afternoon to copy.

Full reasoning: **[first-seller-strategy.md](playbooks/first-seller-strategy.md)** ·
What's next: **[product-decision.md](playbooks/product-decision.md)** ·
Long term: **[long-term-brand-strategy.md](playbooks/long-term-brand-strategy.md)**

## Store state

| | |
|---|---|
| Lead product | **Office Awards Kit** — $24 digital, built and packaged, 8.2 MB |
| Artwork | 38 certificates · 182 listing images · all generated, no camera |
| Shopify | `fbapgj-si.myshopify.com` · **USD** · Advanced plan (**downgrade to Basic — saves $360/mo**) |
| Shipping | ✅ US $5.95, free over $60 · Rest of World $14.95 |
| Etsy | ❌ **Not created. This is the only thing blocking revenue.** |
| Printify | ❌ Not started — and not needed until the physical line goes live |

**Outstanding (needs a human):** Etsy account → publish the kit → downgrade Shopify.
**About 40 minutes, once.** Full steps in [HANDOFF.md](HANDOFF.md).

## Repo map

```
workflow/     30-day-plan · growth-loop · operating-flow · automation-blueprint
playbooks/    first-seller-strategy · product-decision · long-term-brand-strategy
marketing/    office-awards-kit · etsy-cohort-1 · etsy-cohort-2 · video-playbook
              etsy-metrics-brief · pinterest-pins
design/       generate_certificates.py + certs_christmas + certs_office → out/*.png
              generate_mockups.py → mockups/*.png · generate_crops.py → crops/*.png
kit/          build_kit.py → Office-Awards-Kit.zip (maker + 5 PDFs + 38 certificates)
store/        upload_to_shopify.py · product-data · policies-and-pages · paste-sheet
```

<details>
<summary>Archived — earlier directions, kept for reference</summary>

- [`playbooks/fifa-football-pod-playbook.md`](playbooks/fifa-football-pod-playbook.md) —
  football-culture POD. Sound IP research; the World Cup window closed.
- [`playbooks/sleepmaxxing-brand-horizontal-club.md`](playbooks/sleepmaxxing-brand-horizontal-club.md) —
  "Horizontal Club" quiet-luxury sleepwear brand.
- [`playbooks/trending-products-2026.md`](playbooks/trending-products-2026.md) — trend research
  and IP traps (Labubu, licensed characters). Still worth reading before any new product.
- [`playbooks/gag-gift-playbook.md`](playbooks/gag-gift-playbook.md) — sourced-novelty lane and
  the decoded viral mechanics. Revisit when there's revenue for samples.
- [`marketing/halloween-launch-plan.md`](marketing/halloween-launch-plan.md) — parked; needs
  sourced stock and US filming.
- [`prompts/design-and-marketing-prompts.md`](prompts/design-and-marketing-prompts.md) —
  football-direction prompt library. **Do not follow it**; current prompts are in
  `marketing/video-playbook.md`. Kept for its IP-clearance reasoning.
</details>
