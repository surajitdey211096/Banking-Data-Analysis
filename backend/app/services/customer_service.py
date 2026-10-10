
from app.data.loader import load_data


def get_customer_summary():
    data = load_data()
    customers = data["Customers"]

    income = customers["Annual_Income_INR"].fillna(0)
    credit_score = customers["Credit_Score"]

    return {
        "total_customers": int(customers["Customer_ID"].nunique()),
        "average_annual_income_inr": round(float(income.mean()), 2),
        "average_credit_score": (
            round(float(credit_score.mean()), 2)
            if credit_score.notna().any() else None
        ),
        "kyc_status": (
            customers["KYC_Status"].fillna("Unknown")
            .value_counts().to_dict()
        ),
        "customer_segments": (
            customers["Customer_Segment"].fillna("Unknown")
            .value_counts().to_dict()
        ),
        "customers_by_state": (
            customers["State"].fillna("Unknown")
            .value_counts().to_dict()
        ),
        "preferred_channels": (
            customers["Preferred_Channel"].fillna("Unknown")
            .value_counts().to_dict()
        ),
    }


def get_customers(limit=100):
    data = load_data()
    customers = data["Customers"].copy()

    limit = max(1, min(int(limit), 1000))

    # Do not return unnecessary personally identifying details.
    columns = [
        "Customer_ID", "Gender", "City", "State", "Occupation",
        "Annual_Income_INR", "Customer_Segment", "Credit_Score",
        "KYC_Status", "Preferred_Channel"
    ]
    columns = [col for col in columns if col in customers.columns]

    return customers[columns].head(limit).where(
        customers[columns].head(limit).notna(), None
    ).to_dict(orient="records")