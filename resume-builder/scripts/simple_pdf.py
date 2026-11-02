#!/usr/bin/env python3
"""Minimal one-column PDF writer used when Chrome, Chromium or Edge is not available (for example on Claude.ai).

Standard library only. Uses the built-in Helvetica fonts, so text is real, selectable and ATS-readable.
Supports Latin text with accents (Windows-1252). Not for Chinese, Arabic or other scripts: use Chrome for those.
Reads the same markdown format as build_resume.py (see references/format.md).
"""
import re

PAPERS = {"Letter": (612, 792), "A4": (595, 842)}
MARGIN_X, MARGIN_TOP, MARGIN_BOTTOM = 44, 44, 40

# Helvetica character widths (per 1000 units) for ASCII 32 to 126
_W = {" ": 278, "!": 278, '"': 355, "#": 556, "$": 556, "%": 889, "&": 667, "'": 191, "(": 333, ")": 333,
      "*": 389, "+": 584, ",": 278, "-": 333, ".": 278, "/": 278, ":": 278, ";": 278, "<": 584, "=": 584,
      ">": 584, "?": 556, "@": 1015, "[": 278, "\\": 278, "]": 278, "^": 469, "_": 556, "`": 333,
      "{": 334, "|": 260, "}": 334, "~": 584}
for c in "0123456789":
    _W[c] = 556
for c, w in zip("abcdefghijklmnopqrstuvwxyz",
                [556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500]):
    _W[c] = w
for c, w in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                [667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611]):
    _W[c] = w


def width(text, size, bold=False):
    total = sum(_W.get(ch, 556) for ch in text)  # accented letters use the average width
    return total * size / 1000.0 * (1.06 if bold else 1.0)


def esc(text):
    data = text.encode("cp1252", "replace")
    out = []
    for b in data:
        ch = chr(b)
        out.append("\\" + ch if ch in "()\\" else ch)
    return "".join(out)


def strip_inline(text):
    """Return list of (text, bold) segments from **bold** markup."""
    parts, pos = [], 0
    for m in re.finditer(r"\*\*(.+?)\*\*", text):
        if m.start() > pos:
            parts.append((text[pos:m.start()], False))
        parts.append((m.group(1), True))
        pos = m.end()
    if pos < len(text):
        parts.append((text[pos:], False))
    return parts or [("", False)]


def wrap(segments, size, max_w):
    """Greedy word wrap over bold/regular segments. Returns lines, each a list of (word, bold, space_before)."""
    words, prev_end_space = [], False
    for text, bold in segments:
        pieces = text.split(" ")
        for i, w in enumerate(pieces):
            if not w:
                continue
            first = (i == 0 or all(not p for p in pieces[:i]))
            sb = True
            if first and words:
                sb = (text[:1] == " ") or prev_end_space
            words.append((w, bold, sb))
        prev_end_space = text[-1:] == " "
    lines, cur, cur_w = [], [], 0.0
    space = width(" ", size)
    for w, bold, sb in words:
        ww = width(w, size, bold)
        add = ww if not cur else (space if sb else 0) + ww
        if cur and cur_w + add > max_w:
            lines.append([(w, bold, False)])
            cur, cur_w = lines[-1], ww
        else:
            if cur:
                cur.append((w, bold, sb))
            else:
                cur = [(w, bold, False)]
                lines.append(cur)
            cur_w += add
    return lines or [[]]


class Doc:
    def __init__(self, paper="Letter"):
        self.w, self.h = PAPERS.get(paper, PAPERS["Letter"])
        self.pages = [[]]
        self.y = self.h - MARGIN_TOP

    def _need(self, space):
        if self.y - space < MARGIN_BOTTOM:
            self.pages.append([])
            self.y = self.h - MARGIN_TOP

    def text(self, x, y, s, size, bold=False):
        self.pages[-1].append(f"BT /{'F2' if bold else 'F1'} {size} Tf {x:.1f} {y:.1f} Td ({esc(s)}) Tj ET")

    def line(self, x1, y, x2):
        self.pages[-1].append(f"0.5 w {x1:.1f} {y:.1f} m {x2:.1f} {y:.1f} l S")

    def runs(self, x, y, line, size):
        """Draw one wrapped line made of (word, bold) pieces."""
        cur = x
        space = width(" ", size)
        for i, (w, bold, sb) in enumerate(line):
            if i and sb:
                cur += space
            self.text(cur, y, w, size, bold)
            cur += width(w, size, bold)

    def para(self, segments, size=10.5, indent=0, bullet=False, lead=1.28, gap=1.5):
        max_w = self.w - 2 * MARGIN_X - indent
        lines = wrap(segments, size, max_w)
        for i, ln in enumerate(lines):
            self._need(size * lead)
            self.y -= size * lead
            if bullet and i == 0:
                self.text(MARGIN_X + indent - 11, self.y, "\u2022", size)
            self.runs(MARGIN_X + indent, self.y, ln, size)
        self.y -= gap

    def heading(self, s):
        self._need(26)
        self.y -= 16
        self.text(MARGIN_X, self.y, s.upper(), 11, True)
        self.line(MARGIN_X, self.y - 3, self.w - MARGIN_X)
        self.y -= 5

    def row(self, left, right, size=10.5):
        self._need(size * 1.5 + 4)
        self.y -= size * 1.28 + 3
        self.text(MARGIN_X, self.y, left, size, True)
        if right:
            self.text(self.w - MARGIN_X - width(right, size), self.y, right, size)

    def render(self):
        objs = []

        def add(body):
            objs.append(body)
            return len(objs)

        add("<< /Type /Catalog /Pages 2 0 R >>")  # 1
        add("")  # 2 placeholder for Pages
        f1 = add("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
        f2 = add("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
        page_ids = []
        for ops in self.pages:
            stream = "\n".join(ops)
            cid = add(f"<< /Length {len(stream.encode('latin-1', 'replace'))} >>\nstream\n{stream}\nendstream")
            pid = add(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.w} {self.h}] "
                      f"/Resources << /Font << /F1 {f1} 0 R /F2 {f2} 0 R >> >> /Contents {cid} 0 R >>")
            page_ids.append(pid)
        objs[1] = f"<< /Type /Pages /Kids [{' '.join(f'{p} 0 R' for p in page_ids)}] /Count {len(page_ids)} >>"
        out = bytearray(b"%PDF-1.4\n")
        offsets = []
        for i, body in enumerate(objs, 1):
            offsets.append(len(out))
            out += f"{i} 0 obj\n".encode() + body.encode("latin-1", "replace") + b"\nendobj\n"
        xref = len(out)
        out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
        for off in offsets:
            out += f"{off:010d} 00000 n \n".encode()
        out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
        return bytes(out)


def markdown_to_pdf(md, paper="Letter"):
    d = Doc(paper)
    seen_name, contact_done = False, False
    for raw in md.splitlines():
        line = raw.rstrip()
        if not line.strip():
            if seen_name:
                contact_done = True
            d.y -= 3 if contact_done else 0
            continue
        if line.startswith("# "):
            d._need(30)
            d.y -= 20
            d.text(MARGIN_X, d.y, line[2:], 20, True)
            d.y -= 3
            seen_name = True
        elif line.startswith("## "):
            contact_done = True
            d.heading(line[3:])
        elif line.startswith("### "):
            left, _, right = line[4:].partition("::")
            d.row(left.strip(), right.strip())
        elif line.startswith("- "):
            d.para(strip_inline(line[2:]), indent=16, bullet=True)
        else:
            size = 10 if seen_name and not contact_done else 10.5
            d.para(strip_inline(line), size=size, gap=1)
    return d.render(), len(d.pages)
