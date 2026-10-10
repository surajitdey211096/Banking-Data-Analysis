
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class DashboardKPI(BaseModel):
    total_customers: int = Field(ge=0)
    total_transactions: int = Field(ge=0)
    total_transaction_amount: Decimal
    total_active_loans: int = Field(ge=0)
    total_loan_principal: Decimal
    total_fraud_alerts: int = Field(ge=0)


class MonthlyTransactionSummary(BaseModel):
    month: str = Field(pattern=r"^\d{4}-\d{2}$")
    transaction_count: int = Field(ge=0)
    total_amount: Decimal


class DashboardResponse(BaseModel):
    generated_at: date
    kpis: DashboardKPI
    monthly_transactions: list[MonthlyTransactionSummary] = []
