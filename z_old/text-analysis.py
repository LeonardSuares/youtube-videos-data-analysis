import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import string
import os

# 1. Page Config
st.set_page_config(page_title="YouTube Text Analysis", layout="wide")


# 2. Cached Data Loading Function
@st.cache_data
def load_data():
    # Update this path if you move the file
    file_path = r'/export_data/youtube_sample.csv'

    # Check if file exists to prevent hard crash
    if not os.path.exists(file_path):
        st.error(f"File not found at: {file_path}")
        return pd.DataFrame()

    df = pd.read_csv(file_path)
    return df


# 3. Helper Function for Punctuation
def punc_count(text):
    # Counts punctuation characters in a string
    return len([char for char in str(text) if char in string.punctuation])


# --- MAIN APP ---
st.title("📝 YouTube Title & Channel Analysis")

full_df = load_data()

if not full_df.empty:
    # Optional: Show data shape
    with st.expander("View Raw Data Info"):
        st.write(f"Dataset Shape: {full_df.shape}")
        st.dataframe(full_df.head())

    st.divider()

    # --- CHART 1: Top Channels (Plotly) ---
    st.subheader("1. Top 20 Channels by Video Count")

    # Group and sort data
    cdf = full_df.groupby(['channel_title']).size().sort_values(ascending=False).reset_index()
    cdf = cdf.rename(columns={0: 'total_videos'})

    # Create interactive bar chart
    fig_bar = px.bar(
        data_frame=cdf[0:20],
        x='channel_title',
        y='total_videos',
        title="Top 20 Channels by Content Volume",
        color='total_videos'  # Adds a nice color gradient
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # --- CHART 2: Punctuation vs Views & Likes (Seaborn/Matplotlib) ---
    st.subheader("2. Does Punctuation Affect Engagement?")
    st.caption("Analyzing a sample of 10,000 videos to see if more punctuation correlates with Views or Likes.")

    # Process Sample
    sample = full_df[0:10000].copy()
    sample['count_punc'] = sample['title'].apply(punc_count)

    # CREATE TWO COLUMNS FOR SIDE-BY-SIDE PLOTS
    col1, col2 = st.columns(2)

    # --- LEFT COLUMN: VIEWS ---
    with col1:
        st.markdown("**Impact on Views**")
        fig_views, ax1 = plt.subplots(figsize=(10, 6))

        sns.boxplot(x='count_punc', y='views', data=sample, ax=ax1)
        ax1.set_yscale('log')  # Log scale
        ax1.set_title("Views by Punctuation Count")
        ax1.set_xlabel("Punctuation Marks")
        ax1.set_ylabel("Views (Log Scale)")

        st.pyplot(fig_views)

    # --- RIGHT COLUMN: LIKES ---
    with col2:
        st.markdown("**Impact on Likes**")
        fig_likes, ax2 = plt.subplots(figsize=(10, 6))

        sns.boxplot(x='count_punc', y='likes', data=sample, ax=ax2)
        ax2.set_yscale('log')  # Log scale
        ax2.set_title("Likes by Punctuation Count")
        ax2.set_xlabel("Punctuation Marks")
        ax2.set_ylabel("Likes (Log Scale)")

        st.pyplot(fig_likes)