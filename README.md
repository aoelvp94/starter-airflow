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

### How to run the demo
First of all you should create a stack.

#### MLflow
1. Just start the application and attach it to the stack.
2. Start the service.
3. Once the service up, copy the URL for Airflow Variable creation.

#### Airflow
1. Just start the application and attach it to the stack.
2. Run the service selecting the Dockerfile of the repo (and branch) where you are working on.
3. Start the service.
4. Once the service up, go to Airflow UI and log in.
5. Create an Airflow Variable so go to Admin -> Variable and create a variable called `MLFLOW_TRACKING_URI` and put the MLFlow URL into the values placeholder.
6. Run the `ETFL_dag` dag and go to MLFlow UI to see the tracked results.
