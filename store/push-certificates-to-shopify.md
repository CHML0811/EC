# Push the 16 certificates into Shopify — runbook

> ## ⚠️ Superseded — use the script instead
>
> **[`store/upload_to_shopify.py`](upload_to_shopify.py)** does everything below in one
> command, plus policies, pages, variants and prices. It needs no MCP connector and no
> dependencies:
>
> ```bash
> export SHOPIFY_STORE=fbapgj-si.myshopify.com
> export SHOPIFY_TOKEN=shpat_...
> python3 store/upload_to_shopify.py --all            # dry run
> python3 store/upload_to_shopify.py --all --execute
> ```
>
> This document is kept as the reference for what each mutation does, and for anyone
> pasting into **Admin → Apps → Shopify GraphiQL** by hand.
>
> Note the script uploads the **framed mockups** as the featured image, not the flat
> artwork — a product photo converts, a bare PNG doesn't.

## ~~Step 1 and 2 are DONE for cohort 1~~ — expired

The eight staged URLs below expired on **2026-08-16 15:36 UTC**. They are dead. Any run
starts from step 1.

These were the staged URLs. They are listed only so it's clear they were used and are
now dead — **do not try to resume from them**:

```
https://shopify-staged-uploads.storage.googleapis.com/tmp/78201487407/files/52608d0b-a039-4a0c-9528-3f409f3b412b/bma-retirement.png
https://shopify-staged-uploads.storage.googleapis.com/tmp/78201487407/files/5f72686e-a7b2-4a14-b8cb-9d595ec0dbd1/bma-coworker.png
https://shopify-staged-uploads.storage.googleapis.com/tmp/78201487407/files/46c2d8bd-d4db-496f-bfd1-0fcd7282bb92/bma-uncle.png
https://shopify-staged-uploads.storage.googleapis.com/tmp/78201487407/files/c15c9469-5272-4a40-9f67-68beba7b92cf/bma-boss.png
https://shopify-staged-uploads.storage.googleapis.com/tmp/78201487407/files/4f03cfeb-0455-4345-b185-30df17e2b834/bma-new-home.png
https://shopify-staged-uploads.storage.googleapis.com/tmp/78201487407/files/774feb46-ab4a-4d08-ab44-41175f4e8fa0/bma-new-parent.png
https://shopify-staged-uploads.storage.googleapis.com/tmp/78201487407/files/fe79b459-45d3-48d6-9ecb-547886beb29b/bma-graduation.png
https://shopify-staged-uploads.storage.googleapis.com/tmp/78201487407/files/3b465a13-600f-4090-bdb1-5f1b3f4cc126/bma-left-on-read.png
```

Cohort 2 (the eight `bma-x-*` files) was never uploaded.

> These are the certificate artwork files. Better listing imagery already exists in
> `design/mockups/` — use `<slug>-1-framed.png` as each product's featured image and keep
> the flat artwork as a secondary. See [`design/listing-images.md`](../design/listing-images.md).

---


Every mutation below is **schema-validated** against the Admin API, and the staged-upload
path was executed successfully for real. `upload_to_shopify.py` automates all of it; this
remains the reference for what each step does.

---

## Step 1 — request upload slots

```graphql
mutation StageUploads($input: [StagedUploadInput!]!) {
  stagedUploadsCreate(input: $input) {
    stagedTargets { url resourceUrl parameters { name value } }
    userErrors { field message }
  }
}
```

Variables — one entry per file (16 total; first two shown):

```json
{
  "input": [
    { "filename": "bma-retirement.png", "mimeType": "image/png", "resource": "IMAGE", "httpMethod": "POST" },
    { "filename": "bma-coworker.png",   "mimeType": "image/png", "resource": "IMAGE", "httpMethod": "POST" }
  ]
}
```

Full filename list:
```
bma-retirement.png      bma-coworker.png     bma-uncle.png         bma-boss.png
bma-new-home.png        bma-new-parent.png   bma-graduation.png    bma-left-on-read.png
bma-x-secret-santa.png  bma-x-white-elephant.png  bma-x-survived-year.png  bma-x-office-party.png
bma-x-okayest-gift.png  bma-x-mom.png        bma-x-dad.png         bma-x-stocking.png
```

## Step 2 — upload the bytes

Each `stagedTarget` returns a `url` and a list of `parameters`. POST them as multipart form
fields **in order**, with `file` **last**:

```bash
# for each target: every parameter as -F, then the file
curl -X POST "$URL" \
  -F "key=$KEY" -F "policy=$POLICY" -F "x-goog-signature=$SIG" ... \
  -F "file=@design/out/bma-retirement.png"
```

`file` must be the final field or the upload is rejected.

## Step 3 — register the files

```graphql
mutation MakeFiles($files: [FileCreateInput!]!) {
  fileCreate(files: $files) {
    files {
      id
      fileStatus
      alt
      ... on MediaImage { image { url width height } }
    }
    userErrors { field message }
  }
}
```

```json
{
  "files": [
    { "originalSource": "<resourceUrl from step 1>", "contentType": "IMAGE",
      "alt": "Certificate of Minor Achievement — Retirement, Bureau of Minor Achievements" }
  ]
}
```

`fileStatus` returns `UPLOADED`, then flips to `READY` after processing. **Poll until READY**
before using the CDN url — attaching too early gives a broken image.

```graphql
{ files(first: 20, query: "media_type:IMAGE") {
    edges { node { id fileStatus ... on MediaImage { image { url } } } } } }
```

## Step 4 — attach to products

For the 8 cohort-1 certificates, create products via `create-product` with the CDN url, or
attach to existing ones:

```graphql
mutation AddMedia($productId: ID!, $media: [CreateMediaInput!]!) {
  productCreateMedia(productId: $productId, media: $media) {
    media { alt status }
    mediaUserErrors { field message }
  }
}
```

```json
{ "productId": "gid://shopify/Product/...",
  "media": [{ "originalSource": "<CDN url>", "alt": "...", "mediaContentType": "IMAGE" }] }
```

---

## Product payload for the 8 certificates

Titles, descriptions and tags: `marketing/etsy-cohort-1.md`. Common settings:

| Field | Value |
|---|---|
| Vendor | `The Bureau of Minor Achievements` |
| Product type | `Wall Art` |
| Status | `DRAFT` |
| Options | `Size` → `8x10 Print`, `11x14 Print`, `8x10 Framed` |
| Prices | `32.00` / `42.00` / `58.00` |
| Inventory | tracking **off** |
| Tags | from `marketing/etsy-cohort-*.md`, + `season:christmas` on `bma-x-*` |

## Verify

```
[ ] 16 files READY in Shopify Files
[ ] 8 certificate products exist with a featured image
[ ] Prices read $32 / $42 / $58
[ ] Still DRAFT — nothing public until Etsy goes live the same day
```
