
import pandas as pd


class DataCleaner:
    """Clean and validate tabular banking data."""

    @staticmethod
    def standardize_column_names(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Convert column names to lowercase snake_case."""
        result = df.copy()

        result.columns = [
            "_".join(
                str(column)
                .strip()
                .lower()
                .replace("-", " ")
                .split()
            )
            for column in result.columns
        ]

        if result.columns.duplicated().any():
            duplicates = result.columns[
                result.columns.duplicated()
            ].tolist()

            raise ValueError(
                f"Duplicate column names after standardization: "
                f"{duplicates}"
            )

        return result

    @staticmethod
    def remove_duplicate_rows(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Remove fully duplicated rows."""
        return df.drop_duplicates().copy()

    @staticmethod
    def clean_text_columns(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Trim whitespace from text fields."""
        result = df.copy()

        for column in result.select_dtypes(
            include=["object", "string"]
        ).columns:
            result[column] = result[column].map(
                lambda value: (
                    value.strip()
                    if isinstance(value, str)
                    else value
                )
            )

        return result

    @staticmethod
    def handle_missing_values(
        df: pd.DataFrame,
        strategy: str = "preserve",
        fill_values: dict | None = None,
    ) -> pd.DataFrame:
        """
        Strategies:
        preserve - leave missing values unchanged
        drop_rows - remove rows containing missing values
        fill - fill using explicitly supplied column values
        """
        result = df.copy()

        if strategy == "preserve":
            return result

        if strategy == "drop_rows":
            return result.dropna().copy()

        if strategy == "fill":
            if not fill_values:
                raise ValueError(
                    "Provide fill_values for the fill strategy."
                )

            unknown_columns = (
                set(fill_values) - set(result.columns)
            )

            if unknown_columns:
                raise ValueError(
                    f"Unknown columns: {unknown_columns}"
                )

            return result.fillna(fill_values)

        raise ValueError(
            "strategy must be preserve, drop_rows, or fill."
        )

    @staticmethod
    def validate_required_columns(
        df: pd.DataFrame,
        required_columns: list[str],
    ) -> dict:
        """Check required fields and missing values."""
        missing_columns = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        missing_counts = {}

        for column in required_columns:
            if column in df.columns:
                missing_counts[column] = int(
                    df[column].isna().sum()
                )

        return {
            "valid": len(missing_columns) == 0,
            "missing_columns": missing_columns,
            "missing_value_counts": missing_counts,
        }

    def clean(
        self,
        df: pd.DataFrame,
        missing_strategy: str = "preserve",
        fill_values: dict | None = None,
    ) -> pd.DataFrame:
        """Run the standard cleaning pipeline."""
        result = self.standardize_column_names(df)
        result = self.clean_text_columns(result)
        result = self.remove_duplicate_rows(result)

        result = self.handle_missing_values(
            result,
            strategy=missing_strategy,
            fill_values=fill_values,
        )

        return result.reset_index(drop=True)
