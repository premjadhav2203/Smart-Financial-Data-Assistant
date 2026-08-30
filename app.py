import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Smart Financial Data Assistant",
    page_icon="💰",
    layout="wide"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

.hero {
    padding: 2rem;
    border-radius: 20px;
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e293b
    );
    color: white;
    text-align: center;
    margin-bottom: 30px;
}

.hero-title {
    font-size: 3rem;
    font-weight: 700;
}

.hero-subtitle {
    font-size: 1.2rem;
    color: #cbd5e1;
}

.metric-card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
}

.metric-value {
    font-size: 32px;
    font-weight: bold;
}

.metric-title {
    font-size: 14px;
    color: #cbd5e1;
}

.section-title {
    font-size: 1.8rem;
    font-weight: 600;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HERO SECTION
# -----------------------------------

st.markdown("""
<div class="hero">

<div class="hero-title">
💰 Smart Financial Data Assistant
</div>

<br>

<div class="hero-subtitle">
Amdocs Data Analyst Assignment
<br><br>
Transforming Financial Data into Business Decisions using
Analytics, Visualization and AI
</div>

</div>
""", unsafe_allow_html=True)

# -----------------------------------
# PROJECT OVERVIEW
# -----------------------------------

st.markdown("## 🚀 Project Overview")

st.info("""
This solution helps financial institutions understand customer
behavior, identify risk patterns, and generate actionable
business insights using interactive dashboards and AI.
""")

# -----------------------------------
# KPI CARDS
# -----------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Dataset</div>
        <div class="metric-value">1000+</div>
        Customer Records
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Features</div>
        <div class="metric-value">9</div>
        Financial Attributes
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">Dashboard Pages</div>
        <div class="metric-value">4</div>
        Interactive Views
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">AI Powered</div>
        <div class="metric-value">✓</div>
        Gemini Assistant
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# -----------------------------------
# FEATURES
# -----------------------------------

st.markdown("## 📊 What This Solution Provides")

c1, c2 = st.columns(2)

with c1:

    st.success("""
    ✅ Executive Dashboard

    High-level business KPIs and portfolio overview.
    """)

    st.success("""
    ✅ Risk Analysis

    Explore customer risk indicators and credit exposure.
    """)

    st.success("""
    ✅ Customer Segmentation

    Analyze behavior across demographics and loan categories.
    """)

with c2:

    st.success("""
    ✅ AI-Powered Insights

    Automatically generate business recommendations.
    """)

    st.success("""
    ✅ Natural Language Assistant

    Ask questions in plain English.
    """)

    st.success("""
    ✅ Interactive Exploration

    Filters, charts, and drill-down analysis.
    """)

st.markdown("---")

# -----------------------------------
# BUSINESS IMPACT
# -----------------------------------

st.markdown("## 🎯 Business Impact")

st.warning("""
This solution enables stakeholders to:

• Identify high-risk customer segments

• Monitor lending trends

• Understand customer borrowing behavior

• Generate AI-assisted recommendations

• Make data-driven financial decisions
""")

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    "Built using Streamlit • Python • Plotly • Gemini AI • German Credit Dataset"
)