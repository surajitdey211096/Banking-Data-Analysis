
from app.data.loader import load_data
import pandas as pd


def get_loan_summary():
    data = load_data()
    loans = data["Loans"].copy()

    loan_amount = pd.to_numeric(
        loans["Loan_Amount_INR"], errors="coerce"
    ).fillna(0)

    outstanding = pd.to_numeric(
        loans["Outstanding_Principal_INR"], errors="coerce"
    ).fillna(0)

    emi = pd.to_numeric(
        loans["EMI_Amount_INR"], errors="coerce"
    ).fillna(0)

    return {
        "total_loans": int(loans["Loan_ID"].nunique()),
        "total_loan_portfolio_inr": round(float(loan_amount.sum()), 2),
        "total_outstanding_principal_inr": round(
            float(outstanding.sum()), 2
        ),
        "average_loan_amount_inr": round(float(loan_amount.mean()), 2),
        "total_monthly_emi_inr": round(float(emi.sum()), 2),
        "loan_status": (
            loans["Loan_Status"].fillna("Unknown")
            .value_counts().to_dict()
        ),
        "loan_types": (
            loans["Loan_Type"].fillna("Unknown")
            .value_counts().to_dict()
        ),
    }


def get_loan_risk():
    data = load_data()
    loans = data["Loans"].copy()

    dpd = pd.to_numeric(
        loans["Days_Past_Due"], errors="coerce"
    ).fillna(0)

    loans["Days_Past_Due"] = dpd

    overdue = loans[loans["Days_Past_Due"] > 0]

    return {
        "overdue_loan_count": int(overdue["Loan_ID"].nunique()),
        "overdue_outstanding_inr": round(
            float(
                pd.to_numeric(
                    overdue["Outstanding_Principal_INR"],
                    errors="coerce"
                ).fillna(0).sum()
            ),
            2,
        ),
        "days_past_due_buckets": {
            "1_to_30_days": int(dpd.between(1, 30).sum()),
            "31_to_60_days": int(dpd.between(31, 60).sum()),
            "61_to_90_days": int(dpd.between(61, 90).sum()),
            "over_90_days": int((dpd > 90).sum()),
        },
    }