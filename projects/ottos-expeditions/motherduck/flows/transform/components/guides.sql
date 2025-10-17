WITH guides AS (
    SELECT
        *
    FROM
        {{ ref("read_guides", flow="extract-load") }}
)
SELECT
    *
FROM
    guides

{{ with_test("count_greater_than_or_equal", count=0) }}
