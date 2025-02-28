from pendulum import datetime
from datetime import timedelta  # ✅ Correct import for timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from cosmos import DbtTaskGroup, RenderConfig
from cosmos.config import ProfileConfig, ProjectConfig, ExecutionConfig
import os
from pathlib import Path

# Manually set the correct DBT path
DBT_EXECUTABLE = "/dbt_venv/bin/dbt"

# Set DBT project path
DBT_PROJECT_PATH = Path("/appz/home/airflow/dags/dbt/agent_dags/dbt/webshop")

# Custom failure callback for logging
def log_task_failure(context):
    task_id = context.get("task_instance").task_id
    dag_id = context.get("task_instance").dag_id
    log_url = context.get("task_instance").log_url
    exec_date = context.get("execution_date")

    error_message = f"""
        ❌ DAG `{dag_id}` Task `{task_id}` Failed!
        🔗 Logs: {log_url}
        📅 Execution Date: {exec_date}
    """
    print(error_message)

# Airflow Profile Config
profile_config = ProfileConfig(
    profile_name="ai_lab",
    target_name="dev",
    profiles_yml_filepath=str(DBT_PROJECT_PATH / "profiles.yml"),
)

# Print Airflow Variables (Debugging)
def print_variable(**kwargs):
    variable = kwargs.get('dag_run').conf.get('payment_type', 'No Payment Type Provided')
    print(f"Received Payment Type: {variable}")

# DAG Definition
with DAG(
    dag_id="dbt_webshop",
    start_date=datetime(2024, 2, 27),
    schedule='30 15 * * *',  
    catchup=False,
    default_args={
        "owner": "airflow",
        "retries": 3,
        "retry_delay": timedelta(minutes=5),  # ✅ Fixed timedelta import
        "on_failure_callback": log_task_failure,
    },
):
    e1 = PythonOperator(
        task_id="print_variables",
        python_callable=print_variable,
        provide_context=True,
    )

    # DBT Seed Task Group
    dbt_seed_tg = DbtTaskGroup(
        project_config=ProjectConfig(DBT_PROJECT_PATH),
        execution_config=ExecutionConfig(dbt_executable_path=DBT_EXECUTABLE),
        profile_config=profile_config,
        render_config=RenderConfig(select=["path:seeds/"]),
        default_args={"retries": 2},
        group_id="dbt_seed_group"
    )

    # DBT Run Task Group
    dbt_run_tg = DbtTaskGroup(
        project_config=ProjectConfig(DBT_PROJECT_PATH),
        execution_config=ExecutionConfig(dbt_executable_path=DBT_EXECUTABLE),
        profile_config=profile_config,
        render_config=RenderConfig(exclude=["path:seeds/"]),
        default_args={"retries": 2, "on_failure_callback": log_task_failure},
        group_id="dbt_run_group"
    )

    e2 = EmptyOperator(task_id="post_dbt")

    # Task Flow
    e1 >> dbt_seed_tg >> dbt_run_tg >> e2
