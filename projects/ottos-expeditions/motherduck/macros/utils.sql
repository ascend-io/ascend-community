{% macro col(col) %}
    {{ col }}
{% endmacro %}

--Standardize macro to lowercase and trim data
{% macro standardize(col_name) %}
    LOWER(TRIM({{ col_name }}))
{% endmacro %}
