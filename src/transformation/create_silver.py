import duckdb
import json
from pathlib import Path
from datetime import datetime, timezone

RAW = Path("data/raw")
SILVER = Path("data/processed/silver")
REPORT = Path("data/processed/silver_transformation_report.json")

SILVER.mkdir(parents=True, exist_ok=True)

con = duckdb.connect(":memory:")

results = []

def transform(name, query, source_file, key_columns):
    source = RAW / source_file
    output = SILVER / f"{name}.parquet"

    if not source.exists():
        raise FileNotFoundError(source)

    print(f"\nTransforming: {source_file}")

    con.execute(query, [str(source)])

    row_count = con.execute(
        "SELECT COUNT(*) FROM silver_table"
    ).fetchone()[0]

    con.execute(
        "COPY silver_table TO ? (FORMAT PARQUET, COMPRESSION ZSTD)",
        [str(output)]
    )

    parquet_count = con.execute(
        "SELECT COUNT(*) FROM read_parquet(?)",
        [str(output)]
    ).fetchone()[0]

    # Check primary/composite key uniqueness
    key_expression = ", ".join(
        f'"{column}"' for column in key_columns
    )

    duplicate_count = con.execute(
        f"""
        SELECT COUNT(*) - COUNT(DISTINCT ({key_expression}))
        FROM silver_table
        """
    ).fetchone()[0]

    if row_count != parquet_count:
        raise ValueError(f"Row count mismatch: {name}")

    if duplicate_count != 0:
        raise ValueError(f"Duplicate key found: {name}")

    print(f"Rows: {row_count:,}")
    print("Row count validation: PASS")
    print("Key uniqueness validation: PASS")

    results.append({
        "dataset": name,
        "source_file": source_file,
        "output_file": str(output),
        "row_count": row_count,
        "parquet_row_count": parquet_count,
        "duplicate_keys": duplicate_count,
        "validation": "PASS"
    })


print("=" * 65)
print("RETAILPULSE - IMPROVED SILVER TRANSFORMATION")
print("=" * 65)

# 1. Customers
transform(
    "customers",
    """
    CREATE OR REPLACE TABLE silver_table AS
    SELECT
        CAST(customer_id AS VARCHAR) AS customer_id,
        CAST(customer_unique_id AS VARCHAR) AS customer_unique_id,
        CAST(customer_zip_code_prefix AS VARCHAR) AS customer_zip_code_prefix,
        CAST(customer_city AS VARCHAR) AS customer_city,
        CAST(customer_state AS VARCHAR) AS customer_state
    FROM read_csv_auto(?, header = true)
    """,
    "olist_customers_dataset.csv",
    ["customer_id"]
)

# 2. Orders
transform(
    "orders",
    """
    CREATE OR REPLACE TABLE silver_table AS
    SELECT
        CAST(order_id AS VARCHAR) AS order_id,
        CAST(customer_id AS VARCHAR) AS customer_id,
        CAST(order_status AS VARCHAR) AS order_status,
        CAST(order_purchase_timestamp AS TIMESTAMP) AS order_purchase_timestamp,
        CAST(order_approved_at AS TIMESTAMP) AS order_approved_at,
        CAST(order_delivered_carrier_date AS TIMESTAMP) AS order_delivered_carrier_date,
        CAST(order_delivered_customer_date AS TIMESTAMP) AS order_delivered_customer_date,
        CAST(order_estimated_delivery_date AS TIMESTAMP) AS order_estimated_delivery_date
    FROM read_csv_auto(?, header = true)
    """,
    "olist_orders_dataset.csv",
    ["order_id"]
)

# 3. Order items
transform(
    "order_items",
    """
    CREATE OR REPLACE TABLE silver_table AS
    SELECT
        CAST(order_id AS VARCHAR) AS order_id,
        CAST(order_item_id AS BIGINT) AS order_item_id,
        CAST(product_id AS VARCHAR) AS product_id,
        CAST(seller_id AS VARCHAR) AS seller_id,
        CAST(shipping_limit_date AS TIMESTAMP) AS shipping_limit_date,
        CAST(price AS DECIMAL(12,2)) AS price,
        CAST(freight_value AS DECIMAL(12,2)) AS freight_value
    FROM read_csv_auto(?, header = true)
    """,
    "olist_order_items_dataset.csv",
    ["order_id", "order_item_id"]
)

# 4. Payments
transform(
    "payments",
    """
    CREATE OR REPLACE TABLE silver_table AS
    SELECT
        CAST(order_id AS VARCHAR) AS order_id,
        CAST(payment_sequential AS BIGINT) AS payment_sequential,
        CAST(payment_type AS VARCHAR) AS payment_type,
        CAST(payment_installments AS BIGINT) AS payment_installments,
        CAST(payment_value AS DECIMAL(12,2)) AS payment_value
    FROM read_csv_auto(?, header = true)
    """,
    "olist_order_payments_dataset.csv",
    ["order_id", "payment_sequential"]
)

# 5. Reviews
transform(
    "reviews",
    """
    CREATE OR REPLACE TABLE silver_table AS
    SELECT
        CAST(review_id AS VARCHAR) AS review_id,
        CAST(order_id AS VARCHAR) AS order_id,
        CAST(review_score AS INTEGER) AS review_score,
        CAST(review_comment_title AS VARCHAR) AS review_comment_title,
        CAST(review_comment_message AS VARCHAR) AS review_comment_message,
        CAST(review_creation_date AS TIMESTAMP) AS review_creation_date,
        CAST(review_answer_timestamp AS TIMESTAMP) AS review_answer_timestamp
    FROM read_csv_auto(?, header = true)
    """,
    "olist_order_reviews_dataset.csv",
    ["review_id", "order_id"]
)

# 6. Products with category translation
transform(
    "products",
    """
    CREATE OR REPLACE TABLE silver_table AS
    SELECT
        CAST(p.product_id AS VARCHAR) AS product_id,
        CAST(p.product_category_name AS VARCHAR) AS product_category_name,
        COALESCE(
            t.product_category_name_english,
            p.product_category_name
        ) AS product_category_name_english,
        CAST(p.product_name_lenght AS BIGINT) AS product_name_lenght,
        CAST(p.product_description_lenght AS BIGINT) AS product_description_lenght,
        CAST(p.product_photos_qty AS BIGINT) AS product_photos_qty,
        CAST(p.product_weight_g AS BIGINT) AS product_weight_g,
        CAST(p.product_length_cm AS BIGINT) AS product_length_cm,
        CAST(p.product_height_cm AS BIGINT) AS product_height_cm,
        CAST(p.product_width_cm AS BIGINT) AS product_width_cm
    FROM read_csv_auto(?, header = true) p
    LEFT JOIN read_parquet('data/processed/silver/product_category_name_translation.parquet') t
        ON p.product_category_name = t.product_category_name
    """,
    "olist_products_dataset.csv",
    ["product_id"]
)

# 7. Sellers
transform(
    "sellers",
    """
    CREATE OR REPLACE TABLE silver_table AS
    SELECT
        CAST(seller_id AS VARCHAR) AS seller_id,
        CAST(seller_zip_code_prefix AS VARCHAR) AS seller_zip_code_prefix,
        CAST(seller_city AS VARCHAR) AS seller_city,
        CAST(seller_state AS VARCHAR) AS seller_state
    FROM read_csv_auto(?, header = true)
    """,
    "olist_sellers_dataset.csv",
    ["seller_id"]
)

# 8. Category translation
transform(
    "category_translation",
    """
    CREATE OR REPLACE TABLE silver_table AS
    SELECT
        CAST(product_category_name AS VARCHAR) AS product_category_name,
        CAST(product_category_name_english AS VARCHAR) AS product_category_name_english
    FROM read_csv_auto(?, header = true)
    """,
    "product_category_name_translation.csv",
    ["product_category_name"]
)

# 9. Aggregate geolocation to one row per ZIP prefix
geo_source = RAW / "olist_geolocation_dataset.csv"
geo_output = SILVER / "geolocation_by_zip.parquet"

if not geo_source.exists():
    raise FileNotFoundError(geo_source)

print("\nAggregating geolocation by ZIP prefix...")

con.execute(
    """
    CREATE OR REPLACE TABLE silver_table AS
    SELECT
        CAST(geolocation_zip_code_prefix AS VARCHAR) AS geolocation_zip_code_prefix,
        AVG(geolocation_lat) AS average_latitude,
        AVG(geolocation_lng) AS average_longitude,
        MODE(geolocation_city) AS geolocation_city,
        MODE(geolocation_state) AS geolocation_state,
        COUNT(*) AS source_record_count
    FROM read_csv_auto(?, header = true)
    GROUP BY geolocation_zip_code_prefix
    """,
    [str(geo_source)]
)

geo_count = con.execute(
    "SELECT COUNT(*) FROM silver_table"
).fetchone()[0]

con.execute(
    "COPY silver_table TO ? (FORMAT PARQUET, COMPRESSION ZSTD)",
    [str(geo_output)]
)

geo_duplicates = con.execute(
    """
    SELECT COUNT(*) - COUNT(DISTINCT geolocation_zip_code_prefix)
    FROM silver_table
    """
).fetchone()[0]

if geo_duplicates != 0:
    raise ValueError("Duplicate ZIP prefixes in aggregated geolocation")

results.append({
    "dataset": "geolocation_by_zip",
    "source_file": "olist_geolocation_dataset.csv",
    "output_file": str(geo_output),
    "row_count": geo_count,
    "duplicate_keys": geo_duplicates,
    "validation": "PASS"
})

print(f"Unique ZIP prefixes: {geo_count:,}")
print("Geolocation aggregation validation: PASS")

# Save report
report = {
    "project": "RetailPulse",
    "layer": "SILVER",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "total_outputs": len(results),
    "datasets": results
}

with open(REPORT, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=4)

con.close()

print("\n" + "=" * 65)
print("SILVER TRANSFORMATION COMPLETED")
print(f"Output datasets: {len(results)}")
print(f"Report: {REPORT}")
print("=" * 65)
