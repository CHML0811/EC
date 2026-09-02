# Project context for AI assistants

Read this before touching anything. Cursor loads `AGENTS.md` automatically; if you're in a
tool that doesn't, paste it into the chat first.

## What this is

**The Bureau of Minor Achievements** — a fictional government agency issuing official
certificates for things that don't deserve recognition. Sold two ways:

1. **The Office Awards Kit** — $24 digital download. 38 certificates + an offline maker +
   a host's script. Zero cost per sale. **This is the priority.**
2. **Physical certificates** — $32–58 prints via Printify. Built, not yet listed.

Sold on **Etsy** (search intent does the marketing) with Shopify as the brand home.

Run by one person with no ecommerce experience, no supplier relationships, no audience, and
no US presence. Every decision has to respect that.

## Non-negotiables

These were each decided against a real alternative. Don't quietly reverse them.

| Rule | Why |
|---|---|
| **Never invent a number** | No fake review counts, sales figures, or "as seen in". Ever. |
| **US English in buyer-facing copy** | Etsy tag matching is literal. `personalised` ≠ `personalized`. |
| **Etsy tags ≤ 20 characters, exactly 13** | Over 20 and Etsy silently rejects the tag. |
| **No AI-generated humans in marketing** | Uncanny valley kills trust. See `marketing/video-playbook.md`. |
| **Image-to-video only, never text-to-video** | Video models mangle typography and this product *is* typography. |
| **Paper and digital, not apparel** | Apparel keeps ~14% after Etsy fees; paper keeps 40–55%. |
| **Don't add SKUs before 10 sales** | Reasoning in `playbooks/product-decision.md`. |
| **Check IP before any new design** | No brands, characters, logos, or licensed anything. |

## The voice

Deadpan bureaucracy. The joke works *because the document refuses to admit there is one*.

- ✅ *"for opinions delivered at volume, jokes repeated annually, and an unbroken record of standing near the grill without cooking."*
- ❌ *"LOL! The world's funniest uncle award! 😂"*

Never explain the joke. Never use exclamation marks in product copy. Specific beats clever —
"9:14 every morning" is funny, "always late" is not.

## How everything builds

Pure Python 3 + headless Chrome. **No dependencies, no package manager, nothing to install.**
Chrome renders HTML to PNG and PDF; that's the entire toolchain.

**Before and after any change:** `python3 verify.py` — 13 checks covering Chrome, every
build script compiling, Etsy tag limits, US spelling in buyer-facing copy, and doc links.
Exits non-zero on failure. `--full` rebuilds everything and checks the output too.

**First run on a new machine:** a fresh clone has the source but not the build artifacts —
`kit/Office-Awards-Kit.zip` and `design/out/` are gitignored. One command rebuilds them:

```bash
python3 kit/build_kit.py     # 38 certificates + the zip, ~90 seconds
```

If that fails with "No Chrome or Chromium found", install Chrome or point at it:
`export CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'`

```bash
# artwork — 38 certificates, 2400×3000 @ 300dpi
python3 design/generate_certificates.py    # 8 general occasions   (cohort 1)
python3 design/certs_christmas.py          # 8 Christmas           (cohort 2)
python3 design/certs_office.py             # 22 office awards      (cohort 3)

# imagery — cohorts 1+2 only, by design. Cohort 3 ships inside the kit and has never
# been listed individually, so mockups for it would be ~50 MB of unusable repo weight.
python3 design/generate_mockups.py         # 96 Etsy/Pinterest listing images
python3 design/generate_crops.py           # 82 channel crops (story, feed, OG, banners)

# the digital product — runs the whole chain and zips it
python3 kit/build_kit.py                   # → kit/Office-Awards-Kit.zip (8.2 MB)
python3 kit/build_listing_images.py        # → kit/listing/*.png

# storefront
python3 site/build_storefront.py <previews> --local site/index.html

# push the shop to Shopify — needs an Admin API token, no connector involved
export SHOPIFY_STORE=... SHOPIFY_TOKEN=shpat_...
python3 store/upload_to_shopify.py --all              # dry run — the default
python3 store/upload_to_shopify.py --all --execute
```

`design/generate_certificates.py:find_chrome()` checks this container's path, then the
standard macOS / Windows / Linux install locations, then PATH. `CHROME=/path/to/chrome`
overrides everything.

## Things that will bite you

Each of these was a real bug, found and fixed. Don't reintroduce them.

- **Chromium's `--force-device-scale-factor` below 1 does not scale the layout.** It captures
  a smaller window of the same page — you get the top-left corner. To downscale, put the PNG
  in an `<img>` at the target size and screenshot that.
- **`--print-to-pdf` and `--screenshot` need absolute `file://` URIs.** `pathlib.as_uri()`
  throws on a relative path.
- **A class selector beats an element selector.** `.wrap{padding:…}` on a `<section>` silently
  cancels `section{padding:…}`. Use `padding-inline` / `padding-block`.
- **`fieldset{display:flex}` overrides the browser's `[hidden]`.** Restate
  `[hidden]{display:none!important}`.
- **`preserveAspectRatio="none"` SVGs need an explicit width**, or they render short.
- **Certificate text is flex-centred**, so hard-coded crop offsets drift when a citation runs
  long. `design/generate_crops.py` measures with `getBoundingClientRect` instead — follow that
  pattern.
- **The MCP connectors drop constantly.** Fifteen-plus times in one session. Anything that
  has to talk to Shopify should go through `store/upload_to_shopify.py`, which uses the
  Admin API directly and doesn't depend on a connector being up.
- **Shopify staged upload URLs expire after 24 hours.** Don't stage files you aren't about
  to register.

## Where things are

```
playbooks/first-seller-strategy.md   ← read this first. Why digital, why not t-shirts.
playbooks/product-decision.md        what to sell next, and what to refuse
marketing/video-playbook.md          hooks, Grok prompts, what made the last video bad
marketing/etsy-office-awards-kit.md  the $24 listing — title, 13 tags, description
marketing/etsy-cohort-1.md           8 physical listings
marketing/etsy-cohort-2-christmas.md 8 Christmas listings (publish by Oct 1)
store/paste-sheet.html               every Etsy field with copy buttons
store/printify-setup-spec.md         exact blank, provider, sizes, prices
store/upload_to_shopify.py           one command: products, images, policies, pages
store/push-certificates-to-shopify.md the same thing by hand — superseded, kept as reference
prompts/                             ⚠️ ARCHIVED football-direction prompts. Do not follow.
design/  kit/  site/                  build scripts, all documented in their docstrings
```

## The one thing that matters

**Nothing has sold yet.** Every file here is preparation. The only action that changes that is
publishing the Office Awards Kit on Etsy — which needs no Printify, no card on file, and no
shipping setup.

Before adding anything new, ask whether it gets that listing live faster. If not, it can wait.
