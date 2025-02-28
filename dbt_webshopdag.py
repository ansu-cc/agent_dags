from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 28),
    'retries': 1,
}

dbt_project_dir = "/appz/home/airflow/dags/webshop_dags/dbt/webshop"

dbt_seed_commands = [
    "address", "articles", "colors", "customer", "labels", 
    "order_positions", "order_seed", "products", "stock"
]

dbt_run_commands = ["order"]

with DAG(
    'dbt_workflow',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
) as dag:

    with TaskGroup("dbt_seed") as dbt_seed_group:
        for seed in dbt_seed_commands:
            BashOperator(
                task_id=f"dbt_seed_{seed}",
                bash_command=f"cd {dbt_project_dir} && dbt seed --select {seed}"
            )
    
    with TaskGroup("dbt_run") as dbt_run_group:
        for run in dbt_run_commands:
            BashOperator(
                task_id=f"dbt_run_{run}",
                bash_command=f"cd {dbt_project_dir} && dbt run --select {run}"
            )

    dbt_seed_group >> dbt_run_group
#testing
