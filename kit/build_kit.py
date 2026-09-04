#!/usr/bin/env python3
"""
Assemble a kit into the zip a buyer downloads.

    python3 kit/build_kit.py              # → kit/Office-Awards-Kit.zip     (38 certificates)
    python3 kit/build_kit.py --school     # → kit/Classroom-Awards-Kit.zip  (12 certificates)

Runs the whole chain — certificates, maker, documents — then packages the result. The zips
are build artifacts and are not committed; everything needed to rebuild them is.

The two kits are separate products for separate buyers and share no certificates. Cohorts
are named from the design manifests rather than globbed, so adding a cohort for one audience
cannot leak into the other kit — which is exactly what happened when this globbed
design/out, and nothing failed to say so.
"""

import json
import pathlib
import shutil
import subprocess
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent

KITS = {
    "office": {
        "zip": "Office-Awards-Kit.zip",
        "dist": "dist",
        "renderers": ["generate_certificates.py", "certs_christmas.py", "certs_office.py"],
        "manifests": ["manifest.json", "manifest-christmas.json", "manifest-office.json"],
        "maker_flags": [],
        "doc_builder": "kit/build_documents.py",
        "docs": ["Start-Here.pdf", "Hosts-Script.pdf", "Ballot.pdf", "Name-Tents.pdf",
                 "Announcement.pdf"],
    },
    "school": {
        "zip": "Classroom-Awards-Kit.zip",
        "dist": "dist-school",
        "renderers": ["certs_school.py"],
        "manifests": ["manifest-school.json"],
        "maker_flags": ["--school"],
        "doc_builder": "kit/build_school_documents.py",
        "docs": ["Start-Here.pdf", "Teachers-Script.pdf", "Blank-Certificate.pdf"],
    },
}


def run(*cmd: str) -> None:
    subprocess.run([sys.executable, *cmd], check=True, cwd=REPO)


def build(kit: str) -> None:
    spec = KITS[kit]
    dist = ROOT / spec["dist"]
    zip_path = ROOT / spec["zip"]
    dist.mkdir(parents=True, exist_ok=True)

    print("Rendering certificates…")
    for script in spec["renderers"]:
        subprocess.run([sys.executable, script], check=True, cwd=REPO / "design",
                       capture_output=True)

    print("Building the maker…")
    run("kit/build_awards_maker.py", f"kit/{spec['dist']}/AwardsMaker.html",
        *spec["maker_flags"])

    print("Building the documents…")
    run(spec["doc_builder"], f"kit/{spec['dist']}")

    print("Collecting artwork…")
    certs = dist / "certificates"
    if certs.exists():
        shutil.rmtree(certs)
    certs.mkdir()

    out = REPO / "design" / "out"
    pngs = []
    for name in spec["manifests"]:
        entries = json.loads((out / name).read_text(encoding="utf-8"))
        pngs += [out / e["file"] for e in entries]
    missing = [p.name for p in pngs if not p.exists()]
    if missing:
        raise SystemExit(f"manifest names {len(missing)} file(s) that don't exist: {missing[:3]}")
    for p in sorted(pngs):
        shutil.copy2(p, certs / p.name)

    print("Packaging…")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for d in spec["docs"]:
            z.write(dist / d, d)
        z.write(dist / "AwardsMaker.html", "AwardsMaker.html")
        for p in sorted(certs.glob("*.png")):
            z.write(p, f"certificates/{p.name}")

    mb = zip_path.stat().st_size / 1024 / 1024
    print(f"\n{zip_path.name}  {mb:.1f} MB  "
          f"({len(pngs)} certificates + {len(spec['docs'])} PDFs + maker)")
    if mb > 20:
        print("⚠️  Over Etsy's 20 MB per-file limit — split the certificates into a "
              "second download.")


def main() -> None:
    flags = set(sys.argv[1:])
    if flags - {"--school"}:
        sys.exit(__doc__)
    build("school" if "--school" in flags else "office")


if __name__ == "__main__":
    main()
