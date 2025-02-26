{% macro load_sql_dump(file_path) %}
    {% set sql_content = open(file_path).read() %}
    {% do run_query(sql_content) %}
{% endmacro %}
