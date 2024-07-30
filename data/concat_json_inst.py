import os
from pathlib import Path
import json
import itertools


"""
 Dieses script sucht alle Dateien im Verzeichnes des Scripts die auf json enden.
 Diese werden als dict geladen und auf die Liste im key "objects" beschränkt 
  und zusammengeführt. Das Ergebnis wird als neue result.json gespeichert.

"""
def concat_json_inst(json_path="./data/docs_json"):
    # dummy = [y for y in [x for a, b, x in os.walk("./docs_json")][0] if y.endswith("json")]
    dummy = [pos_file for pos_file in os.listdir(json_path) if pos_file.endswith("json")]
    def load_da_json(filename):
        return json.loads(Path(json_path + "/" + filename).read_text())

    # test = itertools.chain.from_iterable(map(load_da_json, dummy))
    test = map(load_da_json, dummy)

    with open("/data/data/docs.json", "w") as f:
        json.dump({"json_docs":list(test)}, f)


    # debugme = load_da_json("doc_id_240723.json")


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    concat_json_inst()
