"""Simple sync DAG by using Airbyte."""
from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor


AIRBYTE_CONN_ID = os.environ["AIRBYTE_CONNECTION_ID"]

with DAG(
    "airbyte_basic_dag",
    start_date=datetime(2020, 12, 23),
    description=__doc__,
    schedule=None,
    catchup=False,
) as dag:
    pre_airbyte_workflow = EmptyOperator(task_id="pre_airbyte_workflow")

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

    post_airbyte_workflow = EmptyOperator(task_id="post_airbyte_workflow")

    pre_airbyte_workflow >> airbyte_sync_task >> airbyte_sensor_task >> post_airbyte_workflow
