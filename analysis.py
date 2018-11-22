# -*- coding: utf-8 -*-
from afinn import Afinn
import query, nltk, re, pprint
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import datetime

# Download punkt
nltk.download(['punkt', 'averaged_perceptron_tagger'])


def analyze():
    db = query.get_db()
    q = "SELECT * FROM Tweet JOIN User ON Tweet.user_id = User.id WHERE User.location LIKE '%Manchester%' ORDER BY User.id LIMIT 10 ;"
    q2 = "SELECT * FROM Tweet where lang = 'en';"
    rows = query.query_db(db, q2)
    afinn = Afinn()
    print("   Tweet ID    |score| Tweet content\n")
    for row in rows:
        tweet_content = row[3].strip("\t\r\n")
        if tweet_content == None: tweet_content = ""
        sentiment = afinn.score(tweet_content)
        print("{} | {} | {}".format(row[0], sentiment, tweet_content))


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


