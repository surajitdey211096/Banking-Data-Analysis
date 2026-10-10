
import pandas as pd


class DataTransformer:
    """Transform cleaned data into analytics-ready datasets."""

    @staticmethod
    def convert_date_columns(
        df: pd.DataFrame,
        date_columns: list[str],
        errors: str = "coerce",
    ) -> pd.DataFrame:
        """Convert specified columns to datetime."""
        result = df.copy()

        for column in date_columns:
            if column not in result.columns:
                raise ValueError(
                    f"Date column not found: {column}"
                )

            result[column] = pd.to_datetime(
                result[column],
                errors=errors,
            )

        return result

    @staticmethod
    def convert_numeric_columns(
        df: pd.DataFrame,
        numeric_columns: list[str],
        errors: str = "coerce",
    ) -> pd.DataFrame:
        """Convert specified columns to numeric types."""
        result = df.copy()

        for column in numeric_columns:
            if column not in result.columns:
                raise ValueError(
                    f"Numeric column not found: {column}"
                )

            result[column] = pd.to_numeric(
                result[column],
                errors=errors,
            )

        return result

    @staticmethod
    def add_transaction_period(
        df: pd.DataFrame,
        date_column: str = "transaction_date",
    ) -> pd.DataFrame:
        """Add year, month and year-month reporting fields."""
        result = df.copy()

        if date_column not in result.columns:
            raise ValueError(
                f"Date column not found: {date_column}"
            )

        dates = pd.to_datetime(
            result[date_column],
            errors="coerce",
        )

        result["transaction_year"] = dates.dt.year
        result["transaction_month"] = dates.dt.month

        result["transaction_year_month"] = (
            dates.dt.strftime("%Y-%m")
        )

        return result

    @staticmethod
    def add_transaction_flags(
        df: pd.DataFrame,
        amount_column: str = "transaction_amount",
        threshold: float = 10000,
    ) -> pd.DataFrame:
        """
        Add analytical flags based on transaction amount.

        The threshold is illustrative, not a fraud rule.
        """
        result = df.copy()

        if amount_column not in result.columns:
            raise ValueError(
                f"Amount column not found: {amount_column}"
            )

        amounts = pd.to_numeric(
            result[amount_column],
            errors="coerce",
        )

        result["high_value_transaction"] = (
            amounts >= threshold
        ).where(amounts.notna(), pd.NA).astype("boolean")

        return result

    @staticmethod
    def group_transaction_summary(
        df: pd.DataFrame,
        group_column: str = "transaction_type",
        amount_column: str = "transaction_amount",
    ) -> pd.DataFrame:
        """Summarize transaction count and amount by category."""
        for column in [group_column, amount_column]:
            if column not in df.columns:
                raise ValueError(
                    f"Required column not found: {column}"
                )

        working = df.copy()

        working[amount_column] = pd.to_numeric(
            working[amount_column],
            errors="coerce",
        )

        summary = (
            working.groupby(
                group_column,
                dropna=False,
            )
            .agg(
                transaction_count=(amount_column, "size"),
                total_amount=(amount_column, "sum"),
                average_amount=(amount_column, "mean"),
            )
            .reset_index()
        )

        return summary

    @staticmethod
    def create_rag_documents(
        df: pd.DataFrame,
        id_column: str,
        text_columns: list[str],
    ) -> list[dict]:
        """
        Convert rows into documents for the RAG pipeline.

        Only include fields approved for AI processing.
        """
        required = [id_column] + text_columns

        missing = [
            column
            for column in required
            if column not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Required columns not found: {missing}"
            )

        documents = []

        for _, row in df[required].iterrows():
            record_id = row[id_column]

            if pd.isna(record_id):
                continue

            fields = []

            for column in text_columns:
                value = row[column]

                if pd.isna(value):
                    continue

                if isinstance(value, pd.Timestamp):
                    value = value.isoformat()

                fields.append(f"{column}: {value}")

            if not fields:
                continue

            documents.append({
                "id": str(record_id),
                "text": " | ".join(fields),
            })

        return documents
