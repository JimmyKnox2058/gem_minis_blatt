import requests 
import time
import os
import json as js
from pathlib import Path
from tqdm import tqdm


"""
Dieses script lädt die Inhaltsliste aller documents vom Server und speichert
 im Unterverzeichnes diesem scripts
"""
def dl_doc_list(dl_path="./data/list_json"):
    if not os.path.isdir(dl_path): 
        os.makedirs(dl_path) 

    url = "https://fragdenstaat.de/api/v1/document/"

    # if starting Download the first time
    start = 0

    # dieser Teil ist für den Fall das was nicht funktioniert und das Programm 
    # neu gestartet wurde nachdem schon die ersten geladen wurden
    # ### old version ### dummy = [x for a, b, x in os.walk(".")][0]
    # dummy = [pos_file for pos_file in os.listdir("./list_json") if pos_file.endswith("json")]
    # dummy = [int(x.split(".")[0]) for x in dummy if x.endswith("json")]
    # start = max(dummy) +50

    for i in tqdm(range(start, 233850, 50)):
        # limit hat sich nicht auf größer 50 ändern lassen, kleiner 50 geht
        sent_option = {"params" : {
                "limit": 50,
                "offset": i,
                "format": "json"}}
            
        response = requests.get(url, **sent_option)
        data = response.json()

        with open(f"{dl_path}/{i}.json", "w") as f:
            js.dump(data, f)

        # Verzögerung um nicht vom Server blockiert zu werden, als ddos-attacke missverstanden zu werden
        time.sleep(0.5)
    
if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    dl_doc_list(dl_path="./list_json")