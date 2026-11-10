import csv
from pathlib import Path
from collections import Counter

DATA_DIR = Path("data/raw")

# Load valid category names from the translation file
valid_categories = set()

with open(
    DATA_DIR / "product_category_name_translation.csv",
    "r",
    encoding="utf-8-sig",
    newline=""
) as file:
    reader = csv.DictReader(file)

    for row in reader:
        valid_categories.add(row["product_category_name"])


# Find products with categories missing from the translation table
orphan_categories = Counter()
orphan_products = []

with open(
    DATA_DIR / "olist_products_dataset.csv",
    "r",
    encoding="utf-8-sig",
    newline=""
) as file:
    reader = csv.DictReader(file)

    for row in reader:
        category = row["product_category_name"]

        if category and category not in valid_categories:
            orphan_categories[category] += 1

            orphan_products.append({
                "product_id": row["product_id"],
                "category": category
            })


print("=" * 60)
print("RETAILPULSE - CATEGORY ORPHAN INVESTIGATION")
print("=" * 60)

print("\nUnique orphan categories:", len(orphan_categories))
print("Affected products:", len(orphan_products))

print("\nOrphan category names and counts:")

for category, count in orphan_categories.items():
    print(f"{category}: {count} products")

print("\nAffected product examples:")

for product in orphan_products[:10]:
    print(product["product_id"], "->", product["category"])

print("\n" + "=" * 60)
