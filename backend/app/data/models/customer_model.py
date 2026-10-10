
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr


class CustomerBase(BaseModel):
    customer_name: str = Field(min_length=1, max_length=150)
    email: EmailStr | None = None
    account_type: str | None = None
    city: str | None = None
    state: str | None = None


class CustomerCreate(CustomerBase):
    customer_id: str = Field(min_length=1, max_length=50)


class CustomerResponse(CustomerBase):
    customer_id: str
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class CustomerSummary(BaseModel):
    total_customers: int = Field(ge=0)
    active_customers: int = Field(ge=0)
    inactive_customers: int = Field(ge=0)
