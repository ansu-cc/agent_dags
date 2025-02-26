from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

# DAG default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 2, 26),
    'retries': 1
}

dag = DAG(
    'load_order_to_tst_webshop',
    default_args=default_args,
    schedule_interval=None,  # Run manually or set a schedule
    catchup=False
)

# Step 1: Create the new database 'tst_webshop'
create_tst_webshop_db = PostgresOperator(
    task_id='create_tst_webshop_db',
    postgres_conn_id='postgres_default',
    sql="CREATE DATABASE tst_webshop;",
    dag=dag
)

# Step 2: Load order.sql into the new database
load_order_sql = BashOperator(
    task_id='load_order_sql',
    bash_command="psql -d tst_webshop -U postgres -f /appz/home/airflow/dags/airflow_dags/dbt/webshop/models/order.sql",
    dag=dag
)

# Define task dependencies
create_tst_webshop_db >> load_order_sql
