import pandas as pd

def generate_ai_insights(df):

    insights = []

    # Age analysis
    age_risk = (
        df.groupby("AgeGroup")["CreditAmount"]
        .mean()
        .sort_values(ascending=False)
    )

    highest_age_group = age_risk.index[0]

    insights.append(
        f"Risk exposure appears highest among customers aged {highest_age_group}."
    )

    # Credit amount analysis
    avg_credit = df["CreditAmount"].mean()

    high_credit_customers = len(
        df[df["CreditAmount"] > avg_credit]
    )

    insights.append(
        f"{high_credit_customers} customers have credit amounts above the portfolio average of ${avg_credit:,.0f}."
    )

    # Duration analysis
    long_duration = len(
        df[df["Duration"] > 24]
    )

    insights.append(
        f"{long_duration} customers have loan durations longer than 24 months, indicating elevated repayment risk."
    )

    # Purpose analysis
    top_purpose = (
        df["Purpose"]
        .value_counts()
        .idxmax()
    )

    insights.append(
        f"Most loans are taken for '{top_purpose}', making it the largest credit segment."
    )

    # Recommendation
    insights.append(
        "Recommended Action: Apply stricter approval checks for customers requesting large credit amounts with long repayment durations."
    )

    return insights
