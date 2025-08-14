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
    'TIMESTAMP' DESC
