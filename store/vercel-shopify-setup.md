# Option B Setup — Vercel front page + Shopify checkout

**Cost: $5/mo (Shopify Starter) + $0 (Vercel) + ~$12/yr domain.**
Your page lives on Vercel; checkout happens on Shopify via **cart permalinks** — plain links,
no JavaScript embed, nothing to break.

```
Visitor → Vercel page (site/index.html) → clicks "Add to cart"
       → https://your-store.myshopify.com/cart/VARIANT_ID:1
       → Shopify checkout (card + PayPal) → supplier auto-fulfils
```

---

## Step 1 · Shopify Starter *(15 min)*

1. shopify.com → start trial → store name **Deadpan Goods**.
2. **Settings → Plan → Starter ($5/mo).**
   Starter has no themed storefront — that's fine, Vercel *is* your storefront. You still get
   full checkout, orders, apps, and discount codes.
3. **Settings → Store details** → currency + address.

## Step 2 · Add the 6 products *(20 min)*

**Products → Add product** for each. Copy the titles, prices, and specs from
[`../site/index.html`](../site/index.html) — the deadpan voice is already written.

For every product set:
- **3+ photos** (your real product shots)
- **Inventory → uncheck "Track quantity"** (or allow overselling — you hold no stock)
- **Shipping → set a real weight** (needed for accurate rates)

Also create **The Uncle Starter Pack** as its own product at **$89**.

## Step 3 · Get your variant IDs *(10 min — the one fiddly bit)*

Each "Add to cart" link needs the product's **variant ID**.

**Easiest method:** open the product in Shopify admin → scroll to **Variants** → click a
variant. The browser URL ends with:

```
/products/1234567890/variants/45123456789012
                              ^^^^^^^^^^^^^^ ← this is your variant ID
```

**If a product has no variants** (single option), get it from JSON instead — visit:

```
https://your-store.myshopify.com/products/YOUR-PRODUCT-HANDLE.json
```

and look for `"variants":[{"id": 45123456789012, ...`

## Step 4 · Wire up the page *(5 min)*

Open [`../site/index.html`](../site/index.html) and edit **only** the `SHOP` block near the top:

```js
const SHOP = {
  domain: "deadpan-goods.myshopify.com",   // ← your real domain
  email_endpoint: "https://formspree.io/f/xxxxx",
  variants: {
    shark:     "45123456789012",
    shorts:    "45123456789013",
    windows:   "45123456789014",
    longslv:   "45123456789015",
    apron:     "45123456789016",
    trophy:    "45123456789017",
    unclepack: "45123456789018"
  }
};
```

That's the only edit. Every button wires itself. Any variant left as `null` falls back to
your store homepage instead of breaking.

> **Keep the `.myshopify.com` domain here** even if you buy a custom domain — cart permalinks
> are most reliable on it.

**Email capture:** free options — **Formspree** (formspree.io, paste the form URL) or
**Klaviyo** (better long-term; gives you the abandoned-cart flow too).

## Step 5 · Deploy to Vercel *(10 min)*

1. Push this repo to GitHub (already done — branch `claude/ai-dropshipping-workflow-0qhevt`).
2. vercel.com → **Add New → Project** → **Import** this repo.
3. **Root Directory → `site`** ← important, or Vercel won't find `index.html`.
4. Framework preset: **Other**. Build command: *(leave empty)*. Output dir: *(leave empty)*.
5. **Deploy** → you get a free `your-project.vercel.app` URL, live in ~30 seconds.
6. Optional: **Settings → Domains** → add your custom domain.

Every future `git push` redeploys automatically.

## Step 6 · Payments *(10 min)*

**Settings → Payments:**
- **Shopify Payments** (cards) — needs your government ID + bank details.
- **PayPal** — connect your PayPal Business account.
- **Shop Pay** — turn on; meaningfully better mobile conversion.

## Step 7 · Fulfilment *(15 min)*

- **POD** (long-sleeve, apron): App Store → **Printify** → design → publish.
- **Sourced** (shark suit, shorts, silhouettes, trophy): App Store → **CJ Dropshipping** or
  **DSers** → import → map variants → **auto-order ON**.
- ⚠️ **Card on file in both**, or orders stall at production.
- ⚠️ **Order one sample of every sourced product before advertising it.**

## Step 8 · Policies + shipping *(10 min)*

- **Settings → Shipping** → free over **$60**, flat **$5.95** below.
- **Settings → Policies** → "Create from template" for refund/privacy/terms → set returns to
  **30 days** to match the page.

## Step 9 · Growth plumbing *(15 min)*

| Tool | Does |
|---|---|
| **TikTok** app (Shopify) | Pixel + TikTok Shop |
| **Meta** app (Shopify) | Pixel for retargeting |
| **Klaviyo** | Abandoned cart ← **highest ROI, do this first** |
| **ManyChat** | Comment-bait auto-DM (the 121K-share mechanic) |

> On Option B the pixel must also fire on the **Vercel page**. Paste the TikTok + Meta base
> pixel snippets just before `</body>` in `site/index.html`.

---

## Checklist

```
Shopify  [ ] Starter plan   [ ] 6 products + Uncle Pack   [ ] Photos uploaded
IDs      [ ] All 7 variant IDs collected
Page     [ ] SHOP block filled   [ ] Email endpoint set   [ ] Pixels pasted
Vercel   [ ] Imported repo   [ ] Root dir = site   [ ] Deployed + URL live
Money    [ ] Shopify Payments   [ ] PayPal   [ ] Shop Pay
Supply   [ ] Printify   [ ] CJ/DSers auto-order   [ ] Card on file both
         [ ] SAMPLES ORDERED
Legal    [ ] Policies   [ ] Shipping rates
Growth   [ ] Pixels   [ ] Abandoned cart   [ ] ManyChat keyword
Final    [ ] TEST ORDER: page → checkout → supplier → tracking
```

**No ad spend until that final test order completes end to end.**
