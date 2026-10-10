
from fastapi import APIRouter, Query
from app.database import fetch_all, fetch_one

router = APIRouter()

@router.get("/summary")
def fraud_summary():
    return fetch_one("""
        SELECT
            COUNT(*) AS flagged_transactions,
            COALESCE(SUM(transaction_amount), 0) AS flagged_value,
            COALESCE(AVG(transaction_amount), 0) AS average_flagged_value
        FROM transactions
        WHERE is_fraud_flag = 1
    """)

@router.get("/transactions")
def flagged_transactions(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    return fetch_all("""
        SELECT
            transaction_id,
            transaction_reference,
            transaction_date,
            account_id,
            transaction_type,
            transaction_amount,
            channel,
            city,
            transaction_status,
            description
        FROM transactions
        WHERE is_fraud_flag = 1
        ORDER BY transaction_date DESC
        LIMIT :limit OFFSET :offset
    """, {"limit": limit, "offset": offset})

@router.get("/by-channel")
def fraud_by_channel():
    return fetch_all("""
        SELECT
            channel,
            COUNT(*) AS flagged_count,
            SUM(transaction_amount) AS flagged_value
        FROM transactions
        WHERE is_fraud_flag = 1
        GROUP BY channel
        ORDER BY flagged_count DESC
    """)

@router.get("/by-type")
def fraud_by_type():
    return fetch_all("""
        SELECT
            transaction_type,
            COUNT(*) AS flagged_count,
            SUM(transaction_amount) AS flagged_value
        FROM transactions
        WHERE is_fraud_flag = 1
        GROUP BY transaction_type
        ORDER BY flagged_count DESC
    """)