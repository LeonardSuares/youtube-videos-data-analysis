import pandas as pd
df = pd.read_csv(r"/export_data/youtube_sample.csv")
df.sample(n=50000).to_csv("data/videos_sample.csv", index=False)