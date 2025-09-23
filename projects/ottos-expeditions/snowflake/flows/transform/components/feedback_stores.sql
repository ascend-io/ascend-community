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
    "TIMESTAMP" DESC

-- Data quality tests
{{ with_test("not_null", column="ID", severity="error") }}
{{ with_test("unique", column="ID", severity="warn") }}
{{ with_test("not_null", column="TIMESTAMP", severity="error") }}
{{ with_test("count_greater_than", count=0, severity="error") }}
{{ with_test("not_empty", column="FEEDBACK_CONTENT", severity="warn") }}
