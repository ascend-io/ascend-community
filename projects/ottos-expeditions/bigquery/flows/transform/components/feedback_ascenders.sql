WITH feedback_ascenders AS (
    SELECT
        *
    FROM
        {{ ref("read_feedback_ascenders", flow="extract-load") }}
)
SELECT
    *
FROM
    feedback_ascenders

{{ with_test("count_greater_than_or_equal", count=0) }}
ORDER BY
    timestamp DESC
