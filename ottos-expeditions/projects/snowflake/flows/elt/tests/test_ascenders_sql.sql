SELECT
    *
FROM
    {{ ref("ascenders") }}
WHERE
    ID IN (
        SELECT
            '"1"' as ID
    )
