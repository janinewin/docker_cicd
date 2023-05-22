# Helm ⛑

Helm helps us automate the deployment of complex k8s from **charts** which can be seen like recipes for settings up complex structures on k8s. You can have a look at available **charts** on https://artifacthub.io/ .

🎯 In this challenge we will use helm to deploy a complex `airflow` setup to our cluster!


## 1️⃣ Setup

To install helm use:

```
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

Then make sure we have a fresh **minikube** cluster running and ready to go!

To add the **airflow chart** to our local computer

```bash
helm repo add airflow-stable https://airflow-helm.github.io/charts
helm repo update
```

Next make a copy of the `.env.copy` as your own `.env`. We are going to fill out some of the values. The `AIRFLOW_NAME` is what we will name our deployed `chart`. Then we will also use `AIRFLOW_NAMESPACE` to use kubectl namespaces.

```
AIRFLOW__WEBSERVER__SECRET_KEY=###
AIRFLOW__CORE__FERNET_KEY=###
```

Are for security

Generate the `AIRFLOW__WEBSERVER__SECRET_KEY` with:

```bash
python -c 'import os; print(os.urandom(16))'
```

and the `AIRFLOW__CORE__FERNET_KEY` with:

```python
from cryptography.fernet import Fernet

fernet_key = Fernet.generate_key()
print(fernet_key.decode())
```

Now also clone the `helm-value.yaml.copy` and we are ready to go!

## 2️⃣ Creating airflow

Lets create our own namespace.

```bash
kubectl create namespace $AIRFLOW_NAMESPACE
```

To access stuff in this namespace we have to append every `kubectl` with `-n airflow`. Lets instead set this as our current namespace:

```bash
kubectl config set-context --current --namespace=airflow
```

Creating our **secrets** 🔐

```bash
kubectl create secret generic airflow-fernet-key --namespace="$AIRFLOW_NAMESPACE" --from-literal=value=$AIRFLOW__CORE__FERNET_KEY
```

```bash
kubectl create secret generic airflow-webserver-secret-key --namespace="$AIRFLOW_NAMESPACE" --from-literal=value=$AIRFLOW__WEBSERVER__SECRET_KEY
```

Now we can apply our chart and options 👇

```bash
helm install \
  "$AIRFLOW_NAME" \
  airflow-stable/airflow \
  --namespace "$AIRFLOW_NAMESPACE" \
  --version "8.6.1" \
  --values ./helm-values.yaml
```

Now go and make a coffee ☕️ this will take a little while.

When you come back and checkout your cluster you will see all the **pods** you need created!

## 3️⃣ Making ready for production

Add a real db 💿

```bash
kubectl create secret generic airflow-pg-password --namespace="$AIRFLOW_NAMESPACE" --from-literal=password=$POSTGRES_PASSWORD
```

```bash
kubectl create secret generic airflow-pg-user --namespace="$AIRFLOW_NAMESPACE" --from-literal=username=$POSTGRES_USER
```
