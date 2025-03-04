WITH route_closures AS (
    SELECT
        *
    FROM
        {{ ref('route_closures' }}
)
SELECT
    *,
    SNOWFLAKE.CORTEX.TRANSLATE(REASON, 'en', 'es') as TRANSLATED
FROM
    route_closures
LIMIT 10

{{ with_test("not_null", column="TRANSLATED") }}
