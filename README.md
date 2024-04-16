# Airflow Restack repository

This is the default Airflow repository to get you started for generating preview environments from a custom Airflow image with Restack github application.

### Dags
1. If you want to extend the image with custom dags, just add them to the dags directory.

### Plugins

1. If you want to extend the image with custom plugins, just add them to the plugins directory.

### Config

1. If you want to extend the image with custom configuration, just add them to the config directory.


### Restack Product Version
Restack will expose a build arg for the Dockerfile called: RESTACK_PRODUCT_VERSION. This will contain the image tag of the product. As seen on this starter repo's Dockerfile you can use it as such:
```dockerfile
ARG RESTACK_PRODUCT_VERSION=2.8.0
FROM apache/airflow:${RESTACK_PRODUCT_VERSION}
```

This way once a new version of airflow is released and you upgrade your app via Restack console,  your ci/cd builds will use the latest version to build your airflow custom image.

### Generating a preview environment

1. Make sure to fork this repository.
2. Follow steps in the [official Restack documentation](https://www.restack.io/docs/airflow-cicd)
3. Once you open a pull request a preview environment will be generated.
4. Once your pull request is merged your initial Airflow application will be provisioned with latest code from the "main" branch.


### How to config demo

First of all you need to create a stack.

#### Airbyte

1. Attach an Airbyte service to your stack and start the app.
2. Once setup is done, go to the UI and log in.
3. Create a source `Alpha Vantage API` to ingest data. Add the public API Key and the symbol to be extracted (e.g. `MSFT`)
4. Create a destination `Big Query` to write the ingested data. Fill fields like `Project ID`, `Dataset Location`, `Default Dataset ID` and choose the `Standard Inserts` method for testing the E2E pipeline. Put the SA content in `Service Account Key JSON` placeholder. 
5. Create the connection and select just `time_series_daily` stream of data.
6. Copy the connection hash id in the URL in a notepad. For example, for https://foo.bar.gcp.restack.it/workspaces/d5f2d913-16cd-44e7-8531-26b7fec1937c/connections/692a8331-2f58-4066-affe-23b71309eab3/status, `692a8331-2f58-4066-affe-23b71309eab3` is the hash code


#### Airflow
1. Attach an Airflow service to your stack.
2. Put the `Dockerfile` of your repo to build the codebase.
3. Set the following environment variables:
   1.  AIRBYTE_CONNECTION_ID: Insert here the copied code from (Airbyte-step 5).
   2.  GCP_PROJECT_ID
   3.  GCP_DATASET
   4.  GCP_DATASET_LOCATION
   5.  GCP_DBT_SERVICE_ACCOUNT: Put here your impersonate account.
4. Start the app. Once setup is done, go to Airflow UI and login.
5. Create an Airbyte connection, go to Admin -> Connections and add a new record with the following fields (port is not mandatory to set):
   1. conn_id: airbyte_conn
   2. conn_type: airbyte
   3. host: The Airbyte URL with `http://` preffix.
   4. login: Username of Airbyte service
   5. password: Password of Airbyte service
6. Turn on `elt_dag` and run the DAG. It should take the data from `Alpha Vantage API` by using an Airbyte Operator and then will run the DBT models on BigQuery by using Astronomer Cosmos.



#### Superset
1. Attach a Superset app to your stack.
2. Put the `Dockerfile` of your repo to build the codebase.
3. Let's create the connection to BQ so go to Settings -> Database Connections -> +DATABASE -> Choose BigQuery and upload your SA account.
4. Go to `Datasets` to create a dataset by selecting a table to query data on BigQuery. 
5. Once dataset created, go to `Charts` to create a chart on the dataset.
