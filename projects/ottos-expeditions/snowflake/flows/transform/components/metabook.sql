WITH metabook AS (
    SELECT
        *
    FROM
        {{ ref("read_metabook", flow="extract-load") }}
)
SELECT
    *
FROM
    metabook
ORDER BY
    'TIMESTAMP' DESC

{{ with_test("not_null", column="timestamp", severity="error") }}
{{ with_test("count_greater_than_or_equal", count=0, severity="error") }}
