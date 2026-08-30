from src.data_loader import load_data
from src.gemini_ai import get_response, is_available

df = load_data()


def _keyword_answer(question: str) -> str:
    """Fast, offline fallback for a handful of common questions."""
    q = question.lower()

    if "average credit" in q:
        return f"Average Credit Amount: {df['CreditAmount'].mean():.2f}"

    if "total customers" in q:
        return f"Total Customers: {len(df)}"

    if "highest age group" in q:
        return df["AgeGroup"].value_counts().idxmax()

    if "maximum credit" in q:
        return str(df["CreditAmount"].max())

    if "high risk" in q or "risk" in q:
        counts = df["Risk"].value_counts().to_dict()
        return f"Risk tier breakdown: {counts}"

    return (
        "Question not understood by the offline assistant.\n\n"
        "Try: average credit, total customers, highest age group, "
        "maximum credit, or risk breakdown.\n\n"
        "(Enable Gemini in your .env for free-form questions.)"
    )


def _dataset_summary() -> str:
    return f"""
Total customers: {len(df)}
Average age: {df['Age'].mean():.2f}
Average credit amount: {df['CreditAmount'].mean():.2f}
Average loan duration (months): {df['Duration'].mean():.2f}
Age group distribution: {df['AgeGroup'].value_counts().to_dict()}
Risk tier distribution: {df['Risk'].value_counts().to_dict()}
Most common loan purpose: {df['Purpose'].mode()[0]}
Housing distribution: {df['Housing'].value_counts().to_dict()}
""".strip()


def ask_data(question: str) -> str:
    """Answer a free-text question about the dataset.

    Uses Gemini (grounded on a dataset summary) when a key is configured,
    and falls back to simple keyword matching otherwise so the assistant
    always returns something useful.
    """
    if not question or not question.strip():
        return "Please type a question first."

    if is_available():
        prompt = f"""
You are a financial data analyst assistant. Answer the user's question
using ONLY the dataset summary below — do not invent numbers that aren't
implied by it. Be concise (2-4 sentences) and reference concrete figures
where relevant.

Dataset summary:
{_dataset_summary()}

Question: {question}
"""
        try:
            return get_response(prompt)
        except Exception as e:
            return (
                f"{_keyword_answer(question)}\n\n"
                f"(Gemini was unavailable, so this is the offline fallback answer. Details: {e})"
            )

    return _keyword_answer(question)
