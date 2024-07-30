"""This file contains methods for topic modelling from a dataframe with word vectors.
    In particular, there is a methods to create a dataframe with topics and a method
    to create word clouds from such a dataframe.
"""
import os
from pathlib import Path
import pandas as pd
import pickle
from wordcloud import WordCloud
from sklearn.decomposition import LatentDirichletAllocation



def make_topic_frame(word_frame: pd.DataFrame, n_topics: int = 50, n_words: int = 20) -> pd.DataFrame:
    """Generates a dataframe of n_topics topics, each containing n_words words.
        The returned dataframe has n_words rows and 2*n_topics columns, each topic having 2 consecutive columns.
        The first column of each topic consists of the n_words words with the highest weights in that topic.
        The second column of each topic consists of the weights as floats.

    Args:
        word_frame (pd.DataFrame): A dataframe with column names being words,
             every column containing a vectorization of its word.
        n_topics (int, optional): Number of topics to return. Defaults to 25.
        n_words (int, optional): Number of words to return for each topic. Defaults to 100.

    Returns:
        pd.DataFrame: Dataframe of n_topics topics, each containing n_words words
    """
    model = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    model.fit(word_frame)
    def display_topics(model, feature_names, no_top_words):
        topic_dict = {}
        for topic_idx, topic in enumerate(model.components_):
            topic_dict["Topic %d words" % (topic_idx)]= [feature_names[i]
                            for i in topic.argsort()[:-no_top_words - 1:-1]]
            topic_dict["Topic %d weights" % (topic_idx)]= [topic[i]
                            for i in topic.argsort()[:-no_top_words - 1:-1]]
        return pd.DataFrame(topic_dict)
    return display_topics(model, word_frame.columns, n_words)

def make_topic_clouds(topic_df: pd.DataFrame, n_words: int =20) ->list['PIL.Image.Image']:
    """Generates a list of wordclouds from a dataframe with topics.

    Args:
        topic_df (pd.DataFrame): Dataframe as returned from make_topic_frame()
        n_words (int, optional): Number of words of each topic to be put into the word cloud. 
            Should not be more than the number of rows of topic_df Defaults to 100.
    Returns:
        list['PIL.Image.Image']: List of word clouds as images.
    """
    topic_clouds=[]
    for i in range(len(topic_df.columns)//2):
        b = pd.Series(topic_df.iloc[:,2*i+1].values, index=topic_df.iloc[:,2*i]).head(n_words)
        if b.iloc[0]>1: 
        #Sometimes non-sense topics appear with low weights <1, this is to get rid of them
            topic_clouds.append(WordCloud(width=1200, height=600).generate_from_frequencies(b).to_image())
    return topic_clouds


def pickle_clouds(wordclouds: list['PIL.Image.Image'],
                  pickle_path: str = "./data/pickle_jar/"):
    """Pickles a dictionary of Images into the file "topic_clouds.pickle".

    Args:
        wordclouds (dict['PIL.Image.Image']): Dictionary of Images to be pickled.
        pickle_path (str, optional): Path to the save location of the file as string. Defaults to "./data/pickle_jar/".
    """
    with open(pickle_path + "topic_clouds.pickle","wb") as f:
        pickle.dump(wordclouds,f)
        
def load_pickle(path = "./data/pickle_jar/"):
    """Loads the data for intended use of this module.

    Args:
        path (str, optional): Path to the location of the files. Defaults to "./data/pickle_jar/".

    Returns:
        _type_: Index of interesting words and dataframe of absolute counts of words for each year.
    """
    with open(path + "interesting_words.pickle","rb") as file:
        interesting_words = pickle.load(file)

    with open(path + "publication_df.pickle","rb") as file:
        publication_df = pickle.load(file)

    return interesting_words, publication_df


def makeTopics():
    """
    Führt die makeTopics.py aus, in default settings
    """
    interesting_words, publication_df = load_pickle()
    topic_frame = make_topic_frame(publication_df[interesting_words])
    clouds =  make_topic_clouds(topic_frame)
    pickle_clouds(clouds)
        
if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    interesting_words, publication_df = load_pickle(path = "./pickle_jar/")
    topic_frame = make_topic_frame(publication_df[interesting_words])
    clouds =  make_topic_clouds(topic_frame)
    pickle_clouds(clouds, pickle_path = "./pickle_jar/")


