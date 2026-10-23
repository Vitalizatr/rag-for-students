import pymupdf
from abstract.reader import ReaderOS
from abstract.chunker import ChunkerStr
from structure.source import Source
data_folder = "./data"

reader = ReaderOS(data_folder)


for file in reader.get_list_of_files(".pdf"):
    with pymupdf.open(file) as doc:
        text = []
        for page in doc:
            text.append(page.get_text())
        
        s = Source.create_from_pdf(file,text)
        c = ChunkerStr(s,500)

        for chunk in c.divade_chinks(text):
            print(chunk)
