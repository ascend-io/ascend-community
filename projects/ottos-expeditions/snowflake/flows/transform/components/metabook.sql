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
