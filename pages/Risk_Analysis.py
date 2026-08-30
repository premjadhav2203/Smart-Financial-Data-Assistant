import streamlit as st
import plotly.express as px

from src.data_loader import load_data

df = load_data()

st.title(" Risk Analysis")

selected_age = st.multiselect(
    "Select Age Groups",
    df["AgeGroup"].unique(),
    default=df["AgeGroup"].unique()
)

filtered = df[
    df["AgeGroup"].isin(selected_age)
]

risk_chart = px.histogram(
    filtered,
    x="AgeGroup",
    color="Risk",
    title="Risk by Age Group"
)

st.plotly_chart(
    risk_chart,
    width="stretch"
)

credit_chart = px.box(
    filtered,
    x="Risk",
    y="CreditAmount",
    title="Credit Amount vs Risk"
)

st.plotly_chart(
    credit_chart,
    width="stretch"
)