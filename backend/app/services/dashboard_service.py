
from app.data.loader import load_data


def get_dashboard_summary():
    data = load_data()

    customers = data["Customers"]
    accounts = data["Accounts"]
    transactions = data["Transactions"]
    loans = data["Loans"]
    service_tickets = data["Service_Tickets"]

    transaction_amount = transactions["Amount_INR"].fillna(0)
    loan_amount = loans["Loan_Amount_INR"].fillna(0)
    outstanding = loans["Outstanding_Principal_INR"].fillna(0)

    fraud_count = 0
    if "Fraud_Flag" in transactions.columns:
        fraud_count = int(
            transactions["Fraud_Flag"]
            .astype(str).str.strip().str.lower()
            .isin(["true", "1", "yes", "y"])
            .sum()
        )

    active_accounts = int(
        accounts["Account_Status"]
        .astype(str).str.strip().str.lower()
        .eq("active").sum()
    )

    resolved_tickets = int(
        service_tickets["Status"]
        .astype(str).str.strip().str.lower()
        .isin(["resolved", "closed"]).sum()
    )

    return {
        "total_customers": int(customers["Customer_ID"].nunique()),
        "total_accounts": int(accounts["Account_ID"].nunique()),
        "active_accounts": active_accounts,
        "total_transactions": int(transactions["Txn_ID"].nunique()),
        "transaction_value_inr": round(float(transaction_amount.sum()), 2),
        "total_loan_portfolio_inr": round(float(loan_amount.sum()), 2),
        "outstanding_loan_inr": round(float(outstanding.sum()), 2),
        "fraud_flagged_transactions": fraud_count,
        "total_service_tickets": int(len(service_tickets)),
        "resolved_service_tickets": resolved_tickets,
    }