
from pathlib import Path
import json

import pandas as pd


SUPPORTED_EXTENSIONS = {".xlsx", ".xls", ".csv", ".json"}


class DataLoader:
    """Load banking datasets from supported file formats."""

    def load_file(self, file_path: str) -> pd.DataFrame:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {path}"
            )

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file format: {path.suffix}"
            )

        extension = path.suffix.lower()

        if extension in {".xlsx", ".xls"}:
            return pd.read_excel(path)

        if extension == ".csv":
            return pd.read_csv(path)

        if extension == ".json":
            return pd.read_json(path)

        raise ValueError("Unable to load the dataset.")

    def load_excel_sheet(
        self,
        file_path: str,
        sheet_name: str,
    ) -> pd.DataFrame:
        """Load one named worksheet from an Excel workbook."""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {path}"
            )

        if path.suffix.lower() not in {".xlsx", ".xls"}:
            raise ValueError("The file must be an Excel workbook.")

        with pd.ExcelFile(path) as workbook:
            if sheet_name not in workbook.sheet_names:
                raise ValueError(
                    f"Sheet '{sheet_name}' not found. "
                    f"Available sheets: {workbook.sheet_names}"
                )

            return pd.read_excel(
                workbook,
                sheet_name=sheet_name,
            )

    def load_all_sheets(self, file_path: str) -> dict:
        """Load every Excel worksheet into a dictionary."""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {path}"
            )

        if path.suffix.lower() not in {".xlsx", ".xls"}:
            raise ValueError("The file must be an Excel workbook.")

        with pd.ExcelFile(path) as workbook:
            return {
                sheet: pd.read_excel(workbook, sheet_name=sheet)
                for sheet in workbook.sheet_names
            }

    def get_dataset_info(self, df: pd.DataFrame) -> dict:
        """Return basic dataset metadata."""
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "missing_values": (
                df.isna().sum().to_dict()
            ),
            "duplicate_rows": int(df.duplicated().sum()),
        }
