

import os
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Get data directory
data = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

# Read the whole text
text = open(path.join(data, 'manus.txt')).read()

# Generate word cloud
wordcloud = WordCloud().generate(text)

# Display word cloud
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

