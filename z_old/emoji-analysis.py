import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
import nltk
import emoji
import plotly.graph_objs as go
from plotly.offline import iplot
from collections import Counter
from wordcloud import WordCloud, STOPWORDS

nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer

# 1. Shows all columns (You already have this)
pd.set_option('display.max_columns', None)

# 2. DISABLES WRAPPING by setting the display width to a very high number
pd.set_option('display.width', 1000)

import  warnings
from warnings import filterwarnings
filterwarnings("ignore")

sia = SentimentIntensityAnalyzer()

comments = pd.read_csv(r'/z_old/UScomments.csv', on_bad_lines='skip')
# print(comments.isnull().sum())
comments.dropna(inplace=True)

# print(comments.shape)
sample_df = comments[0:20000]
sentiment_scores = []

for comment in sample_df['comment_text']:
    score = sia.polarity_scores(str(comment))['compound']
    sentiment_scores.append(score)
sample_df['polarity'] = sentiment_scores
# print(sample_df.head(10))
emojis_info = emoji.emoji_list('trending 😉')
# print(emojis_info)
all_emojis_found = []

for comment in sample_df['comment_text']:
    emojis_info = emoji.emoji_list(comment)
    emojis_found = [item['emoji'] for item in emojis_info]
    all_emojis_found.extend(emojis_found)

# print(all_emojis_found[0:10])
emojis_count_list_top10 = Counter(all_emojis_found).most_common(10)

emojis = [emoji for emoji, count in emojis_count_list_top10]
counts = [count for emoji, count in emojis_count_list_top10]

iplot([go.Bar(x = emojis, y = counts)])
# iplot.show()