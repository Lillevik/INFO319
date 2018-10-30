# Spark shit
import findspark
findspark.init('/opt/apache-spark')
import pyspark as ps
import pandas as pd
import warnings
from pyspark.sql import SQLContext
# Local shit
import query as q
import cleaner as c
# Other shit
import os

def get_tweets():
    db = q.get_db()
    query = "SELECT User.screen_name, Tweet.text, Tweet.lang FROM Tweet join User ON Tweet.user_id = User.id WHERE Tweet.lang LIKE 'en' ORDER BY Tweet.created_at DESC LIMIT 10;"
    dataset = q.query_db(db, query)
    clean_data = []
    for k, v in enumerate(dataset):
        content = c.tweet_cleaner(v[1])
        #print(k, v[2],v[1].strip('\n\r\t'), "|", content.strip('\n'))
        clean_data.append([v[0], content])
    return clean_data

def create_dataframe():
    try:
        # create SparkContext on all CPUs available: in my case I have 4 CPUs on my laptop
        sc = ps.SparkContext('local[1]')
        sqlContext = SQLContext(sc)
        data = get_tweets()
        df = pd.DataFrame(data)
        print(df.head())
        return df

    except ValueError:
        warnings.warn("SparkContext already exists in this scope")

create_dataframe()