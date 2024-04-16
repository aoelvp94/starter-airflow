"""Simple ELT DAG by using Airbyte and DBT."""
from datetime import datetime
import os

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor

from cosmos import DbtTaskGroup, ExecutionConfig, ProjectConfig, ProfileConfig, RenderConfig
from cosmos.constants import TestBehavior

AIRBYTE_CONN_ID = os.environ["AIRBYTE_CONNECTION_ID"]
DBT_PROJECT_PATH = os.environ["DBT_PROJECT_DIR"]
PROFILE_CONFIG = ProfileConfig(
    profile_name="dbt_project",
    target_name="dev",
    profiles_yml_filepath=os.environ["DBT_PROFILE_DIR"],
)
EXECUTION_CONFIG = ExecutionConfig(
    dbt_executable_path=DBT_PROJECT_PATH,
)

with DAG(
    "elt_dag",
    start_date=datetime(2020, 12, 23),
    description=__doc__,
    schedule=None,
    catchup=False,
) as dag:
    pre_elt_workflow = EmptyOperator(task_id="pre_elt_workflow")

    airbyte_sync_task = AirbyteTriggerSyncOperator(
        task_id="airbyte_sync",
        connection_id=AIRBYTE_CONN_ID,
        airbyte_conn_id="airbyte_conn",
        timeout=3600,
        wait_seconds=3,
        asynchronous=True,
    )

    airbyte_sensor_task = AirbyteJobSensor(
        task_id="airbyte_sensor",
        airbyte_conn_id="airbyte_conn",
        airbyte_job_id=airbyte_sync_task.output,
    )

    transform_data = DbtTaskGroup(
        render_config=RenderConfig(
            test_behavior=TestBehavior.AFTER_ALL,
            select=["path:tests", "path:models", "path:seeds"],
        ),
        group_id="transform_data",
        project_config=ProjectConfig(DBT_PROJECT_PATH),
        profile_config=PROFILE_CONFIG,
        execution_config=EXECUTION_CONFIG,
        operator_args={"install_deps": True, "append_env": True},
        default_args={"retries": 1},
    )

    post_elt_workflow = EmptyOperator(task_id="post_elt_workflow")

    pre_elt_workflow >> airbyte_sync_task >> airbyte_sensor_task >> transform_data >> post_elt_workflow
