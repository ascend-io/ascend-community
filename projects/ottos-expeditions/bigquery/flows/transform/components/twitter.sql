WITH twitter AS (
    SELECT
        *
    FROM
        {{ ref("read_twitter", flow="extract-load", reshape="map") }}
)
SELECT
    *
FROM
    twitter
ORDER BY
    timestamp DESC

{{ with_test("not_null", column="timestamp") }}

