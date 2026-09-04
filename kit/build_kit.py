#!/usr/bin/env python3
"""
Assemble the Office Awards Kit into the zip a buyer downloads.

    python3 kit/build_kit.py

Runs the whole chain — certificates, maker, documents — then packages the result as
kit/Office-Awards-Kit.zip. The zip is a build artifact and is not committed; everything
needed to rebuild it is.
"""

import json
import pathlib
import shutil
import subprocess
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
DIST = ROOT / "dist"
ZIP = ROOT / "Office-Awards-Kit.zip"

# Which cohorts belong in THIS kit. The classroom set (manifest-school.json) is
# deliberately absent — it is a different product for a different buyer.
KIT_MANIFESTS = ["manifest.json", "manifest-christmas.json", "manifest-office.json"]

DOCS = ["Start-Here.pdf", "Hosts-Script.pdf", "Ballot.pdf", "Name-Tents.pdf",
        "Announcement.pdf"]


def run(*cmd: str) -> None:
    subprocess.run([sys.executable, *cmd], check=True, cwd=REPO)


def main() -> None:
    DIST.mkdir(parents=True, exist_ok=True)

    print("Rendering certificates…")
    for script in ("generate_certificates.py", "certs_christmas.py", "certs_office.py"):
        subprocess.run([sys.executable, script], check=True, cwd=REPO / "design",
                       capture_output=True)

    print("Building the maker…")
    run("kit/build_awards_maker.py", "kit/dist/AwardsMaker.html")

    print("Building the documents…")
    run("kit/build_documents.py", "kit/dist")

    print("Collecting artwork…")
    certs = DIST / "certificates"
    if certs.exists():
        shutil.rmtree(certs)
    certs.mkdir()

    # Named from the manifests, NOT globbed. This used to take every bma-*.png in
    # design/out, so adding a cohort for a different audience silently swept it into this
    # kit — the classroom set did exactly that — and the listing's "38 certificates"
    # stopped being true without anything failing.
    out = REPO / "design" / "out"
    pngs = []
    for name in KIT_MANIFESTS:
        entries = json.loads((out / name).read_text(encoding="utf-8"))
        pngs += [out / e["file"] for e in entries]
    missing = [p.name for p in pngs if not p.exists()]
    if missing:
        raise SystemExit(f"manifest names {len(missing)} file(s) that don't exist: {missing[:3]}")
    for p in sorted(pngs):
        shutil.copy2(p, certs / p.name)

    print("Packaging…")
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for d in DOCS:
            z.write(DIST / d, d)
        z.write(DIST / "AwardsMaker.html", "AwardsMaker.html")
        for p in sorted(certs.glob("*.png")):
            z.write(p, f"certificates/{p.name}")

    mb = ZIP.stat().st_size / 1024 / 1024
    print(f"\n{ZIP.name}  {mb:.1f} MB  ({len(pngs)} certificates + {len(DOCS)} PDFs + maker)")
    if mb > 20:
        print("⚠️  Over Etsy's 20 MB per-file limit — split the certificates into a "
              "second download.")


if __name__ == "__main__":
    main()
