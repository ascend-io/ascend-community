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
    "TIMESTAMP" DESC

-- Data quality tests
{{ with_test("not_null", column="ID", severity="error") }}
{{ with_test("not_null", column="TIMESTAMP", severity="error") }}
{{ with_test("count_greater_than", count=0, severity="error") }}
{{ with_test("in_set", column="FEEDBACK", values=["negative", "neutral", "positive"], severity="warn") }}
{{ with_test("not_empty", column="FEEDBACK_CONTENT", severity="warn") }}
