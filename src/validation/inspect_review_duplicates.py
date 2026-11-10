import csv
from collections import Counter, defaultdict
from pathlib import Path

file_path = Path("data/raw/olist_order_reviews_dataset.csv")

review_counts = Counter()
review_records = defaultdict(list)
exact_rows = Counter()

with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        review_id = row["review_id"]

        review_counts[review_id] += 1
        review_records[review_id].append(row)

        exact_rows[tuple(row.values())] += 1

duplicates = {
    review_id: count
    for review_id, count in review_counts.items()
    if count > 1
}

print("=" * 60)
print("REVIEW DUPLICATE INVESTIGATION")
print("=" * 60)

print("Total records:", sum(review_counts.values()))
print("Unique review IDs:", len(review_counts))
print("Repeated review IDs:", len(duplicates))
print("Excess records from repeated IDs:",
      sum(count - 1 for count in duplicates.values()))

print("\nExact duplicate rows:",
      sum(count - 1 for count in exact_rows.values() if count > 1))

print("\nFirst 5 repeated review IDs:")

for review_id in list(duplicates.keys())[:5]:
    print("\nReview ID:", review_id)

    for row in review_records[review_id]:
        print({
            "order_id": row["order_id"],
            "review_score": row["review_score"],
            "review_comment_title": row["review_comment_title"]
        })

print("\nINVESTIGATION COMPLETED")
