import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Find the project root automatically
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

EXPECTED_FILES = [
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv",
]


def inspect_csv(file_path):
    """Read a CSV without changing it and collect basic metadata."""

    row_count = 0
    missing_values = {}

    with file_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError(f"CSV has no header: {file_path.name}")

        columns = reader.fieldnames

        for column in columns:
            missing_values[column] = 0

        for row in reader:
            row_count += 1

            for column in columns:
                value = row.get(column)

                if value is None or value.strip() == "":
                    missing_values[column] += 1

    return {
        "file_name": file_path.name,
        "row_count": row_count,
        "column_count": len(columns),
        "columns": columns,
        "missing_values": missing_values,
        "file_size_bytes": file_path.stat().st_size,
    }


def main():
    print("=" * 65)
    print("          RETAILPULSE - BRONZE DATA INGESTION")
    print("=" * 65)

    if not RAW_DIR.exists():
        print(f"ERROR: Raw data directory not found: {RAW_DIR}")
        sys.exit(1)

    # Check that all expected datasets exist
    missing_files = [
        name for name in EXPECTED_FILES
        if not (RAW_DIR / name).is_file()
    ]

    if missing_files:
        print("ERROR: These expected CSV files are missing:")
        for name in missing_files:
            print(f" - {name}")
        sys.exit(1)

    print(f"\nAll {len(EXPECTED_FILES)} expected CSV files found.")
    print("\nInspecting datasets...\n")

    datasets = []

    for file_name in EXPECTED_FILES:
        file_path = RAW_DIR / file_name

        try:
            metadata = inspect_csv(file_path)
            datasets.append(metadata)

            print(f"Dataset: {metadata['file_name']}")
            print(f"Rows: {metadata['row_count']:,}")
            print(f"Columns: {metadata['column_count']}")
            print("-" * 45)

        except Exception as error:
            print(f"ERROR processing {file_name}: {error}")
            sys.exit(1)

    # Create ingestion metadata report
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    report = {
        "project": "RetailPulse",
        "layer": "BRONZE",
        "ingestion_timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "source_directory": "data/raw",
        "total_datasets": len(datasets),
        "datasets": datasets,
    }

    report_path = OUTPUT_DIR / "bronze_ingestion_report.json"

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("=" * 65)
    print("BRONZE INGESTION COMPLETED SUCCESSFULLY")
    print(f"Datasets processed: {len(datasets)}")
    print(f"Metadata report: {report_path.relative_to(PROJECT_ROOT)}")
    print("=" * 65)


if __name__ == "__main__":
    main()
