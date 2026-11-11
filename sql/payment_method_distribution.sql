SELECT
    payment_type,
    COUNT(*) AS transactions,
    ROUND(SUM(payment_value), 2) AS total_payment
FROM read_parquet('data/processed/gold/fact_payments.parquet')
GROUP BY payment_type
ORDER BY total_payment DESC;
