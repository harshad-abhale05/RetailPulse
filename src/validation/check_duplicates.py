import csv
from pathlib import Path

DATA_DIR = Path("data/raw")

key_definitions = {
    "olist_customers_dataset.csv": ["customer_id"],
    "olist_orders_dataset.csv": ["order_id"],
    "olist_products_dataset.csv": ["product_id"],
    "olist_sellers_dataset.csv": ["seller_id"],
    "olist_order_reviews_dataset.csv": ["review_id"],
    "olist_order_items_dataset.csv": ["order_id", "order_item_id"],
    "olist_order_payments_dataset.csv": ["order_id", "payment_sequential"],
    "product_category_name_translation.csv": ["product_category_name"],
}

print("=" * 65)
print("       RETAILPULSE - PRIMARY KEY VALIDATION")
print("=" * 65)

for filename, key_columns in key_definitions.items():

    file_path = DATA_DIR / filename
    unique_keys = set()
    duplicate_count = 0
    total_rows = 0

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:
            total_rows += 1

            key = tuple(row[column] for column in key_columns)

            if key in unique_keys:
                duplicate_count += 1
            else:
                unique_keys.add(key)

    print(f"\nDataset: {filename}")
    print(f"Candidate key: {key_columns}")
    print(f"Total records: {total_rows}")
    print(f"Unique keys: {len(unique_keys)}")
    print(f"Duplicate keys: {duplicate_count}")

    if duplicate_count == 0:
        print("Result: PASS")
    else:
        print("Result: DUPLICATES FOUND")

print("\n" + "=" * 65)
print("VALIDATION COMPLETED")
print("=" * 65)
