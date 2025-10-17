SELECT *
FROM {{ ref(input_name) }}
ORDER BY {{random_func}}
LIMIT {{threshold_promoters}}