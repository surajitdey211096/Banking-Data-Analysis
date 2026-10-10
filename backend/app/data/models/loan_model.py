
from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class LoanStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ACTIVE = "active"
    CLOSED = "closed"


class LoanCreate(BaseModel):
    loan_id: str = Field(min_length=1, max_length=50)
    customer_id: str = Field(min_length=1, max_length=50)

    loan_type: str = Field(min_length=1, max_length=100)
    principal_amount: Decimal = Field(
        gt=0, max_digits=18, decimal_places=2
    )
    interest_rate: Decimal = Field(
        ge=0, le=100, max_digits=5, decimal_places=2
    )
    loan_start_date: date
    loan_end_date: date | None = None

    status: LoanStatus = LoanStatus.PENDING


class LoanResponse(LoanCreate):
    model_config = ConfigDict(from_attributes=True)


class LoanSummary(BaseModel):
    total_loans: int = Field(ge=0)
    approved_loans: int = Field(ge=0)
    rejected_loans: int = Field(ge=0)
    total_principal_amount: Decimal
