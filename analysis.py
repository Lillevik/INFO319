# -*- coding: utf-8 -*-
from afinn import Afinn


def is_positive(text_content, min_value, emoticons=True):
    """
    :param text_content: A text of words.
    :param min_value: minimum score considered positive
    :param emoticons: Use emoticons or not.
    :return: Returns a boolean
    """
    return Afinn(emoticons=emoticons).score(text_content) >= min_value


def get_sentiment(text_content, emoticons=True):
    """
    :param text_content: Returns the sentiment score of a text
    :param emoticons: Use emoticons or not.
    :return: Returns a semtiment score of the text.
    """
    return Afinn(emoticons=emoticons).score(text_content)


def format_tweet(tweet):
    """
    This functions formats the data sent to the api.
    :param tweet:
    :return:
    """
    if 'extended_tweet' in tweet:
        ext_tweet = tweet['extended_tweet']
        if ext_tweet is not None and 'full_text' in ext_tweet:
            tweet['text'] = tweet['extended_tweet']["full_text"]
    tweet['sentiment_score'] = get_sentiment(tweet['text'])
    return tweet


def get_tweet_content(tweet):
    if 'extended_tweet' in tweet:
        ext_tweet = tweet['extended_tweet']
        if ext_tweet is not None and 'full_text' in ext_tweet:
            return tweet['extended_tweet']["full_text"]
        return tweet['text']
    return tweet['text']


# Our filter function
def filter_tweet(tweet):
    """
    This function returns True if the tweet conditions we
    have require is set
    :param tweet: A dict containing the twitter json
    :return: Boolean: True if requirements are met, False otherwise
    """
    try:
        followers_count = tweet['user']['followers_count']  # The number followers the user has
        friends_count = tweet['user']['friends_count']  # The number of people the user follow

        if 'lang' in tweet:
            if tweet['lang'] == 'en' and followers_count >= 200 and friends_count >= 200:
                return True
        return False
    except Exception as e:
        return False


def filter_linking_word(word):
    linking_words = [
        'the', 'a', 'in', 'of', 'and', 'as', 'also', 'too', 'to', 'rt', 'you', 'i', 'me',
        'is', 'for', 'and', 'all', 'this', 'was', 'that', 'an', 'have', 'on', 'from', 'with',
        'are', 'at', 'it', '-', 'got', 'get', '&amp;'
    ]
    return word.lower() not in linking_words and not word.startswith('http')
