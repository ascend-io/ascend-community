SELECT
    ascender_id,
    total_purchases,
    total_spent,
    CASE
        WHEN total_purchases = 1 THEN 'One-time'
        WHEN total_purchases = 2 THEN 'Returning'
        WHEN total_purchases BETWEEN 3 AND 5 THEN 'Repeating'
        WHEN total_purchases > 5 THEN 'Recurring'
        ELSE 'Unknown'
    END as customer_segment
FROM (
    SELECT
        ascender_id::STRING as ascender_id,
        COUNT(*) as total_purchases,
        SUM(price) as total_spent
    FROM {{ ref("sales") }}
    WHERE ascender_id IS NOT NULL
    GROUP BY ascender_id
)
ORDER BY
    CASE customer_segment
        WHEN 'Recurring' THEN 1
        WHEN 'Repeating' THEN 2
        WHEN 'Returning' THEN 3
        WHEN 'One-time' THEN 4
        ELSE 5
    END,
    total_spent DESC