import os
from pathlib import Path
import pandas as pd
import pickle
import numpy as np


def load_pickle(path = "./data/pickle_jar/"):
    #Load stats
    with open(path + "statsTotal.pickle","rb") as file:
        word_total_df = pickle.load(file)

    with open(path + "relativeYearly.pickle","rb") as file:
        rel_freq_year = pickle.load(file)

    return word_total_df, rel_freq_year

def interesting_words (word_total_df, lower=1.7, higher=3):
    """
    Function to return a subframe of rel_freq_year, as analyzing too big a frame
    takes too much resources and not every word is interesting to correlate.
    Returns a subframe with all words with a standard deviation between 'lower'
    and 'higher'.
    """ 
    idx = (word_total_df[(word_total_df['std_normalized']<higher) &
                       (lower < word_total_df['std_normalized']) ]).index
    return idx

def correlations (sub_frame_rel_freq):
    """
    Returns a frame with all correlations of a dataframe. Input should be a sub-
    frame of rel_freq_year. Output is a frame with index and columns labelled by
    words with cells containing the correlation.
    """
    return sub_frame_rel_freq.corr()

def strong_correlations (cor_df,cor_min= 0.9):
    """
    Returns a dictionary of all strongly correlated word pairs. Input is a 
    dataframe with correlations of word pairs, eg. from the function 
    'correlations' and a boundary 0<=cor_min<=1 for how strong the correlation
    should be. Keys of the returned dictionary are word pairs and values are
    correlations.
    """
    # Extract values and row, column names
    arr = cor_df.values
    index_names = cor_df.index
    col_names = cor_df.columns

#  Get indices where such threshold is crossed; avoid diagonal elems
    R,C = np.where(np.triu(arr,1)>cor_min)

# Arrange those in columns and put out as a dataframe
    out_arr = np.column_stack((index_names[R],col_names[C],arr[R,C]))
    df_out = pd.DataFrame(out_arr,columns=[['row_name','col_name','value']])
    return df_out

def pickle_correlations(word_total_df, rel_freq_year, lower=1.7, higher=3,
                        cor_min= 0.9, path = "./data/pickle_jar/"):
    """ Main Funktion
    """
    interesting = interesting_words(word_total_df, lower, higher)
    cor_df = correlations(rel_freq_year[interesting])
    strongs = strong_correlations(cor_df, cor_min)
    with open(path + "correlations.pickle","wb") as f:
        cor_df.to_pickle(f)
    with open(path + "strong_correlations.pickle","wb") as f:
        strongs.to_pickle(f)
    with open(path + "interesting_words.pickle","wb") as f:
        pickle.dump(interesting,f)

def makeCorrelation():
    """Default verhalten zum ausführen aus init_pickle.py
    """
    word_total_df, rel_freq_year = load_pickle()
    pickle_correlations(word_total_df, rel_freq_year)


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    word_total_df, rel_freq_year = load_pickle(path = "./pickle_jar/")
    pickle_correlations(word_total_df, rel_freq_year, lower=1.7, higher=3,cor_min= 0.9, path = "./pickle_jar/")

"""
#Tests:
    
word_total_df, rel_freq_year = load_pickle(path = "./pickle_jar/")

interesting = interesting_words(word_total_df)

tic=time.perf_counter()
cor = correlations(rel_freq_year[interesting])
toc=time.perf_counter()
print(toc-tic)

tic=time.perf_counter()
strongs= strong_correlations(cor, 0.9)
toc=time.perf_counter()
print(toc-tic)
"""