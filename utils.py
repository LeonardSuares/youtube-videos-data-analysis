import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
import nltk
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

comments = pd.read_csv(r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\youtube-videos-data-analysis\UScomments.csv', on_bad_lines= 'skip')
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

filter_pos = (sample_df['polarity'] >= 0.8) & ((sample_df['polarity'] <= 1.0))
comments_positive = sample_df[filter_pos]

filter_neg = (sample_df['polarity'] >= -1.0) & ((sample_df['polarity'] <= 0.8))
comments_negative = sample_df[filter_neg]

# print(comments_negative)

total_positive_comments = ' '.join(comments_positive['comment_text'])
wordcloud_positive = WordCloud(stopwords= set(STOPWORDS)).generate(total_positive_comments)

plt.figure(figsize=(15, 5))
plt.imshow(wordcloud_positive)
plt.axis('off')
plt.title("Positive Comments Word Cloud")
plt.show()

total_negative_comments = ' '.join(comments_negative['comment_text'])
wordcloud_negative = WordCloud(stopwords= set(STOPWORDS)).generate(total_negative_comments)

plt.figure(figsize=(15, 5))
plt.imshow(wordcloud_negative)
plt.axis('off')
plt.title("Negative Comments Word Cloud")
plt.show()

