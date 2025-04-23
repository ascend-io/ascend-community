SELECT
    *
FROM
    {{ ref("ascenders") }}
WHERE
    id IN (
        SELECT
            "1" as id
    )
