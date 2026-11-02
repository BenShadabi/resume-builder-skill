#!/usr/bin/env python3
"""Check that this computer can run the resume builder. Prints plain-language results.

Usage: check_setup.py
Needs: Python 3.8+ and one of Google Chrome, Chromium or Microsoft Edge (used to print PDFs).
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
        ok = False
        print("MISSING Google Chrome, Chromium or Edge. Install one (chrome.google.com), "
              "or ask for the .html version and use Print, then Save as PDF.")
    print(f"INFO  System: {platform.system()}")
    print("INFO  Nothing else to install. Your files stay on this computer.")
    print("READY" if ok else "NOT READY: fix the items marked MISSING")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
