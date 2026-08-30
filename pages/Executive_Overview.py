import streamlit as st
from src.data_loader import load_data

df = load_data()

st.title("📊 Executive Overview")

total_customers = len(df)
avg_age = df["Age"].mean()
avg_credit = df["CreditAmount"].mean()
high_risk_rate = (df["Risk"] == "High").mean() * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric("Customers", total_customers)
col2.metric("Average Age", round(avg_age, 1))
col3.metric("Average Credit", f"${avg_credit:,.0f}")
col4.metric("High-Risk Rate %", round(high_risk_rate, 1))

st.caption(
    "Risk tier is produced by an unsupervised K-Means segmentation model "
    "(see src/risk_model.py) since the source dataset has no ground-truth label."
)

st.subheader("Risk Tier Breakdown")
st.bar_chart(df["Risk"].value_counts())

st.subheader("Sample Records")
st.dataframe(df.head(10), width="stretch")
