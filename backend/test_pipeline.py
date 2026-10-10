
from pathlib import Path

from app.data.loader import DataLoader
from app.data.cleaning import DataCleaner
from app.data.transformation import DataTransformer


def main():
    # Project backend directory
    base_dir = Path(__file__).resolve().parent

    # Find the data folder
    data_dir = base_dir / "data"

    # Automatically find Excel files in data/
    excel_files = list(data_dir.glob("*.xlsx"))

    if not excel_files:
        print(f"ERROR: No Excel file found in {data_dir}")
        print("Place your banking Excel file inside the data folder.")
        return

    file_path = excel_files[0]
    print(f"Loading file: {file_path.name}")

    # Step 1: Load data
    loader = DataLoader()
    raw_df = loader.load_file(str(file_path))

    print("\n--- RAW DATA ---")
    print(raw_df.head())
    print("Shape:", raw_df.shape)

    # Step 2: Clean data
    cleaner = DataCleaner()
    clean_df = cleaner.clean(
        raw_df,
        missing_strategy="preserve",
    )

    print("\n--- CLEANED DATA ---")
    print(clean_df.head())
    print("Shape:", clean_df.shape)

    # Step 3: Transform data
    transformer = DataTransformer()

    if "transaction_date" in clean_df.columns:
        clean_df = transformer.add_transaction_period(
            clean_df,
            date_column="transaction_date",
        )

    if "transaction_amount" in clean_df.columns:
        clean_df = transformer.add_transaction_flags(
            clean_df,
            amount_column="transaction_amount",
            threshold=10000,
        )

    # Step 4: Export processed data
    output_path = data_dir / "banking_processed.csv"

    clean_df.to_csv(output_path, index=False)

    print("\n--- PIPELINE COMPLETED ---")
    print(f"Output saved to: {output_path}")
    print("Processed shape:", clean_df.shape)


if __name__ == "__main__":
    main()
