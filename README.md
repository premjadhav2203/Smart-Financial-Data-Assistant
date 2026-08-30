# 💰 Smart Financial Data Assistant

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.62-FF4B4B)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8-F7931E)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

An interactive Streamlit dashboard that turns the German Credit dataset into
executive KPIs, risk segmentation, and an AI-powered natural-language
assistant — built as a data analyst portfolio project.

**[Live demo →](#deployment)** *(add your Streamlit Cloud link here once deployed)*

<!-- Add a screenshot of the running app here, e.g.: -->
<!-- ![App screenshot](docs/screenshot.png) -->

## What this project does

| Page | What it shows |
|---|---|
| **Home** | Project overview and headline KPIs |
| **Executive Overview** | Portfolio-level metrics — customer count, average age, average credit, high-risk rate |
| **Risk Analysis** | Interactive charts of risk tier by age group and credit amount, filterable by age group |
| **Business Insights** | Correlation heatmap, rule-based findings, and an optional Gemini-generated executive summary |
| **AI Assistant** | Ask questions about the dataset in plain English (Gemini-powered, with an offline keyword-matching fallback) |

## An honest note on the risk model

The version of the German Credit dataset used here (`data/german_credit_data.csv`
— Age, Sex, Job, Housing, Saving accounts, Checking account, Credit amount,
Duration, Purpose) does **not** ship with a ground-truth "good/bad" default
label. That's a real limitation of this specific data release, not something
this project works around by guessing.

Rather than inventing a proxy label and training a classifier on it — which
would *look* like machine learning but would really just be curve-fitting to
a label made up after the fact — this project uses **unsupervised K-Means
clustering** (`src/risk_model.py`) on each customer's financial and
demographic features, then ranks the resulting clusters by average credit
exposure (loan size adjusted for duration) into explainable **Low / Medium /
High** risk tiers. This is a legitimate, standard approach used in practice
when a labeled outcome isn't available yet.

See `notebooks/eda.ipynb` for the full exploratory analysis and a
reproduction of the model with sanity-check plots.

## Tech stack

- **Streamlit** — multipage dashboard UI
- **pandas / numpy** — data loading and feature engineering
- **scikit-learn** — K-Means clustering, feature scaling/encoding
- **Plotly / Matplotlib / Seaborn** — interactive and static visualizations
- **Google Gemini API** (`google-genai`) — natural-language insights and Q&A, with automatic offline fallback

## Getting started

```bash
git clone <your-repo-url>
cd smart-financial-assistant
pip install -r requirements.txt

cp .env.example .env
# (optional) add your Gemini API key to .env — the app works without it,
# it just runs the AI features in offline/keyword mode instead

streamlit run app.py
```

Get a free Gemini API key at https://aistudio.google.com/apikey — the app
runs fully without one, it just falls back to offline mode for the AI
features (see `.env.example`).

## Project structure

```
smart-financial-assistant/
├── app.py                     # Landing page
├── pages/                     # Streamlit multipage app screens
│   ├── Executive_Overview.py
│   ├── Risk_Analysis.py
│   ├── Business_Insights.py
│   └── AI_Assistant.py
├── src/
│   ├── data_loader.py         # Loading + cleaning
│   ├── risk_model.py          # K-Means risk segmentation (trained + persisted)
│   ├── insights.py            # Rule-based findings
│   ├── ai_insights.py         # Rule-based "AI-style" insights
│   ├── gemini_ai.py           # Gemini API wrapper (lazy, fails gracefully)
│   └── AI_Assistant.py        # Natural-language Q&A (Gemini + offline fallback)
├── models/
│   └── risk_model.joblib      # Persisted clustering pipeline
├── notebooks/
│   └── eda.ipynb              # Exploratory data analysis, pre-run with output
├── data/
│   └── german_credit_data.csv
├── .env.example
└── requirements.txt
```

## Deployment

The app is ready to deploy for free on **Streamlit Community Cloud**:

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub, and click "New app".
3. Point it at your repo, branch `main`, main file `app.py`.
4. Under "Advanced settings → Secrets", add:
   ```toml
   GOOGLE_API_KEY = "your-key-here"
   ```
   (optional — skip this to run in offline mode)
5. Deploy. You'll get a public `*.streamlit.app` URL to put on your CV/portfolio.

## Possible next steps

- Swap K-Means for a more granular anomaly-detection model (e.g. Isolation Forest) to flag individually unusual applicants rather than only cluster-level tiers.
- Add a "what-if" page where a user can enter a hypothetical applicant's details and see which risk tier they'd fall into.
- Add unit tests for `src/risk_model.py` and `src/data_loader.py`.

## Credit

Built on the German Credit Data (Hofmann, 1994), UCI Machine Learning
Repository, distributed here via the reduced release commonly used on
Kaggle.
