
from fastapi import APIRouter, HTTPException, Query
from app.database import fetch_all, fetch_one

router = APIRouter()

@router.get("/")
def list_loans(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    loan_type: str | None = None,
    status: str | None = None,
    risk_grade: str | None = None,
):
    return fetch_all("""
        SELECT
            loan_id, loan_number, customer_id, branch_id,
            loan_type, application_date, disbursement_date,
            principal_amount, outstanding_amount,
            interest_rate, tenure_months, monthly_emi,
            loan_status, risk_grade
        FROM loans
        WHERE (:loan_type IS NULL OR loan_type = :loan_type)
          AND (:status IS NULL OR loan_status = :status)
          AND (:risk_grade IS NULL OR risk_grade = :risk_grade)
        ORDER BY loan_id
        LIMIT :limit OFFSET :offset
    """, {
        "loan_type": loan_type,
        "status": status,
        "risk_grade": risk_grade,
        "limit": limit,
        "offset": offset,
    })

@router.get("/summary")
def loan_summary():
    return fetch_all("""
        SELECT
            loan_type,
            COUNT(*) AS loan_count,
            SUM(principal_amount) AS total_principal,
            SUM(outstanding_amount) AS total_outstanding,
            AVG(interest_rate) AS average_interest_rate
        FROM loans
        GROUP BY loan_type
        ORDER BY total_outstanding DESC
    """)

@router.get("/risk-analysis")
def loan_risk_analysis():
    return fetch_all("""
        SELECT
            risk_grade,
            loan_status,
            COUNT(*) AS loan_count,
            SUM(outstanding_amount) AS outstanding_amount
        FROM loans
        GROUP BY risk_grade, loan_status
        ORDER BY risk_grade, loan_status
    """)

@router.get("/{loan_id}")
def loan_detail(loan_id: int):
    loan = fetch_one("""
        SELECT *
        FROM loans
        WHERE loan_id = :loan_id
    """, {"loan_id": loan_id})

    if not loan:
        raise HTTPException(404, detail="Loan not found")

    loan["payments"] = fetch_all("""
        SELECT
            payment_id, payment_date, installment_number,
            due_amount, paid_amount, payment_method,
            payment_status, days_late
        FROM loan_payments
        WHERE loan_id = :loan_id
        ORDER BY installment_number
    """, {"loan_id": loan_id})

    return loan