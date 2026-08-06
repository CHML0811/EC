# US Market Setup — do these before any traffic

Your store carries **demo defaults from a Brazilian template**. Left alone, a US customer
gets charged ~US$18 shipping in the wrong currency. Four fixes, ~10 minutes total.

---

## 1 · Currency → USD ⚠️ do this first

**Settings → General → Store defaults → Store currency → US Dollar (USD)**

- This **cannot** be changed through the API — it's admin-only, by design.
- Shopify **locks it once you have orders.** You have zero orders, so it's free and instant
  right now. This gets much harder later.
- Prices are stored as plain numbers, so everything already created lands correctly:
  49 → **$49**, 34 → **$34**, 65 → **$65**. No re-pricing needed.

## 2 · Country & timezone

**Settings → General:**
- **Timezone** → currently **(GMT-03:00) Brazil**. Set to your actual timezone, or
  **(GMT-05:00) Eastern Time** to read reports in your customers' clock.
- Keep the business address as Hong Kong — that's your legal address and it's fine. The
  *market* is what needs to be US, not the address.

## 3 · Shipping zones 🚨 the one that breaks orders

**Settings → Shipping and delivery → General profile.** Current state:

| Zone | Countries | Rate | Problem |
|---|---|---|---|
| "Domestic" | 🇧🇷 **Brazil only** | R$22 | Template leftover — irrelevant |
| "International" | 28 countries incl. 🇺🇸 US | **R$98 (~US$18)** | **Your entire market pays $18 shipping** |

**Fix:**
1. **Delete** the "Domestic" (Brazil) zone.
2. **Create a zone: "United States"** → add United States → two rates:
   - `Free shipping` — **minimum order price $60.00** → **$0.00**
   - `Standard shipping` — **$0.00–$59.99** → **$5.95**
3. **Rename** "International" → "Rest of World", remove the US from it, set a flat **$14.95**
   (or turn it off entirely and sell US-only while you learn — simpler, and recommended).

That $60 free-shipping threshold is deliberate: it pushes buyers to the **$65 Haunt The Whole
House** and **$89 Uncle Pack** bundles, which is where your margin actually lives.

## 4 · Store name

**Settings → General → Store name** → currently **"My Store"** → **Deadpan Goods**.

---

## Verify

```
[ ] Currency reads USD, products show $49 / $34 / $65
[ ] Timezone correct
[ ] "United States" zone exists with free-over-$60 and $5.95
[ ] Brazil zone deleted, US removed from International
[ ] Store name is Deadpan Goods
[ ] Test checkout as a US address → shipping shows $5.95 or free
```

**Do not run a single ad until that last line passes.**

---

## Later: Shopify Markets (optional, Advanced includes it)

Once US is working, **Settings → Markets** lets you sell internationally with auto-converted
local pricing. Worth it in H2 — ignore it until the US market is profitable. One market done
well beats five done badly.
