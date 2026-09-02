# Printify Setup Spec — exactly what to click

> **⚠️ Fee correction.** The tables below use Etsy at ~23%. The real cut on an
> **organic** sale is **~11%** (6.5% + 3% + $0.25 + $0.20 listing). The extra 15% is
> Offsite Ads, which applies only to ad-driven sales and is optional under $10k/yr.
> **Every margin below is therefore conservative — the real ones are better.**
> Full breakdown: [`playbooks/where-to-sell.md`](../playbooks/where-to-sell.md).



For all 16 Bureau certificates. Getting the blank and provider right is a **margin decision**,
not a preference — the wrong pick quietly costs $4–8 per sale.

---

## Before anything: connect

1. **printify.com** → free account
2. **My Stores → Add store → Shopify** → authorize `fbapgj-si.myshopify.com`
3. **Settings → Billing** → add a card. *Printify charges you at order time; without a card on
   file, orders stall in production and the customer waits.*

## The product: matte poster, not "art print"

Create **one Printify product per certificate** (16 total).

| Setting | Choose | Why |
|---|---|---|
| Catalog category | **Home & Living → Wall Art → Posters** | Cheapest base, best margin |
| Product | **Matte Vertical Poster** (or "Premium Matte Vertical") | Matte reads as a document; gloss reads as a cheap print and kills the joke |
| Print provider | **Pick a US provider with the highest "Fulfilment" rating.** Prefer one printing in multiple US regions. | US printing = 3–5 day delivery, our biggest advantage over Chinese dropshippers |
| Sizes to enable | **8×10", 11×14"** only | Our artwork is 8:10. Other ratios will crop the border. |
| Frame | Add the framed variant **only if the same provider offers it** | Splitting providers = two parcels, two shipping charges, one angry customer |

> ⚠️ **Do not enable 12×18, 18×24, or any non-8:10 size.** The artwork is 2400×3000 (exactly
> 8:10). Anything else crops the guilloché border or the seal, and it will look like a mistake
> rather than a joke.

## Upload

Artwork is in `design/out/`. Upload the PNG, then in the placement editor:

> **Listing images are already done** — 96 of them, in `design/mockups/`, generated without
> Printify. See [`design/listing-images.md`](../design/listing-images.md). Printify's own
> mockups are still worth swapping in as the **thumbnail** once they exist, because a real
> photographed frame beats a rendered one. It replaces one image of six, not the set.


- **Scale to fill** the print area
- **Do not add bleed or margin** — the border is part of the design and is already inset
- Check the preview at 8×10 **and** 11×14; the seal and serial number must both be fully visible

## Pricing — set retail manually, don't use the % markup

Printify's automatic markup will produce ugly numbers and squeeze your margin. Set these:

| Size | Retail | Typical base | Etsy ~23% | **You keep** |
|---|---:|---:|---:|---:|
| 8×10 | **$32.00** | ~$10 | $7.36 | **~$14.64 (46%)** |
| 11×14 | **$42.00** | ~$14 | $9.66 | **~$18.34 (44%)** |
| Framed 8×10 | **$58.00** | ~$25 | $13.34 | **~$19.66 (34%)** |

**Check the real base cost in Printify before publishing.** Providers differ. If a provider's
8×10 base is above **$13**, pick a different provider — that pushes margin under 40% and the
maths stops working.

## Publish

- Push to **Shopify** first (brand home), then connect Etsy separately
- Set every product to **draft** in Shopify until the Etsy listings go live the same day
- **Tag each one:** `bureau`, `certificate`, `personalised`, plus `season:christmas` on the
  eight `bma-x-*` designs

## ⚠️ The personalisation gap

**Printify alone cannot capture a custom name.** The artwork has a `{ Recipient Name }`
placeholder — something has to fill it. Three options, cheapest first:

| Option | Cost | How it works |
|---|---|---|
| **Manual (start here)** | $0 | Buyer types the name in Etsy's personalisation box. You edit the name into the file and upload it before fulfilling. ~3 min/order. Fine under ~20 orders/week. |
| **Teeinblue / Customily** | ~$20–40/mo | Live preview, auto-generates the print file. Worth it once volume hurts. |
| **Sell it un-personalised** | $0 | Drop the name line entirely. Simpler — but loses the moat and the Etsy personalisation ranking boost. |

**Recommendation: start manual.** Three minutes per order is nothing at this volume, and you
learn what buyers actually type before paying for software. Enable Etsy's personalisation
field with a **40-character limit** and the prompt: *"Name exactly as it should appear —
we print it as typed."*

## Verify before you advertise

```
[ ] Card on file in Printify
[ ] Provider is US-based, high fulfilment rating, 8x10 base under $13
[ ] Only 8x10 and 11x14 enabled
[ ] Preview checked — seal and serial fully visible at both sizes
[ ] Retail set manually: $32 / $42 / $58
[ ] Products synced to Shopify as draft
[ ] ONE test order placed through real checkout -> lands in Printify -> tracking received
```

**That last line is the gate.** Until a real order flows end to end, don't spend on ads.
