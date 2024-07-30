import os
from pathlib import Path
import pandas as pd
import pickle
from makeCorrelation import interesting_words, load_pickle
from wordcloud import WordCloud

   

def make_word_clouds(df_total: pd.DataFrame, df_year: pd.DataFrame,
                   min_std: float = 1.7, max_std: float = 3) -> dict['PIL.Image.Image']:
    """Generates a dictionary of PIL.Image.Image of Wordclouds from two Dataframes.

    Args:
        df_total (pd.DataFrame): DataFrame with words as indices, and a column 'std_normalized' containing a normalized standard deviation.
        df_year (pd.DataFrame): DataFrame with words as columns, and indices being years. Cell values should be relative or absolute frequencies of the word in a year.
        min_std (float, optional): lower bound for the standard deviation, words with lower std will not be considered. Defaults to 1.7.
        max_std (float, optional): upper bound for the standard deviation, words with higher std will not be considered. Defaults to 3.

    Returns:
        dict['PIL.Image.Image']: Dictionary of Images of Wordclouds indexed by years.
    """
    words = interesting_words(df_total,lower=min_std,higher=max_std)
    intr_words_df = df_year[words]
    important_words_year = {}
    wordclouds = {}
    for key in intr_words_df.index:
        important_words_year[key]=intr_words_df.loc[key].sort_values(
            ascending=False).head(100).to_dict()
        wordclouds[key] = WordCloud(width=1200, height=600).generate_from_frequencies(
            important_words_year[key]).to_image()
    return wordclouds

def pickle_clouds(wordclouds: dict['PIL.Image.Image'],
                  pickle_path: str = "./data/pickle_jar/"):
    """Pickles a dictionary of Images into the file "word_clouds.pickle".

    Args:
        wordclouds (dict['PIL.Image.Image']): Dictionary of Images to be pickled.
        pickle_path (str, optional): Path to the save location of the file as string. Defaults to "./data/pickle_jar/".
    """
    with open(pickle_path + "word_clouds.pickle","wb") as f:
        pickle.dump(wordclouds,f)

def makeClouds():
    """
    Führt die makeCoulds.py aus, in default settings
    """
    word_total_df, rel_freq_year = load_pickle()
    clouds = make_word_clouds(df_total = word_total_df,
                              df_year = rel_freq_year)
    pickle_clouds(clouds)   

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    word_total_df, rel_freq_year = load_pickle(path = "./pickle_jar/")
    clouds = make_word_clouds(df_total = word_total_df,
                              df_year = rel_freq_year)
    pickle_clouds(clouds, pickle_path = "./pickle_jar/")