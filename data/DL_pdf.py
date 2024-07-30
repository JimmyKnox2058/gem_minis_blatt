import requests 
# import time
import os
import json
from pathlib import Path
import pandas as pd
from tqdm import tqdm


"""
Dieses script lädt die pdf vom Server und speichert im Unterordner
"""
def dl_pdf(dl_path="./data/docs_pdf", json_path= "./data/data"):
    if not os.path.isdir(dl_path): 
        os.makedirs(dl_path) 

    dummy = json.loads(Path(json_path + "/list_doc.json").read_text())
    df = pd.DataFrame(dummy["objects"])
    df = df.loc[df["title"].str.startswith("GMBl Nr")]
    dummy = df["file_url"].tolist()

    for i in tqdm(dummy):
        response = requests.get(i)
        filename = i.rsplit("/", 1)[1]
        open(f"{dl_path}/{filename}", "wb").write(bytes(response.content))
    
        
        # ausgeführt ohne sleep. hat geklappt und gab keine server Blockierung
        # time.sleep(0.5)

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    dl_pdf(dl_path="./docs_pdf", json_path= "./data")
    