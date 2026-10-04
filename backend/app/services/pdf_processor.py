import re
from pathlib import Path

from pypdf import PdfReader

HEADING = re.compile(r"^(\d+(\.\d+)*\.?\s+\S.{2,80}|[A-Z][A-Z \-&]{5,60})$")


def extract_chunks(path: Path, size: int = 900, overlap: int = 150) -> tuple[list[dict], int]:
    """Split a PDF into overlapping text chunks tagged with page number and nearest section heading."""
    reader = PdfReader(str(path))
    chunks, section = [], "General"
    for n, page in enumerate(reader.pages, 1):
        lines = [l.strip() for l in (page.extract_text() or "").splitlines() if l.strip()]
        for l in lines:
            if HEADING.match(l):
                section = l[:80]
        body = " ".join(lines)
        for start in range(0, len(body), size - overlap):
            piece = body[start:start + size].strip()
            if len(piece) > 40:
                chunks.append({"text": piece, "page": n, "section": section})
    return chunks, len(reader.pages)
