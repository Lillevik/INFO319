import tweepy, os, json, sqlite3

consumer_token = "A416DpVGgr6ojpB3ITnnh3ZIe"
consumer_secret = "CJbxJRIxRpmVsGg5d8bxRzpSW0qMuaeRuCRyl2bSI9KISGPo92"
access_token = "379895356-xWon3y2j9ZLPeGbnZOpHUMy7dT5siXTic5BtHIXY"
access_token_secret = "aCFWjzo7J6D5ok7bXCTss8y2NTJeqvKpsbKCi6jovP9a1"


# override tweepy.StreamListener to add logic to on_status
class CrisisStreamListener(tweepy.StreamListener):
    """
    This is the Stream handler class.
    """

    def __init__(self):
        super().__init__()
        self.dirpath = os.path.abspath(os.path.dirname(__file__))
        self.db_filename = os.path.join(self.dirpath, "Tweets_db.sqlite")
        self.out_filename = os.path.join(self.dirpath, "Tweets.json")
        if not os.path.isfile(self.out_filename):
            # Create if it does not exist
            with open(self.out_filename, 'w+') as fb:
                fb.close()
        self.db = sqlite3.connect(self.db_filename)

    def on_status(self, tweet):
        """
        Handles the incoming tweet event.
        Storing the data locally.
        :param tweet: A tweet object.
        :return:
        """
        try:
            self.append_tweet(tweet._json)
            self.insert_tweet(tweet)
            print(tweet.created_at)
        except KeyboardInterrupt:
            print("Program was stopped by the keyboard.")
        except Exception as e:
            print(e, tweet._json)

    def on_error(self, status_code):
        """
        Handles the stream errors
        :param status_code:
        :return:
        """
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False
        # returning non-False reconnects the stream, with backoff.

    def append_tweet(self, json_string):
        """
        Appends a json twitter object to file.
        :param json_string: String representation of the
        tweet.
        :return: None
        """
        out_file = open(self.out_filename, 'a', encoding="utf-8")
        out_file.write(json.dumps(json_string) + "\n")
        out_file.close()

    def insert_tweet(self, tweet):
        """
        Inserts a tweet to the database
        :param tweet: A twitter object.
        :return: None
        """
        query = "INSERT INTO Tweet  (created_at, id, id_str, text, source," \
                " truncated, quoted_status_id, quoted_status_id_str, is_quote_status," \
                " quote_count, reply_count, retweet_count, favorite_count, favorited," \
                " retweeted, filter_level, lang, timestamp_ms)" \
                " VALUES " \
                "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?); "
        params = [
            int(tweet.created_at.strftime('%Y%m%d%H%M%S')),
            self.get_value(tweet, 'id'),
            self.get_value(tweet, 'id_str'),
            self.get_value(tweet, 'text'),
            self.get_value(tweet, 'source'),
            self.get_value(tweet, 'truncated'),
            self.get_value(tweet, 'quoted_status_id'),
            self.get_value(tweet, 'quoted_status_id_str'),
            self.get_value(tweet, 'is_quote_status'),
            self.get_value(tweet, 'quote_count'),
            self.get_value(tweet, 'reply_count'),
            self.get_value(tweet, 'retweet_count'),
            self.get_value(tweet, 'favorite_count'),
            self.get_value(tweet, 'favorited'),
            self.get_value(tweet, 'retweeted'),
            self.get_value(tweet, 'filter_level'),
            self.get_value(tweet, 'lang'),
            self.get_value(tweet, 'timestamp_ms'),
        ]
        self.db.cursor().execute(query, params)
        self.db.commit()

    def get_value(self, tweet, key):
        """
        Gets a value from a tweet
        and returns None if it's not there.
        :param tweet: Tweet object
        :param key: Dict key
        :return: Object | None
        """
        if key in tweet._json:
            return tweet._json[key]
        return None


def create_db_tables():
    """
    Create database tables if they
    do not already exist.
    :return: None
    """
    dir = os.path.abspath(os.path.dirname(__file__))
    db = sqlite3.connect(os.path.join(dir, 'Tweets_db.sqlite'))
    with open(os.path.join(dir, 'db_creation.sql')) as fp:
        query = fp.read()
        db.cursor().execute(query)
        db.close()


def run():
    """
    Run the twitter stream program
    :return:
    """
    print("Starting up...")
    create_db_tables()
    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    cslListener = CrisisStreamListener()
    cslStream = tweepy.Stream(auth=auth, listener=cslListener)

    print("Waiting for Twitter data.")
    # The api user an OR operator. This means we can't filter on both location
    # and terms. We are there fore collecting all tweets based on location and
    # will filter on terms manually afterwards or before database insertiion.
    cslStream.filter(  # track=['crisis'],
        locations=[4.4224534002, 57.6773084094, 13.2416495125, 63.8360955113 ]) # Sørlige halvdel av Norge.



# Start the stream
run()
