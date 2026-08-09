# Go Live — sell-first, no samples

Strategy: **test demand with real orders.** No sample round. The `first-10 protocol`
(`workflow/growth-loop.md` §4) does the sample's job.

---

## ✅ Done

- Currency **USD**
- Shipping: **US $5.95 · free over $60 · Rest of World $14.95** (Brazil zones deleted)
- **8 products** live in Shopify with full copy, prices, SEO tags, SKUs, variants
- **Halloween collection** (smart, auto-fills on `tag:halloween`)

## 🚧 Blocking the first sale

### 1 · Product photos ← the only real blocker
Products with no images look broken and can't be advertised — Meta and TikTok both require a
product image. Fastest paths, in order:

- **Supplier images (do this now).** CJ / AliExpress listings include photos intended for
  resellers. Free, instant, good enough to test demand. Grab 3–5 per product, including a
  recent buyer photo if there is one — those convert better than the studio shot.
- **Your phone.** For the window silhouettes, the day/night flip needs *any* lit window. You
  don't need the product to shoot the hook — you need the reaction.
- **AI hero shots.** Higgsfield is at **1.52 credits (free plan)**, so this needs credits.
  Prompts are ready in `marketing/poster-system.html` §3.

Quality bar to test demand is **adequate, not beautiful.** Upgrade after the first winner.

### 2 · Payments
**Settings → Payments** → Shopify Payments (needs ID + bank) + PayPal + Shop Pay.
Without this there is no checkout.

### 3 · Fulfilment route
You don't need an app on day one — **manual fulfilment is fine for the first orders.** When
one comes in, place it with the supplier by hand and paste the tracking into Shopify. Install
CJ / DSers once orders are steady enough that manual becomes annoying.

## ⚙️ Two-minute cleanups

- **Store name** — still "My Store" → **Deadpan Goods** (Settings → General)
- **Timezone** — still **-03 (Brazil)** → your actual zone (Settings → General)
- **Policies** — Settings → Policies → "Create from template" → set returns to **30 days**

## 🚀 Publish

Products are **DRAFT**. Once photos are on, flip them to **ACTIVE** — I can do that in one
call, or Products → select all → Set as active.

**Publish order:** Creepy Window Silhouettes + Haunt The Whole House first. Halloween is the
live season and the rest can follow.

---

## Launch sequence

```
[ ] Supplier picked off reviews (≥4.8 rating, ≥1,000 orders, read the 1-3 star ones)
[ ] Photos uploaded (supplier images are fine)
[ ] Payments live
[ ] Store name + timezone + policies
[ ] Products ACTIVE
[ ] Test order through checkout — confirm $5.95 / free over $60
[ ] Post hook #1 (day/night flip) — organic, zero spend
[ ] First 10 orders: track every one, email each buyer at delivery
[ ] 10 clean deliveries → start paid
```

**The one rule that replaces the sample:** ad spend stays flat until the first ten orders
land clean. That's the whole trade — you're moving faster in exchange for watching those ten
like a hawk.
