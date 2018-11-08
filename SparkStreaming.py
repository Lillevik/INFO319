# Run using spark-submit python_file.py
import json
import traceback
import requests
from datetime import datetime

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
import db_handling


# Lazily instantiated global instance of SparkSession
def get_spark_session_instance():
    if "sparkSessionSingletonInstance" not in globals():
        globals()["sparkSessionSingletonInstance"] = SparkSession \
            .builder \
            .config("local[*]", "Twitter Streaming") \
            .getOrCreate()
    return globals()["sparkSessionSingletonInstance"]


# Lazily instantiated global instance of SparkSession
def get_spark_context_instance():
    if "sparkContextSingletonInstance" not in globals():
        globals()["sparkContextSingletonInstance"] = SparkContext("local[2]", "Twitter Streaming context")
    return globals()["sparkContextSingletonInstance"]


# Our filter function:
def filter_tweets(tweet):
    try:
        if 'lang' in tweet:
            global text
            if tweet['lang'] == 'en':
                if 'extended_tweet' in tweet:
                    text = tweet['extended_tweet']["full_text"]
                    tweet['text'] = text
                return True
        return False
    except Exception as e:
        print(str(e) + " : ", tweet)
        print(traceback.format_exc())


def filter_linking_word(word):
    linking_words = [
        'the', 'a', 'in', 'of', 'and', 'as', 'also', 'too', 'to', 'rt', 'you', 'i', 'me',
        'is', 'for', 'and', 'all', 'this', 'was', 'that', 'an', 'have', 'on', 'from', 'with',
        'are', 'at', 'it', '-', 'got', 'get'
    ]
    return word.lower() not in linking_words and not word.startswith('http')  # TODO: Add more words?


# Create the spark context
sc = SparkContext("local[2]", "Twitter Streaming context")
sc.setLogLevel("ERROR")

# Create the sql context and connect to stream
sqlContext = get_spark_session_instance()
ssc = StreamingContext(sc, 10)  # 10 is the batch interval in seconds
IP = "localhost"
Port = 5555

lines = ssc.socketTextStream(IP, Port)
tweet_objects = lines.map(lambda json_string: (json.loads(json_string))) \
    .filter(lambda tweet: filter_tweets(tweet))

tweet_contents = tweet_objects.map(lambda tweet_object: tweet_object['text'])

words = tweet_contents.flatMap(lambda line: line.split()) \
    .filter(lambda word: filter_linking_word(word))
hashtags = words.filter(lambda word: word.startswith('#'))

wordPairs = words.map(lambda word: (word, 1))
hashtagPairs = hashtags.map(lambda hashtag: (hashtag, 1))

wordCounts = wordPairs.reduceByKeyAndWindow(lambda x, y: int(x) + int(y), lambda x, y: int(x) - int(y), 1200,
                                            10)  # Last 20 minutes, updates every 10 seconds
hashtagCount = hashtagPairs.reduceByKeyAndWindow(lambda x, y: int(x) + int(y), lambda x, y: int(x) - int(y), 1200,
                                                 10)  # Last 20 minutes, updates every 10 seconds

sortedWordCount = wordCounts.transform(lambda rdd: rdd.sortBy(lambda x: x[1], False))
sortedHashtagCount = hashtagCount.transform(lambda rdd: rdd.sortBy(lambda x: x[1], False))


def handler(rdd, url):
    # Send data to api
    requests.post(url, data={'count': json.dumps(rdd.collect())})


def send_tweets(rdd, url):
    tweets = rdd.collect()
    for tweet in tweets:
        db_handling.insert_tweet(tweet)
        requests.post(url, data={'tweet': json.dumps(tweet)})


sortedWordCount.foreachRDD(lambda rdd: handler(rdd, 'http://localhost:5000/incomingWordCount'))
sortedHashtagCount.foreachRDD(lambda rdd: handler(rdd, 'http://localhost:5000/incomingHashtagCount'))
tweet_objects.foreachRDD(lambda rdd: send_tweets(rdd, "http://localhost:5000/incomingTweet"))


sortedWordCount.saveAsTextFiles("./word_counts/".format(str(datetime.now()) + ".json"))
sortedHashtagCount.saveAsTextFiles("./hashtag_counts/".format(str(datetime.now()) + ".json"))


# sortedWordCount.pprint()
# sortedHashtagCount.pprint()

# You must start the Spark StreamingContext, and await process termination…
ssc.checkpoint("./checkpoints/")
ssc.start()
ssc.awaitTermination()
