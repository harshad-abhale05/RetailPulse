import duckdb
import json
from pathlib import Path
from datetime import datetime, timezone

SILVER = "data/processed/silver"
GOLD = Path("data/processed/gold")

GOLD.mkdir(parents=True, exist_ok=True)

con = duckdb.connect()

tables = {

    "fact_orders": f"""
        SELECT
            order_id,
            customer_id,
            order_status,
            order_purchase_timestamp,
            order_approved_at,
            order_delivered_carrier_date,
            order_delivered_customer_date,
            order_estimated_delivery_date
        FROM read_parquet('{SILVER}/orders.parquet')
    """,

    "fact_order_items": f"""
        SELECT
            order_id,
            order_item_id,
            product_id,
            seller_id,
            shipping_limit_date,
            price,
            freight_value,
            price + freight_value AS total_item_value
        FROM read_parquet('{SILVER}/order_items.parquet')
    """,

    "fact_payments": f"""
        SELECT
            order_id,
            payment_sequential,
            payment_type,
            payment_installments,
            payment_value
        FROM read_parquet('{SILVER}/payments.parquet')
    """,

    "fact_reviews": f"""
        SELECT
            review_id,
            order_id,
            review_score,
            review_comment_title,
            review_comment_message,
            review_creation_date,
            review_answer_timestamp
        FROM read_parquet('{SILVER}/reviews.parquet')
    """,

    "dim_customers": f"""
        SELECT
            c.customer_id,
            c.customer_unique_id,
            c.customer_zip_code_prefix,
            c.customer_city,
            c.customer_state,
            g.average_latitude,
            g.average_longitude
        FROM read_parquet('{SILVER}/customers.parquet') c
        LEFT JOIN read_parquet('{SILVER}/geolocation_by_zip.parquet') g
        ON c.customer_zip_code_prefix = g.geolocation_zip_code_prefix
    """,

    "dim_products": f"""
        SELECT
            product_id,
            product_category_name,
            product_category_name_english,
            product_name_lenght,
            product_description_lenght,
            product_photos_qty,
            product_weight_g,
            product_length_cm,
            product_height_cm,
            product_width_cm
        FROM read_parquet('{SILVER}/products.parquet')
    """,

    "dim_sellers": f"""
        SELECT
            s.seller_id,
            s.seller_zip_code_prefix,
            s.seller_city,
            s.seller_state,
            g.average_latitude,
            g.average_longitude
        FROM read_parquet('{SILVER}/sellers.parquet') s
        LEFT JOIN read_parquet('{SILVER}/geolocation_by_zip.parquet') g
        ON s.seller_zip_code_prefix = g.geolocation_zip_code_prefix
    """
}

report = {
    "project": "RetailPulse",
    "layer": "GOLD",
    "created_at_utc": datetime.now(timezone.utc).isoformat(),
    "tables": []
}

print("=" * 60)
print("RETAILPULSE - GOLD LAYER")
print("=" * 60)

for table_name, query in tables.items():

    print(f"\nCreating {table_name}...")

    con.execute(
        f"CREATE OR REPLACE TABLE gold_table AS {query}"
    )

    count = con.execute(
        "SELECT COUNT(*) FROM gold_table"
    ).fetchone()[0]

    output = GOLD / f"{table_name}.parquet"

    con.execute(
        "COPY gold_table TO ? (FORMAT PARQUET, COMPRESSION ZSTD)",
        [str(output)]
    )

    parquet_count = con.execute(
        "SELECT COUNT(*) FROM read_parquet(?)",
        [str(output)]
    ).fetchone()[0]

    if count != parquet_count:
        raise ValueError(f"Row count mismatch: {table_name}")

    print(f"Rows: {count:,}")
    print("Validation: PASS")

    report["tables"].append({
        "table_name": table_name,
        "row_count": count,
        "validation": "PASS",
        "output_file": str(output)
    })

# Create date dimension
print("\nCreating dim_date...")

con.execute(f"""
    CREATE OR REPLACE TABLE gold_table AS
    SELECT DISTINCT
        CAST(order_purchase_timestamp AS DATE) AS date_key,
        EXTRACT(YEAR FROM order_purchase_timestamp) AS year,
        EXTRACT(MONTH FROM order_purchase_timestamp) AS month,
        EXTRACT(DAY FROM order_purchase_timestamp) AS day,
        STRFTIME(order_purchase_timestamp, '%B') AS month_name,
        STRFTIME(order_purchase_timestamp, '%A') AS day_name,
        EXTRACT(QUARTER FROM order_purchase_timestamp) AS quarter
    FROM read_parquet('{SILVER}/orders.parquet')
""")

count = con.execute(
    "SELECT COUNT(*) FROM gold_table"
).fetchone()[0]

con.execute(
    "COPY gold_table TO ? (FORMAT PARQUET, COMPRESSION ZSTD)",
    [str(GOLD / "dim_date.parquet")]
)

report["tables"].append({
    "table_name": "dim_date",
    "row_count": count,
    "validation": "PASS",
    "output_file": str(GOLD / "dim_date.parquet")
})

# Save report
with open(GOLD / "gold_report.json", "w") as f:
    json.dump(report, f, indent=4)

con.close()

print("\n" + "=" * 60)
print("GOLD LAYER COMPLETED SUCCESSFULLY")
print(f"Tables created: {len(report['tables'])}")
print("=" * 60)