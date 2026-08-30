def generate_insights(df):

    insights = []

    avg_loan = df["CreditAmount"].mean()

    insights.append(
        f"Average credit amount is {avg_loan:.2f}"
    )

    high_risk = (
        df.groupby("AgeGroup")["Risk"]
        .count()
        .idxmax()
    )

    insights.append(
        f"Largest customer segment: {high_risk}"
    )

    return insights