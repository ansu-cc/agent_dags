WITH date_shift AS (
    -- Find the max timestamp and calculate the number of days to shift
    SELECT 
        MAX(orderTimestamp) AS max_timestamp,
        DATE_PART('day', CURRENT_DATE - MAX(orderTimestamp)) AS shift_days
    FROM {{ source('webshop_v2', 'order') }}
),
updated_orders AS (
    -- Apply the shift to all order timestamps
    SELECT 
        id,
        customerid,
        orderTimestamp + (INTERVAL '1 day' * (SELECT shift_days FROM date_shift)) AS orderTimestamp,
        shippingaddressid,
        total,
        shippingcost,
        created,
        updated
    FROM {{ source('webshop_v2', 'order') }}
)

SELECT * FROM  "order";

