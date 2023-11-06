###  Airflow setup

This is a set of terraform files designed to setup Airflow in its entirety for you on GKE.

### Steps

1. Create a repo for your dags

```bash
gh repo create --private --source=.
```

2.

Get the deploy token from the repo!

3.

Make a copy of the `main.auto.tfvars.sample` fill the values

4.

Provision the resources

```bash
terraform init
terraform apply
```


5.

Setup an airflow webserver secret

```bash
kubectl create secret generic airflow-webserver-secret --from-literal="webserver-secret-key=$(python3 -c 'import secrets; print(secrets.token_hex(16))')"
```

6.

Fill the missing repo key in values.yaml

7.

Install the helm chart for airflow

```bash
helm upgrade  --install airflow apache-airflow/airflow --values=values.yamlhelm upgrade  --install airflow apache-airflow/airflow --values=values.yaml
```

You should be ready to go!
