import streamlit as st
import plotly.express as px
from utils import load_video_data

# Set page to wide mode for better chart spacing
st.set_page_config(layout="wide", page_title="YouTube Category Insights")

st.title("📊 Category Performance Analysis")
df = load_video_data()

# --- TOP KPI SECTION ---
# Adding some quick context before the big chart
total_videos = len(df)
top_category = df['category_name'].value_counts().idxmax()

col1, col2, col3 = st.columns(3)
col1.metric("Total Videos Analyzed", f"{total_videos:,}")
col2.metric("Most Active Category", top_category)
col3.metric("Unique Categories", df['category_name'].nunique())

st.divider()

# --- CHART CONTROLS ---
# Using columns for the selector so it doesn't take up the whole width
ctrl_col, info_col = st.columns([1, 2])

with ctrl_col:
    metric = st.selectbox(
        "Select Metric to compare",
        options=['views', 'likes', 'dislikes', 'like_rate'],
        format_func=lambda x: x.replace('_', ' ').title()
    )
    st.info(
        f"💡 This box plot shows the spread of {metric} across different genres. Use the toggle below to switch to a log scale if the data is skewed.")
    use_log = st.toggle("Use Log Scale", value=True if metric in ['likes', 'views'] else False)

# --- MAIN CHART ---
with st.container():
    # Adjusted height for better vertical fit
    fig = px.box(
        df,
        x='category_name',
        y=metric,
        color='category_name',
        log_y=use_log,
        points=False,  # Hides outliers by default for a cleaner look; hover still works
        color_discrete_sequence=px.colors.qualitative.Safe,
        template="plotly_white",
        height=550
    )

    fig.update_layout(
        xaxis_title="Video Category",
        yaxis_title=metric.replace('_', ' ').title(),
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis={'categoryorder': 'total descending'}  # Orders boxes from highest to lowest
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- SUMMARY TABLE ---
with st.expander("📂 View Category Summary Statistics"):
    summary_df = df.groupby('category_name')[metric].describe().round(2)
    st.dataframe(summary_df, use_container_width=True)