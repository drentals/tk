#!/usr/bin/env python3
"""
fix_statement.py 

Replace an address on page 1 of a Taekus statement PDF

with a provided address

while embedding the full ABC Monument Grotesk Regular (or any OTF / TTF
you supply) so all glyphs render and the font remains consistent.

─────────────────────────────────────────────────────────────
USAGE
    python fix_statement.py in.pdf out.pdf full_font.otf

DEPENDENCIES
    pip install PyMuPDF==1.25.5
"""

import sys
from pathlib import Path
import re
import fitz  # PyMuPDF 1.25.5  wheel

# Update this with the strings to replace
OLD = ["555 Main Street", "APT 1", "Some City, KS 11111"]
NEW = "222 Maint Street Ojai, CA"


def find_box(page):
    rects = [page.search_for(t, quads=False)[0] for t in OLD]
    rects.sort(key=lambda r: r.y0)
    return rects[0] | rects[-1]            # union rectangle


def shrink(font_path, box, size, text):
    f = fitz.Font(fontfile=str(font_path))
    max_w = box.x1 - box.x0
    for line in text.splitlines():
        w = f.text_length(line, fontsize=size)
        if w > max_w:
            size = size * max_w / w * 0.96  # 4 % margin
    return size


def main(src_pdf: Path, dst_pdf: Path, font_path: Path):
    doc  = fitz.open(src_pdf)
    page = doc[0]

    box = find_box(page)
    base_size = (
        page.get_text("dict", clip=box)
        ["blocks"][0]["lines"][0]["spans"][0]["size"]
    )

    # ─ Embed full Monument Grotesk and resolve tag string ───────────────
    ret = page.insert_font(fontfile=str(font_path))   # int (xref) or str(tag)
    if isinstance(ret, int):                          # convert xref → 'F#'
        tag = next(t[3] for t in page.get_fonts(full=False) if t[0] == ret)
    else:
        tag = ret

    # ─ Remove old address ───────────────────────────────────────────────
    page.add_redact_annot(box, fill=(1, 1, 1))
    page.apply_redactions()

    # ─ Ensure new text fits & insert ────────────────────────────────────
    size = shrink(font_path, box, base_size, NEW)
    page.insert_textbox(
        box,
        NEW,
        fontname=tag,
        fontsize=size,
        align=fitz.TEXT_ALIGN_LEFT,
    )

    doc.save(dst_pdf, garbage=4, deflate=True, clean=True)
    print("✓ Address replaced →", dst_pdf)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage:\n  python fix_statement.py in.pdf out.pdf full_font.otf")
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))

