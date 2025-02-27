-- {{ config(
--     materialized='table',
--     alias='updated_order'
-- ) }}

-- WITH date_shift AS (
--     SELECT 
--         MAX(orderTimestamp) AS max_timestamp,
--         DATE_PART('day', CURRENT_DATE - MAX(orderTimestamp)) AS shift_days
--     FROM {{ source('webshop_v2', 'updated_order') }}
-- ),
-- shifted_orders AS (
--     SELECT 
--         id,
--         customerid,
--         orderTimestamp + (INTERVAL '1 day' * date_shift.shift_days) AS orderTimestamp,
--         shippingaddressid,
--         total,
--         shippingcost,
--         created,
--         updated
--     FROM {{ source('webshop_v2', 'updated_order') }}, date_shift
-- )

-- SELECT * FROM shifted_orders

{{ config(
    materialized:'incremental',
    unique_key:'id'
) }}

SELECT
    id,
    customerid,
    ordertimestamp + (CURRENT_DATE - MAX(ordertimestamp) OVER()) AS ordertimestamp,
    shippingaddressid,
    total,
    shippingcost,
    created,
    updated
FROM webshop_v2.updated_order

{% if is_incremental() %}
WHERE ordertimestamp > (SELECT MAX(ordertimestamp) FROM {{ this }})
{% endif %}
