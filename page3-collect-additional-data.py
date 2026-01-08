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
from sqlalchemy import create_engine
from plotly.offline import iplot
from collections import Counter
from wordcloud import WordCloud, STOPWORDS

# nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer

# 1. Shows all columns (You already have this)
pd.set_option('display.max_columns', None)

# 2. DISABLES WRAPPING by setting the display width to a very high number
pd.set_option('display.width', 1000)

import  warnings
from warnings import filterwarnings
filterwarnings("ignore")

files = os.listdir(r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\youtube-videos-data-analysis\additional_data')

files_csv = [file for file in files if '.csv' in file]

# print(files_csv)
full_df = pd.DataFrame()
path = r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\youtube-videos-data-analysis\additional_data'

for file in files_csv:
    current_df = pd.read_csv(path+'/'+file, encoding='iso-8859-1', on_bad_lines='skip')
    full_df = pd.concat([full_df,current_df], ignore_index=True)

# print(full_df[full_df.duplicated()].shape)

full_df = full_df.drop_duplicates()

print(full_df.shape)

full_df[0:1000].to_csv(r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\youtube-videos-data-analysis\export_data/youtube_sample.csv', index = False)
full_df[0:1000].to_json(r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\youtube-videos-data-analysis\export_data/youtube_sample.json')

engine = create_engine(r"sqlite:///C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\youtube-videos-data-analysis\export_data\youtube_sample.sqlite")

full_df[0:1000].to_sql('Users', con=engine, if_exists='append')