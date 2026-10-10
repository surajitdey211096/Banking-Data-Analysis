
from app.data.loader import load_data
import pandas as pd


def _fraud_mask(transactions):
    # Handles common Boolean, numeric, and text representations.
    return (
        transactions["Fraud_Flag"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "1", "yes", "y", "fraud"])
    )


def get_fraud_summary():
    data = load_data()
    transactions = data["Transactions"].copy()

    flagged = _fraud_mask(transactions)
    fraud_transactions = transactions[flagged].copy()

    amounts = pd.to_numeric(
        fraud_transactions["Amount_INR"], errors="coerce"
    ).fillna(0)

    total_count = len(transactions)
    fraud_count = len(fraud_transactions)

    return {
        "total_transactions": total_count,
        "fraud_flagged_count": fraud_count,
        "fraud_rate_pct": round(
            (fraud_count / total_count * 100)
            if total_count else 0,
            2,
        ),
        "fraud_flagged_value_inr": round(float(amounts.sum()), 2),
        "fraud_by_channel": (
            fraud_transactions["Channel"].fillna("Unknown")
            .value_counts().to_dict()
        ),
        "fraud_by_city": (
            fraud_transactions["Txn_City"].fillna("Unknown")
            .value_counts().to_dict()
        ),
        "fraud_by_category": (
            fraud_transactions["Category"].fillna("Unknown")
            .value_counts().to_dict()
        ),
    }


def get_fraud_transactions(limit=100):
    data = load_data()
    transactions = data["Transactions"].copy()

    limit = max(1, min(int(limit), 1000))
    fraud_transactions = transactions[_fraud_mask(transactions)]

    columns = [
        "Txn_ID", "Txn_Date", "Account_ID", "Amount_INR",
        "Channel", "Category", "Txn_Status", "Fraud_Flag",
        "Txn_City"
    ]
    columns = [
        col for col in columns if col in fraud_transactions.columns
    ]

    return fraud_transactions[columns].head(limit).to_dict(
        orient="records"
    )