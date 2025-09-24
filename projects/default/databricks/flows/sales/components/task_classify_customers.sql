{{
  config(
    type="task",
    dependencies=[
      ref("sales"),
    ]
  )
}}

WITH combined_sales AS (
  -- Use the unified sales table which already has ascender_id properly handled
  SELECT 
    ascender_id::STRING as ascender_id,
    timestamp,
    price
  FROM {{ ref("sales") }}
  WHERE ascender_id IS NOT NULL
),

customer_purchase_stats AS (
  -- Calculate purchase statistics per customer
  SELECT 
    ascender_id,
    COUNT(*) as total_purchases,
    MIN(timestamp) as first_purchase_date,
    MAX(timestamp) as last_purchase_date,
    SUM(price) as total_spent,
    AVG(price) as avg_order_value,
    -- Calculate days between first and last purchase
    DATEDIFF(DAY, MIN(timestamp), MAX(timestamp)) as customer_lifespan_days,
    -- Calculate average days between purchases
    CASE 
      WHEN COUNT(*) > 1 THEN 
        DATEDIFF(DAY, MIN(timestamp), MAX(timestamp)) / NULLIF(COUNT(*) - 1, 0)
      ELSE NULL 
    END as avg_days_between_purchases
  FROM combined_sales
  GROUP BY ascender_id
),

customer_segmentation AS (
  SELECT 
    ascender_id,
    total_purchases,
    first_purchase_date,
    last_purchase_date,
    total_spent,
    avg_order_value,
    customer_lifespan_days,
    avg_days_between_purchases,
    -- Categorize customers based on purchase behavior
    CASE 
      WHEN total_purchases = 1 THEN 'One-time'
      WHEN total_purchases = 2 THEN 'Returning'
      WHEN total_purchases BETWEEN 3 AND 5 THEN 'Repeating'
      WHEN total_purchases > 5 AND avg_days_between_purchases <= 30 THEN 'Recurring'
      WHEN total_purchases > 5 AND avg_days_between_purchases > 30 THEN 'Repeating'
      ELSE 'Unknown'
    END as customer_segment,
    -- Additional insights
    CASE 
      WHEN customer_lifespan_days <= 30 THEN 'New (0-30 days)'
      WHEN customer_lifespan_days <= 90 THEN 'Recent (31-90 days)'
      WHEN customer_lifespan_days <= 365 THEN 'Established (3-12 months)'
      ELSE 'Long-term (1+ years)'
    END as customer_age_segment,
    -- Calculate customer value tier
    CASE 
      WHEN total_spent >= 1000 THEN 'High'
      WHEN total_spent >= 500 THEN 'Medium'
      WHEN total_spent >= 100 THEN 'Low'
      ELSE 'Minimal Value'
    END as value_tier
  FROM customer_purchase_stats
)

SELECT 
  ascender_id,
  customer_segment,
  customer_age_segment,
  value_tier,
  total_purchases,
  total_spent,
  avg_order_value,
  customer_lifespan_days,
  avg_days_between_purchases,
  first_purchase_date,
  last_purchase_date
FROM customer_segmentation
ORDER BY 
  CASE customer_segment 
    WHEN 'Recurring' THEN 1
    WHEN 'Repeating' THEN 2  
    WHEN 'Returning' THEN 3
    WHEN 'One-time' THEN 4
    ELSE 5
  END,
  total_spent DESC
