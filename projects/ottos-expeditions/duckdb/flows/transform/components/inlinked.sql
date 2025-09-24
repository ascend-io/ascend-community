WITH inlinked AS (
    SELECT
        *
    FROM
        {{ ref("read_inlinked", flow="extract-load") }}
)
SELECT
    *
FROM
    inlinked
ORDER BY
    timestamp DESC

{{ with_test("not_null", column="timestamp", severity="error") }}
{{ with_test("count_greater_than_or_equal", count=0, severity="error") }}
