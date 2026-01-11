import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import plotly.express as px

pd.set_option('display.max_columns', None)

# 2. DISABLES WRAPPING by setting the display width to a very high number
pd.set_option('display.width', 1000)

import  warnings
from warnings import filterwarnings
filterwarnings("ignore")

full_df = pd.read_csv(r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\youtube-videos-data-analysis\export_data\youtube_sample.csv')

# # full_df['channel_title'].value_counts()
# print(full_df.shape)
cdf = full_df.groupby(['channel_title']).size().sort_values(ascending=False).reset_index()
cdf = cdf.rename(columns={0:'total_videos'})
fig = px.bar(data_frame=cdf[0:20], x='channel_title', y='total_videos')
fig.show()