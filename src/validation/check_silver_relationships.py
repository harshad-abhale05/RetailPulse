import duckdb

con = duckdb.connect()

BASE = "data/processed/silver"

checks = [
    (
        "Orders -> Customers",
        f"""
        SELECT COUNT(*)
        FROM read_parquet('{BASE}/orders.parquet') o
        LEFT JOIN read_parquet('{BASE}/customers.parquet') c
        ON o.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
        """
    ),
    (
        "Order Items -> Orders",
        f"""
        SELECT COUNT(*)
        FROM read_parquet('{BASE}/order_items.parquet') i
        LEFT JOIN read_parquet('{BASE}/orders.parquet') o
        ON i.order_id = o.order_id
        WHERE o.order_id IS NULL
        """
    ),
    (
        "Order Items -> Products",
        f"""
        SELECT COUNT(*)
        FROM read_parquet('{BASE}/order_items.parquet') i
        LEFT JOIN read_parquet('{BASE}/products.parquet') p
        ON i.product_id = p.product_id
        WHERE p.product_id IS NULL
        """
    ),
    (
        "Order Items -> Sellers",
        f"""
        SELECT COUNT(*)
        FROM read_parquet('{BASE}/order_items.parquet') i
        LEFT JOIN read_parquet('{BASE}/sellers.parquet') s
        ON i.seller_id = s.seller_id
        WHERE s.seller_id IS NULL
        """
    ),
    (
        "Payments -> Orders",
        f"""
        SELECT COUNT(*)
        FROM read_parquet('{BASE}/payments.parquet') p
        LEFT JOIN read_parquet('{BASE}/orders.parquet') o
        ON p.order_id = o.order_id
        WHERE o.order_id IS NULL
        """
    ),
    (
        "Reviews -> Orders",
        f"""
        SELECT COUNT(*)
        FROM read_parquet('{BASE}/reviews.parquet') r
        LEFT JOIN read_parquet('{BASE}/orders.parquet') o
        ON r.order_id = o.order_id
        WHERE o.order_id IS NULL
        """
    ),
    (
        "Customers -> Geolocation",
        f"""
        SELECT COUNT(DISTINCT c.customer_zip_code_prefix)
        FROM read_parquet('{BASE}/customers.parquet') c
        LEFT JOIN read_parquet('{BASE}/geolocation_by_zip.parquet') g
        ON c.customer_zip_code_prefix = g.geolocation_zip_code_prefix
        WHERE g.geolocation_zip_code_prefix IS NULL
        """
    ),
    (
        "Sellers -> Geolocation",
        f"""
        SELECT COUNT(DISTINCT s.seller_zip_code_prefix)
        FROM read_parquet('{BASE}/sellers.parquet') s
        LEFT JOIN read_parquet('{BASE}/geolocation_by_zip.parquet') g
        ON s.seller_zip_code_prefix = g.geolocation_zip_code_prefix
        WHERE g.geolocation_zip_code_prefix IS NULL
        """
    )
]

print("=" * 60)
print("RETAILPULSE - SILVER RELATIONSHIP VALIDATION")
print("=" * 60)

for name, query in checks:
    failures = con.execute(query).fetchone()[0]

    if failures == 0:
        status = "PASS"
    elif "Geolocation" in name:
        status = "REVIEW"
    else:
        status = "FAIL"

    print(f"\n{name}")
    print(f"Unmatched records/prefixes: {failures:,}")
    print(f"Status: {status}")

    if status == "FAIL":
        raise ValueError(f"Relationship validation failed: {name}")

print("\nVALIDATION COMPLETED")
con.close()