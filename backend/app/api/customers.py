
from fastapi import APIRouter, HTTPException, Query
from app.database import fetch_all, fetch_one

router = APIRouter()

@router.get("/")
def list_customers(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    city: str | None = None,
    segment: str | None = None,
):
    sql = """
        SELECT
            customer_id, customer_code,
            first_name, last_name,
            city, state, occupation,
            annual_income, credit_score,
            customer_segment, kyc_status, customer_status
        FROM customers
        WHERE (:city IS NULL OR city = :city)
          AND (:segment IS NULL OR customer_segment = :segment)
        ORDER BY customer_id
        LIMIT :limit OFFSET :offset
    """
    return fetch_all(sql, {
        "city": city,
        "segment": segment,
        "limit": limit,
        "offset": offset,
    })

@router.get("/summary")
def customer_summary():
    return fetch_all("""
        SELECT
            customer_segment,
            customer_status,
            COUNT(*) AS customer_count
        FROM customers
        GROUP BY customer_segment, customer_status
        ORDER BY customer_segment
    """)

@router.get("/{customer_id}")
def customer_detail(customer_id: int):
    customer = fetch_one("""
        SELECT
            customer_id, customer_code,
            first_name, last_name, gender,
            city, state, occupation,
            annual_income, credit_score,
            customer_segment, kyc_status, customer_status,
            registration_date
        FROM customers
        WHERE customer_id = :customer_id
    """, {"customer_id": customer_id})

    if not customer:
        raise HTTPException(404, detail="Customer not found")

    customer["accounts"] = fetch_all("""
        SELECT account_id, account_type, balance,
               account_status, opening_date
        FROM accounts
        WHERE customer_id = :customer_id
    """, {"customer_id": customer_id})

    customer["loans"] = fetch_all("""
        SELECT loan_id, loan_type, principal_amount,
               outstanding_amount, loan_status, risk_grade
        FROM loans
        WHERE customer_id = :customer_id
    """, {"customer_id": customer_id})

    return customer