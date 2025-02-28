from pendulum import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from cosmos import DbtTaskGroup, RenderConfig
from cosmos.config import ProfileConfig, ProjectConfig, ExecutionConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping
from pathlib import Path
import os

# Failure callback function
def on_failure_callback(context, SVC_NAME):
    svc = SVC_NAME
    task = context.get("task_instance").task_id
    dag = context.get("task_instance").dag_id
    ti = context.get("task_instance")
    exec_date = context.get("execution_date")
    dag_run = context.get('dag_run')
    log_url = context.get("task_instance").log_url
    msg = f"""
            SVC: {svc}
            Dag: {dag}
            Task: {task}
            DagRun: {dag_run}
            TaskInstance: {ti}
            Log Url: {log_url}
            Execution Time: {exec_date}
            """
    print(msg)

# Profile configuration for dbt
profile_config = ProfileConfig(
    profile_name="ai_lab",
    target_name="dev",
    profiles_yml_filepath="/appz/home/airflow/dags/dbt/agent_dags/dbt/webshop/profiles.yml",
)

# Function to print Airflow variable
def print_variable(**kwargs):
    variable = kwargs['dag_run'].conf.get('payment_type')
    print(variable)

# Load README file for DAG documentation
readme_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'README.md')
with open(readme_path, 'r') as file:
    readme_content = file.read()

# Define the DAG
with DAG(
    dag_id="dbt_webshop",
    start_date=datetime(2024, 2, 27),
    schedule='30 23 * * *',  # Runs every day at 5 AM IST (UTC+5:30)
    tags=["dbt-webshop"],
    doc_md=readme_content,
    default_args={"owner": "airflow"},
    catchup=False,
):
    # Print Variables Task
    e1 = PythonOperator(
        task_id="print_variables",
        python_callable=print_variable,
        provide_context=True,
    )

    # dbt Seed Task Group (with full refresh)
    dbt_seed_tg = DbtTaskGroup(
        project_config=ProjectConfig(Path("/appz/home/airflow/dags/dbt/agent_dags/dbt/webshop")),
        operator_args={"append_env": True},
        profile_config=profile_config,
        execution_config=ExecutionConfig(
            dbt_executable_path="/dbt_venv/bin/dbt",
            dbt_args=["--full-refresh"]  # Full refresh enabled
        ),
        render_config=RenderConfig(select=["path:seeds/"]),
        default_args={"retries": 2},
        group_id="dbt_seed_group"
    )

    # dbt Run Task Group (Excludes Seeds)
    dbt_run_tg = DbtTaskGroup(
        project_config=ProjectConfig(Path("/appz/home/airflow/dags/dbt/agent_dags/dbt/webshop")),
        operator_args={"append_env": True},
        profile_config=profile_config,
        execution_config=ExecutionConfig(dbt_executable_path="/dbt_venv/bin/dbt"),
        render_config=RenderConfig(exclude=["path:seeds/"]),
        default_args={
            "retries": 1,
            'on_failure_callback': lambda context: on_failure_callback(context, "WEBSHOP_SVC_NAME"),
        },
        group_id="dbt_run_group"
    )
    
    # Empty Operator for Post-Processing
    e2 = EmptyOperator(task_id="post_dbt")
    
    # DAG Task Dependencies
    e1 >> dbt_seed_tg >> dbt_run_tg >> e2
