# Run using spark-submit <python_file.py>
import db_handling, analysis, json, requests
from datetime import datetime
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession


# Lazily instantiated global instance of SparkSession
def get_spark_context_instance():
    if "sparkContextSingletonInstance" not in globals():
        globals()["sparkContextSingletonInstance"] = SparkContext("local[2]", "Twitter Streaming context")
    return globals()["sparkContextSingletonInstance"]


def send_count(rdd, url):
    # Send data to api
    requests.post(url, data={'count': json.dumps(rdd.collect())})


def send_tweet(data, url):
    requests.post(url, data={'tweet': json.dumps(data)})


def store_and_send_tweet(rdd):
    tweets = rdd.collect()
    for tweet in tweets:
        tweet = format_tweet(tweet)
        # Store each tweet in the database
        data = {
            'id': tweet['id'],
            'text': tweet['text'],
            'sentiment_score': tweet['sentiment_score'],
            'profile_image_url': tweet['user']['profile_image_url'],
            'screen_name': tweet['user']['screen_name'],
        }
        send_tweet(data, 'http://localhost:5000/incomingTweet')
        db_handling.insert_tweet(tweet)


def format_tweet(tweet):
    if 'extended_tweet' in tweet:
        ext_tweet = tweet['extended_tweet']
        if ext_tweet is not None and 'full_text' in ext_tweet:
            tweet['text'] = tweet['extended_tweet']["full_text"]
            print("USing extended")
    tweet['sentiment_score'] = analysis.get_sentiment(tweet['text'])
    return tweet


# Our filter function:
def filter_tweets(tweet):
    try:
        if 'lang' in tweet:
            if tweet['lang'] == 'en':
                print(type(tweet), tweet['text'])
                return True
        return False
    except Exception as e:
        print("Error: " + str(e))
        return False


def filter_linking_word(word):
    linking_words = [
        'the', 'a', 'in', 'of', 'and', 'as', 'also', 'too', 'to', 'rt', 'you', 'i', 'me',
        'is', 'for', 'and', 'all', 'this', 'was', 'that', 'an', 'have', 'on', 'from', 'with',
        'are', 'at', 'it', '-', 'got', 'get', '&amp;'
    ]
    return word.lower() not in linking_words and not word.startswith('http')  # TODO: Add more words?


# Create the spark context
sc = get_spark_context_instance()  # SparkContext("local[*]", "Twitter Streaming context")
sc.setLogLevel("ERROR")  # Limit output to error messages only.

# Create the sql context and connect to stream
ssc = StreamingContext(sc, 10)  # 10 is the batch interval in seconds
IP = "localhost"
Port = 5555

lines = ssc.socketTextStream(IP, Port)
tweet_objects = lines.map(json.loads) \
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

sortedWordCount.foreachRDD(lambda rdd: send_count(rdd, 'http://localhost:5000/incomingWordCount'))
sortedHashtagCount.foreachRDD(lambda rdd: send_count(rdd, 'http://localhost:5000/incomingHashtagCount'))
# Store filtered tweets to the database
tweet_objects.foreachRDD(lambda rdd: store_and_send_tweet(rdd))

# Map tweets to reduce data send to api TODO: <-


sortedWordCount.saveAsTextFiles("./word_counts/".format(str(datetime.now()) + ".json"))
sortedHashtagCount.saveAsTextFiles("./hashtag_counts/".format(str(datetime.now()) + ".json"))

# sortedWordCount.pprint()
# sortedHashtagCount.pprint()

# You must start the Spark StreamingContext, and await process termination…
ssc.checkpoint("./checkpoints/")
ssc.start()
ssc.awaitTermination()
