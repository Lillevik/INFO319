from afinn import Afinn
import query
import spark
import os

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

#    for x in range(): 

analyze()