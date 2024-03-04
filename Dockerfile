ARG RESTACK_PRODUCT_VERSION=2.8.0

FROM apache/airflow:${RESTACK_PRODUCT_VERSION}

RUN mkdir -p dags && \
    mkdir -p config && \
    mkdir -p logs && \
    mkdir -p plugins

COPY --chown=airflow:root dags/ /opt/airflow/dags
COPY --chown=airflow:root config/ /opt/airflow/config
COPY --chown=airflow:root plugins/ /opt/airflow/plugins
COPY --chown=airflow:root dbt_project/ /opt/airflow/dbt_project

RUN apt update && apt install -y git

COPY requirements.txt /
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
RUN cd /opt/airflow/dbt_project && dbt deps
