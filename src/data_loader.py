import pandas as pd
import streamlit as st
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "german_credit_data.csv"


def load_raw_data() -> pd.DataFrame:
    """Load and clean the raw dataset, without any risk scoring applied."""
    df = pd.read_csv(DATA_PATH)
    df.drop_duplicates(inplace=True)

    # The CSV ships with an unnamed index column from its original export
    unnamed_cols = [c for c in df.columns if c.startswith("Unnamed")]
    if unnamed_cols:
        df.drop(columns=unnamed_cols, inplace=True)

    # Normalize column names and rename to canonical names
    df.columns = df.columns.str.strip()
    df.rename(
        columns={
            "Credit amount": "CreditAmount",
            "Saving accounts": "SavingAccounts",
            "Checking account": "CheckingAccount",
        },
        inplace=True,
    )

    if "CreditAmount" not in df.columns:
        raise ValueError(
            f"Missing required column 'CreditAmount' after normalization. Available columns: {df.columns.tolist()}"
        )

    if "Age" not in df.columns:
        raise ValueError(
            f"Missing required column 'Age'. Available columns: {df.columns.tolist()}"
        )

    # Create AgeGroup if not already present
    if "AgeGroup" not in df.columns:
        df["AgeGroup"] = pd.cut(
            df["Age"],
            bins=[18, 30, 45, 60, 100],
            labels=["18-30", "31-45", "46-60", "60+"],
        )

    return df


@st.cache_data(show_spinner="Loading data and scoring customer risk...")
def load_data() -> pd.DataFrame:
    """Load the cleaned dataset with Low/Medium/High risk tiers attached.

    Risk tiers come from an unsupervised K-Means segmentation model
    (see src/risk_model.py) since the source dataset has no ground-truth
    risk label. Results are cached for the Streamlit session.
    """
    from src.risk_model import assign_risk

    df = load_raw_data()
    df = assign_risk(df)
    return df
