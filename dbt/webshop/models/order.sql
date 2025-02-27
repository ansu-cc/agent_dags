{{ config(
    materialized='incremental',
    unique_key='id'
) }}

WITH date_shift AS (
    SELECT
        MAX(ordertimestamp)::TIMESTAMP AS max_timestamp,  -- Ensure correct type
        DATE_PART('day', CURRENT_DATE - MAX(ordertimestamp)::DATE) AS shift_days
    FROM {{ ref('order_seed') }}  -- Use ref() for dbt-managed tables
),
shifted_orders AS (
    SELECT
        id,
        customerid,
        ordertimestamp + (INTERVAL '1 day' * date_shift.shift_days) AS ordertimestamp,
        shippingaddressid,
        total,
        shippingcost,
        created,
        updated
    FROM {{ ref('order_seed') }}, date_shift
)

-- Ensure proper WHERE condition for incremental models
SELECT * FROM shifted_orders
{% if is_incremental() %}
WHERE ordertimestamp > (SELECT MAX(ordertimestamp) FROM {{ this }})
{% endif %};

