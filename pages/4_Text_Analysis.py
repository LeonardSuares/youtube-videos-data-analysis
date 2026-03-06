import streamlit as st
import pandas as pd
import plotly.express as px
import string
import os
# Import the centralized data loader from your utils file
from utils import load_video_data

# 1. Page Configuration
st.set_page_config(page_title="YouTube Text Analysis", layout="wide")

# 2. Helper Function for Punctuation
def punc_count(text):
    """Counts punctuation characters in a string to analyze 'clickbait' trends."""
    return len([char for char in str(text) if char in string.punctuation])

# --- MAIN APP ---
st.title("📝 Title Strategy & Channel Analysis")

# 3. Load Data using the optimized Parquet loader
with st.spinner('Loading text analysis data...'):
    full_df = load_video_data()

if not full_df.empty:
    # --- TOP KPI SECTION ---
    # Quick metrics to show high-level text trends
    avg_punc = full_df['title'].apply(punc_count).mean()
    most_active = full_df['channel_title'].value_counts().idxmax()

    c1, c2, c3 = st.columns(3)
    c1.metric("Avg. Punctuation per Title", f"{avg_punc:.1f}")
    c2.metric("Most Active Channel", most_active)
    c3.metric("Total Videos in Sample", f"{len(full_df):,}")

    st.divider()

    # --- SECTION 1: CHANNEL VOLUME ---
    st.subheader("📊 Content Volume by Channel")
    st.caption("Which channels are the most frequent uploaders in this dataset?")

    # Group and sort data for the bar chart
    cdf = full_df.groupby(['channel_title']).size().sort_values(ascending=False).reset_index()
    cdf.columns = ['channel_title', 'total_videos']

    # Horizontal bar chart is best for long channel names
    fig_bar = px.bar(
        cdf.head(20),
        y='channel_title',
        x='total_videos',
        orientation='h',
        text='total_videos',
        color='total_videos',
        color_continuous_scale='Bluered',
        template="plotly_white",
        height=600,
        title="Top 20 Channels by Video Count"
    )

    fig_bar.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # --- SECTION 2: PUNCTUATION IMPACT ---
    st.subheader("⁉️ Does Punctuation Drive Engagement?")
    st.info("Analyzing if punctuation count (exclamation marks, question marks, etc.) correlates with higher views or likes.")

    # Create a copy for punctuation analysis
    sample_size = min(10000, len(full_df))
    sample = full_df.sample(sample_size).copy()
    sample['count_punc'] = sample['title'].apply(punc_count)

    # Allow user to toggle between different success metrics
    metric_choice = st.radio("Select Metric to Compare:", ["views", "likes"], horizontal=True)

    # Interactive Plotly Box Plot
    fig_punc = px.box(
        sample,
        x='count_punc',
        y=metric_choice,
        color='count_punc',
        log_y=True,
        points=False, # Hides outlier dots for a cleaner look
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Prism,
        height=500,
        labels={'count_punc': 'Punctuation Marks', 'views': 'Total Views', 'likes': 'Total Likes'}
    )

    fig_punc.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=10, b=20),
        xaxis_title="Number of Punctuation Marks in Title"
    )

    st.plotly_chart(fig_punc, use_container_width=True)

    with st.expander("💡 Data Insights"):
        st.write(f"""
        - **Metric Selected:** {metric_choice.title()}
        - **Logarithmic Scale:** Used to account for the massive range between standard videos and viral hits.
        - **Hover Action:** You can hover over each box to see the specific median, min, and max values for that group.
        """)
else:
    st.error("Data could not be loaded. Please ensure 'videos_sample.parquet' exists in your /data folder.")