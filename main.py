import pymupdf
from abstract.reader import ReaderOS
import re
data_folder = "./data"

reader = ReaderOS(data_folder)

def structure_correct(s:str):
    res = ""
    i = 0
    while i < len(s)-2:
        if(False):
            res+=f"{s[i]}{s[i+2]}"
            i+=3
        else:
            res+=s[i]
            i+=1
    return res

count = 0
for file in reader.get_list_of_files(".pdf"):
    with pymupdf.open(file) as doc:
        for i,page in enumerate(doc):
            count+=len(page.get_text())


print(count)