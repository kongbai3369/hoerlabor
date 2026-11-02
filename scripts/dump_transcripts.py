import pypdf

def dump_pages(pdf_path, pages, title):
    print(f"================ {title} ================")
    reader = pypdf.PdfReader(pdf_path)
    for p in pages:
        if p <= len(reader.pages):
            print(f"--- PAGE {p} ---")
            print(reader.pages[p-1].extract_text()[:1500])

dump_pages(r"D:\GermanCorpus\raw\goethe\goethe_b1_transkription.pdf", [34, 35], "Goethe B1 Transkript")
dump_pages(r"D:\GermanCorpus\raw\goethe\goethe_b2_transkription.pdf", [38, 39], "Goethe B2 Transkript")
dump_pages(r"D:\GermanCorpus\raw\goethe\goethe_c1_transkription.pdf", [39, 40], "Goethe C1 Transkript")
dump_pages(r"D:\GermanCorpus\raw\testdaf\testdaf_modellsatz_01_hv_transkription.pdf", [1, 3], "TestDaF 01 Transkript")
