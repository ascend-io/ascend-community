WITH feedback_website AS (
    SELECT
        *
    FROM
        {{ ref(
            "read_feedback_website",
            flow="extract-load",
            reshape={
                "time": {
                    "column": "timestamp",
                    "granularity": "month"
                }
            }
        ) }}
)
SELECT
    *
FROM
    feedback_website
ORDER BY
    'TIMESTAMP' DESC

{{ with_test("not_null", column="timestamp", severity="error") }}
{{ with_test("count_greater_than_or_equal", count=0, severity="error") }}
