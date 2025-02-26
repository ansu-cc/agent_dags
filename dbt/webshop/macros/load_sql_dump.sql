{% macro load_sql_dump(file_path) %}
    {% set sql_content = read_file(file_path) %}
    {% do run_query(sql_content) %}
{% endmacro %}
