{% macro get_low_missingness_sensors(relation, threshold=0.2, exclude=['row_id']) %}

  {% set columns = [] %}
  {% for col in adapter.get_columns_in_relation(relation) %}
    {% if col.name not in exclude %}
      {% do columns.append(col) %}
    {% endif %}
  {% endfor %}

  {% set null_pct_selects = [] %}
  {% for col in columns %}
    {% do null_pct_selects.append(
        "SUM(CASE WHEN " ~ col.quoted ~ " IS NULL THEN 1 ELSE 0 END)::FLOAT / COUNT(*) AS " ~ col.quoted
    ) %}
  {% endfor %}

  {% set null_pct_query %}
    SELECT {{ null_pct_selects | join(', ') }}
    FROM {{ relation }}
  {% endset %}

  {% set keep_columns = [] %}
  {% if execute %}
    {% set results = run_query(null_pct_query) %}
    {% set row = results.rows[0] %}
    {% for col in columns %}
      {% if row[col.name] < threshold %}
        {% do keep_columns.append(col.name) %}
      {% endif %}
    {% endfor %}
  {% endif %}

  {{ return(keep_columns) }}

{% endmacro %}
