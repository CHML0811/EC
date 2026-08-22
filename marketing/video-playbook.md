# The video playbook — how not to make another piece of trash

Your last attempt failed for reasons that are known and fixable. This is the diagnosis, the
current data, and the exact prompts.

**One thing stated plainly up front: nobody can guarantee a video goes viral, and anyone who
tells you otherwise is selling something.** What you can do is stack the odds — use the hook
type that measurably outperforms, respect the metric the algorithm actually ranks on, and
ship ten variants instead of one. Then let the data pick the winner. That's the whole method.

---

## Why the last one was trash

Four failure modes, all avoidable:

| What went wrong | Why it kills the video |
|---|---|
| **AI-generated humans** | The uncanny valley tell in 2026 isn't the face — it's **speech patterns**. Dramatic close-ups still break. Viewers who sense AI discount the whole thing. ([uncanny valley 2026](https://hailuoai.video/pages/blog/uncanny-valley-effect-ai-video-explained), [AI vs real UGC](https://inbeat.agency/blog/ai-ugc-ads-vs-real-ugc)) |
| **Text-to-video for a text product** | Every video model mangles typography. Our entire product *is* typography. Text-to-video will produce a certificate covered in melted gibberish letters. |
| **One video** | The only real advantage AI gives you is volume. One AI video is strictly worse than one real video. Ten AI videos beat both. |
| **No product in the first 2 seconds** | 90% of underperforming TikToks fail in the first three seconds. ([hook data](https://www.opus.pro/blog/tiktok-hooks-that-go-viral-2026)) |

---

## What the data says now

**The algorithm changed in Q2 2026. It ranks on 3-second retention above everything else** —
a video holding 80% of viewers at 3 seconds out-distributes one holding 60% at 30 seconds.
63% of top-performing videos win their audience inside those three seconds, and 71% of users
have already decided. ([TikTok hook research](https://www.opus.pro/blog/tiktok-hooks-that-go-viral-2026), [hook guide](https://www.lemonlight.com/blog/the-top-10-hooks-businesses-can-use-to-make-tiktok-marketing-work/))

**The highest-performing hook type is the Product or Outcome Showcase** — showing the
finished thing in the first two seconds. It averages roughly **2× the views** of the
worst-performing hook type. Not a clever line. The product.

**AI video lands within 5–20% of real creator content on the metrics** — and testing ten
hooks instead of one more than covers that gap. ([AI UGC vs real](https://inbeat.agency/blog/ai-ugc-ads-vs-real-ugc))

**Grok Imagine, concretely:** 15 seconds per clip (30s by stitching), **720p ceiling**, and
critically — **it does image-to-video, not just text-to-video.** ([Grok limits](https://vmake.ai/blog/grok-xai-video-generation-length-limit), [capabilities](https://pixverse.ai/en/blog/grok-imagine-video-generation-capabilities-2026))

---

## The five rules

1. **Image-to-video only. Never text-to-video.** Start every clip from a real PNG in this
   repo. The model animates our actual certificate instead of hallucinating one. This single
   rule eliminates the melted-typography failure entirely.
2. **No AI humans.** No faces, no talking heads, no voiceover from a synthetic voice. Hands
   are borderline; avoid them too. The product is an object — shoot the object.
3. **Product visible at 0:00.** Not at 0:03. The highest-performing hook type is literally
   "show the thing immediately."
4. **The joke arrives as on-screen text**, in the platform's own caption style. Text is free,
   instant, and cannot go uncanny.
5. **Ten variants minimum.** Same product, ten different first-lines. This is the only
   reason to use AI at all.

---

## Tier A — the best video needs no AI at all

**Screen-record the Awards Maker.** Open `AwardsMaker.html`, hit *Whole team*, paste ten
names, press print, watch ten finished certificates appear.

This beats anything Grok can generate, and it isn't close:

- It **is** a product/outcome showcase — the #1 hook type, by definition
- Zero uncanny valley risk, because nothing is generated
- It proves the product is real software, which is the actual objection blocking the sale
- It costs nothing and takes four minutes

**Shoot it like this:**

| Time | On screen | Caption |
|---|---|---|
| 0:00–0:02 | Names already pasted in. Cursor moves to Print. | `POV: you have to run the office awards and you have 20 minutes` |
| 0:02–0:05 | Print preview fills with certificate after certificate | `it makes one for every single person` |
| 0:05–0:09 | Scroll the print preview fast — page after page | `38 different awards` |
| 0:09–0:12 | Stop on the funniest one, hold still so it's readable | *(let the certificate be the punchline)* |
| 0:12–0:15 | Cut to the printed stack | `nobody gets left out. that's the whole trick.` |

Record at 1080×1920. Use a trending audio, not music you picked.

## Tier B — Grok, for b-roll and atmosphere

Use Grok for the 2–4 second establishing shots that make Tier A feel produced. Always
image-to-video, always from a file in this repo.

**Every prompt must carry this clause**, or the model will rewrite the text on the
certificate into nonsense:

> `Do not alter, warp, re-render or regenerate any text, lettering, seal or border in the
> source image. All typography must remain perfectly static, sharp and legible. Camera and
> lighting move; the artwork does not.`

### Prompt 1 — the wall reveal
**Source:** `design/mockups/retirement-1-framed.png`
```
Slow, steady push-in toward a framed certificate hanging on a warm neutral wall. Very
subtle handheld drift. Soft afternoon window light moves almost imperceptibly across the
glass. Shallow depth of field. Calm, premium, understated. Do not alter, warp, re-render or
regenerate any text, lettering, seal or border in the source image. All typography must
remain perfectly static, sharp and legible. Camera and lighting move; the artwork does not.
```

### Prompt 2 — the desk drop
**Source:** `design/out/bma-o-punctuality.png`
```
Top-down view of a printed certificate resting on a plain wooden desk. Gentle parallax as
the camera rises slightly. Dust motes drift in a shaft of window light. Faint paper texture
catches the light. No people, no hands. Do not alter, warp, re-render or regenerate any
text, lettering, seal or border in the source image. All typography must remain perfectly
static, sharp and legible. Camera and lighting move; the artwork does not.
```

### Prompt 3 — the stack
**Source:** `design/crops/hero-wide.png`
```
Three certificates fanned on a desk. Extremely slow lateral camera slide revealing them one
by one. Warm office light, late afternoon. Quiet, deadpan, no motion in the paper itself.
Do not alter, warp, re-render or regenerate any text, lettering, seal or border in the
source image. All typography must remain perfectly static, sharp and legible. Camera and
lighting move; the artwork does not.
```

**Settings:** vertical 9:16, 720p (Grok's ceiling — do not fight it), 5–6 seconds per clip.
Generate **four takes of each** and bin three. At $0.08/second that's about $1.50 for a
dozen usable seconds.

**Check every clip at full size before using it.** If a single letter has warped, throw it
away. A certificate with garbled text is worse than no video, because it makes the *product*
look fake.

## Tier C — never

- AI-generated people, faces, or synthetic voiceover
- Text-to-video for anything showing a certificate
- Any clip where you have to squint to check whether the text survived
- Stock footage of a generic "happy office team"

---

## The ten hooks to test

Same video, ten different opening captions. Hook types drawn from what's ranking now —
product showcase, curiosity gap, and the "most people get this wrong" family.

| # | Opening caption | Type |
|---|---|---|
| 1 | `POV: you have to run the office awards and you have 20 minutes` | POV / product |
| 2 | `the certificate that got the loudest reaction at our christmas party` | Outcome |
| 3 | `we gave everyone in the office an award for their worst habit` | Curiosity |
| 4 | `most office awards fail for one reason: not everyone gets one` | Most-get-wrong |
| 5 | `stop giving out "employee of the month" if you want people to laugh` | Stop doing X |
| 6 | `there is a Certificate of Approximate Punctuality and someone is getting it` | Absurd specific |
| 7 | `reading these out loud is the entire joke` | Curiosity gap |
| 8 | `38 awards. nobody gets left out. that's the whole trick.` | Product showcase |
| 9 | `here's what nobody tells you about running office awards` | Nobody-tells-you |
| 10 | `my coworker's face when they got "Permanent Audio Only"` | Reaction |

**Post one per day for ten days.** Same video body, different first two seconds. Change
nothing else — otherwise you learn nothing about which hook won.

---

## How to read the result

Watch **3-second retention**, in TikTok analytics, and nothing else at first.

| 3s retention | What it means | Do |
|---|---|---|
| Below 50% | Hook failed | Kill it. Don't touch the video body. |
| 50–70% | Hook works, body doesn't | Keep the hook, recut everything after 0:03 |
| Above 70% | Winner | Make five more variants of *this* hook |

**Do not judge on likes or follows.** Watch time is what gets distribution; likes are what
happens after distribution. Optimizing for likes is optimizing for the wrong end of the
chain.

**If all ten sit under 50%**, the problem isn't the hooks — it's that the product needs
showing rather than describing. Go back to Tier A and make the screen recording longer and
faster.

---

## The honest expectation

Ten videos from a new account with no following will most likely produce: eight that get
200–800 views, one that gets a few thousand, and possibly one that breaks out. **That's a
normal, healthy result** — not a failure.

The breakout is not the goal. **Finding which hook holds 70% at three seconds is the goal**,
because that hook is then reusable forever, in ads, in the Etsy listing's first image, and in
every video after it.

And remember which channel is actually doing the work: **Etsy search is the sales engine
here.** Video is a supplement. If you have one hour, publishing the Etsy listing beats making
a video, every time.
