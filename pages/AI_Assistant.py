import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from src.AI_Assistant import ask_data
from src.gemini_ai import is_available

st.title("🤖 Financial AI Assistant")

if is_available():
    st.caption("✅ Gemini is connected — ask any question in plain English.")
else:
    st.caption(
        "⚠️ Gemini isn't configured, so this is running in offline keyword mode. "
        "Add GOOGLE_API_KEY to your .env to enable free-form questions."
    )

st.markdown(
    "Examples: *average credit*, *total customers*, *highest age group*, "
    "*maximum credit*, *which customers look highest risk and why?*"
)

question = st.text_input("Ask a question about the dataset")

if st.button("Ask") and question:
    with st.spinner("Thinking..."):
        answer = ask_data(question)
    st.markdown(answer)
