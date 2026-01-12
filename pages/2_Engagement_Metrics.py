import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import plotly.express as px

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(page_title="YouTube Analytics", layout="wide")


# 2. CACHED DATA LOADING (Fixes the 5-minute wait)
@st.cache_data
def load_and_prep_data():
    # Update this path to your specific folder
    path = r'C:\Users\leona\PycharmProjects\Python Data Analysis Projects\AAProject sets - 2\youtube-videos-data-analysis\additional_data'

    files = os.listdir(path)
    files_csv = [file for file in files if '.csv' in file]

    full_df = pd.DataFrame()
    for file in files_csv:
        # Construct full path safely
        file_path = os.path.join(path, file)
        current_df = pd.read_csv(file_path, encoding='iso-8859-1', on_bad_lines='skip')
        full_df = pd.concat([full_df, current_df], ignore_index=True)

    # Remove duplicates
    full_df = full_df.drop_duplicates()

    # Load Categories
    json_path = os.path.join(path, 'US_category_id.json')
    json_df = pd.read_json(json_path)

    cat_dict = {}
    for item in json_df['items'].values:
        cat_dict[int(item['id'])] = item['snippet']['title']

    full_df['category_name'] = full_df['category_id'].map(cat_dict)

    # Calculate Rates
    full_df['like_rate'] = (full_df['likes'] / full_df['views']) * 100
    full_df['dislike_rate'] = (full_df['dislikes'] / full_df['views']) * 100
    full_df['comment_count_rate'] = (full_df['comment_count'] / full_df['views']) * 100

    return full_df


# --- MAIN APP UI ---

st.title("📊 YouTube Video Analysis Dashboard")

# Load data with a spinner so the user knows it's working
with st.spinner('Loading massive dataset...'):
    full_df = load_and_prep_data()

# Optional: Show Raw Data in an expander
with st.expander("View Raw Data Snippet"):
    st.dataframe(full_df.head(100))

st.markdown("---")

# --- SECTION 1: CATEGORY DISTRIBUTION (Side-by-Side) ---
st.subheader("Category Performance Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**1. Distribution of Likes (Log Scale)**")
    fig1 = plt.figure(figsize=(10, 6))
    sns.boxplot(x='category_name', y='likes', data=full_df)
    plt.yscale('log')
    plt.xticks(rotation=90)
    plt.title("Likes per Category (Log Scale)")
    st.pyplot(fig1)

with col2:
    st.markdown("**2. Like Rate (Likes / Views)**")
    fig2 = plt.figure(figsize=(10, 6))
    sns.boxplot(x='category_name', y='like_rate', data=full_df)
    plt.xticks(rotation=90)
    plt.title("Like Rate % per Category")
    st.pyplot(fig2)

st.markdown("---")

# --- SECTION 2: CORRELATIONS (Side-by-Side) ---
st.subheader("Correlation & Regression Analysis")

col3, col4 = st.columns(2)

with col3:
    st.markdown("**3. Correlation Heatmap**")
    # Calculate correlation matrix
    corr_matrix = full_df[['views', 'likes', 'dislikes']].corr()

    fig3 = plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title("Correlation: Views vs Likes vs Dislikes")
    st.pyplot(fig3)

with col4:
    st.markdown("**4. Regression: Views vs. Likes**")
    # We take a sample to speed up the regression plot rendering
    sample_df = full_df.sample(n=5000, random_state=42)

    fig4 = plt.figure(figsize=(10, 6))
    sns.regplot(x='views', y='likes', data=sample_df, scatter_kws={'alpha': 0.5})
    plt.title("Regression Plot (Sampled Data)")
    st.pyplot(fig4)