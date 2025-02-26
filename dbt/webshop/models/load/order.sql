{{ config(
    materialized='table',
    schema='webshop',
    pre_hook="{{ load_sql_dump('scripts/order.sql') }}"
) }}

SELECT * FROM webshop."order";
