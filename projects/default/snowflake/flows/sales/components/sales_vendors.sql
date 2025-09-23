SELECT
    id,
    price,
    quantity,
    route_id,
    tax,
    timestamp,
    vendor_id,
    '0' AS store_id,
    NULL AS ascender_id
FROM {{ ref('read_sales_vendors') }}

{{ with_test("not_null", column="id") }}
{{ with_test("not_null", column="timestamp") }}
{{ with_test("count_greater_than", count=0) }}