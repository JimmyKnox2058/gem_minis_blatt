import os
from pathlib import Path
import json
import itertools

"""
 Dieses script sucht alle Dateien im Verzeichnes des Scripts die auf json enden.
 Diese werden als dict geladen und auf die Liste im key "objects" beschränkt 
  und zusammengeführt. Das Ergebnis wird als neue result.json gespeichert.
"""
def concat_json_list(data_path="./data/data", json_path="./data/list_json"):
    if not os.path.isdir(data_path): 
        os.makedirs(data_path) 


    path_list = [pos_file for pos_file in os.listdir(json_path) if pos_file.endswith("json")]

    def load_da_json(filename):
        return json.loads(Path(json_path+ "/" + filename).read_text())["objects"]

    test = itertools.chain.from_iterable(map(load_da_json, path_list))

    with open(data_path + "/list_doc.json", "w") as f:
        json.dump({"objects":list(test)}, f)


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    concat_json_list(data_path="./data", json_path="./list_json")