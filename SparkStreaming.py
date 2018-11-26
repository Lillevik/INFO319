# Run using spark-submit <python_file.py>
import db_handling, analysis, json, requests
from datetime import datetime
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


def send_data_to_api(data, url, data_type):
    # Send tweet data to the api
    requests.post(url, data={data_type: json.dumps(data)})


def store_and_send_tweet(rdd):
    tweets = rdd.collect()
    tweet_list = []
    for tweet in tweets:
        tweet = analysis.format_tweet(tweet)
        # Store each tweet in the database
        data = {
            'id': tweet['id'],
            'text': tweet['text'],
            'sentiment_score': tweet['sentiment_score'],
            'profile_image_url': tweet['user']['profile_image_url'],
            'screen_name': tweet['user']['screen_name'],
        }
        tweet_list.append(data)
        db_handling.insert_tweet(tweet)
    send_data_to_api(tweet_list, 'http://localhost:5000/incomingTweet', 'tweet')


# Create the spark context
sc = SparkContext("local[2]", "Twitter Streaming context")
sc.setLogLevel("ERROR")  # Limit output to error messages only.

# Create the spark streaming context and connect to stream
ssc = StreamingContext(sc, 10)  # 10 is the batch interval in seconds
IP = "localhost"
Port = 5555

# Read the incoming lines
lines = ssc.socketTextStream(IP, Port)

# Map the incominng text lines to json objects
# and filter these using the custom filter function
tweet_objects = lines.map(json.loads) \
    .filter(lambda tweet: analysis.filter_tweet(tweet))

# Map the tweet objects to a new stream of just the tweet content
tweet_contents = tweet_objects.map(lambda tweet_object: analysis.get_tweet_content(tweet_object))

# Filter out unnecessary noise from the words
words = tweet_contents.flatMap(lambda line: line.split()) \
    .filter(lambda word: analysis.filter_linking_word(word))

# Extract the hashtags from the words
hashtags = words.filter(lambda word: word.startswith('#'))

# Assign the words and hashtags with a value of 1
wordPairs = words.map(lambda word: (word, 1))
hashtagPairs = hashtags.map(lambda hashtag: (hashtag, 1))

# Complete a wordcount using a key and 20 minute window
wordCounts = wordPairs \
    .reduceByKeyAndWindow(lambda x, y: int(x) + int(y), lambda x, y: int(x) - int(y), 1200,
                          10)  # Last 20 minutes, updates every 10 seconds
hashtagCount = hashtagPairs \
    .reduceByKeyAndWindow(lambda x, y: int(x) + int(y), lambda x, y: int(x) - int(y), 1200,
                          10)  # Last 20 minutes, updates every 10 seconds

# Sort the words and hashtags in decending order
sortedWordCount = wordCounts.transform(lambda rdd: rdd.sortBy(lambda x: x[1], False))
sortedHashtagCount = hashtagCount.transform(lambda rdd: rdd.sortBy(lambda x: x[1], False))

# Send word and hashtag counts to the api
sortedWordCount.foreachRDD(lambda rdd: send_data_to_api(rdd.collect(), 'http://localhost:5000/incomingWordCount', 'count'))
sortedHashtagCount.foreachRDD(lambda rdd: send_data_to_api(rdd.collect(), 'http://localhost:5000/incomingHashtagCount', 'count'))

# Store filtered tweets to the database and send them to the api
tweet_objects.foreachRDD(lambda rdd: store_and_send_tweet(rdd))

# Save counts to file
sortedWordCount.saveAsTextFiles("./spark_data/word_counts/".format(str(datetime.now()) + ".json"))
sortedHashtagCount.saveAsTextFiles("./spark_data/hashtag_counts/".format(str(datetime.now()) + ".json"))

# Starts the streaming context
ssc.checkpoint("./spark_data/checkpoints/")
ssc.start()
ssc.awaitTermination()
