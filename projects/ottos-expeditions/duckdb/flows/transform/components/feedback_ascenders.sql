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
ORDER BY
    timestamp DESC

{{ with_test("not_null", column="timestamp", severity="error") }}
{{ with_test("count_greater_than_or_equal", count=0, severity="error") }}
