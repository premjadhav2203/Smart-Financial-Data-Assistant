"""
Customer risk segmentation.

Important context: the German Credit dataset shipped in data/ has NO
ground-truth "good/bad" risk label — it only contains demographic and
loan features. That means a supervised classifier isn't honestly
possible on this data alone. Instead, this module fits an unsupervised
K-Means model on each customer's financial and demographic features and
ranks the resulting clusters by their average credit exposure (loan
size adjusted for duration) to produce explainable Low / Medium / High
risk tiers.

This replaces the previous placeholder logic, which simply flagged the
top 25% of customers by credit amount as "bad" and ignored every other
feature.

Usage:
    from src.risk_model import assign_risk
    df = assign_risk(df)          # adds a 'Risk' (and 'RiskCluster') column

To retrain and overwrite the persisted model:
    python -m src.risk_model
"""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "risk_model.joblib"

NUMERIC_FEATURES = ["Age", "Job", "CreditAmount", "Duration"]
CATEGORICAL_FEATURES = ["Sex", "Housing", "SavingAccounts", "CheckingAccount", "Purpose"]
TIER_ORDER = ["Low", "Medium", "High"]


def _prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    features = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES].copy()
    for col in CATEGORICAL_FEATURES:
        # Saving/Checking account are legitimately missing for many
        # customers (no such account) — treat that as its own category
        # rather than dropping rows or imputing a fake value.
        features[col] = features[col].fillna("none")
    return features


def _build_pipeline(n_clusters: int) -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )
    return Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("cluster", KMeans(n_clusters=n_clusters, random_state=42, n_init=10)),
        ]
    )


def train_risk_model(df: pd.DataFrame, n_clusters: int = 3) -> dict:
    """Fit the clustering pipeline and rank clusters into risk tiers."""
    features = _prepare_features(df)

    pipeline = _build_pipeline(n_clusters)
    cluster_labels = pipeline.fit_predict(features)

    # Exposure score: bigger loans held for longer are riskier. log1p on
    # duration keeps a handful of very long loans from dominating the score.
    exposure = (
        df.assign(_cluster=cluster_labels)
        .groupby("_cluster")
        .apply(lambda g: (g["CreditAmount"].mean()) * np.log1p(g["Duration"].mean()))
    )
    ranked_clusters = exposure.sort_values().index.tolist()
    tier_names = TIER_ORDER[:n_clusters]
    cluster_to_tier = dict(zip(ranked_clusters, tier_names))

    artifact = {
        "pipeline": pipeline,
        "cluster_to_tier": cluster_to_tier,
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "n_clusters": n_clusters,
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, MODEL_PATH)
    return artifact


def load_or_train_risk_model(df: pd.DataFrame) -> dict:
    if MODEL_PATH.exists():
        try:
            return joblib.load(MODEL_PATH)
        except Exception:
            pass  # fall through and retrain if the file is corrupt/incompatible
    return train_risk_model(df)


def assign_risk(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of df with 'RiskCluster' and 'Risk' (Low/Medium/High) columns."""
    artifact = load_or_train_risk_model(df)
    features = _prepare_features(df)[artifact["numeric_features"] + artifact["categorical_features"]]

    cluster_labels = artifact["pipeline"].predict(features)
    out = df.copy()
    out["RiskCluster"] = cluster_labels
    out["Risk"] = out["RiskCluster"].map(artifact["cluster_to_tier"])
    return out


if __name__ == "__main__":
    from src.data_loader import load_raw_data

    raw = load_raw_data()
    artifact = train_risk_model(raw)
    scored = assign_risk(raw)
    print(f"Risk model trained and saved to {MODEL_PATH}")
    print(scored["Risk"].value_counts())
