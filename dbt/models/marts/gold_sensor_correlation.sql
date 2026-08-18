{{ config(materialized='table') }}

{% set silver = ref('stg_silver') %}
{% set sensor_cols = get_prefixed_columns(silver, 'sensor_') %}

with stats as (

    select
        {% for col in sensor_cols %}
        avg(case when label = -1 then {{ col }} end) as {{ col }}_pass,
        avg(case when label = 1 then {{ col }} end) as {{ col }}_fail{{ "," if not loop.last }}
        {% endfor %}
    from {{ silver }}

),

unpivoted as (
    {% for col in sensor_cols %}
    select '{{ col }}' as sensor, abs({{ col }}_pass - {{ col }}_fail) as mean_difference from stats
    {{ "union all" if not loop.last }}
    {% endfor %}
)

select sensor, mean_difference
from unpivoted
order by mean_difference desc
limit 20
