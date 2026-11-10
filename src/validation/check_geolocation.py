import csv
from pathlib import Path

DATA_DIR = Path("data/raw")


def load_prefixes(filename):
    prefixes = set()

    with open(DATA_DIR / filename, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            value = row["geolocation_zip_code_prefix"]
            if value:
                prefixes.add(value)

    return prefixes


geo_prefixes = load_prefixes("olist_geolocation_dataset.csv")

relationships = [
    ("olist_customers_dataset.csv", "customer_zip_code_prefix"),
    ("olist_sellers_dataset.csv", "seller_zip_code_prefix"),
]

print("=" * 60)
print("RETAILPULSE - GEOLOCATION COVERAGE VALIDATION")
print("=" * 60)

for filename, column in relationships:
    total = 0
    unmatched = set()

    with open(DATA_DIR / filename, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            prefix = row[column]

            if prefix:
                total += 1

                if prefix not in geo_prefixes:
                    unmatched.add(prefix)

    print(f"\nDataset: {filename}")
    print("Records checked:", total)
    print("Unmatched unique ZIP prefixes:", len(unmatched))
    print("Result:", "PASS" if not unmatched else "INVESTIGATE")

    if unmatched:
        print("Examples:", list(unmatched)[:10])

print("\nGEOLOCATION VALIDATION COMPLETED")
