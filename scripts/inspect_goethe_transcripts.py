import pypdf
import re

def search_pdf(path, name):
    print(f"================ {name} ================")
    reader = pypdf.PdfReader(path)
    found_pages = []
    for idx, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if "transkription" in text.lower() or "hörtext" in text.lower() or "teil 1" in text.lower():
            found_pages.append((idx + 1, text))
    print(f"Total pages: {len(reader.pages)}, matched pages: {len(found_pages)}")
    for p_num, text in found_pages:
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        header = " | ".join(lines[:4])
        print(f"Page {p_num}: {header[:120]}")

search_pdf(r"D:\GermanCorpus\raw\goethe\goethe_b1_transkription.pdf", "Goethe B1")
search_pdf(r"D:\GermanCorpus\raw\goethe\goethe_b2_transkription.pdf", "Goethe B2")
search_pdf(r"D:\GermanCorpus\raw\goethe\goethe_c1_transkription.pdf", "Goethe C1")
