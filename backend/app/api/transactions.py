
from datetime import date
from fastapi import APIRouter, HTTPException, Query
from app.database import fetch_all, fetch_one

router = APIRouter()

@router.get("/")
def list_transactions(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    transaction_type: str | None = None,
    channel: str | None = None,
    status: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(400, detail="start_date must be before end_date")

    return fetch_all("""
        SELECT
            transaction_id, transaction_reference,
            account_id, transaction_date,
            transaction_type, debit_amount, credit_amount,
            transaction_amount, channel, city,
            transaction_status, is_fraud_flag
        FROM transactions
        WHERE (:transaction_type IS NULL
               OR transaction_type = :transaction_type)
          AND (:channel IS NULL OR channel = :channel)
          AND (:status IS NULL OR transaction_status = :status)
          AND (:start_date IS NULL
               OR transaction_date >= :start_date)
          AND (:end_date IS NULL
               OR transaction_date < DATE_ADD(:end_date, INTERVAL 1 DAY))
        ORDER BY transaction_date DESC
        LIMIT :limit OFFSET :offset
    """, {
        "transaction_type": transaction_type,
        "channel": channel,
        "status": status,
        "start_date": start_date,
        "end_date": end_date,
        "limit": limit,
        "offset": offset,
    })

@router.get("/summary")
def transaction_summary():
    return fetch_one("""
        SELECT
            COUNT(*) AS total_transactions,
            COALESCE(SUM(transaction_amount), 0) AS total_value,
            COALESCE(AVG(transaction_amount), 0) AS average_value,
            SUM(transaction_status = 'Success') AS successful_count,
            SUM(transaction_status = 'Failed') AS failed_count,
            SUM(is_fraud_flag = 1) AS flagged_count
        FROM transactions
    """)

@router.get("/{transaction_id}")
def transaction_detail(transaction_id: int):
    transaction = fetch_one("""
        SELECT *
        FROM transactions
        WHERE transaction_id = :transaction_id
    """, {"transaction_id": transaction_id})

    if not transaction:
        raise HTTPException(404, detail="Transaction not found")

    return transaction