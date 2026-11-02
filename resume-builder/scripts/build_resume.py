#!/usr/bin/env python3
"""Turn resume.md into an ATS-friendly one-column PDF using headless Chrome or Chromium.

Usage: build_resume.py resume.md [out.pdf]

Uses Chrome, Chromium or Edge if installed, otherwise a built-in standard-library PDF writer. No Python packages needed.
Prints the page count. See references/format.md for the markdown format.
"""
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]

CSS = """
@page { size: PAPER; margin: 0.55in 0.6in; }
body { font-family: Calibri, Carlito, 'Helvetica Neue', Arial, sans-serif; font-size: 10.5pt;
       line-height: 1.28; color: #111; margin: 0; }
h1 { font-size: 20pt; margin: 0 0 2pt 0; letter-spacing: 0.3px; }
.contact { font-size: 10pt; margin: 0; }
h2 { font-size: 11pt; margin: 10pt 0 3pt 0; padding-bottom: 1pt; border-bottom: 1px solid #333;
     letter-spacing: 0.6px; }
.row { display: flex; justify-content: space-between; margin-top: 4pt; font-weight: bold; }
.row span.r { font-weight: normal; }
p { margin: 1pt 0; }
ul { margin: 2pt 0 2pt 16pt; padding: 0; }
li { margin: 1pt 0; }
"""


def find_chrome():
    for c in CHROME_CANDIDATES:
        if Path(c).exists() or shutil.which(c):
            return c
    return None


def is_root():
    return hasattr(os, "geteuid") and os.geteuid() == 0


def chrome_works(chrome):
    """Try printing a tiny page. Returns True only if Chrome really produces a PDF here (it can hang or fail in sandboxes)."""
    flags = ["--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--disable-dev-shm-usage"]
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        flags.append("--no-sandbox")
    with tempfile.TemporaryDirectory() as d:
        page, out = Path(d) / "t.html", Path(d) / "t.pdf"
        page.write_text("<html><body>test</body></html>", encoding="utf-8")
        try:
            subprocess.run([chrome, *flags, f"--user-data-dir={d}/p", f"--print-to-pdf={out}", page.as_uri()],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20)
            return out.exists() and out.stat().st_size > 500
        except (subprocess.SubprocessError, OSError):
            return False


def inline(text):
    t = html.escape(text)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)


def to_html(md, paper="Letter", lang="en"):
    out, in_list, seen_name, contact_done = [], False, False, False

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for raw in md.splitlines():
        line = raw.rstrip()
        if not line.strip():
            close_list()
            if seen_name:
                contact_done = True
            continue
        if line.startswith("# "):
            close_list()
            out.append(f"<h1>{inline(line[2:])}</h1>")
            seen_name = True
        elif line.startswith("## "):
            close_list()
            contact_done = True
            out.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("### "):
            close_list()
            left, _, right = line[4:].partition("::")
            out.append(f'<div class="row"><span>{inline(left.strip())}</span>'
                       f'<span class="r">{inline(right.strip())}</span></div>')
        elif line.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(line[2:])}</li>")
        else:
            close_list()
            cls = ' class="contact"' if seen_name and not contact_done else ""
            out.append(f"<p{cls}>{inline(line)}</p>")
    close_list()
    css = CSS.replace("PAPER", paper)
    return f"<!doctype html><html lang='{lang}'><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(out)}</body></html>"


def page_count(pdf):
    return len(re.findall(rb"/Type\s*/Page[^s]", Path(pdf).read_bytes()))


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Turn a resume or letter .md into a one-column PDF (needs Chrome, Chromium or Edge).")
    ap.add_argument("source", help="the .md file (see references/format.md)")
    ap.add_argument("output", nargs="?", help="PDF path (default: same name as the .md)")
    ap.add_argument("--paper", choices=["Letter", "A4"], default="Letter", help="paper size (A4 for most countries outside North America)")
    ap.add_argument("--lang", default="en", help="language code for the PDF, for example es or fr")
    ap.add_argument("--engine", choices=["auto", "chrome", "builtin"], default="auto", help="auto uses Chrome if installed, otherwise the built-in writer")
    ap.add_argument("--max-pages", type=int, default=1, help="warn above this many pages (default 1)")
    args = ap.parse_args()
    src = Path(args.source).resolve()
    dst = (Path(args.output) if args.output else src.with_suffix(".pdf")).resolve()
    chrome = None if args.engine == "builtin" else find_chrome()
    if chrome and args.engine == "auto" and is_root():
        chrome = None  # root usually means a sandbox or container, where Chrome is slow or hangs: use the built-in writer
    if chrome and args.engine == "auto" and not chrome_works(chrome):
        chrome = None  # found but not working here (common in sandboxes): use the built-in writer
    if not chrome:
        if args.engine == "chrome":
            sys.exit("Chrome, Chromium or Edge was not found. Install one, or use --engine builtin.")
        from simple_pdf import markdown_to_pdf
        data, pages = markdown_to_pdf(src.read_text(encoding="utf-8"), args.paper)
        dst.write_bytes(data)
        print(f"Wrote {dst} ({pages} page{'s' if pages != 1 else ''}) using the built-in PDF writer "
              "(plain Helvetica; install Chrome for the nicer Calibri-style layout)")
        if pages > args.max_pages:
            print(f"WARNING: more than {args.max_pages} page(s). Cut the oldest or least relevant bullets, then rebuild.")
        return
    doc = to_html(src.read_text(encoding="utf-8"), args.paper, args.lang)
    html_path = dst.with_suffix(".html")
    html_path.write_text(doc, encoding="utf-8")
    flags = ["--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--disable-dev-shm-usage"]
    if hasattr(os, "geteuid") and os.geteuid() == 0:  # root in a container: Chrome refuses to start without this
        flags.append("--no-sandbox")
    ok = False
    with tempfile.TemporaryDirectory() as profile:
        try:
            if dst.exists():
                dst.unlink()
            subprocess.run([chrome, *flags, f"--user-data-dir={profile}", f"--print-to-pdf={dst}", html_path.as_uri()],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
            ok = dst.exists() and dst.stat().st_size > 500
        except (subprocess.SubprocessError, OSError):
            ok = False
    html_path.unlink(missing_ok=True)
    if not ok:
        if args.engine == "chrome":
            sys.exit("Chrome could not print the PDF. Use --engine builtin.")
        from simple_pdf import markdown_to_pdf
        data, pages = markdown_to_pdf(src.read_text(encoding="utf-8"), args.paper)
        dst.write_bytes(data)
        print(f"Chrome did not work here, so I used the built-in PDF writer instead.")
        print(f"Wrote {dst} ({pages} page{'s' if pages != 1 else ''})")
        if pages > args.max_pages:
            print(f"WARNING: more than {args.max_pages} page(s). Cut the oldest or least relevant bullets, then rebuild.")
        return
    pages = page_count(dst)
    print(f"Wrote {dst} ({pages} page{'s' if pages != 1 else ''})")
    if pages > args.max_pages:
        print(f"WARNING: more than {args.max_pages} page(s). Cut the oldest or least relevant bullets, then rebuild.")
    html_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
