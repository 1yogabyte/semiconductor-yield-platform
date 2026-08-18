{% macro get_prefixed_columns(relation, prefix) %}
  {% set columns = [] %}
  {% for col in adapter.get_columns_in_relation(relation) %}
    {% if col.name.startswith(prefix) %}
      {% do columns.append(col.name) %}
    {% endif %}
  {% endfor %}
  {{ return(columns) }}
{% endmacro %}
