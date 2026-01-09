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

# print(full_df['category_id'].unique())

json_df = pd.read_json(r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\youtube-videos-data-analysis\additional_data/US_category_id.json')
# print(json_df['items'][0])

cat_dict = {}

for item in json_df['items'].values:
    cat_dict[int(item['id'])] = item['snippet']['title']

full_df['category_name'] = full_df['category_id'].map(cat_dict)
# print(cat_dict)
# print(full_df.head(10))

# ... (All your previous code remains the same)

full_df['category_name'] = full_df['category_id'].map(cat_dict)

# --- START OF STREAMLIT UI ---

st.title("YouTube Data Analysis")
st.write("Data loaded successfully! Generating chart...")

# 1. Create a Figure Object explicitly
fig = plt.figure(figsize=(14, 8))

# 2. Create the Boxplot (Seaborn draws on the active figure 'fig')
sns.boxplot(x='category_name', y='likes', data=full_df)

# 3. Apply Log Scale & Formatting
plt.yscale('log')
plt.xticks(rotation='vertical')
plt.title("Distribution of Likes by Category (Log Scale)", fontsize=16)
plt.xlabel("Category Name", fontsize=12)
plt.ylabel("Likes (Log Scale)", fontsize=12)

# 4. STREAMLIT DISPLAY COMMAND
# Instead of plt.show(), we pass the 'fig' object to Streamlit
st.pyplot(fig)