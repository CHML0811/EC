# Automation & Connection Blueprint — Horizontal Club

The honest version: **fulfilment, payments, email flows, and retargeting can be fully
automated. Creative + taste + IP clearance cannot** (and shouldn't be). There is no
one-button "brand on autopilot" — this blueprint automates the grunt work so you only touch
the judgment calls.

> Note: you said **Printful** (earlier Printify). Both work identically for this — steps
> below use Printful; Printify is a drop-in alternative with the same flow.

---

## What's automated vs. what needs you

| Piece | Automated? | Who / how |
|---|---|---|
| Order → print → ship | ✅ Fully | Printful, once connected |
| Taking payment | ✅ Fully | Shopify + PayPal + cards |
| Welcome / abandoned-cart / post-purchase emails | ✅ After setup | Shopify Email or Klaviyo flows |
| Retargeting ads (75%+ viewers, ATC-no-buy) | ✅ After setup | TikTok + Meta pixels |
| Generating designs & ad videos | ⚙️ Assisted | Higgsfield (needs credits) → you approve |
| **IP clearance on each design** | ❌ Manual | You (protects the store) |
| Brand-voice replies, sample QA, the "does this resonate" call | ❌ Manual | You |

---

## Step 1 — Shopify store (you, ~30 min)
1. Create the store. Plan: **Basic $39/mo** for a full store, or **Starter $5/mo** if you
   only sell via TikTok/IG links + buy-buttons at first.
2. Theme: free **Dawn** theme, restyled to the palette (Cloud Cream `#F4EEE4`, Espresso
   `#3B2F27`). Or run the Vercel landing page (`store/landing-page.html`) as the front door
   and send buyers into Shopify checkout.
3. Add logo + brand colours + the manifesto to the About page.

## Step 2 — Connect Printful (you ~10 min, automated after)
1. Shopify **App Store → install "Printful" → Authorize**.
2. In Printful, build each product from `store/product-listings.md`: upload the design →
   pick the **premium blank** → set placement → set the **retail price** listed → **Sync to
   Shopify**.
3. Done: every order now auto-routes to Printful for print + ship. Zero manual fulfilment.

## Step 3 — Connect PayPal + cards (you ~10 min)
1. You need a **PayPal Business** account (free to open).
2. Shopify **Settings → Payments** → activate **PayPal** + **Shopify Payments** (cards).
3. ⚠️ Cash-flow note: when an order comes in, **Printful charges *your* card/balance** for
   production, while the customer's money lands in your Shopify/PayPal payout (often a day or
   two later). Keep a card on file in Printful so fulfilment never stalls.

## Step 4 — Marketing automation
**Email/SMS flows (set once, run forever):** Shopify Email (free) or **Klaviyo** (free to
250 contacts). Build three flows — copy is in `store/product-listings.md`:
- **Welcome** → manifesto + Member's Kit
- **Abandoned checkout** → gentle, in-voice nudge
- **Post-purchase** → "you're in the Club" + UGC ask

**Pixels + retargeting (automated once installed):** add **TikTok Pixel** + **Meta Pixel**
via Shopify. Audiences: *viewed 75%+ of an ad* and *add-to-cart, no purchase*. Retarget with
proof + the Member's Kit. (Never retarget with a discount — stay premium.)

**Content engine (assisted):** Higgsfield generates designs + 3-sec-hook ad videos (needs
credits) → connect TikTok in Higgsfield → publish. Cadence: 1–2 organic videos/day; promote
only the hooks that hold past 3 seconds.

## Step 5 — Keep these manual (on purpose)
IP clearance on every new design, brand-voice replies, sample QA, and the taste call on what
"feels" Horizontal Club. This is the moat — don't outsource it to a bot.

---

## Monthly cost

| Item | Cost |
|---|---|
| Shopify | $5 (Starter) – $39 (Basic) |
| Printful | $0 base (you pay per order, deducted from margin) |
| PayPal / cards | ~2.9% + fixed per sale |
| Klaviyo | $0 to 250 contacts |
| Higgsfield | $0 (trial) / credit top-ups / $17–49 plan |
| **Ad spend (the real cost)** | **$300–1,000 to get first signal** |

**Bottom line:** ~$50–80/mo in tools + your ad budget. The machine runs itself on
fulfilment and payments; you stay in charge of creative and taste.
