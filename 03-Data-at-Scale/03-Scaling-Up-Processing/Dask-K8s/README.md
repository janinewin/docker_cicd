# Dask on K8s

🎯 We have seen **dask** distribute over multiple cores on a single machine, now the goal is to distribute computation across multiple machines by leveraging **dask** with **k8s**.

We will be able to process over **1,000,000,000** cells of new york taxi data in around **10 seconds** 💪

## 1️⃣ Cluster setup!

Lets start by creating a cluster with a lot of **cpus** ideal for distributing our task across!

👇 Run to create our **cluster**

```bash
gcloud container clusters create my-dask \
		--machine-type e2-highcpu-4 \
    --num-nodes 2 \
		--zone=europe-west1-b \
    --node-locations=europe-west1-b,europe-west1-c,europe-west1-d
```

Will create **six machines** (of `e2-highcpu-4`) **two** in each of the **node-locations**.

While it is provisioning you can get ready to run the **helm** 🪖 chart.

📚 **Checkout** `config.yaml` try to understand what we are defining here!

<details>
<summary markdown='span'>💡 Config.yaml meaning</summary>

We are telling the cluster what the **worker** pods need in terms of **resources**. Adding the extra pip packages. ❗️ It is super important that the versions of packages you need for your code are the same locally and on the **pods** to allow it to be distributed. Finally we are disabling jupyter we are going to use the **jupyter on your vm!**

</details>

Hopefully the **cluster** will be done provisioning! Checkout the nodes:

```bash
kubectl get nodes
```

## 2️⃣ Adding our helm chart


We can install the **helm** chart on the cluster by first adding the repo.

```bash
helm repo add dask https://helm.dask.org/
helm repo update
```

Then apply the chart 👇

```bash
helm install dask-release dask/dask -f config.yaml --version=2022.1
1.0
```

❓ Checkout the pods created. Then you can **port forward** from port **80** on the `dask-release-scheduler` **service** to **8000** on your vm.

<details>
<summary markdown='span'>💡 Port forwarding reminder!</summary>

```bash
kubectl port-forward services/dask-release-scheduler 8000:80
```

</details>

This lets us access the dashboard which will allow us to track the computations across our **cluster!**

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W3D3-processing/dask/dask-dashboard.png" width=700>

## 3️⃣ Notebook time 📚

❓ **Open up `dask.ipynb` with `jupyter` (not vscode) and follow the notebook!**

## 4️⃣ Taking it further 🕵️

❓ If you have **time** you can change `config.yaml` and delete the part disabling jupyter! Then `helm upgrade` and connect to jupyter on the cluster and dask provides some great notebooks to further your knowledge!
