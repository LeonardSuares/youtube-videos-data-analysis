import streamlit as st
from utils import load_video_data

st.set_page_config(page_title="YouTube Analytics", layout="wide", page_icon="📺")

st.title("📺 YouTube Video Analytics Hub")
df = load_video_data()

# --- KPI METRICS ---
st.subheader("Platform Snapshot")
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Videos", f"{len(df):,}")
c2.metric("Avg Views", f"{int(df['views'].mean()):,}")
c3.metric("Max Likes", f"{int(df['likes'].max()):,}")
c4.metric("Categories", df['category_name'].nunique())

st.divider()

# --- TOP PERFORMERS ---
st.subheader("Top 10 Most Viewed Videos")
top_10 = df.nlargest(10, 'views')[['title', 'channel_title', 'views', 'likes']]
st.table(top_10)

st.sidebar.success("Select an analysis module above.")