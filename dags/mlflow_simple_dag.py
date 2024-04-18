"""ETFL for artists data"""

import logging
from datetime import timedelta

import mlflow
import pandas as pd
import numpy as np
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from airflow.utils.dates import days_ago

from sklearn import datasets

from train import fit_model

@dag(
    "ETFL_dag_v3",
    default_args={
    "owner": "Restack",
    "depends_on_past": False,
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    },
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=["ETFL"],
)
def taskflow_api_etl():

    @task
    def get_data_task():
        # Load Diabetes datasets
        diabetes = datasets.load_diabetes()
        X = diabetes.data
        y = diabetes.target

        # Create pandas DataFrame for sklearn ElasticNet linear_model
        Y = np.array([y]).transpose()
        d = np.concatenate((X, Y), axis=1)
        cols = diabetes.feature_names + ["progression"]
        data = pd.DataFrame(d, columns=cols)
        return data.to_json()


    @task
    def fit_model_task(df_to_train, alpha, l1_ratio):
        context = get_current_context()
        mlflow.set_tracking_uri("{{ var.value.get('MLFLOW_TRACKING_URI', 'localhost') }}")
        mlflow.set_experiment("elasticnet_diabetes")
        with mlflow.start_run(run_name=f"elasticnet_{context['execution_date']}"):
            fit_model(df_to_train, alpha, l1_ratio)
            
    
    result = get_data_task()
    [fit_model_task(result, 1, 2), fit_model_task(result, 0.5, 4), fit_model_task(result, 2, 1)]


taskflow_api_etl_dag = taskflow_api_etl()
