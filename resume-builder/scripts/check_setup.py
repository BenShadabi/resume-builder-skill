#!/usr/bin/env python3
"""Check that this computer can run the resume builder. Prints plain-language results.

Usage: check_setup.py
Needs: Python 3.8+. Chrome, Chromium or Edge is optional (nicer PDFs); otherwise a built-in writer is used.
"""
import platform
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_resume import find_chrome  # noqa: E402


def main():
    ok = True
    v = sys.version_info
    if v >= (3, 8):
        print(f"OK    Python {v.major}.{v.minor} found")
    else:
        ok = False
        print("MISSING Python 3.8 or newer. Install from python.org, then run this again.")
    chrome = find_chrome()
    if chrome:
        print(f"OK    PDF printer found: {chrome}")
    else:
        print("OK    No Chrome found, so PDFs use the built-in writer (plain Helvetica, one column). "
              "That is fine; install Chrome only if you want the nicer layout.")
    print(f"INFO  System: {platform.system()}")
    print("INFO  Nothing else to install. Your files stay on this computer.")
    print("READY" if ok else "NOT READY: fix the items marked MISSING")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
