import sqlite3, json
from os import path
from datetime import datetime

dirpath = path.abspath(path.dirname(__file__))
db_filename = path.join(dirpath, "emergency_tweets.sqlite")


def insert_tweet(tweet):
    """
    Inserts a tweet to the database
    :param tweet: A twitter object.
    :return: None
    """

    db = sqlite3.connect(db_filename)

    tweet_query = "INSERT INTO Tweet  (created_at, id, id_str, text, source," \
                  " truncated, quoted_status_id, quoted_status_id_str, is_quote_status," \
                  " quote_count, reply_count, retweet_count, favorite_count, favorited," \
                  " retweeted, filter_level, lang, timestamp_ms, lat, lon, place_id, user_id)" \
                  " VALUES " \
                  "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?); "
    lat = None
    lon = None
    coords = get_value(tweet, 'geo')
    if coords:
        coords = coords['coordinates']
        lat = coords[0]
        lon = coords[1]

    global content
    if 'extended_tweet' in tweet:
        content = tweet['extended_tweet']['full_text']
    else:
        content = tweet['text']
    place_id = None
    if 'place' in tweet:
        place = tweet['place']
        if place:
            place_id = tweet['place']['id']
    "Thu Nov 08 19:16:38 +0000 2018"

    created_at = datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S %z %Y")
    tweet_params = [
        int(created_at.strftime('%Y%m%d%H%M%S')),
        get_value(tweet, 'id'),
        get_value(tweet, 'id_str'),
        content,
        get_value(tweet, 'source'),
        get_value(tweet, 'truncated'),
        get_value(tweet, 'quoted_status_id'),
        get_value(tweet, 'quoted_status_id_str'),
        get_value(tweet, 'is_quote_status'),
        get_value(tweet, 'quote_count'),
        get_value(tweet, 'reply_count'),
        get_value(tweet, 'retweet_count'),
        get_value(tweet, 'favorite_count'),
        get_value(tweet, 'favorited'),
        get_value(tweet, 'retweeted'),
        get_value(tweet, 'filter_level'),
        get_value(tweet, 'lang'),
        get_value(tweet, 'timestamp_ms'),
        lat,
        lon,
        place_id,
        tweet['user']['id']
    ]

    user_query = "INSERT INTO User (id, id_str, name, screen_name, location, url, description, verified," \
                 " followers_count, friends_count, favourites_count, statuses_count, lang, created_at) " \
                 " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"

    user_params = [
        tweet['user']['id'],
        tweet['user']['id_str'],
        tweet['user']['name'],
        tweet['user']['screen_name'],
        tweet['user']['location'],
        tweet['user']['url'],
        tweet['user']['description'],
        tweet['user']['verified'],
        tweet['user']['followers_count'],
        tweet['user']['friends_count'],
        tweet['user']['favourites_count'],
        tweet['user']['statuses_count'],
        tweet['user']['lang'],
        tweet['user']['created_at']
    ]

    cursor = db.cursor()
    try:
        cursor.execute(tweet_query, tweet_params)
        cursor.execute(user_query, user_params)
    except sqlite3.IntegrityError:
        pass
    try:
        if place_id:
            place_query = "INSERT INTO Place (id, url, place_type, name, full_name, country_code, country, bounding_box)" \
                          " values (?, ?, ?, ?, ?, ?, ?, ?);"
            place_params = [
                tweet['place']['id'],
                tweet['place']['url'],
                tweet['place']['place_type'],
                tweet['place']['name'],
                tweet['place']['full_name'],
                tweet['place']['country_code'],
                tweet['place']['country'],
                json.dumps(tweet['place']['bounding_box'])
            ]
            cursor.execute(place_query, place_params)
    except sqlite3.IntegrityError as e:
        pass
    db.commit()


def get_value(tweet, key):
    """
    Gets a value from a tweet
    and returns None if it's not there.
    :param tweet: Tweet object
    :param key: Dict key
    :return: Object | None
    """
    if key in tweet:
        return tweet[key]
    return None


def create_db_tables():
    """
    Create database tables if they
    do not already exist.
    :return: None
    """
    dir = path.abspath(path.dirname(__file__))
    db = sqlite3.connect(path.join(dir, 'emergency_tweets.sqlite'))
    with open(path.join(dir, 'db_creation.sql')) as fp:
        queries = fp.read().split("--split--")
        for query in queries:
            db.cursor().execute(query)
        db.commit()
        db.close()


if not path.isfile(db_filename):
    create_db_tables()
