import pandas as pd
import streamlit as st
import os
import json


@st.cache_data
def load_video_data():
    # Load videos (Recommend using a 50k row sample for GitHub/Streamlit Cloud)
    df = pd.read_csv(os.path.join("data", "videos_sample.csv"), encoding='iso-8859-1', on_bad_lines='skip')

    # Load and Map Categories
    with open(os.path.join("data", "US_category_id.json"), 'r') as f:
        categories = json.load(f)

    cat_dict = {int(item['id']): item['snippet']['title'] for item in categories['items']}
    df['category_name'] = df['category_id'].map(cat_dict)

    # Pre-calculate Rates
    df['like_rate'] = (df['likes'] / df['views']) * 100
    df['dislike_rate'] = (df['dislikes'] / df['views']) * 100
    df['comment_rate'] = (df['comment_count'] / df['views']) * 100

    return df.drop_duplicates()


@st.cache_data
def load_comment_data():
    df = pd.read_csv(os.path.join("data", "UScomments.csv"), on_bad_lines='skip')
    return df.dropna()