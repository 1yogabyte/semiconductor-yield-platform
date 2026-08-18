{{ config(materialized='table') }}

{% set sensor_relation = source('bronze', 'raw_sensors') %}
{% set keep_cols = get_low_missingness_sensors(sensor_relation, 0.2) %}

with sensors as (

    select
        row_id,
        {% for col in keep_cols %}
        coalesce("{{ col }}", median("{{ col }}") over ()) as sensor_{{ col }}{{ "," if not loop.last }}
        {% endfor %}
    from {{ sensor_relation }}

),

labels as (

    select
        row_id,
        "0" as label,
        strptime("1", '%d/%m/%Y %H:%M:%S') as timestamp
    from {{ source('bronze', 'raw_labels') }}

)

select
    sensors.* exclude (row_id),
    labels.label,
    labels.timestamp
from sensors
inner join labels using (row_id)
