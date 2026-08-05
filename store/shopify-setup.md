# Shopify + Website Setup — Deadpan Goods

Exact click-path. ~60–90 minutes end to end. Everything here needs **your** logins, so this
is the part I can't do for you — but nothing below requires guesswork.

**Two front doors, and you need to decide which:**

| Option | What it is | Cost | Pick it if |
|---|---|---|---|
| **A · Shopify only** *(recommended)* | Shopify hosts everything. Restyle a free theme to the brand. | $39/mo | You want one system, real checkout, apps. **Start here.** |
| **B · Vercel page + Shopify checkout** | `storefront.html` on Vercel; buttons link into Shopify. | $5/mo + free | You want a custom-looking front page fast and cheap. |

You can run B first and fold into A later — the branding carries over.

---

## Step 1 · Create the store *(15 min)*

1. shopify.com → start free trial → store name **Deadpan Goods** (or your pick).
2. **Settings → Plan** → **Basic ($39/mo)**. (Starter $5/mo has no full storefront — only
   buy-buttons/links, which is Option B.)
3. **Settings → Store details** → set currency, address, and the store email.

## Step 2 · Buy the domain *(5 min)*

- **Settings → Domains → Buy new domain** (~$12–18/yr). Buying inside Shopify auto-connects
  it; no DNS work.
- Check the matching **@handle on TikTok + Instagram** before you commit to the name.

## Step 3 · Theme + brand styling *(20 min)*

Install the free **Dawn** theme → **Customize**, then set these to match the poster system:

| Setting | Value |
|---|---|
| Background / paper | `#E4E2D8` |
| Text / ink | `#17150F` |
| Accent / buttons | `#D93B24` (clearance red) |
| Highlight | `#E4D93C` (acid yellow) |
| Secondary | `#565E42` (olive) |
| Heading font | A heavy condensed sans — closest Shopify default: **Archivo Black** or **Oswald** |
| Body font | **Helvetica / Inter** |
| Corner radius | **0px** — square corners. Rounded corners kill the deadpan look. |

**Announcement bar:** `Free shipping over $60 · Ships in 3–5 days · Nobody has to know it was you`

**Homepage sections, in order:** Announcement bar → Hero (headline: *"We are very serious
about stupid things."*) → Featured collection (the goods) → the Uncle Starter Pack →
Fine print (4 promises) → Email signup.

Copy for all of it is already written in [`storefront.html`](storefront.html) — lift it verbatim.

## Step 4 · Add products *(20 min)*

For each: **Products → Add product** → title, description, **3+ photos**, price, and set
**Inventory → "Continue selling when out of stock"** (dropshipping has no local stock).

Starter six (from the storefront):

| Product | Price | Lane |
|---|---|---|
| Inflatable Shark Suit | $49 | B — sourced |
| Hairy Leg Camo Shorts | $34 | B — sourced |
| Creepy Window Silhouettes | $26 | B — sourced |
| Statement Long-Sleeve | $38 | A — POD |
| "Licensed To Grill" Apron | $32 | A — POD |
| World's Okayest Trophy | $28 | B — sourced |

**Uncle Starter Pack ($89):** create it as its own product, or install the free
**Shopify Bundles** app to build it from the individual SKUs.

> **Write descriptions in the deadpan voice:** real specs first, one absurd spec last.
> *"100% nylon · one size fits most · battery fan included · ruins weddings."*

## Step 5 · Connect fulfilment *(15 min)*

- **Lane A (POD):** App Store → **Printify** → authorize → build product → upload design →
  set price → **Publish to Shopify**.
- **Lane B (sourced):** App Store → **CJ Dropshipping** (or **DSers**) → import product →
  **map the variant** to the supplier SKU → enable **auto-order**.
- ⚠️ **Order one sample per Lane-B product before you advertise it.** Novelty goods vary
  wildly between suppliers.

## Step 6 · Payments *(10 min)*

1. **Settings → Payments → Activate Shopify Payments** (cards) — needs your ID + bank details.
2. Same page → **PayPal** → connect your **PayPal Business** account.
3. Turn on **Shop Pay** — accelerated checkout, meaningfully better mobile conversion.
4. **Put a card on file inside Printify and CJ**, or orders stall at production.

## Step 7 · Shipping + policies *(10 min)*

- **Settings → Shipping** → **Free shipping over $60**, flat **$5.95** under it.
- **Settings → Policies** → click **"Create from template"** for refund/privacy/terms, then
  edit. Set returns to **30 days** to match the storefront promise.
- Put **real delivery windows** on Lane-B product pages. Overpromising is the #1 source of
  chargebacks in novelty dropshipping.

## Step 8 · Marketing plumbing *(15 min)*

| Tool | Where | Does |
|---|---|---|
| **TikTok** app | Shopify App Store | Installs the pixel + enables TikTok Shop |
| **Meta** app | Shopify App Store | Installs the Meta pixel for retargeting |
| **Shopify Email** / **Klaviyo** | App Store | Welcome + abandoned-cart + post-purchase flows |
| **ManyChat** | manychat.com | The comment-bait auto-DM — **your highest-leverage automation** |

**Abandoned checkout is the single highest-ROI flow — turn it on first.**

---

## Option B · Deploy the Vercel page *(10 min)*

1. Push this repo to GitHub → vercel.com → **New Project** → import it.
2. Set the root to `store/` and deploy → you get a free `*.vercel.app` URL.
3. In `storefront.html`, replace **`REPLACE_SHOP_URL`** with your Shopify product/cart URL
   and **`REPLACE_EMAIL_ENDPOINT`** with your Klaviyo/Formspree endpoint.
4. Point ads and link-in-bio at the Vercel page; checkout happens in Shopify.

---

## Launch checklist

```
Store    [ ] Shopify Basic live   [ ] Domain connected   [ ] Handles claimed
Brand    [ ] Dawn theme restyled  [ ] 0px corners  [ ] Announcement bar
Products [ ] 6 products + photos  [ ] Deadpan descriptions  [ ] Uncle Pack built
Supply   [ ] Printify connected   [ ] CJ/DSers auto-order ON
         [ ] SAMPLES ORDERED (Lane B)   [ ] Card on file with both
Money    [ ] Shopify Payments  [ ] PayPal  [ ] Shop Pay
Legal    [ ] Refund/privacy/terms  [ ] Shipping rates  [ ] Real delivery windows
Growth   [ ] TikTok pixel  [ ] Meta pixel  [ ] Abandoned cart  [ ] ManyChat keyword
Final    [ ] TEST ORDER placed → routed to supplier → tracking received
```

**Do not spend a dollar on ads until the test order completes end to end.**
