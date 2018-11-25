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
    if 'extended_tweet' in tweet:
        ext_tweet = tweet['extended_tweet']
        if ext_tweet is not None and 'full_text' in ext_tweet:
            tweet['text'] = tweet['extended_tweet']["full_text"]

    tweet['sentiment_score'] = get_sentiment(tweet['text'])
    return tweet


# Our filter function
def filter_tweets(tweet):
    try:
        if 'lang' in tweet:
            if tweet['lang'] == 'en':
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
