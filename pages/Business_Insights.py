import os
from dotenv import load_dotenv
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

load_dotenv()

from src.data_loader import load_data
from src.insights import generate_insights
from src.ai_insights import generate_ai_insights
from src.gemini_ai import get_response, is_available

GEMINI_AVAILABLE = is_available()
GEMINI_IMPORT_ERROR = (
    None
    if GEMINI_AVAILABLE
    else "Gemini integration is disabled or no API key was found. Set GOOGLE_API_KEY in your .env to enable it."
)

# -----------------------------
# LOAD DATA
# -----------------------------

df = load_data()

st.title("📈 Business Insights Dashboard")

st.markdown("""
Analyze key business trends, customer behavior,
and AI-generated recommendations.
""")

# -----------------------------
# CORRELATION HEATMAP
# -----------------------------

st.subheader("📊 Correlation Analysis")

numeric = df.select_dtypes(
    include=["int64", "float64"]
)

corr = numeric.corr()

fig, ax = plt.subplots(figsize=(10, 6))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    ax=ax
)

st.pyplot(fig)

# -----------------------------
# BASIC INSIGHTS
# -----------------------------

st.subheader(" Key Findings")

for insight in generate_insights(df):
    st.success(insight)

# -----------------------------
# AI INSIGHTS (RULE-BASED)
# -----------------------------

st.subheader(" AI-Powered Insights")

ai_insights = generate_ai_insights(df)

for insight in ai_insights:
    st.info(insight)

# -----------------------------
# GEMINI INSIGHTS (OPTIONAL)
# -----------------------------

if GEMINI_AVAILABLE:

    st.subheader(" Gemini Executive Summary")

    summary = f"""
    You are a Senior Financial Data Analyst.

    Dataset Summary:

    Total Customers: {len(df)}

    Average Age:
    {df['Age'].mean():.2f}

    Average Credit Amount:
    {df['CreditAmount'].mean():.2f}

    Average Loan Duration:
    {df['Duration'].mean():.2f}

    Most Common Purpose:
    {df['Purpose'].mode()[0]}

    Generate:

    1. Five executive insights
    2. Three business risks
    3. Three actionable recommendations

    Use concise business language.
    """

    try:
        ai_summary = get_response(summary)
        st.markdown(ai_summary)

    except Exception as e:
        st.error("Gemini Executive Summary is unavailable.")
        st.info(str(e))
        st.info(
            "This usually means your Gemini project does not have access permission or the API key is invalid. "
            "Please verify your Google/Gemini credentials or disable Gemini integration."
        )

else:
    st.info("Gemini integration is disabled or unavailable.")
    if GEMINI_IMPORT_ERROR:
        st.info(GEMINI_IMPORT_ERROR)

# -----------------------------
# EXECUTIVE RECOMMENDATIONS
# -----------------------------

st.subheader(" Executive Recommendations")

st.warning("""
1. Monitor customers requesting high credit amounts.

2. Apply additional checks for long-duration loans.

3. Review customer segments associated with the highest borrowing levels.

4. Strengthen approval criteria for high-risk applications.

5. Create automated alerts for unusual lending patterns.
""")

# -----------------------------
# DATA PREVIEW
# -----------------------------

with st.expander("View Dataset"):

    st.dataframe(
        df.head(20),
        width="stretch"
    )