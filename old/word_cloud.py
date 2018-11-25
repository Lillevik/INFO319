import os, sqlite3
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Get data directory
data = path.abspath(path.dirname(__file__))
text_content = ""
conn = sqlite3.connect(path.join(data, 'Tweets_db.sqlite'))
tweets = conn.execute("SELECT text FROM Tweet;").fetchall()
tweetOut = None
try:
    for tweet in tweets:
        tweetOut = tweet
        for word in tweet[0].split(" "):
            if word.startswith("#"):
                text_content += word + " "
except sqlite3.DatabaseError as e:
    print(e)
    print(tweetOut, "\n")



# Generate word cloud
wordcloud = WordCloud().generate(text_content)


# Display word cloud
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.savefig("HashTags.png")

