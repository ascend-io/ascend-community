SELECT TOP {{threshold_neutral}} *
FROM {{ ref(input_name) }}
ORDER BY {{random_func}}
