{% from 'macros/utils.sql' import col %}

WITH feedback_stores AS (
    SELECT
        *
    FROM
        {{ ref("read_feedback_stores", flow="extract-load") }}
)
SELECT
    {{ col('*') }}
FROM
    feedback_stores
ORDER BY
    timestamp DESC

{{ with_test("not_null", column="timestamp", severity="error") }}
{{ with_test("count_greater_than_or_equal", count=0, severity="error") }}
