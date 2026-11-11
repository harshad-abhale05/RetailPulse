SELECT
    review_score,
    COUNT(*) AS total_reviews,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(),
        2
    ) AS percentage
FROM read_parquet('data/processed/gold/fact_reviews.parquet')
GROUP BY review_score
ORDER BY review_score;
