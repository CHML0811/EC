#!/usr/bin/env python3
"""
Health check for the whole project.

    python3 verify.py           # fast — no rendering, a couple of seconds
    python3 verify.py --full    # also rebuilds everything and checks the output

Run this first if you're picking the project up after a break, or before trusting
anything an assistant just changed. Exits non-zero if anything fails, so it works as a
pre-commit or CI step too.

It checks the things that actually rot: a missing Chrome, an Etsy tag that grew past the
20-character limit, a British spelling creeping into buyer-facing copy, a doc link
pointing at a file somebody renamed.
"""

import argparse
import pathlib
import re
import subprocess
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "design"))

PASS, FAIL, WARN = "  \033[32m✓\033[0m", "  \033[31m✗\033[0m", "  \033[33m!\033[0m"
results: list[bool] = []


def check(ok: bool, msg: str, detail: str = "") -> bool:
    print(f"{PASS if ok else FAIL} {msg}")
    if detail and not ok:
        for line in detail.splitlines()[:8]:
            print(f"      {line}")
    results.append(ok)
    return ok


def warn(msg: str) -> None:
    print(f"{WARN} {msg}")


# --------------------------------------------------------------- environment
def check_env() -> None:
    print("\nEnvironment")
    check(sys.version_info >= (3, 9),
          f"Python {sys.version_info.major}.{sys.version_info.minor} (need 3.9+)")
    try:
        import generate_certificates as g
        chrome = g.find_chrome()
        check(True, f"Chrome found — {chrome}")
    except SystemExit as e:
        check(False, "Chrome not found", str(e))
    except Exception as e:            # noqa: BLE001 — any import failure is a real failure
        check(False, f"design/generate_certificates.py won't import: {e}")


# --------------------------------------------------------------- sources
BUILD_SCRIPTS = [
    "design/generate_certificates.py", "design/certs_christmas.py", "design/certs_office.py",
    "design/generate_mockups.py", "design/generate_crops.py",
    "kit/build_awards_maker.py", "kit/build_documents.py", "kit/build_kit.py",
    "kit/build_listing_images.py", "site/build_storefront.py", "store/upload_to_shopify.py",
]
KEY_DOCS = ["README.md", "AGENTS.md", "HANDOFF.md", "CLAUDE.md",
            "marketing/etsy-office-awards-kit.md", "playbooks/first-seller-strategy.md"]


def check_sources() -> None:
    print("\nSources")
    missing = [p for p in BUILD_SCRIPTS + KEY_DOCS if not (ROOT / p).exists()]
    check(not missing, f"{len(BUILD_SCRIPTS + KEY_DOCS)} source files present",
          "missing: " + ", ".join(missing))

    bad = []
    for p in BUILD_SCRIPTS:
        r = subprocess.run([sys.executable, "-m", "py_compile", str(ROOT / p)],
                           capture_output=True, text=True)
        if r.returncode:
            bad.append(f"{p}: {r.stderr.strip().splitlines()[-1] if r.stderr else '?'}")
    check(not bad, "every build script compiles", "\n".join(bad))


# --------------------------------------------------------------- listing data
BRITISH = re.compile(r"\b(personalis\w*|colour\w*|honour\w*|favourit\w*|humour|"
                     r"recognis\w*|organis\w*|apologis\w*|catalogue|whilst|mum)\b", re.I)
BUYER_FACING = ["marketing/etsy-cohort-1.md", "marketing/etsy-cohort-2-christmas.md",
                "marketing/etsy-office-awards-kit.md", "marketing/pinterest-pins.md",
                "store/policies-and-pages.md", "site/index.html"]


def check_listings() -> None:
    print("\nListing data")
    rows, problems = 0, []
    for f in ("marketing/etsy-cohort-1.md", "marketing/etsy-cohort-2-christmas.md"):
        path = ROOT / f
        if not path.exists():
            problems.append(f"{f} missing")
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.startswith("**Tags:**"):
                continue
            rows += 1
            tags = [t.strip(" `") for t in line[9:].split("·")]
            if len(tags) != 13:
                problems.append(f"{f}: {len(tags)} tags, expected 13 — {tags[0]}")
            for t in tags:
                if len(t) > 20:
                    problems.append(f"{f}: tag over 20 chars — {t!r} ({len(t)})")
                if tags.count(t) > 1:
                    problems.append(f"{f}: duplicate tag — {t!r}")
    check(rows == 16, f"16 listings with tag rows (found {rows})")
    check(not problems, "every tag inside Etsy's limits", "\n".join(dict.fromkeys(problems)))

    hits = []
    for f in BUYER_FACING:
        path = ROOT / f
        if not path.exists():
            continue
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for m in BRITISH.finditer(line):
                hits.append(f"{f}:{i} — {m.group(0)}")
    check(not hits, "buyer-facing copy is US English", "\n".join(hits))


# --------------------------------------------------------------- doc links
LINK = re.compile(r"\[[^\]]+\]\((?!https?:|#|mailto:)([^)#]+)")


def check_links() -> None:
    print("\nDocumentation links")
    broken = []
    for md in ROOT.rglob("*.md"):
        if ".git" in md.parts:
            continue
        for i, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            for m in LINK.finditer(line):
                target = (md.parent / m.group(1).strip()).resolve()
                if not target.exists():
                    broken.append(f"{md.relative_to(ROOT)}:{i} → {m.group(1)}")
    check(not broken, "every internal doc link resolves", "\n".join(broken))


# --------------------------------------------------------------- artifacts
def check_artifacts(full: bool) -> None:
    print("\nBuild artifacts")
    zip_path = ROOT / "kit" / "Office-Awards-Kit.zip"

    if full:
        print("      building (about 90 seconds)…")
        r = subprocess.run([sys.executable, "kit/build_kit.py"], cwd=ROOT,
                           capture_output=True, text=True)
        if not check(r.returncode == 0, "kit/build_kit.py runs clean",
                     (r.stderr or r.stdout)[-600:]):
            return
    elif not zip_path.exists():
        warn("kit/Office-Awards-Kit.zip not built yet — run: python3 kit/build_kit.py")
        warn("(that's expected on a fresh clone; artifacts are gitignored)")
        return

    certs = sorted((ROOT / "design" / "out").glob("bma-*.png"))
    check(len(certs) == 38, f"38 certificates rendered (found {len(certs)})")

    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
    png = sum(1 for n in names if n.endswith(".png"))
    pdf = sum(1 for n in names if n.endswith(".pdf"))
    mb = zip_path.stat().st_size / 1024 / 1024
    check(png == 38 and pdf == 5 and any(n.endswith("AwardsMaker.html") for n in names),
          f"kit zip complete — {png} certificates, {pdf} PDFs, maker, {mb:.1f} MB")
    check(mb < 20, f"kit zip under Etsy's 20 MB limit ({mb:.1f} MB)")

    maker = ROOT / "kit" / "dist" / "AwardsMaker.html"
    if maker.exists():
        text = maker.read_text(encoding="utf-8")
        n = text.count('"slug"')
        check(n == 38, f"maker carries all 38 designs (found {n})")
        check("[hidden]{display:none !important}" in text,
              "maker keeps the [hidden] override (both panels showed without it)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--full", action="store_true", help="also rebuild everything")
    a = ap.parse_args()

    print("Bureau of Minor Achievements — health check")
    check_env()
    check_sources()
    check_listings()
    check_links()
    check_artifacts(a.full)

    failed = results.count(False)
    print(f"\n{'─' * 46}")
    if failed:
        print(f"\033[31m{failed} of {len(results)} checks failed.\033[0m")
        sys.exit(1)
    print(f"\033[32mAll {len(results)} checks passed.\033[0m")
    if not a.full:
        print("Run with --full to rebuild and verify the output too.")


if __name__ == "__main__":
    main()
