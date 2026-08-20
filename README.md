# Deadpan Goods — AI-Run Print-on-Demand Gift Brand

Personalised joke certificates from **The Bureau of Minor Achievements** — a fictional agency
issuing official certifications for things that don't deserve them. Deadpan voice, real
quality, sold where gift buyers are already searching.

> *"Recognition, finally, for meeting expectations approximately."*

**Stack:** Claude (research, design, listings, analysis) → **Printify** (US printing, free
auto-generated mockups) → **Etsy** (primary channel) + **Shopify** (brand home) → Pinterest,
then TikTok Shop affiliate.

---

## Start here

| | |
|---|---|
| 🎯 **[30-day plan](workflow/30-day-plan.md)** | Aug 9 → Sep 8. Weekly gates, honest revenue target, ~$34 budget. **Read this first.** |
| 📦 **[Etsy cohort 1](marketing/etsy-cohort-1.md)** | 8 listings — titles, 13 tags each, descriptions, pricing ladder |
| 🎄 **[Etsy cohort 2 — Christmas](marketing/etsy-cohort-2-christmas.md)** | 8 Secret Santa / gift-exchange listings. **Publish by Oct 1** to rank for December. |
| ⚡ **[Paste sheet](store/paste-sheet.html)** | Every field in the order Etsy asks, with copy buttons. **Open this while you set up.** |
| 🔧 **[Push certs to Shopify](store/push-certificates-to-shopify.md)** | Validated runbook to upload the artwork and create the 8 products. Pending — connector unstable. |
| 🖨️ **[Printify setup spec](store/printify-setup-spec.md)** | Exactly which blank, provider, sizes and prices. **Do this next.** |
| 🎨 **[Certificate generator](design/generate_certificates.py)** | `python3 design/generate_certificates.py` → 8 print-ready 300dpi designs in `design/out/` |
| 🖼️ **[Listing images](design/listing-images.md)** | 96 generated mockups in `design/mockups/` — framed, hook, detail, sizes, info, pin. **Upload 1–5 in order.** |
| 🎁 **[Office Awards Kit](marketing/etsy-office-awards-kit.md)** | The digital product — 38 awards, a working maker, a host's script. `python3 kit/build_kit.py`. **List this first.** |
| 🧭 **[First-seller strategy](playbooks/first-seller-strategy.md)** | Impulse vs intent, necessity vs AOV, why the winners here sell digital kits. **Read before building anything new.** |
| 🧭 **[What to sell next](playbooks/product-decision.md)** | Market data, three candidates, the sequence. Bulk orders first — 20× the order value at $0 cost. |
| 🏛️ **[Storefront](site/index.html)** | `python3 site/build_storefront.py <previews> --local site/index.html` — catalog built from the manifests |
| 📌 **[Pinterest pins](marketing/pinterest-pins.md)** | 40 pins, 6 boards, image crops. Free traffic — a December play made in August. |
| 📊 **[Etsy metrics brief](marketing/etsy-metrics-brief.html)** | The metric that actually decides ranking, threshold bands, the 30-day no-touch rule |
| 🔁 **[Growth loop](workflow/growth-loop.md)** | The weekly cycle. Runs automatically every Monday. |

## The strategy in four lines

1. **Print-on-demand, not sourced goods.** Printify auto-generates the product photos, so
   there's no camera, no samples, and $0 upfront.
2. **Paper goods, not apparel.** Etsy takes 20–25%. Certificates keep 34–46%; t-shirts keep 14%.
3. **Etsy, not TikTok organic.** Buyers there already search "funny gift for uncle" with a card
   out. No audience or daily content required.
4. **Owned IP, not resold SKUs.** The Bureau is a world competitors can't clone, and
   personalisation makes it stickier still.

Full reasoning: **[beginner-fit-strategy.md](playbooks/beginner-fit-strategy.md)** ·
Long term: **[long-term-brand-strategy.md](playbooks/long-term-brand-strategy.md)** ·
The moat: **[original-design-line.md](playbooks/original-design-line.md)**

## Store state

| | |
|---|---|
| Shopify | `fbapgj-si.myshopify.com` · **USD** · Advanced plan (**downgrade to Basic — saves $360/mo**) |
| Shipping | ✅ US $5.95, free over $60 · Rest of World $14.95 |
| Products | 38 certificates rendered · 8 novelty SKUs (draft) · [product-data.md](store/product-data.md) |
| Policies | Written, ready to push · [policies-and-pages.md](store/policies-and-pages.md) |
| Go-live | [go-live-checklist.md](store/go-live-checklist.md) |

**Outstanding (needs a human):** Printify + Etsy accounts · activate payments (ID/bank) ·
rename store to *Deadpan Goods* · timezone → GMT+8. About 45 minutes, once.

## Repo map

```
workflow/     30-day-plan · growth-loop · operating-flow · automation-blueprint
playbooks/    beginner-fit-strategy · long-term-brand-strategy · original-design-line
marketing/    etsy-cohort-1 · etsy-cohort-2 · etsy-metrics-brief · pinterest-pins
design/       generate_certificates.py + certs_christmas + certs_office → out/*.png
              generate_mockups.py → mockups/*.png · generate_crops.py → crops/*.png
kit/          build_kit.py → Office-Awards-Kit.zip (maker + 5 PDFs + 38 certificates)
store/        product-data · policies-and-pages · shopify/us-market setup · storefront
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
</details>
