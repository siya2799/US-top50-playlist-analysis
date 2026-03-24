# 🎧 US Top 50 Playlist Analysis & Interactive Dashboard

### 📌 Overview

This project analyzes the performance dynamics of songs in the US Top 50 playlist, focusing on ranking trends, artist influence, and content characteristics. It combines **data analysis, KPI design, and an interactive Streamlit dashboard** to deliver actionable insights.

The goal is to understand **what drives song success, longevity, and popularity** within playlist ecosystems.

---

### 🚀 Live Demo

https://jqbxsqvwdf5wwp5ct2eybd.streamlit.app/

---

### 📊 Key Features

*🔹 Playlist Ranking Analysis*

* Daily rank distribution
* Rank movement patterns
* Entry vs exit behavior
* Fast risers vs slow decliners

*🔹 Song-Level Performance*

* Longest chart presence
* Highest average popularity
* Peak rank vs longevity comparison

*🔹 Artist Performance*

* Artist dominance index
* Number of unique songs per artist
* Total days on playlist

*🔹 Popularity Analytics*

* Popularity vs rank relationship
* Popularity distribution across Top 10/20/50
* Popularity stability vs rank volatility

*🔹 Content Analysis*

* Explicit vs non-explicit performance
* Single vs album track comparison
* Song duration impact (optimal: 2–4 minutes)
* Album size impact (optimal: 0–40 tracks)

---

### 🧠 Key Insights

* Rankings are largely stable with minimal daily fluctuation
* Early success strongly predicts long-term performance
* Fast risers show strong momentum, while slow decliners maintain longevity
* Only a few songs sustain high popularity over extended periods
* Higher popularity correlates with longer chart presence
* A small group of artists dominate playlist visibility
* Top 10 songs show higher and more stable popularity
* Explicit content has minimal impact on performance
* Singles perform better in ranking, while compilation tracks show high popularity
* Optimal song duration: **2–4 minutes**
* Optimal album size: **0–40 tracks**

---

 ### 📈 KPIs Implemented

* Days on Chart
* Average Rank
* Best Rank
* Rank Volatility
* Popularity Trend
* Artist Dominance Index (normalized 0–100%)
* Explicit Content Share

---

### 🖥️ Streamlit Dashboard Features

* Interactive filters:

  * Date range
  * Artist selection
  * Rank range
  * Album type

* Visualizations:

  * Rank trend charts
  * Popularity vs rank scatter plots
  * Artist dominance leaderboard
  * Content performance panels

* UI Enhancements:

  * Dark theme + neon styling
  * Interactive Plotly charts (hover insights)
  * Dynamic Top 10 songs with album covers
  * Artist showcase with dominance scores

### 🛠️ Tech Stack

* **Python**
* **Pandas** – Data processing
* **Plotly** – Interactive visualizations
* **Streamlit** – Web app framework

---

### 📂 Project Structure

```
├── app.py
├── data/
│   └── Atlantic_United_States.csv
├── requirements.txt
└── .streamlit/
    └── config.toml
```

---

### ⚙️ Installation & Run Locally

python enviroment
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
streamlit run app.py
```

---

### 📌 Deployment

This app is deployed using **Streamlit Cloud**.

To deploy:

1. Push code to GitHub
2. Connect repository on Streamlit Cloud
3. Select `app.py` as entry point

---

### 🎯 Business / Policy Relevance

This analysis provides insights into:

* Content strategy optimization
* Artist performance evaluation
* Playlist curation decisions
* Audience engagement patterns

---

### 💬 Author

**Siya Pangam**
https://github.com/siya2799

www.linkedin.com/in/siya-pangam-424b9a1a0

---

### ⭐ Acknowledgements

Dataset: Atlantic_United_States.csv

---
