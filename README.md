# 📺 YouTube Video Analytics Hub

**Live Application:** [View on Streamlit Cloud]([your-link-here](https://youtube-videos-data-analysis-5kszowasilg4adq2caee9i.streamlit.app/))

## 📖 Project Overview
This project is a high-performance analytics dashboard designed to analyze 50,000+ viral YouTube videos. It serves as a comprehensive tool for content strategists to explore category trends, engagement correlations, and sentiment patterns using advanced data engineering and NLP techniques.

---

## 🚀 Key Features

* **Interactive Snapshots:** Real-time KPI tracking for views, likes, and category distributions across the platform.
* **Advanced Engagement Analytics:** Interactive scatter plots with **OLS Regression trendlines** to visualize the relationship between views and audience interaction.
* **Sentiment & Emoji Analysis:** NLP-driven deep dive into user comments using **TextBlob** and emoji frequency mapping.
* **Text Strategy Insights:** Statistical analysis of video titles, including the impact of punctuation and "clickbait" formatting on performance.
* **Optimized Engine:** Fully powered by **Parquet** data files for 10x faster loading compared to standard CSV implementations.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit (Multi-page Architecture)
* **Data Engineering:** Pandas, PyArrow, Brotli (Parquet Optimization)
* **Analytics:** Statsmodels (OLS Regression), NumPy
* **NLP:** TextBlob, Emoji, WordCloud
* **Visualization:** Plotly Express (Interactive), Seaborn/Matplotlib

---

## 🎯 Project Motivation & Insights

### Why this project?
With the explosion of digital content, understanding the "DNA of Virality" is crucial for creators and brands. This project was developed to move beyond surface-level metrics and explore the underlying factors that drive engagement on YouTube. I focused on solving three specific technical and analytical challenges:

* **Data Lifecycle Optimization:** Migrating from raw CSVs to **Parquet with Brotli compression** to handle 50,000+ records with a 70% smaller storage footprint and near-instant load times.
* **Predictive Patterns:** Using **Ordinary Least Squares (OLS) Regression** to quantify the correlation between views and likes, helping to identify "engagement outliers".
* **The "Clickbait" Variable:** Analyzing the statistical impact of title punctuation and sentiment on total reach to determine if aggressive formatting actually correlates with higher performance.

### 💡 Key Insights Discovered
* **Engagement Saturation:** Higher view counts do not always scale linearly with likes; specific categories reach a "participation plateau" earlier than others.
* **The Punctuation Paradox:** While excessive punctuation in titles is often associated with clickbait, the data shows a "sweet spot" (typically 1-3 marks) that maximizes CTR without diminishing brand trust.
* **Sentiment Trends:** Comments with extreme polarity (highly positive or highly negative) drive significantly higher engagement rates than neutral feedback, suggesting that emotional provocation is a key driver for the YouTube algorithm.

---

## 📂 Project Structure
```text
youtube-videos-data-analysis/
├── Home.py                # Dashboard entry point & platform KPIs
├── utils.py               # Centralized data engine (Parquet/Caching)
├── data/                  # Optimized data directory (Parquet & JSON)
│   ├── videos_sample.parquet
│   └── UScomments_sample.parquet
├── pages/                 # Analysis modules
│   ├── 1_Category_Insights.py
│   ├── 2_Engagement_Metrics.py
│   ├── 3_Sentiment_Analysis.py
│   └── 4_Text_Analysis.py
├── requirements.txt       # Project dependencies
└── README.md
