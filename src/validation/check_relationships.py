import csv
from pathlib import Path

DATA_DIR = Path("data/raw")


def load_column(filename, column):
    values = set()

    with open(DATA_DIR / filename, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            value = row[column]
            if value:
                values.add(value)

    return values


def check_relationship(child_file, child_column, parent_file, parent_column):

    parent_values = load_column(parent_file, parent_column)

    total = 0
    orphan_count = 0

    with open(DATA_DIR / child_file, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            value = row[child_column]

            if not value:
                continue

            total += 1

            if value not in parent_values:
                orphan_count += 1

    print(f"\n{child_file}.{child_column}")
    print(f"    -> {parent_file}.{parent_column}")
    print("Records checked:", total)
    print("Orphan records:", orphan_count)
    print("Result:", "PASS" if orphan_count == 0 else "INVESTIGATE")


relationships = [
    ("olist_orders_dataset.csv", "customer_id",
     "olist_customers_dataset.csv", "customer_id"),

    ("olist_order_items_dataset.csv", "order_id",
     "olist_orders_dataset.csv", "order_id"),

    ("olist_order_items_dataset.csv", "product_id",
     "olist_products_dataset.csv", "product_id"),

    ("olist_order_items_dataset.csv", "seller_id",
     "olist_sellers_dataset.csv", "seller_id"),

    ("olist_order_payments_dataset.csv", "order_id",
     "olist_orders_dataset.csv", "order_id"),

    ("olist_order_reviews_dataset.csv", "order_id",
     "olist_orders_dataset.csv", "order_id"),

    ("olist_products_dataset.csv", "product_category_name",
     "product_category_name_translation.csv", "product_category_name"),
]


print("=" * 65)
print("       RETAILPULSE - FOREIGN KEY VALIDATION")
print("=" * 65)

for relationship in relationships:
    check_relationship(*relationship)

print("\n" + "=" * 65)
print("RELATIONSHIP VALIDATION COMPLETED")
print("=" * 65)
