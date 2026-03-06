import pandas as pd
import streamlit as st
import os
import json


@st.cache_data
def load_video_data():
    # Update paths to the new .parquet extension
    video_path = os.path.join("data", "videos_sample.parquet")
    json_path = os.path.join("data", "US_category_id.json")

    # Use read_parquet instead of read_csv
    df = pd.read_parquet(video_path)

    # Load and Map Categories
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            categories = json.load(f)
        cat_dict = {int(item['id']): item['snippet']['title'] for item in categories['items']}
        df['category_name'] = df['category_id'].map(cat_dict)

    # Rates are already calculated or can be re-calculated here for safety
    df['like_rate'] = (df['likes'] / df['views']) * 100
    df['dislike_rate'] = (df['dislikes'] / df['views']) * 100
    df['comment_rate'] = (df['comment_count'] / df['views']) * 100

    return df.drop_duplicates()


@st.cache_data
def load_comment_data():
    # Update path to the new .parquet extension
    comment_path = os.path.join("data", "UScomments_sample.parquet")

    if os.path.exists(comment_path):
        return pd.read_parquet(comment_path).dropna()
    else:
        st.error("Comment data file not found. Ensure UScomments_sample.parquet is in the /data folder.")
        return pd.DataFrame()