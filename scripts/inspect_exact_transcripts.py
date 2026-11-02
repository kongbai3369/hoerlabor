import subprocess
import pypdf
import os

RAW_GOETHE = r"D:\GermanCorpus\raw\goethe"
RAW_TESTDAF = r"D:\GermanCorpus\raw\testdaf"
FFMPEG = r"C:\Users\king\AppData\Local\Python\pythoncore-3.15-64\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

# Let's extract full text from TestDaF 01 and TestDaF 02 transcripts
def read_pdf(path):
    reader = pypdf.PdfReader(path)
    return "\n".join([page.extract_text() for page in reader.pages])

tdaf1_txt = read_pdf(os.path.join(RAW_TESTDAF, "testdaf_modellsatz_01_hv_transkription.pdf"))
tdaf2_txt = read_pdf(os.path.join(RAW_TESTDAF, "testdaf_modellsatz_02_hv_transkription.pdf"))

print("=== TESTDAF 01 PREVIEW ===")
for line in tdaf1_txt.split("\n")[:45]:
    if line.strip():
        print("  ", line.strip())

print("\n=== TESTDAF 02 PREVIEW ===")
for line in tdaf2_txt.split("\n")[:45]:
    if line.strip():
        print("  ", line.strip())
