WITH metagram AS (
    SELECT
        *
    FROM
        {{ ref("read_metagram", flow="extract-load") }}
)
SELECT
    *
FROM
    metagram
ORDER BY
    timestamp DESC

{{ with_test("not_null", column="timestamp", severity="error") }}
{{ with_test("count_greater_than_or_equal", count=0, severity="error") }}
