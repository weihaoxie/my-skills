"""Extract figure regions from a PDF by rendering image-block bboxes.

Usage: python extract_figs.py <pdf_path> <out_dir>
Outputs PNGs named {stem}_p{page}_fig{n}.png plus a summary printed to stdout.
"""
import os
import sys

import fitz  # PyMuPDF


def main():
    pdf_path = sys.argv[1]
    out_dir = sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(pdf_path))[0]

    doc = fitz.open(pdf_path)
    print(f"PDF: {pdf_path}")
    print(f"pages: {doc.page_count}")

    # Collect candidate figure bboxes (image blocks, excluding tiny icons
    # and near-full-page backgrounds).
    candidates = []
    for pno in range(doc.page_count):
        page = doc[pno]
        pw, ph = page.rect.width, page.rect.height
        for i, info in enumerate(page.get_image_info()):
            bbox = info["bbox"]
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            if w < 80 or h < 80:
                continue
            if w > pw * 0.98 and h > ph * 0.98:
                continue
            candidates.append((pno + 1, i, bbox, w, h))

    print(f"candidate figures: {len(candidates)}")

    # Merge overlapping bboxes on the same page (one figure split into
    # several raster parts should be rendered once).
    by_page = {}
    for pno, i, bbox, w, h in candidates:
        by_page.setdefault(pno, []).append(bbox)

    saved = 0
    for pno, boxes in sorted(by_page.items()):
        merged = []
        for b in boxes:
            b = fitz.Rect(b)
            placed = False
            for m in merged:
                if fitz.Rect(m).intersects(b):
                    m |= b  # union in place
                    placed = True
                    break
            if not placed:
                merged.append(b)
        # A second pass to absorb chains (A touches B, B touches C)
        changed = True
        while changed:
            changed = False
            for a in range(len(merged)):
                for b in range(a + 1, len(merged)):
                    if merged[a].intersects(merged[b]):
                        merged[a] |= merged[b]
                        merged.pop(b)
                        changed = True
                        break
                if changed:
                    break

        for j, rect in enumerate(sorted(merged, key=lambda r: (r.y0, r.x0)), start=1):
            page = doc[pno - 1]
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=rect)
            out = os.path.join(out_dir, f"{stem}_p{pno}_fig{j}.png")
            pix.save(out)
            saved += 1
            print(f"saved {os.path.basename(out)}  ({pix.width}x{pix.height}px, page {pno})")

    print(f"TOTAL saved: {saved}")


if __name__ == "__main__":
    main()
