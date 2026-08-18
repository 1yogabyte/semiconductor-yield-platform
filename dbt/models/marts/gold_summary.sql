{{ config(materialized='table') }}

select
    count(*) as total_units,
    sum(case when label = -1 then 1 else 0 end) as total_pass,
    sum(case when label = 1 then 1 else 0 end) as total_fail,
    100.0 * avg(case when label = -1 then 1 else 0 end) as yield_rate_pct,
    min(timestamp) as date_start,
    max(timestamp) as date_end,
    {{ get_prefixed_columns(ref('stg_silver'), 'sensor_') | length }} as n_sensors
from {{ ref('stg_silver') }}
