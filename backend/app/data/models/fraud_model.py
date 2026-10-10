
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class FraudStatus(str, Enum):
    REVIEW = "review"
    CONFIRMED = "confirmed"
    FALSE_POSITIVE = "false_positive"
    CLEARED = "cleared"


class FraudAlertCreate(BaseModel):
    alert_id: str = Field(min_length=1, max_length=50)
    transaction_id: str = Field(min_length=1, max_length=50)

    fraud_score: float = Field(ge=0, le=1)
    risk_level: str = Field(min_length=1, max_length=30)
    reason: str | None = None

    status: FraudStatus = FraudStatus.REVIEW
    detected_at: datetime


class FraudAlertResponse(FraudAlertCreate):
    model_config = ConfigDict(from_attributes=True)


class FraudSummary(BaseModel):
    total_alerts: int = Field(ge=0)
    pending_reviews: int = Field(ge=0)
    confirmed_cases: int = Field(ge=0)
    false_positives: int = Field(ge=0)
