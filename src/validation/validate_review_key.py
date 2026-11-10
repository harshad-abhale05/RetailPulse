import csv
from collections import Counter
from pathlib import Path

file_path = Path("data/raw/olist_order_reviews_dataset.csv")

review_ids = Counter()
composite_keys = Counter()

with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        review_ids[row["review_id"]] += 1

        key = (
            row["review_id"],
            row["order_id"]
        )

        composite_keys[key] += 1

print("=" * 60)
print("REVIEW COMPOSITE KEY VALIDATION")
print("=" * 60)

print("Total records:", sum(review_ids.values()))
print("Unique review IDs:", len(review_ids))
print("Unique review_id + order_id combinations:", len(composite_keys))

print(
    "Duplicate composite keys:",
    sum(count - 1 for count in composite_keys.values())
)

print("\nMaximum occurrences of one review ID:", max(review_ids.values()))
print("Maximum occurrences of one composite key:", max(composite_keys.values()))

print("\nVALIDATION COMPLETED")
