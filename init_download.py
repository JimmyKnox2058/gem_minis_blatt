import os
from pathlib import Path

from data.concat_json_inst import concat_json_inst
from data.concat_json_list import concat_json_list
from data.DL_doc_instance import dl_doc_inst
from data.DL_doc_list import dl_doc_list
from data.DL_pdf import dl_pdf

"""Diese Datei nur einmal starten um die Daten von www.fragdenstaat.de
runter zu laden.
Dies kann einige Zeit in Anspruch nehmen.
Führt den Dowload von den JSON nicht aus wenn die benötigten Dateien vorhanden sind.

Muss nur 1 mal ausgeführt werden!


"""
if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    if not os.path.exists("./data/data/list_docs.json"):
        dl_doc_list()
        concat_json_list()
    if not os.path.exists("./data/data/list_docs.json"):
        dl_doc_inst()
        concat_json_inst()
    dl_pdf()
