-- Union the two read components and run distinct to remove duplicates
SELECT DISTINCT
    id,
    name,
    breed,
    age,
    route
FROM (
    SELECT
        id,
        name,
        breed,
        age,
        route
    FROM {{ ref('read_goats') }}
    
    UNION ALL
    
    SELECT
        id,
        name,
        breed,
        age,
        route
    FROM {{ ref('read_goats_python') }}
)

{{ with_test("count_equal", count=150) }}
{{ with_test("not_null", column="id") }}
{{ with_test("unique", column="id") }}
{{ with_test("not_null", column="name") }}
{{ with_test("not_null", column="breed") }}
{{ with_test("not_null", column="age") }}
{{ with_test("greater_than", column="age", value=0) }}
{{ with_test("not_null", column="route") }}