SELECT TOP {{threshold_promoters}} *
FROM {{ ref(input_name) }}
ORDER BY {{random_func}}
