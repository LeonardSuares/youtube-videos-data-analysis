import streamlit as st
import plotly.express as px
from utils import load_video_data

# 1. Page Configuration
st.set_page_config(page_title="YouTube Analytics Hub", layout="wide", page_icon="📺")

# 2. Hero Section
st.title("📺 YouTube Video Analytics Hub")
st.markdown("""
    Explore trending patterns, sentiment, and engagement metrics across a dataset of **50,000+ viral YouTube videos**. 
    This dashboard provides a deep dive into what makes content successful on the platform.
""")

# 3. Data Loading
with st.spinner('Refreshing Platform Snapshot...'):
    df = load_video_data()

st.divider()

# --- KPI METRICS ---
st.subheader("🚀 Platform Snapshot")
c1, c2, c3, c4 = st.columns(4)

# Formatting numbers for readability
c1.metric("Total Videos", f"{len(df):,}")
c2.metric("Avg Views", f"{int(df['views'].mean()):,}")
c3.metric("Max Likes", f"{int(df['likes'].max()):,}")
c4.metric("Unique Categories", df['category_name'].nunique())

st.divider()

# --- VISUAL OVERVIEW ---
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("🔥 Top 10 Most Viewed Videos")
    top_10 = df.nlargest(10, 'views')

    fig_top = px.bar(
        top_10,
        x='views',
        y='title',
        orientation='h',
        color='views',
        color_continuous_scale='Reds',
        template="plotly_white",
        labels={'title': 'Video Title', 'views': 'Total Views'},
        height=500
    )
    fig_top.update_layout(yaxis={'categoryorder': 'total ascending'}, coloraxis_showscale=False)
    st.plotly_chart(fig_top, use_container_width=True)

with col_right:
    st.subheader("💡 Quick Insights")
    # Dynamic insights based on data
    most_common_cat = df['category_name'].value_counts().idxmax()
    high_engagement = df[df['like_rate'] > df['like_rate'].median()]

    st.info(f"**Dominant Content:** The **{most_common_cat}** category has the highest frequency in this dataset.")
    st.success(
        f"**Engagement Tip:** Videos in the top 50th percentile of like-rates average over **{int(high_engagement['views'].mean()):,}** views.")

    with st.expander("🛠️ Tech Stack Info"):
        st.write("""
            - **Backend:** Python (Pandas)
            - **Storage:** Parquet (Brotli Compressed)
            - **Frontend:** Streamlit
            - **Visuals:** Plotly Express
        """)

# --- NAVIGATION HINT ---
st.sidebar.info("💡 **Navigation:** Use the sidebar to explore specific analysis modules.")