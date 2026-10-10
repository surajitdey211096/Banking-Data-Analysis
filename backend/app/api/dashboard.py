from fastapi import APIRouter, HTTPException
import pandas as pd
from pathlib import Path


router = APIRouter()


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[3]

EXCEL_FILE = BASE_DIR / "data" / "Banking_Dataset.xlsx"


# ============================================================
# LOAD EXCEL DATA
# ============================================================

def load_banking_data():
    """
    Load all banking sheets from Excel.
    """

    if not EXCEL_FILE.exists():
        raise FileNotFoundError(
            f"Banking dataset not found: {EXCEL_FILE}"
        )

    try:
        data = pd.read_excel(
            EXCEL_FILE,
            sheet_name=None,
            engine="openpyxl"
        )

        return data

    except Exception as e:
        raise Exception(
            f"Unable to read Banking_Dataset.xlsx: {str(e)}"
        )


# ============================================================
# HELPER FUNCTION
# ============================================================

def find_column(df, possible_names):
    """
    Find a column from multiple possible column names.
    """

    normalized_columns = {
        str(column).strip().lower(): column
        for column in df.columns
    }

    for name in possible_names:

        name = name.lower()

        if name in normalized_columns:
            return normalized_columns[name]

    return None


# ============================================================
# ROOT DASHBOARD
# ============================================================

@router.get("/")
def dashboard_home():

    return {
        "message": "Banking Dashboard API",
        "endpoints": [
            "/api/dashboard/summary",
            "/api/dashboard/transactions",
            "/api/dashboard/transaction-types",
            "/api/dashboard/channels",
            "/api/dashboard/loans",
            "/api/dashboard/branches",
        ]
    }


# ============================================================
# KPI SUMMARY
# ============================================================

@router.get("/summary")
def dashboard_summary():

    try:

        data = load_banking_data()

        customers = data.get("Customers", pd.DataFrame())
        accounts = data.get("Accounts", pd.DataFrame())
        transactions = data.get("Transactions", pd.DataFrame())
        loans = data.get("Loans", pd.DataFrame())
        cards = data.get("Cards", pd.DataFrame())
        tickets = data.get("Service_Tickets", pd.DataFrame())

        # ----------------------------------------------------
        # TRANSACTION AMOUNT
        # ----------------------------------------------------

        transaction_amount = 0

        if not transactions.empty:

            amount_column = find_column(
                transactions,
                [
                    "transaction_amount",
                    "amount",
                    "transaction value"
                ]
            )

            if amount_column:

                transaction_amount = float(
                    pd.to_numeric(
                        transactions[amount_column],
                        errors="coerce"
                    ).fillna(0).sum()
                )

        # ----------------------------------------------------
        # LOAN AMOUNT
        # ----------------------------------------------------

        loan_amount = 0

        if not loans.empty:

            loan_column = find_column(
                loans,
                [
                    "loan_amount",
                    "principal_amount",
                    "outstanding_amount",
                    "amount"
                ]
            )

            if loan_column:

                loan_amount = float(
                    pd.to_numeric(
                        loans[loan_column],
                        errors="coerce"
                    ).fillna(0).sum()
                )

        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        return {
            "status": "success",

            "kpis": {

                "total_customers": int(
                    len(customers)
                ),

                "total_accounts": int(
                    len(accounts)
                ),

                "total_transactions": int(
                    len(transactions)
                ),

                "total_loans": int(
                    len(loans)
                ),

                "total_cards": int(
                    len(cards)
                ),

                "total_service_tickets": int(
                    len(tickets)
                ),

                "total_transaction_amount": round(
                    transaction_amount,
                    2
                ),

                "total_loan_amount": round(
                    loan_amount,
                    2
                )
            }
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# TRANSACTION TREND
# ============================================================

@router.get("/transactions")
def transaction_trend():

    try:

        data = load_banking_data()

        transactions = data.get(
            "Transactions",
            pd.DataFrame()
        )

        if transactions.empty:

            return {
                "status": "success",
                "data": []
            }

        date_column = find_column(
            transactions,
            [
                "transaction_date",
                "date",
                "transaction_datetime"
            ]
        )

        amount_column = find_column(
            transactions,
            [
                "transaction_amount",
                "amount",
                "transaction value"
            ]
        )

        if not date_column:

            return {
                "status": "success",
                "data": []
            }

        transactions[date_column] = pd.to_datetime(
            transactions[date_column],
            errors="coerce"
        )

        transactions = transactions.dropna(
            subset=[date_column]
        )

        # Monthly aggregation

        if amount_column:

            transactions[amount_column] = pd.to_numeric(
                transactions[amount_column],
                errors="coerce"
            ).fillna(0)

            result = (
                transactions
                .set_index(date_column)
                .resample("ME")
                .agg(
                    transaction_count=(
                        amount_column,
                        "count"
                    ),
                    transaction_amount=(
                        amount_column,
                        "sum"
                    )
                )
                .reset_index()
            )

        else:

            result = (
                transactions
                .set_index(date_column)
                .resample("ME")
                .size()
                .reset_index(
                    name="transaction_count"
                )
            )

            result["transaction_amount"] = 0

        result[date_column] = (
            result[date_column]
            .dt.strftime("%Y-%m")
        )

        return {
            "status": "success",
            "data": result.to_dict(
                orient="records"
            )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# TRANSACTION TYPE
# ============================================================

@router.get("/transaction-types")
def transaction_types():

    try:

        data = load_banking_data()

        transactions = data.get(
            "Transactions",
            pd.DataFrame()
        )

        if transactions.empty:

            return {
                "status": "success",
                "data": []
            }

        type_column = find_column(
            transactions,
            [
                "transaction_type",
                "type",
                "transaction type"
            ]
        )

        if not type_column:

            return {
                "status": "success",
                "data": []
            }

        result = (
            transactions[type_column]
            .fillna("Unknown")
            .astype(str)
            .value_counts()
            .reset_index()
        )

        result.columns = [
            "transaction_type",
            "transaction_count"
        ]

        return {
            "status": "success",
            "data": result.to_dict(
                orient="records"
            )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# TRANSACTION CHANNEL
# ============================================================

@router.get("/channels")
def transaction_channels():

    try:

        data = load_banking_data()

        transactions = data.get(
            "Transactions",
            pd.DataFrame()
        )

        if transactions.empty:

            return {
                "status": "success",
                "data": []
            }

        channel_column = find_column(
            transactions,
            [
                "channel",
                "transaction_channel",
                "payment_channel"
            ]
        )

        if not channel_column:

            return {
                "status": "success",
                "data": []
            }

        result = (
            transactions[channel_column]
            .fillna("Unknown")
            .astype(str)
            .value_counts()
            .reset_index()
        )

        result.columns = [
            "channel",
            "transaction_count"
        ]

        return {
            "status": "success",
            "data": result.to_dict(
                orient="records"
            )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# LOAN PORTFOLIO
# ============================================================

@router.get("/loans")
def loan_portfolio():

    try:

        data = load_banking_data()

        loans = data.get(
            "Loans",
            pd.DataFrame()
        )

        if loans.empty:

            return {
                "status": "success",
                "data": []
            }

        loan_type_column = find_column(
            loans,
            [
                "loan_type",
                "type",
                "loan type"
            ]
        )

        amount_column = find_column(
            loans,
            [
                "loan_amount",
                "principal_amount",
                "outstanding_amount",
                "amount"
            ]
        )

        if not loan_type_column:

            return {
                "status": "success",
                "data": []
            }

        loans[loan_type_column] = (
            loans[loan_type_column]
            .fillna("Unknown")
            .astype(str)
        )

        if amount_column:

            loans[amount_column] = pd.to_numeric(
                loans[amount_column],
                errors="coerce"
            ).fillna(0)

            result = (
                loans
                .groupby(loan_type_column)
                .agg(
                    loan_count=(
                        loan_type_column,
                        "size"
                    ),
                    loan_amount=(
                        amount_column,
                        "sum"
                    )
                )
                .reset_index()
            )

        else:

            result = (
                loans
                .groupby(loan_type_column)
                .size()
                .reset_index(
                    name="loan_count"
                )
            )

            result["loan_amount"] = 0

        result = result.rename(
            columns={
                loan_type_column: "loan_type"
            }
        )

        return {
            "status": "success",
            "data": result.to_dict(
                orient="records"
            )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# BRANCH ANALYTICS
# ============================================================

@router.get("/branches")
def branch_analytics():

    try:

        data = load_banking_data()

        branches = data.get(
            "Branches",
            pd.DataFrame()
        )

        if branches.empty:

            return {
                "status": "success",
                "data": []
            }

        # Return branch information

        result = branches.copy()

        # Convert NaN → None

        result = result.where(
            pd.notnull(result),
            None
        )

        return {
            "status": "success",
            "data": result.to_dict(
                orient="records"
            )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )