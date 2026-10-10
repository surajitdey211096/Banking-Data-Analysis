
from app.data.loader import load_data
import pandas as pd


def get_transaction_summary():
    data = load_data()
    transactions = data["Transactions"].copy()

    amounts = pd.to_numeric(
        transactions["Amount_INR"], errors="coerce"
    ).fillna(0)

    return {
        "total_transactions": int(transactions["Txn_ID"].nunique()),
        "total_transaction_value_inr": round(float(amounts.sum()), 2),
        "average_transaction_value_inr": round(float(amounts.mean()), 2),
        "transaction_status": (
            transactions["Txn_Status"].fillna("Unknown")
            .value_counts().to_dict()
        ),
        "payment_modes": (
            transactions["Payment_Mode"].fillna("Unknown")
            .value_counts().to_dict()
        ),
        "channels": (
            transactions["Channel"].fillna("Unknown")
            .value_counts().to_dict()
        ),
        "categories": (
            transactions["Category"].fillna("Unknown")
            .value_counts().to_dict()
        ),
    }


def get_transaction_trend():
    data = load_data()
    transactions = data["Transactions"].copy()

    transactions["Txn_Date"] = pd.to_datetime(
        transactions["Txn_Date"], errors="coerce"
    )
    transactions["Amount_INR"] = pd.to_numeric(
        transactions["Amount_INR"], errors="coerce"
    ).fillna(0)

    transactions = transactions.dropna(subset=["Txn_Date"])

    transactions["Month"] = (
        transactions["Txn_Date"].dt.to_period("M").astype(str)
    )

    trend = (
        transactions.groupby("Month", as_index=False)
        .agg(
            transaction_count=("Txn_ID", "nunique"),
            transaction_value_inr=("Amount_INR", "sum"),
        )
        .sort_values("Month")
    )

    trend["transaction_value_inr"] = (
        trend["transaction_value_inr"].round(2)
    )

    return trend.to_dict(orient="records")


def get_transactions(limit=100):
    data = load_data()
    transactions = data["Transactions"].copy()

    limit = max(1, min(int(limit), 1000))

    columns = [
        "Txn_ID", "Txn_Date", "Account_ID", "Txn_Type",
        "Amount_INR", "Payment_Mode", "Channel", "Category",
        "Txn_Status", "Fraud_Flag", "Txn_City"
    ]
    columns = [col for col in columns if col in transactions.columns]

    return transactions[columns].head(limit).to_dict(orient="records")