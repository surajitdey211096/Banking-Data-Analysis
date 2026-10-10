
from fastapi import APIRouter, HTTPException
from app.database import fetch_all, fetch_one

router = APIRouter()

@router.get("/")
def list_branches():
    return fetch_all("""
        SELECT
            branch_id, branch_code, branch_name,
            city, state, branch_type,
            manager_name, employee_count, branch_status
        FROM branches
        ORDER BY branch_name
    """)

@router.get("/performance")
def branch_performance():
    return fetch_all("""
        SELECT *
        FROM vw_branch_performance
        ORDER BY total_deposits DESC
    """)

@router.get("/{branch_id}")
def branch_detail(branch_id: int):
    branch = fetch_one("""
        SELECT *
        FROM branches
        WHERE branch_id = :branch_id
    """, {"branch_id": branch_id})

    if not branch:
        raise HTTPException(404, detail="Branch not found")

    branch["account_summary"] = fetch_one("""
        SELECT
            COUNT(*) AS account_count,
            COALESCE(SUM(balance), 0) AS total_balance
        FROM accounts
        WHERE branch_id = :branch_id
    """, {"branch_id": branch_id})

    branch["loan_summary"] = fetch_one("""
        SELECT
            COUNT(*) AS loan_count,
            COALESCE(SUM(principal_amount), 0) AS principal_amount,
            COALESCE(SUM(outstanding_amount), 0) AS outstanding_amount
        FROM loans
        WHERE branch_id = :branch_id
    """, {"branch_id": branch_id})

    return branch