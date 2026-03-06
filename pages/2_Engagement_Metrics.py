import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# CHANGE THIS LINE: Change load_and_prep_data to load_video_data
from utils import load_video_data

# 1. Page Configuration
st.set_page_config(page_title="YouTube Engagement Analytics", layout="wide")

st.title("📈 Engagement Metrics & Correlations")

# 2. Data Loading
with st.spinner('Accessing YouTube Dataset...'):
    # AND CHANGE THIS LINE: Use the correct function name
    full_df = load_video_data()

# --- TOP KPI ROW ---
avg_like_rate = full_df['like_rate'].mean()
top_performing_cat = full_df.groupby('category_name')['like_rate'].mean().idxmax()

m1, m2, m3 = st.columns(3)
m1.metric("Avg. Global Like Rate", f"{avg_like_rate:.2f}%")
m2.metric("Highest Engagement Category", top_performing_cat)
m3.metric("Total Sampled Videos", f"{len(full_df):,}")

st.divider()

# --- SECTION 1: CATEGORY DISTRIBUTIONS ---
st.subheader("Category Engagement Distribution")
dist_col1, dist_col2 = st.columns(2)

with dist_col1:
    st.markdown("### 🍯 Likes Spread (Log Scale)")
    # Plotly Box handles Log Scale and Interactivity better
    fig_likes = px.box(
        full_df,
        x='category_name',
        y='likes',
        color='category_name',
        log_y=True,
        template="plotly_white",
        height=500
    )
    fig_likes.update_layout(showlegend=False, xaxis_title="", yaxis_title="Likes (Log)")
    st.plotly_chart(fig_likes, use_container_width=True)

with dist_col2:
    st.markdown("### ⚡ Like Rate %")
    fig_rate = px.box(
        full_df,
        x='category_name',
        y='like_rate',
        color='category_name',
        template="plotly_white",
        height=500
    )
    fig_rate.update_layout(showlegend=False, xaxis_title="", yaxis_title="Like Rate (%)")
    # Setting a reasonable range for the Y-axis to avoid outlier stretching
    fig_rate.update_yaxes(range=[0, full_df['like_rate'].quantile(0.95)])
    st.plotly_chart(fig_rate, use_container_width=True)

st.divider()

# --- SECTION 2: CORRELATIONS & REGRESSION ---
st.subheader("Correlation & Regression Analysis")
corr_col1, corr_col2 = st.columns([1, 1.2])

with corr_col1:
    st.markdown("### 🌡️ Metrics Heatmap")
    corr_matrix = full_df[['views', 'likes', 'dislikes', 'comment_count']].corr()

    # Plotly Heatmap for interactivity
    fig_heat = px.imshow(
        corr_matrix,
        text_auto=".2f",
        color_continuous_scale='RdBu_r',
        aspect="auto",
        template="plotly_white"
    )
    fig_heat.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_heat, use_container_width=True)

with corr_col2:
    st.markdown("### 📉 Views vs. Likes Trend")
    # Using a sample for performance, but Plotly Scatter is faster than Regplot
    sample_df = full_df.sample(n=3000, random_state=42)

    fig_reg = px.scatter(
        sample_df,
        x='views',
        y='likes',
        trendline="ols",  # Adds the regression line
        hover_data=['category_name'],
        opacity=0.6,
        color='category_name',
        template="plotly_white",
        height=500
    )
    fig_reg.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_reg, use_container_width=True)