import streamlit as st
import plotly.express as px
from utils import load_video_data

st.title("📊 Category Performance")
df = load_video_data()

# PROMPT: Metric Selector
metric = st.selectbox("Select Metric to compare by Category",
                     ['likes', 'views', 'dislikes', 'like_rate'])

st.subheader(f"Distribution of {metric.replace('_', ' ').title()} per Category")

fig = px.box(df, x='category_name', y=metric, color='category_name',
             log_y=True if metric in ['likes', 'views'] else False,
             title=f"Category vs {metric}")

fig.update_layout(xaxis_title="Category", yaxis_title=metric, showlegend=False)
st.plotly_chart(fig, use_container_width=True)