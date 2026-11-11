SELECT
    i.seller_id,
    s.seller_city,
    s.seller_state,
    ROUND(SUM(i.price), 2) AS revenue,
    COUNT(*) AS items_sold
FROM read_parquet('data/processed/gold/fact_order_items.parquet') i
JOIN read_parquet('data/processed/gold/dim_sellers.parquet') s
    ON i.seller_id = s.seller_id
GROUP BY 1, 2, 3
ORDER BY revenue DESC
LIMIT 10;
