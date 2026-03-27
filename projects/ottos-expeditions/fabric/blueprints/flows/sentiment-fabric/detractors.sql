SELECT TOP {{threshold_detractors}} *
FROM {{ ref(input_name) }}
ORDER BY {{random_func}}
