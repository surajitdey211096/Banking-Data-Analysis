
from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    PAYMENT = "payment"


class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    FLAGGED = "flagged"


class TransactionCreate(BaseModel):
    transaction_id: str = Field(min_length=1, max_length=50)
    customer_id: str = Field(min_length=1, max_length=50)
    transaction_type: TransactionType
    amount: Decimal = Field(gt=0, max_digits=18, decimal_places=2)
    transaction_date: datetime
    status: TransactionStatus = TransactionStatus.PENDING
    currency: str = Field(default="INR", min_length=3, max_length=3)


class TransactionResponse(TransactionCreate):
    model_config = ConfigDict(from_attributes=True)


class TransactionSummary(BaseModel):
    total_transactions: int = Field(ge=0)
    total_amount: Decimal
    successful_transactions: int = Field(ge=0)
    failed_transactions: int = Field(ge=0)
