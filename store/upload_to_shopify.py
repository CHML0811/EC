#!/usr/bin/env python3
"""
Upload the whole shop to Shopify — products, images, policies and pages.

Talks to the Admin API directly over stdlib urllib. No MCP connector, no dependencies,
nothing to install. The connector dropped fifteen-plus times while this project was built;
this exists so that stops mattering.

    # 1. Shopify admin → Settings → Apps and sales channels → Develop apps
    #    → Create an app → Configure Admin API scopes → tick:
    #         write_products, write_files, write_legal_policies, write_online_store_pages
    #    → Install app → reveal the Admin API access token (starts shpat_)
    export SHOPIFY_STORE=fbapgj-si.myshopify.com
    export SHOPIFY_TOKEN=shpat_xxxxxxxxxxxxxxxx

    python3 store/upload_to_shopify.py --all              # dry run: prints, sends nothing
    python3 store/upload_to_shopify.py --all --execute    # actually writes

Dry run is the default on purpose. Nothing is sent until --execute.

Idempotent: products are matched on handle and skipped if they already exist, so a run
that dies halfway can simply be run again. Use --force to update matched products anyway.

Status: the product and page paths have now been run against the live store
(fbapgj-si.myshopify.com) via the Shopify connector — 17 products with images and three
priced variants each, plus the About and FAQ pages. Two bugs that only showed up against a
real store are fixed here: productCreate returns ONE variant rather than fanning out the
option values, and the listing parser used to swallow the copy from the section after the
last listing.

⚠️  Still untested from this script directly: policies. The connector's token lacks
`write_legal_policies`, so shopPolicyUpdate was rejected there. A custom app token with that
scope should work — that is what this script is for. Start with `--policies --execute` and
check Settings → Policies afterwards.
"""

import argparse
import json
import mimetypes
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request
import uuid

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = "2025-01"

PRICES = [("8x10 Print", "32.00"), ("11x14 Print", "42.00"), ("8x10 Framed", "58.00")]
IMAGE_ORDER = ["1-framed", "2-hook", "3-detail", "4-sizes", "5-info"]

LISTINGS = [
    (ROOT / "marketing" / "etsy-cohort-1.md", []),
    (ROOT / "marketing" / "etsy-cohort-2-christmas.md", ["season:christmas"]),
]

POLICY_TYPES = {
    "Refund Policy": "REFUND_POLICY",
    "Shipping Policy": "SHIPPING_POLICY",
    "Privacy Policy": "PRIVACY_POLICY",
    "Terms of Service": "TERMS_OF_SERVICE",
}


# ----------------------------------------------------------------- transport
class Shopify:
    def __init__(self, store: str, token: str, execute: bool):
        self.url = f"https://{store}/admin/api/{API}/graphql.json"
        self.token = token
        self.execute = execute
        self.calls = 0

    def __call__(self, query: str, variables: dict | None = None, label: str = "") -> dict:
        if not self.execute:
            name = label or query.strip().split("(")[0].split()[-1]
            print(f"    [dry-run] would call {name}")
            return {}
        body = json.dumps({"query": query, "variables": variables or {}}).encode()
        req = urllib.request.Request(self.url, data=body, headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.token,
        })
        # Shopify throttles on a leaky bucket; 429 and 5xx are both worth retrying
        for attempt in range(5):
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    payload = json.loads(r.read())
                break
            except urllib.error.HTTPError as e:
                if e.code in (429, 500, 502, 503, 504) and attempt < 4:
                    wait = 2 ** attempt
                    print(f"    HTTP {e.code}, retrying in {wait}s")
                    time.sleep(wait)
                    continue
                raise SystemExit(f"Shopify error {e.code}: {e.read().decode()[:400]}")
        self.calls += 1
        if payload.get("errors"):
            raise SystemExit(f"GraphQL error: {json.dumps(payload['errors'])[:600]}")
        # every mutation nests its own userErrors; surface them rather than failing silently
        for key, val in (payload.get("data") or {}).items():
            if isinstance(val, dict):
                errs = val.get("userErrors") or val.get("mediaUserErrors") or []
                if errs:
                    raise SystemExit(f"{key} userErrors: {json.dumps(errs)[:600]}")
        return payload.get("data") or {}


# ----------------------------------------------------------------- listings
def parse_listings(path: pathlib.Path, extra_tags: list[str]) -> list[dict]:
    """Read the Etsy listing docs so titles and tags have exactly one source of truth."""
    out, cur = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            # Any h2 closes the current listing. Sections like `## Bundle — ...` and
            # `## Publishing checklist` are not listings, but they do carry blockquotes,
            # and without this the last listing swallowed their copy.
            if cur:
                out.append(cur)
            m = re.match(r"^## \d+ · .+ — `bma-(.+)\.png`", line)
            cur = ({"slug": m.group(1), "title": "", "tags": [], "desc": []}
                   if m else None)
            continue
        if not cur:
            continue
        if line.startswith("**Title:**"):
            cur["title"] = line.split("`")[1]
        elif line.startswith("**Tags:**"):
            cur["tags"] = [t.strip(" `") for t in line[9:].split("·")] + extra_tags
        elif line.startswith("> "):
            cur["desc"].append(line[2:].strip())
        elif line.strip() == ">":
            cur["desc"].append("")
    if cur:
        out.append(cur)
    return out


BOLD = re.compile(r"\*\*(.+?)\*\*")


def to_html(lines: list[str]) -> str:
    """Blockquote copy → HTML. Bullet runs become one list; everything else a paragraph.

    Inline `**bold**` is converted too — the Christmas listings put the shipping cutoff in
    bold, and without this it reached the storefront as literal asterisks.
    """
    lines = [BOLD.sub(r"<strong>\1</strong>", ln) for ln in lines]
    html, bullets = [], []

    def flush():
        if bullets:
            html.append("<ul>" + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>")
            bullets.clear()

    for ln in lines:
        if not ln:
            flush()
        elif ln.startswith("•"):
            bullets.append(ln.lstrip("• ").strip())
        else:
            flush()
            html.append(f"<p>{ln}</p>")
    flush()
    return "".join(html)


# ----------------------------------------------------------------- images
STAGE = """
mutation Stage($input: [StagedUploadInput!]!) {
  stagedUploadsCreate(input: $input) {
    stagedTargets { url resourceUrl parameters { name value } }
    userErrors { field message }
  }
}"""


def upload_image(api: Shopify, path: pathlib.Path) -> str | None:
    """Stage one file and POST its bytes. Returns the resourceUrl for productCreate media."""
    if not path.exists():
        print(f"    ! missing {path.name}")
        return None
    data = api(STAGE, {"input": [{
        "filename": path.name, "mimeType": mimetypes.guess_type(path.name)[0] or "image/png",
        "resource": "IMAGE", "httpMethod": "POST",
    }]}, "stagedUploadsCreate")
    if not api.execute:
        return f"staged://{path.name}"

    tgt = data["stagedUploadsCreate"]["stagedTargets"][0]
    boundary = uuid.uuid4().hex
    parts = []
    for p in tgt["parameters"]:                      # order matters
        parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{p['name']}\""
                     f"\r\n\r\n{p['value']}\r\n".encode())
    parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
                 f"filename=\"{path.name}\"\r\nContent-Type: image/png\r\n\r\n".encode())
    parts.append(path.read_bytes())
    parts.append(f"\r\n--{boundary}--\r\n".encode())  # `file` must be the final field

    req = urllib.request.Request(tgt["url"], data=b"".join(parts), headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        if r.status not in (200, 201, 204):
            raise SystemExit(f"upload of {path.name} failed: HTTP {r.status}")
    return tgt["resourceUrl"]


# ----------------------------------------------------------------- products
FIND = """query Find($handle: String!) { productByHandle(handle: $handle) { id title } }"""

CREATE = """
mutation Create($product: ProductCreateInput!, $media: [CreateMediaInput!]) {
  productCreate(product: $product, media: $media) {
    product { id handle title variants(first: 10) { nodes { id title } } }
    userErrors { field message }
  }
}"""

SET_PRICES = """
mutation Prices($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
  productVariantsBulkUpdate(productId: $productId, variants: $variants) {
    productVariants { id title price }
    userErrors { field message }
  }
}"""

ADD_VARIANTS = """
mutation AddVariants($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
  productVariantsBulkCreate(productId: $productId, variants: $variants) {
    productVariants { id title price }
    userErrors { field message }
  }
}"""


def push_products(api: Shopify, limit: int | None, force: bool, n_images: int) -> None:
    items = []
    for path, extra in LISTINGS:
        if path.exists():
            items += parse_listings(path, extra)
    if limit:
        items = items[:limit]
    print(f"\n== Products ({len(items)}) ==")

    for it in items:
        handle = f"bma-{it['slug']}"
        print(f"  {handle}")

        if api.execute and not force:
            found = api(FIND, {"handle": handle}, "productByHandle")
            if (found.get("productByHandle") or {}).get("id"):
                print("    exists, skipping")
                continue

        media = []
        for suffix in IMAGE_ORDER[:n_images]:
            src = ROOT / "design" / "mockups" / f"{it['slug']}-{suffix}.png"
            url = upload_image(api, src)
            if url:
                media.append({"originalSource": url, "mediaContentType": "IMAGE",
                              "alt": it["title"][:120]})
        print(f"    {len(media)} images")

        data = api(CREATE, {
            "product": {
                "title": it["title"][:255],
                "handle": handle,
                "descriptionHtml": to_html(it["desc"]),
                "vendor": "The Bureau of Minor Achievements",
                "productType": "Wall Art",
                "status": "DRAFT",
                "tags": it["tags"],
                "productOptions": [{"name": "Size",
                                    "values": [{"name": n} for n, _ in PRICES]}],
            },
            "media": media,
        }, "productCreate")

        if not api.execute:
            continue
        prod = data["productCreate"]["product"]

        # productCreate does NOT fan the option values out into variants — it returns a
        # single variant on the first value ("8x10 Print"). Verified against a live store:
        # without this the other two sizes never exist and the product sells at one price.
        by_title = {v["title"]: v["id"] for v in prod["variants"]["nodes"]}
        missing = [(n, p) for n, p in PRICES if n not in by_title]
        if missing:
            made = api(ADD_VARIANTS, {"productId": prod["id"], "variants": [
                {"price": p, "optionValues": [{"optionName": "Size", "name": n}]}
                for n, p in missing
            ]}, "productVariantsBulkCreate")
            for v in made["productVariantsBulkCreate"]["productVariants"]:
                by_title[v["title"]] = v["id"]

        # the one variant productCreate did make still carries no price
        updates = [{"id": by_title[n], "price": p} for n, p in PRICES if n in by_title]
        if updates:
            api(SET_PRICES, {"productId": prod["id"], "variants": updates}, "prices")
        if len(by_title) != len(PRICES):
            print(f"    ! only {len(by_title)}/{len(PRICES)} variants — check this product")
        print(f"    created, {len(by_title)} variants, {len(updates)} prices set")


# ----------------------------------------------------------------- policies
POLICY = """
mutation Policy($policy: ShopPolicyInput!) {
  shopPolicyUpdate(shopPolicy: $policy) {
    shopPolicy { id type url } userErrors { field message }
  }
}"""

PAGE = """
mutation Page($page: PageCreateInput!) {
  pageCreate(page: $page) { page { id handle title } userErrors { field message } }
}"""


def split_doc() -> dict[str, list[str]]:
    """Slice policies-and-pages.md on its H2s."""
    out, key = {}, None
    for ln in (ROOT / "store" / "policies-and-pages.md").read_text(encoding="utf-8").splitlines():
        if ln.startswith("## "):
            key = ln[3:].strip()
            out[key] = []
        elif key:
            out[key].append(ln)
    return out


def md_to_html(lines: list[str]) -> str:
    """Markdown → HTML.

    The source is hard-wrapped at ~90 columns, so consecutive non-blank lines have to be
    joined into one paragraph. Emitting one <p> per source line splits sentences in half.
    """
    html: list[str] = []
    para: list[str] = []
    items: list[str] = []
    kind = ""

    def inline(t: str) -> str:
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", t)
        return re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', t)

    def flush() -> None:
        nonlocal kind
        if para:
            html.append(f"<p>{inline(' '.join(para))}</p>")
            para.clear()
        if items:
            tag = "ol" if kind == "ol" else "ul"
            html.append(f"<{tag}>" + "".join(f"<li>{inline(i)}</li>" for i in items) + f"</{tag}>")
            items.clear()
        kind = ""

    for raw in lines:
        ln = raw.rstrip()
        if not ln or ln.startswith("---") or ln.startswith("```") or ln.startswith(">"):
            flush()
            continue
        if ln.startswith("### "):
            flush()
            html.append(f"<h3>{inline(ln[4:])}</h3>")
            continue
        m_ol = re.match(r"^\d+\.\s+(.*)", ln)
        m_ul = re.match(r"^[-*•]\s+(.*)", ln)
        if m_ol or m_ul:
            if para:
                html.append(f"<p>{inline(' '.join(para))}</p>")
                para.clear()
            new_kind = "ol" if m_ol else "ul"
            if kind and kind != new_kind:
                flush()
            kind = new_kind
            items.append((m_ol or m_ul).group(1))
            continue
        if items:            # a plain line ends the list
            flush()
        para.append(ln)
    flush()
    return "".join(html)


# Any address on a domain we don't own. The policies were rewritten for the Bureau and now
# carry the store's real inbox, so this normally finds nothing — it stays as a guard against
# a placeholder creeping back in.
PLACEHOLDER = re.compile(r"[\w.+-]+@(?:deadpangoods|example)\.com")


def fix_email(html: str, real: str | None) -> tuple[str, bool]:
    """Catch any support address on a domain that doesn't exist.

    Publishing one points customers at an inbox nobody reads, which is worse than having no
    policy at all. Substitute a real address if one was supplied, else report it.
    """
    if not PLACEHOLDER.search(html):
        return html, False
    if real:
        return PLACEHOLDER.sub(real, html), False
    return html, True


def push_policies(api: Shopify, real_email: str | None, allow_placeholder: bool) -> None:
    doc = split_doc()
    print("\n== Policies ==")
    flagged = []
    bodies = {}
    for name, ptype in POLICY_TYPES.items():
        if name not in doc:
            print(f"  ! {name} not found in policies-and-pages.md")
            continue
        body, is_placeholder = fix_email(md_to_html(doc[name]), real_email)
        bodies[name] = (ptype, body)
        if is_placeholder:
            flagged.append(name)

    if flagged and not allow_placeholder:
        print(f"  ⚠️  {', '.join(flagged)} name a support address on a domain we don't own,")
        print("      so no mailbox exists behind it. Customers who email it get silence,")
        print("      and Etsy/Shopify both expect a reachable address.")
        print("      Fix with:  SHOPIFY_SUPPORT_EMAIL=you@real.com  (or --allow-placeholder-email)")
        return

    for name, (ptype, body) in bodies.items():
        print(f"  {name} → {ptype}")
        api(POLICY, {"policy": {"type": ptype, "body": body}}, ptype)


def push_pages(api: Shopify, real_email: str | None) -> None:
    doc = split_doc()
    print("\n== Pages ==")
    for key, title, handle in [("Page: About", "About", "about"),
                               ("Page: FAQ", "FAQ", "faq")]:
        if key not in doc:
            print(f"  ! {key} not found")
            continue
        body, _ = fix_email(md_to_html(doc[key]), real_email)
        print(f"  {title}")
        api(PAGE, {"page": {"title": title, "handle": handle,
                            "body": body}}, f"page:{handle}")


# ----------------------------------------------------------------- cli
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--products", action="store_true")
    ap.add_argument("--policies", action="store_true")
    ap.add_argument("--pages", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--execute", action="store_true", help="actually write (default: dry run)")
    ap.add_argument("--force", action="store_true", help="don't skip products that exist")
    ap.add_argument("--limit", type=int, help="only the first N products — use 1 to test")
    ap.add_argument("--images", type=int, default=5, help="images per product (max 5)")
    ap.add_argument("--allow-placeholder-email", action="store_true",
                    help="publish policies even with the placeholder support address")
    a = ap.parse_args()

    if not (a.products or a.policies or a.pages or a.all):
        ap.print_help()
        sys.exit(0)

    store = os.environ.get("SHOPIFY_STORE")
    token = os.environ.get("SHOPIFY_TOKEN")
    if a.execute and not (store and token):
        sys.exit("Set SHOPIFY_STORE and SHOPIFY_TOKEN. See the docstring for how to get one.")

    api = Shopify(store or "dry-run.myshopify.com", token or "", a.execute)
    print(f"{'EXECUTING against ' + str(store) if a.execute else 'DRY RUN — nothing will be sent'}")

    if a.all or a.products:
        push_products(api, a.limit, a.force, max(1, min(a.images, 5)))
    email = os.environ.get("SHOPIFY_SUPPORT_EMAIL")
    if a.all or a.policies:
        push_policies(api, email, a.allow_placeholder_email)
    if a.all or a.pages:
        push_pages(api, email)

    print(f"\n{api.calls} API calls." if a.execute else
          "\nDry run complete. Re-run with --execute to write.")


if __name__ == "__main__":
    main()
