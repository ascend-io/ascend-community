{% from 'macros/utils.sql' import standardize %}

SELECT
    id,
    {{ standardize('name') }} AS clean_name,
    breed,
    age,
    route
FROM {{ ref('read_goats', flow='extract-load') }}
