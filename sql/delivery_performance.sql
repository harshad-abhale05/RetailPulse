SELECT
    order_status,
    COUNT(*) AS total_orders,
    ROUND(
        AVG(
            DATE_DIFF(
                'day',
                CAST(order_purchase_timestamp AS DATE),
                CAST(order_delivered_customer_date AS DATE)
            )
        ),
        2
    ) AS average_delivery_days
FROM read_parquet('data/processed/gold/fact_orders.parquet')
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
GROUP BY order_status;
