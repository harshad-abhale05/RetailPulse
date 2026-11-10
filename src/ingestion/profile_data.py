import csv
from pathlib import Path

DATA_DIR = Path("data/raw")

print("\n" + "=" * 65)
print("          RETAILPULSE - DATA PROFILING")
print("=" * 65)

for file_path in sorted(DATA_DIR.glob("*.csv")):

    print(f"\n\nDATASET: {file_path.name}")
    print("-" * 65)

    row_count = 0
    missing_values = {}
    sample_rows = []

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        columns = reader.fieldnames

        if not columns:
            print("No column headers found.")
            continue

        missing_values = {column: 0 for column in columns}

        for row in reader:
            row_count += 1

            for column in columns:
                if row[column] is None or row[column].strip() == "":
                    missing_values[column] += 1

            if len(sample_rows) < 3:
                sample_rows.append(row)

    print("Total rows:", row_count)
    print("Total columns:", len(columns))

    print("\nColumn names:")
    print(columns)

    print("\nMissing values:")
    for column, count in missing_values.items():
        print(f"{column}: {count}")

    print("\nFirst 3 records:")
    for row in sample_rows:
        print(row)

print("\n" + "=" * 65)
print("DATA PROFILING COMPLETED")
print("=" * 65)
