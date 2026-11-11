SELECT
    COALESCE(p.product_category_name_english, 'Unknown') AS category,
    COUNT(*) AS units_sold,
    ROUND(SUM(i.price), 2) AS product_revenue
FROM read_parquet('data/processed/gold/fact_order_items.parquet') i
JOIN read_parquet('data/processed/gold/dim_products.parquet') p
    ON i.product_id = p.product_id
GROUP BY 1
ORDER BY units_sold DESC
LIMIT 10;
