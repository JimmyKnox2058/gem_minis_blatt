import requests 
import time
import os
import json
from pathlib import Path
import pandas as pd
from tqdm import tqdm

"""
Dieses script lädt die documents mittels API vom Server und speichert
 im Unterordner als x.json mit x = id 
"""
def dl_doc_inst(dl_path="./data/docs_json", json_path= "./data/data"):
    
    if not os.path.isdir(dl_path): 
        os.makedirs(dl_path) 

    dummy = json.loads(Path(json_path + "/list_doc.json").read_text())
    df = pd.DataFrame(dummy["objects"])
    df = df.loc[df["title"].str.startswith("GMBl Nr")]
    dummy = df["id"].tolist()
    # i = dummy[0]
    for i in tqdm(dummy):
        url = f"https://fragdenstaat.de/api/v1/document/{i}/"
        response = requests.get(url)
        data = response.json()

        with open(f"{dl_path}/doc_id_{i}.json", "w") as f:
            json.dump(data, f)
        # Verzögerung um nicht vom Server blockiert zu werden, als ddos-attacke missverstanden zu werden
        time.sleep(0.5)

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    dl_doc_inst(dl_path="./docs_json", json_path= "./data")