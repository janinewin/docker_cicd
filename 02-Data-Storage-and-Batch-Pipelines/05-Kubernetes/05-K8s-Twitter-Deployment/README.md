# 05 - Deploy Twitter Microservices into Google Cloud Kubernetes

In this last challenge, we will deploy our Twitter Microservices application to [Google Cloud Kubernetes](<https://cloud.google.com/kubernetes-engine>).
 **Google Kubernetes Engine (GKE)** is Google managed cloud service to deploy an application with K8s.

## Set up

Let's first define the region where we will deploy our clusters here in Europe.

```bash
gcloud config set compute/zone europe-west1
```

To create clusters in GKE, one must choose a mode of operation: **Autopilot or Standard**.

We will use the Autopilot mode in this challenge as it is a managed cluster configuration mode in which most of the configuration is already done and preconfigured.
If you are curious, you can learn more about the difference between these two modes [here](<https://cloud.google.com/kubernetes-engine/docs/concepts/types-of-clusters#modes>)

Let's launch our first cluster on GKE!

```bash
gcloud container clusters create-auto <user.github_nickname> \
    --region=europe-west1
```

‡
It will take several minutes to create the cluster.
When it's over, you should see :

```
Creating cluster <your_github_name> in europe-west1... Cluster is being health-checked (master is healthy
)...done.
Created [https://container.googleapis.com/v1/projects/***].
To inspect the contents of your cluster, go to: https://console.cloud.google.com/kubernetes/workload_/gcloud/europe-west1/****
kubeconfig entry generated for <your_github_name>.
NAME           LOCATION      MASTER_VERSION  MASTER_IP      MACHINE_TYPE  NODE_VERSION    NUM_NODES  STATUS
<your_github_name>  europe-west1  1.22.8-gke.202  34.79.124.243  e2-medium     1.22.8-gke.202  3          RUNNING
```

If not, please call a TA for help.

By default, GKE will create a cluster with three nodes, one master node and two working nodes.

## Get authentication credentials for the cluster

After creating the cluster, we need to get **authentication credentials** to interact with the cluster:

```bash
gcloud container clusters get-credentials <user.github_nickname>
```

This command configures `kubectl` to use the cluster created.
‡

Let's deploy our app and create our services, deployments, pods and volumes!

## Step 1 - Push our docker image to the google container registry

First, we need to push our docker image user-service and tweeter-service to **Google Container Registry** so that Google Kubernetes Engine can fetch them and create as many containers as we want from these images!

```bash
docker compose -f docker-compose.yaml build
```

Let's rename them appropriately so that docker knows where to push: in the right registry and within the right project!

```bash
docker tag 05-k8s-twitter-deployment_tweet-service eu.gcr.io/wagon-devops-day-5/<user.github_nickname>_tweet-service
docker tag 05-k8s-twitter-deployment_user-service eu.gcr.io/wagon-devops-day-5/<user.github_nickname>_user-service
```

Let's now push our image to the registry.

```bash
docker push eu.gcr.io/wagon-devops-day-5/<user.github_nickname>_tweet-service
docker push eu.gcr.io/wagon-devops-day-5/<user.github_nickname>_user-service
```

## Step 2 - Update Deployments

One last thing to do, and we are good to go!
We need to update our **Deployments** to specify to Kubernetes to fetch our image from our google registry!

```yaml
# in tweet-service-deployment.yaml
 #[...]
spec:
      containers:
        - image: eu.gcr.io/wagon-devops-day-5/<user.github_nickname>_tweet-service
          name: tweet-service
          imagePullPolicy: Always
      #[...]
```

We now specify `imagePullPolicy: Always` so that every time GKE launches a container, it queries google container registry to look for newly updated images.

```yaml
# in user-service-deployment.yaml
 #[...]
spec:
      containers:
        - image: eu.gcr.io/wagon-devops-day-5/<user.github_nickname>_user-service
          name: user-service
          imagePullPolicy: Always
      #[...]
```

Let's create our resources on our google clusters!

```bash
kubectl apply -f .
```

Let's inspect the pods, it can take a while for them to be instanciated.

```bash
kubectl get pods
```

At some point, you should see your containers running.

To try the app, let's find **the external IP** of the user and tweet services by running the following commands:

```bash
kubectl get service tweet-service
kubectl get service user-service
```

Tada! The services are up! Let's  try them by going to `EXTERNAL-IP/PORT`


Good job! You manage to deploy your first microservices to the Cloud with Kubernetes!
You can inspect the [user interface](https://console.cloud.google.com/kubernetes) and have a look at your running microservices 🔥


## Clean up

To avoid incurring charges to Le Wagon's Google Cloud account for the resources used on this challenge, **please delete all resources after completing the challenge**

```bash
kubectl delete all --all
```

This command deletes the Compute Engine load balancer we created when we exposed the Deployment.

Then, let's delete the cluster by running :

```
gcloud container clusters delete <user.github_nickname>
```
