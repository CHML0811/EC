# Project context for AI assistants

Read this before touching anything. Cursor loads `AGENTS.md` automatically; if you're in a
tool that doesn't, paste it into the chat first.

**Doing the work, not reading about it? → [`TODO.md`](TODO.md).** Ordered, with acceptance
criteria and paste-ready prompts.

## What this is

**The Bureau of Minor Achievements** — a fictional government agency issuing official
certificates for things that don't deserve recognition. Three products, all built:

| | | |
|---|---|---|
| **Office Awards Kit** | $14.99 digital · 8.2 MB | 38 certificates + offline maker + host's script |
| **Classroom Awards Kit** | price unset · 2.8 MB | 12 certificates + offline maker + teacher's script |
| **Physical certificates** | $32–58 via Printify | 16 listings written, Printify not started |

Sold on **Etsy** (search intent does the marketing), with Shopify as the brand home and the
bulk-order desk.

Run by one person with no ecommerce experience, no supplier relationships, no audience, and
no US presence. Every decision has to respect that.

## Non-negotiables

These were each decided against a real alternative. Don't quietly reverse them.

| Rule | Why |
|---|---|
| **Never invent a number** | No fake review counts, sales figures, or "as seen in". Ever. |
| **Never invent a price** | Two prices are deliberately unset pending live Etsy grid data. Guessing compounds an error rather than fixing it. |
| **US English in buyer-facing copy** | Etsy tag matching is literal. `personalised` ≠ `personalized`. |
| **Etsy tags: exactly 13, each ≤ 20 characters** | Over 20 and Etsy silently rejects the tag. |
| **No tag shared between two listings** | A shared primary keyword means Etsy buries one of them. Enforced by `store/build_launch_console.py`. |
| **No AI-generated humans in marketing** | Uncanny valley kills trust. See `marketing/video-playbook.md`. |
| **Image-to-video only, never text-to-video** | Video models mangle typography and this product *is* typography. |
| **Paper and digital, not apparel** | Apparel margin is far worse after print costs. |
| **Etsy takes ~11%, not 23%** | 6.5% + 3% + $0.25 + $0.20. The extra 15% is Offsite Ads, applies **only** to ad-driven sales, optional under $10k/yr. |
| **Don't add new product *types* before 10 sales** | Mugs, apparel, sourced goods. Reasoning in `playbooks/product-decision.md`. |
| **More listings of what exists is not a new SKU** | That distinction is the whole growth plan. A new cohort reuses everything; a mug needs a supply chain. |
| **Check IP before any new design** | No brands, characters, logos, or licensed anything. |
| **Classroom awards are about situations, never children** | Never ability, effort, behavior or appearance. These are read out in front of parents. |

## The voice

Deadpan bureaucracy. The joke works *because the document refuses to admit there is one*.

- ✅ *"for opinions delivered at volume, jokes repeated annually, and an unbroken record of standing near the grill without cooking."*
- ❌ *"LOL! The world's funniest uncle award! 😂"*

Never explain the joke. Never use exclamation marks in product copy. Specific beats clever —
"9:14 every morning" is funny, "always late" is not. Punch at situations, never at people.

## How everything builds

Pure Python 3 + headless Chrome. **No dependencies, no package manager, nothing to install.**
Chrome renders HTML to PNG and PDF; that's the entire toolchain.

**Before and after any change:** `python3 verify.py` — 15 checks covering Chrome, every build
script compiling, Etsy tag limits, US spelling in buyer-facing copy, doc links, cohort
counts, and whether the launch console still matches the listing docs. Exits non-zero on
failure. `--full` rebuilds everything and checks the output too.

**First run on a new machine:** a fresh clone has the source but not the build artifacts —
the zips and `design/out/` are gitignored. Two commands rebuild everything:

```bash
python3 kit/build_kit.py             # 38 certificates + Office-Awards-Kit.zip, ~90 sec
python3 kit/build_kit.py --school    # 12 certificates + Classroom-Awards-Kit.zip
```

If that fails with "No Chrome or Chromium found", install Chrome or point at it:
`export CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'`

```bash
# artwork — 2400×3000 @ 300dpi
python3 design/generate_certificates.py    # 8 general occasions   (cohort 1)
python3 design/certs_christmas.py          # 8 Christmas           (cohort 2)
python3 design/certs_office.py             # 22 office awards      (cohort 3)
python3 design/certs_school.py             # 12 classroom awards   (cohort 4)

# imagery — cohorts 1+2 only, by design. Cohorts 3 and 4 ship inside the kits and have
# never been listed individually, so mockups for them would be unusable repo weight.
python3 design/generate_mockups.py         # 96 Etsy/Pinterest listing images
python3 design/generate_crops.py           # 82 channel crops

# the digital products
python3 kit/build_kit.py                   # → kit/Office-Awards-Kit.zip    (8.2 MB)
python3 kit/build_kit.py --school          # → kit/Classroom-Awards-Kit.zip (2.8 MB)
python3 kit/build_listing_images.py             # → kit-1…4      (office)
python3 kit/build_listing_images.py --christmas # → kit-x1-hero  (Christmas)
python3 kit/build_listing_images.py --school    # → kit-s1…s4    (classroom)

# the tool you actually work from — generated from marketing/*.md, never hand-edited
python3 store/build_launch_console.py      # → store/etsy-launch-console.html

# storefront
python3 site/build_storefront.py <previews> --local site/index.html

# push the shop to Shopify — needs an Admin API token, no connector involved
export SHOPIFY_STORE=... SHOPIFY_TOKEN=shpat_... SHOPIFY_SUPPORT_EMAIL=you@real.com
python3 store/upload_to_shopify.py --all              # dry run — the default
python3 store/upload_to_shopify.py --all --execute
```

`design/generate_certificates.py:find_chrome()` checks this container's path, then the
standard macOS / Windows / Linux install locations, then PATH. `CHROME=/path/to/chrome`
overrides everything.

## Two structural rules the build depends on

**1. Cohorts are named from manifests, never globbed.** `kit/build_kit.py` has a `KITS` dict;
each kit lists the manifests it ships. This used to glob `design/out/bma-*.png`, so adding
the classroom cohort silently swept 12 extra certificates into the Office kit — the zip would
have carried 50 while the listing sold 38, and nothing failed. **A new cohort is a dict entry.
Never go back to globbing.**

**2. Buyer-facing copy lives in `marketing/*.md` and nowhere else.** The launch console is
generated from those docs by `store/build_launch_console.py`. It used to hardcode the copy,
and drifted: the published console carried an old title, a superseded tag set and a price
that had changed twice. `verify.py` now regenerates and diffs, so staleness fails. **Edit the
markdown, then rebuild the console. Never edit the HTML directly.**

## Things that will bite you

Each of these was a real bug, found and fixed. Don't reintroduce them.

**Rendering**
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
  long. `design/generate_crops.py` measures with `getBoundingClientRect` instead.
- **A tile grid built for 38 items overflows at 12.** Four-across tiles are far taller than
  eight-across and pushed the caption off the sheet. `scene_grid` caps its width below 20 items.

**Shopify** — all three found by running against the live store, none catchable in a dry run
- **`productCreate` does not fan option values out into variants.** It returns ONE variant on
  the first value. The other sizes need `productVariantsBulkCreate` afterwards.
- **Variants from `productVariantsBulkCreate` default to `tracked: true` at quantity 0**,
  unlike the one `productCreate` makes. That silently showed 11x14 and Framed as *sold out*
  on all 16 print products. Pass `inventoryItem: {tracked: false}`.
- **A digital product still defaults to `requiresShipping: true`.** Checkout demands an
  address and adds shipping to a download. Set it false explicitly.
- **The connector's token lacks `write_legal_policies`.** Policies must go through
  `store/upload_to_shopify.py` with a custom app token, or be pasted by hand.
- **Shopify staged upload URLs expire after 24 hours.** Don't stage files you aren't about to
  register. For product images, a public `originalSource` URL is simpler — Shopify fetches it.
- **The MCP connectors drop constantly.** Fifteen-plus times in one session, and several more
  mid-mutation. Anything that must talk to Shopify should be able to run through
  `store/upload_to_shopify.py`, which uses the Admin API directly.

**Parsing**
- **A markdown parser that only closes a section at the next section of the same kind will
  swallow the one after it.** The listing parser absorbed the bundle section's copy into the
  last Christmas listing. Any `##` closes a listing now.
- **`str.format` breaks on CSS braces.** Use `<!--TOKEN-->` replacement in HTML templates.
- **Hard-wrapped markdown becomes one `<p>` per line** unless you join paragraphs first,
  which splits sentences mid-clause on the storefront.

## Where things are

```
TODO.md                              ← the ordered task list. Start here.
HANDOFF.md                           the 45-minute path to a live listing
playbooks/first-seller-strategy.md   why digital, why not t-shirts
playbooks/etsy-market-fit.md         who buys on Etsy, and the six cheapest expansions
playbooks/will-this-sell.md          what was verified vs assumed, and the gap
playbooks/where-to-sell.md           real fee numbers, Etsy vs own site
playbooks/product-decision.md        what to sell next, and what to refuse
marketing/etsy-office-awards-kit.md  listing #1 — title, 13 tags, description
marketing/etsy-christmas-awards-kit.md listing #2 — same zip, seasonal keywords
marketing/etsy-teacher-awards-kit.md listing #3 — classroom, needs a price
marketing/etsy-cohort-1.md           8 physical listings
marketing/etsy-cohort-2-christmas.md 8 Christmas physical listings
marketing/video-playbook.md          hooks, Grok prompts, what made the last video bad
store/build_launch_console.py        generates the console from the listing docs
store/etsy-launch-console.html       GENERATED — do not hand-edit
store/upload_to_shopify.py           one command: products, images, policies, pages
store/policies-and-pages.md          the four policies + About and FAQ
store/printify-setup-spec.md         exact blank, provider, sizes, prices
design/  kit/  site/                 build scripts, documented in their docstrings
prompts/                             ⚠️ ARCHIVED football-direction prompts. Do not follow.
```

## Where the business actually stands

| | |
|---|---|
| Etsy | ❌ **No account. This is the only thing blocking revenue.** |
| Listings written | 3 (office, Christmas, classroom) — none published |
| Shopify catalog | ✅ 17 products live in admin, all DRAFT, images and prices set |
| Shopify pages | ✅ About, FAQ, 4 collections, both menus wired |
| Shopify policies | ❌ Blocked on API scope — paste by hand or use a custom app token |
| Digital delivery | ❌ No app installed. **Activating the kit product without it means a buyer pays and gets nothing.** |
| Shopify plan | ⚠️ Advanced $399/mo. Nothing here uses an Advanced feature. |
| Printify | ❌ Not started, and not needed until the physical line goes live |
| Revenue | **$0.** Nothing has sold. |

## The one thing that matters

**Nothing has sold yet.** Every file here is preparation. The only action that changes that is
publishing on Etsy — which needs no Printify, no card on file, and no shipping setup.

Before adding anything new, ask whether it gets a listing live faster. If not, it can wait.
Building is easy and listing is boring; that asymmetry is the main risk to this project.
