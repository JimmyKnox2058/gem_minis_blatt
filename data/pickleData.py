import os
from pathlib import Path
import json
import pandas as pd
import re
import collections, functools, operator
import pickle

"""
Liest die docs.json in einen pd.DataFrame ein und aggregiert es mit 
Word-Counter und speichert diese als pickle.

wordCountTotal.pickle ist ein collections.Counter dict-subtyp
wordCountByYear.pickle ist ein pd.DataFrame
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

#for a given string returns a dictionary of word counts of that string
def wordCountInString(string) -> collections.Counter:
    """
    Datenbereinigung:
        Enfernt Sonderzeichen und änliches aus dem Text
    Args:
        string (str): Text

    Returns:
        collections.Counter: Wörter gezählt als key-value
    """
    #First split the string into different words, using '\n' or ' ' as separators.
    re_pat = re.compile(r"[\W_]+")
    string = re_pat.sub(" ", string)
    wordList = re.split('\n| ',string.casefold())
    #Useless shrubbery:
    stripString= "0123456789\r\"\f\t.,!?-/\\\'():!§$%^&"
    #Strip each word of useless shrubbery.
    wordList = map(lambda word: word.strip(stripString), wordList)
    #Repress small words.
    wordList = [x for x in wordList if len(x) >1]
    return collections.Counter(wordList)

def pickleData(json_path= "./data/data/", pickle_path= "./data/pickle_jar/"):
    """
    Hauptfunktion dieses Moduls. -> siehe Doku
    Args:
        json_path (str, optional): Quell-Pfad für docs.json Defaults to "./data/data/".
        pickle_path (str, optional): Ziel-Pfad Defaults to "./data/pickle_jar/".
    """

    dummy = json.loads(Path(json_path + "docs.json").read_text())
    df = pd.json_normalize(dummy["json_docs"])
    df["pages"] = df["pages"].apply(convert_pages_to_dict)

    wordCountByPublication=pd.DataFrame(data={'id':df['id'],
                        'wordCounts':df["pages"].apply(lambda x: wordCountInString(" ".join(x.values()))),
                        'year':df['data.year'] })
    wordCountByPublication.to_pickle("wordCountByPublication.pickle")

    wordCountTotal=wordCountByPublication['wordCounts'].sum()
    with open(pickle_path + "wordCountTotal.pickle","wb") as f:
        pickle.dump(wordCountTotal,f)

    wordCountsbyYear=wordCountByPublication.groupby('year')['wordCounts'].sum()

    with open(pickle_path + "wordCountByYear.pickle","wb") as f:
        wordCountsbyYear.to_pickle(f)



if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    pickleData(json_path= "./data/", pickle_path= "./pickle_jar/")
