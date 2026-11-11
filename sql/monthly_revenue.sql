SELECT
    EXTRACT(YEAR FROM o.order_purchase_timestamp) AS year,
    EXTRACT(MONTH FROM o.order_purchase_timestamp) AS month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(i.total_item_value), 2) AS revenue
FROM read_parquet('data/processed/gold/fact_orders.parquet') o
JOIN read_parquet('data/processed/gold/fact_order_items.parquet') i
    ON o.order_id = i.order_id
WHERE o.order_status = 'delivered'
GROUP BY 1, 2
ORDER BY 1, 2;
