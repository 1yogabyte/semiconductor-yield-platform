{{ config(materialized='table') }}

select
    strftime(timestamp, '%Y-%m') as month,
    100.0 * avg(case when label = -1 then 1 else 0 end) as yield_rate_pct
from {{ ref('stg_silver') }}
group by 1
order by 1
