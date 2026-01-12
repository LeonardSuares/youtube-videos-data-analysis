import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_comment_data
from collections import Counter
import emoji
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title("💬 Comment & Sentiment Analysis")
comments = load_comment_data().sample(10000) # Sample for speed

# --- EMOJI ANALYSIS ---
st.subheader("Top 10 Emojis in Comments")
all_emojis = []
for comment in comments['comment_text']:
    emojis_info = emoji.emoji_list(str(comment))
    all_emojis.extend([item['emoji'] for item in emojis_info])

emoji_counts = pd.DataFrame(Counter(all_emojis).most_common(10), columns=['Emoji', 'Count'])
fig_emoji = px.bar(emoji_counts, x='Emoji', y='Count', color='Count', color_continuous_scale='Viridis')
st.plotly_chart(fig_emoji, use_container_width=True)

# --- WORDCLOUDS ---
st.divider()
st.subheader("Comment Word Cloud")
text = " ".join(str(c) for c in comments['comment_text'])
wc = WordCloud(stopwords=set(STOPWORDS), background_color='white', width=800, height=400).generate(text)

fig_wc, ax = plt.subplots()
ax.imshow(wc, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig_wc)