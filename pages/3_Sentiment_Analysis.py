import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_comment_data
from collections import Counter
import emoji
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from textblob import TextBlob

# Page Config
st.set_page_config(layout="wide", page_title="YouTube Sentiment Analysis")

st.title("💬 Comment & Sentiment Analysis")

# 1. Data Loading & Enrichment
with st.spinner("Analyzing comments..."):
    # Sampling for performance
    comments = load_comment_data()
    sample_df = comments.sample(min(10000, len(comments)))

    # Calculate Polarity for actual Sentiment Analysis
    sample_df['polarity'] = sample_df['comment_text'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    sample_df['sentiment'] = sample_df['polarity'].apply(
        lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral')
    )

# --- TOP KPI SECTION ---
st.subheader("Quick Sentiment Overview")
c1, c2, c3 = st.columns(3)

pos_per = (sample_df['sentiment'] == 'Positive').mean() * 100
neg_per = (sample_df['sentiment'] == 'Negative').mean() * 100

c1.metric("Overall Vibe", "Positive" if pos_per > neg_per else "Negative")
c2.metric("Positive Comments", f"{pos_per:.1f}%")
c3.metric("Negative Comments", f"{neg_per:.1f}%")

st.divider()

# --- SECTION 1: EMOJIS & SENTIMENT SPLIT ---
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 🏆 Top 10 Emojis")
    all_emojis = []
    for comment in sample_df['comment_text']:
        emojis_info = emoji.emoji_list(str(comment))
        all_emojis.extend([item['emoji'] for item in emojis_info])

    emoji_counts = pd.DataFrame(Counter(all_emojis).most_common(10), columns=['Emoji', 'Count'])

    fig_emoji = px.bar(
        emoji_counts,
        x='Emoji',
        y='Count',
        color='Count',
        color_continuous_scale='Sunsetdark',
        template="plotly_white",
        height=400
    )
    fig_emoji.update_layout(coloraxis_showscale=False, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_emoji, use_container_width=True)

with col2:
    st.markdown("### 📊 Sentiment Distribution")
    fig_pie = px.pie(
        sample_df,
        names='sentiment',
        color='sentiment',
        color_discrete_map={'Positive': '#2ecc71', 'Negative': '#e74c3c', 'Neutral': '#95a5a6'},
        hole=0.4,
        template="plotly_white",
        height=400
    )
    fig_pie.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# --- SECTION 2: WORD CLOUDS BY SENTIMENT ---
st.subheader("☁️ Word Cloud Analysis")
# Let the user choose which "vibe" they want to see the words for
vibe_choice = st.radio("Show Word Cloud for:", ["All", "Positive", "Negative"], horizontal=True)

if vibe_choice == "All":
    cloud_text = " ".join(str(c) for c in sample_df['comment_text'])
elif vibe_choice == "Positive":
    cloud_text = " ".join(str(c) for c in sample_df[sample_df['sentiment'] == 'Positive']['comment_text'])
else:
    cloud_text = " ".join(str(c) for c in sample_df[sample_df['sentiment'] == 'Negative']['comment_text'])

if cloud_text.strip():
    wc = WordCloud(
        stopwords=set(STOPWORDS),
        background_color='white',
        width=1200,
        height=500,
        colormap='viridis' if vibe_choice != "Negative" else 'magma'
    ).generate(cloud_text)

    fig_wc, ax = plt.subplots(figsize=(12, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig_wc)
else:
    st.warning("Not enough text found to generate a cloud for this selection.")