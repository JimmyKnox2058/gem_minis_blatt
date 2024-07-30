import os
from pathlib import Path
import pandas as pd
import pickle

def del_rare_words(counter: 'collections.Counter', rare_words: list[str]) -> 'collections.Counter':
    """Deletes all words in 'rare_words' from the keys in 'counter'.

    Args:
        counter (collections.Counter): Counter object
        rare_words (list[str]): list of words to delete from counter

    Returns:
        collections.Counter: 'counter' with rare_words deleted.
    """
    for word in rare_words:
        del(counter[word])

def make_stats(pickle_path="./data/pickle_jar/", min_count=100):
    """ Lädt Datensätze mit Worthäufigkeiten und erstellt Dataframes mit Statistiken zu den Wörtern.

    Args:
        pickle_path (str, optional): Quell-Pfad. Defaults to "./data/pickle_jar/".
        min_count (int, optional): Wörter, die über alle Jahre kumuliert seltener
            als min_count vorkommen, werden aus dem Datensatz gelöscht. Defaults to 100.
    Returns:
        word_year_df, Dataframe: Frame with absolute count of words. Columns are words 
            and index are years.
        rel_freq_year, DataFrame: Frame with relative count of words. Columns are words
            and index are years.
        word_total_df, DataFrame: Frame with statistics of words cumulated over all years. 
            Index are words, columns are total count of that word, 
            mean of the relative counts (of each year),
            and a normalized standard deviation of the relative counts.
        publication_df, DataFrame: Frame with absolute count of words. Columns are words
            and index are titles of publications.
    """
    #Load counter with all words and their number of occurences
    with open(pickle_path + "wordCountTotal.pickle","rb") as file:
        word_total = pickle.load(file)
    #load Series with all word counters for all years
    word_year = pd.read_pickle(pickle_path + "wordCountByYear.pickle")
    #All words that appear at most n times in all documents together
    rare_words = [x for x in word_total if word_total[x]<min_count]
    #delete all rare words from the counter of all words
    del_rare_words(word_total, rare_words)
    #delete all rare words from every yearly counter
    word_year.apply(lambda x: del_rare_words(x,rare_words))
    # Cast counters in dataframe into dict
    #  -counters don't behave well with pd.Series
    word_year= word_year.apply(dict)
    # frame with number of occurences of a word in a year
    # first line unpacks the dictionaries in word_year into a dataframe,
    #  columns are words and index are years
    word_year_df = word_year.apply(pd.Series)
    word_year_df.fillna(0,inplace=True)
    
    with open(pickle_path + "wordCountByPublication.pickle","rb") as file:
        publications = pickle.load(file)
    publications['wordCounts'].apply(lambda x: del_rare_words(x,rare_words))
    publication_df = publications['wordCounts'].apply(pd.Series)
    publication_df.set_index(publications['title'], inplace = True)
    publication_df.fillna(0, inplace=True)  
    # Series with the total number of words for every year
    yearlyNumberOfWords = word_year_df.sum(axis=1)
    # Dataframe with the relative frequency of every word in every year
    rel_freq_year = word_year_df.divide(yearlyNumberOfWords, axis=0)
    # make dataframe with all data aggregated over the years for every word
    #  - first fill with words and total occurences of that word
    word_total_df = pd.DataFrame(dict(word_total).items(),columns=['word','total'])
    word_total_df.set_index('word',inplace=True)
    # relative frequency of every word for the total of all years
    #  - normalized by the number of words in every year
    word_total_df['relative frequency'] = rel_freq_year.mean(axis=0)
    # add measure for how strongly the relevance of a word is distributed over the years
    # standard deviation of the relative frequencies -
    #  - normalized such that all words only occuring in a single year have std=10
    word_total_df['std_normalized'] = rel_freq_year.std(axis=0).divide(
        word_total_df['relative frequency'])
    # normalize to std=10
    word_total_df['std_normalized']=word_total_df['std_normalized'].divide(word_total_df['std_normalized'].max())*10
    return word_year_df, rel_freq_year, word_total_df, publication_df

def pickle_everything(word_year_df, rel_freq_year, word_total_df,
                      publication_df,
                      pickle_path = "./data/pickle_jar/"):
    """speichert die DataFrames in pickle ab.

    Args:
        word_year_df (DataFrame): _description_
        rel_freq_year (DataFrame): _description_
        word_total_df (DataFrame): _description_
        publication_df (DataFrame): _description_
        pickle_path (str, optional): Ziel-Pfad . Defaults to "./data/pickle_jar/".
    """
    with open(pickle_path + "statsTotal.pickle","wb") as f:
        word_total_df.to_pickle(f)
    with open(pickle_path + "absoluteYearly.pickle","wb") as f:
        word_year_df.to_pickle(f)
    with open(pickle_path + "relativeYearly.pickle","wb") as f:
        rel_freq_year.to_pickle(f)
    with open(pickle_path + "publication_df.pickle","wb") as f:
        publication_df.to_pickle(f)


if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent
    os.chdir(BASE_DIR)
    word_year_df, rel_freq_year, word_total_df, publication_df = make_stats(pickle_path="./pickle_jar/", min_count=100)
    pickle_everything(word_year_df, rel_freq_year, word_total_df, 
                      publication_df, pickle_path="./pickle_jar/")



