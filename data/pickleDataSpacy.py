import os
from pathlib import Path
import json
import pandas as pd
import collections
import pickle
import spacy
from multiprocessing import Pool
import numpy as np

"""
Liest die docs.json in einen pd.DataFrame ein und aggregiert es mit 
Word-Counter und speichert diese als pickle.

wordCountTotal.pickle ist ein collections.Counter dict-subtyp
wordCountByYear.pickle ist ein pd.DataFrame
"""

def convert_pages_to_dict(data) -> dict['str']:
    """ändert die ursprünglichen json page in ein dictionary mit der Form:
        {Seite:Text}

    Args:
        data : 'pages'-Eintrag der gedownloadeten json-Dateien.

    Returns:
        dict['str']: Dictionary mit Seitenzahlen als Keys und Seitentext als Werte.
    """
    result = {}
    for i in data: 
        result.update({i["number"] : i["content"]})
    return result

#for a given string returns a dictionary of word counts of that string
def wordCountInString(string, nlp=spacy.load("de_core_news_sm")) -> collections.Counter:
    """
    Zählt lemmatisierte Adjektive und Nomen in 'string'.
    Args:
        string (str): String mit Text oder Dictionary mit Strings als Values.
        nlp: 
    Returns:
        collections.Counter: Lemmatisierte Wörter gezählt als key-value.
    """
    if type(string) == dict:
        string = " ".join(string.values())
    nlp.max_length = 10000000

    doc = nlp(string)
    wordList = [token.lemma_.casefold() for token in doc if 
                token.is_alpha and not token.is_stop and (
                    token.pos_ =='ADJ' or token.pos_=='NOUN'
                    or token.pos_=='PROPN')]
    wordList = [word for word in wordList if len(word)>3]
    return collections.Counter(wordList)

def apply_wordcountinstring(df):
    """
    Helper function to apply wordCountInString() to a dataframe.
    """
    return df.apply(wordCountInString)

def pickleData(json_path= "./data/data/", pickle_path= "./data/pickle_jar/"):
    """
    Hauptfunktion dieses Moduls. Liest die konkatenierten json ein, erstellt Dataframes
        mit absoluten Worthäufigkeiten nach Publikation, Jahr und insgesamt.
        Pickelt diese Dataframes anschließend zur Weiterverarbeitung.
    Args:
        json_path (str, optional): Quell-Pfad für docs.json Defaults to "./data/data/".
        pickle_path (str, optional): Ziel-Pfad Defaults to "./data/pickle_jar/".
    """
    dummy = json.loads(Path(json_path + "docs.json").read_text())
    df = pd.json_normalize(dummy["json_docs"])
    df["pages"] = df["pages"].apply(convert_pages_to_dict)

    wordCountByPublication=pd.DataFrame(data={'title':df['title'],
                        'wordCounts':df["pages"],
                        'year':df['data.year'] })

    with Pool() as p:
        summe1 = p.map(apply_wordcountinstring, np.array_split(wordCountByPublication["wordCounts"], 74))

    wordCountByPublication["wordCounts"] = pd.concat(summe1)
    
    with open(pickle_path + "wordCountByPublication.pickle","wb") as f:
        wordCountByPublication.to_pickle(f)

    wordCountsbyYear=wordCountByPublication.groupby('year')['wordCounts'].sum()
    with open(pickle_path + "wordCountByYear.pickle","wb") as f:
        wordCountsbyYear.to_pickle(f)

    wordCountTotal=wordCountsbyYear.sum()
    with open(pickle_path + "wordCountTotal.pickle","wb") as f:
        pickle.dump(wordCountTotal, f)

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    pickleData(json_path= "./data/", pickle_path= "./pickle_jar/")
