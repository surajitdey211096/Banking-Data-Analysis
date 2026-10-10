
from app.models.customer_model import (
    CustomerBase,
    CustomerCreate,
    CustomerResponse,
    CustomerSummary,
)

from app.models.transaction_model import (
    TransactionCreate,
    TransactionResponse,
    TransactionSummary,
    TransactionType,
    TransactionStatus,
)

from app.models.loan_model import (
    LoanCreate,
    LoanResponse,
    LoanSummary,
    LoanStatus,
)

from app.models.fraud_model import (
    FraudAlertCreate,
    FraudAlertResponse,
    FraudSummary,
    FraudStatus,
)

from app.models.dashboard_model import (
    DashboardKPI,
    DashboardResponse,
    MonthlyTransactionSummary,
)
