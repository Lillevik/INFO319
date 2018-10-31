# Spark shit
import findspark
findspark.init('/opt/apache-spark')
import pyspark as ps
import pandas as pd
import numpy as np
import warnings
from pyspark.sql import SQLContext
# Local shit
import query as q
import cleaner as c
# Other shit
import os


def get_tweets():
    """ Retrieves data from SQLite database and cleans the strings.
        :return: clean_data: List object with clean data_strings ready for analysing.
        TODO: Real time.
    """
    db = q.get_db()
    query = "SELECT Tweet.id, Tweet.text, Tweet.lang FROM Tweet WHERE Tweet.lang LIKE 'en' ORDER BY Tweet.created_at ASC LIMIT 40;"
    dataset = q.query_db(db, query)
    clean_data = []
    for k, v in enumerate(dataset):
        content = c.tweet_cleaner(v[1])
        #print(k, v[2],v[1].strip('\n\r\t'), "|", content.strip('\n'))
        clean_data.append([v[0], content])
    return clean_data


def create_dataframe():
    """ Used to create a pandas.DataFrame object to store data in memory.
        :return df: This DataFrame object.
    """
    try:
        data = get_tweets()
        df = pd.DataFrame(data)
        df.rename(columns={0: 'id', 1: 'text'}, inplace=True)
        print(df)
        return df

    except ValueError:
        warnings.warn("SparkContext already exists in this scope")


def term_frequency_vectorizer(df):
    """ Calculates word frequencies using CountVectorizer.
        Used for term frequency visualization.
        :param df: DataFrame object from create_dataframe()
    """
    from sklearn.feature_extraction.text import CountVectorizer
    cvec = CountVectorizer()
    cvec.fit_transform(df.text)
    words = cvec.get_feature_names()
    print("Len cvec.get_feature_names():", len(words))
    print("{} \n".format(cvec))

    neg_doc_matrix = cvec.transform(df[df.text == 0].text)
    pos_doc_matrix = cvec.transform(df[df.text == 1].text)
    neg_tf = np.sum(neg_doc_matrix, axis=0)
    pos_tf = np.sum(pos_doc_matrix, axis=0)
    neg = np.squeeze(np.asarray(neg_tf))
    pos = np.squeeze(np.asarray(pos_tf))
    term_freq_df = pd.DataFrame([neg, pos], columns=cvec.get_feature_names()).transpose()
    print("{}\n{}\n{}".format(neg, pos, term_freq_df))


def spark(df):
    """ Creates a spark instance used to analyze stuff.
        :param df: DataFrame object with data.
    """
    sc = ps.SparkContext('local[1]')  # create SparkContext on [1/x] CPUs.
    sqlContext = SQLContext(sc)


df = create_dataframe()
print("Data cleaned, Frame made.\n")
term_frequency_vectorizer(df)