import pandas as pd
import os

# 1. Process Video Data
df_videos = pd.read_csv("videos_sample.csv", encoding='iso-8859-1', on_bad_lines='skip')

# Clean numeric columns: convert to numeric and turn errors (text) into NaN, then fill with 0
for col in ['views', 'likes', 'dislikes', 'comment_count']:
    if col in df_videos.columns:
        df_videos[col] = pd.to_numeric(df_videos[col], errors='coerce').fillna(0).astype('int64')

df_videos.sample(n=min(50000, len(df_videos))).to_parquet("videos_sample.parquet", compression='brotli', index=False)

# 2. Process Comment Data
# Adding low_memory=False to stop the DtypeWarning
df_comments = pd.read_csv("UScomments.csv", on_bad_lines='skip', low_memory=False)

# Comments often have 'likes' columns that need the same cleaning
if 'likes' in df_comments.columns:
    df_comments['likes'] = pd.to_numeric(df_comments['likes'], errors='coerce').fillna(0).astype('int64')

# Ensure comment_text is string to avoid Arrow errors
df_comments['comment_text'] = df_comments['comment_text'].astype(str)

df_comments.sample(n=min(20000, len(df_comments))).to_parquet("UScomments_sample.parquet", compression='brotli', index=False)

print("✅ Success! Data cleaned and Parquet files created.")