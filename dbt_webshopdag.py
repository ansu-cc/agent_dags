from pendulum import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from cosmos import DbtTaskGroup, RenderConfig
from cosmos.config import ProfileConfig, ProjectConfig, ExecutionConfig
from pathlib import Path

# Airflow Profile Configuration for dbt
profile_config = ProfileConfig(
    profile_name="ai_lab",
    target_name="dev",
    profiles_yml_filepath="/appz/home/airflow/dags/dbt/webshop/profiles.yml",
)

# Define DAG
with DAG(
    dag_id="webshop_dbt_daily",
    start_date=datetime(2024, 2, 28),
    schedule='0 6 * * *',  # Runs every morning at 6 AM
    tags=["dbt", "webshop", "daily_run"],
    default_args={"owner": "airflow", "retries": 2},
    catchup=False,
):
    start = EmptyOperator(task_id="start")

    # Step 1: Run dbt seed to load data
    dbt_seed_tg = DbtTaskGroup(
        project_config=ProjectConfig(Path("/appz/home/airflow/dags/dbt/webshop")),
        operator_args={"append_env": True},
        profile_config=profile_config,
        execution_config=ExecutionConfig(dbt_executable_path="/dbt_venv/bin/dbt"),
        render_config=RenderConfig(select=["seeds"]),  # Equivalent to `dbt seed`
        group_id="dbt_seed",
    )

    # Step 2: Run dbt models (Update Order Timestamp)
    dbt_run_tg = DbtTaskGroup(
        project_config=ProjectConfig(Path("/appz/home/airflow/dags/dbt/webshop")),
        operator_args={"append_env": True},
        profile_config=profile_config,
        execution_config=ExecutionConfig(dbt_executable_path="/dbt_venv/bin/dbt"),
        render_config=RenderConfig(select=["models"]),  # Equivalent to `dbt run`
        group_id="dbt_run",
    )

    end = EmptyOperator(task_id="end")

    # Task flow: dbt seed -> dbt run
    start >> dbt_seed_tg >> dbt_run_tg >> end






