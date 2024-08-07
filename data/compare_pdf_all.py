#import PyPDF2 as py2 
from py_pdf_parser.loaders import load_file
#from py_pdf_parser.visualise import visualise
import os
from pathlib import Path
import json
import pandas as pd
import numpy as np
import re
import itertools
from multiprocessing import Pool


import time 
tic=time.perf_counter()

"""
    Vergleicht PDF mit Text und suche PDF Fehler.
    Text der geladenen json Dateien wird mit dem von der PDF ausgelesenen Text verglichen.
    Dabei wird der Text in kurze Stücke geteilt, Leerzeichen entfernt und eine "in" Abfrage gemacht.
    Wenn die Abfrage True ergibt, wird True in Liste eintragen. Wenn False, wird der Text in Liste eintragen.
    Das heißt: Text == False und Fehler kann untersucht werden.
"""

def convert_pages_to_dict(data):
    """
    ändert die ursprünglichen json page in ein dictionary mit der Form:
        {Seite:Text}
    """
    result = {}
    for i in data: 
        result.update({i["number"] : i["content"]})
    return result

def map_apply(doc_element):
    doc_element = doc_element.replace(" ", "")
    a = re.split("\n|\t|\r",doc_element)    
    return a

def is_in_text(text_snipet, text):
    if text_snipet:
        if text_snipet in text:
            return True
        else:
            return text_snipet
        
def PDF_compare_result(dummy_tuple):
    filename, text = dummy_tuple
    document = load_file("./data/docs_pdf/" + filename)
    iterme = [i.text() for i in document.elements]

    iterme = itertools.chain.from_iterable(map(map_apply, iterme))
    iterme = list(iterme)    
    result = map(is_in_text, iterme, itertools.repeat(text, len(iterme)))
    return list(result)

def apply_dummy_func(df):
    """
    Funktion wird benötigt für Multiprocessing.
    Damit Pool() children erzeugen kann.
    """
    return df.apply(PDF_compare_result)

def main(json_path = "./data/data/", pickle_path = "./data/pickle_jar/"):
    df = pd.json_normalize(json.loads(Path(json_path + "docs.json").read_text())["json_docs"])
    df["pages"] = df["pages"].apply(convert_pages_to_dict)
    df["PDF_compare"] = df["pages"].apply(lambda x: " ".join(x.values()))
    df["PDF_compare"] = df["PDF_compare"].apply(lambda x: x.replace("\t", " ").replace("\n", " "))
    df["PDF_compare"] = df["PDF_compare"].apply(lambda x: x.replace(" ", ""))
    df["file_url"] = df["file_url"].apply(lambda x: x.rsplit("/", 1)[1])
    df["PDF_compare"] = df[["file_url", "PDF_compare"]].apply(tuple, axis=1)
    df = df[["id", "file_url", "PDF_compare"]].copy()    
    
    with Pool() as p:
        summe = p.map(apply_dummy_func, np.array_split(df["PDF_compare"], 74))
    
    df["PDF_compare"] = pd.concat(summe)
    toc=time.perf_counter()
    print("time", toc-tic)
    
    with open(pickle_path + "comp_pdf.pickle","wb") as f:
        df.to_pickle(f)


if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent.parent
    os.chdir(BASE_DIR)
    json_path = "./data/data/"
    pickle_path = "./data/pickle_jar/"
    df = pd.json_normalize(json.loads(Path(json_path + "docs.json").read_text())["json_docs"])
    df["pages"] = df["pages"].apply(convert_pages_to_dict)
    df["PDF_compare"] = df["pages"].apply(lambda x: " ".join(x.values()))
    df["PDF_compare"] = df["PDF_compare"].apply(lambda x: x.replace("\t", " ").replace("\n", " "))
    df["PDF_compare"] = df["PDF_compare"].apply(lambda x: x.replace(" ", ""))
    df["file_url"] = df["file_url"].apply(lambda x: x.rsplit("/", 1)[1])
    df["PDF_compare"] = df[["file_url", "PDF_compare"]].apply(tuple, axis=1)
    df = df[["id", "file_url", "PDF_compare"]].copy()    
    
    with Pool() as p:
        summe = p.map(apply_dummy_func, np.array_split(df["PDF_compare"], 74))
    
    df["PDF_compare"] = pd.concat(summe)
    toc=time.perf_counter()
    print("time", toc-tic)
    
    with open(pickle_path + "comp_pdf.pickle","wb") as f:
        df.to_pickle(f)


