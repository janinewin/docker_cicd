### Minikube & Kubectl 101

🎯 In this challenge, we will learn how to deploy our first application with **Kubernetes** and **Minikube** by putting a FastAPI endpoint onto a cluster. 🚀

Minikube allows developers to run Kubernetes **locally** on their machine, as though it was a cluster of nodes.
It is an excellent tool to **help developers and new Kubernetes users in deploying applications with K8s**.

Under the hood, Minikube creates a virtual machine in your container in which there is single cluster of one node.

To use Minikube, as mentioned in the [documentation](<https://minikube.sigs.k8s.io/docs/start/>), you'll need:

- **2 CPUs** or more
- **2GB of RAM**
- **20GB** of free disk space
- **Container or virtual machine manager** such as: Docker, Hyperkit, Podman, etc.

In our case, we will use Docker to launch Minikube.

## Launching Minikube 🚀

To launch Minikube and start a cluster, you'll need to open a terminal and run the following command :

```bash
minikube start
```


Please wait Minikube to start, it can take up to a few minutes.

Once started, you can interact with your cluster thanks to `kubectl`, just like for for any other K8s cluster.

For instance, you can inspect your cluster node.

```bash
kubectl get node
```

You should see something like

```txt
NAME       STATUS   ROLES                  AGE   VERSION
minikube   Ready    control-plane,master   75s   v1.23.3
```

## First step - Sharing your Docker daemon 🐳

When you work with Minikube, you work within a VM with its own docker daemon.

In order to let our local Docker daemon to communicate with Minikube's Docker daemon, we need to run the following command:

```bash
eval $(minikube docker-env)
```

This command specifies to the Docker client to use the Docker service running inside the Minikube virtual machine.
Now any ‘docker’ command you run in this current terminal will run against the Docker inside Minikube cluster.


❓ Now ‘build’ against the docker inside Minikube, which is instantly accessible to Kubernetes cluster.

```bash
docker build -t app .
```

*Alternatively, there is one other effective way to push your local Docker image directly to Minikube, which could save time from building the images in Minikube again: `minikube image load <image_name>`*

## Our first K8s service 🗄️

Let's create our first service on Kubernetes.
A service is an **abstraction** that defines a set of **Pods** running in your cluster, and a **policy** by which to reach them. Sometimes this pattern is called a [**micro-service**](https://en.wikipedia.org/wiki/Microservices).

When created, the Service is assigned a unique IP address.
This address is tied to the lifespan of the Service, and will not change while the Service is alive.

Pods can be configured to talk to the Service, and know that communication to the Service will be automatically load-balanced out to some pod that is part of the Service.

These Pods are exposed through endpoints. When a Pod dies, it is automatically removed from the endpoints, and new Pods matching the Service's selector will automatically get added to the endpoints.

❓ Create a configuration file for our service - `service.yaml` - and copy below content into it.

```yaml
#service.yaml
apiVersion: v1
kind: Service

metadata:
  name: fastapi-service

spec:
  type: LoadBalancer
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8000
  selector:
    app: fastapi

```

In the first part, we specify that the configuration file is for a Service that we named `fastapi-service`.

A selector usually determines the set of Pods targeted by a Service.
In the spec, we specify that it is a **LoadBalancer service**.
This specification creates a new Service object named "fastapi-service", which targets TCP port 8000 on any Pod with the `fastapi` label.

We then expose it on an abstracted Service port 8080.

`targetPort`: is the port the container accepts traffic on.
`port`: is the abstracted Service port, which can be any port other pods use to access the Service.

Let's create our service 👇

```bash
kubectl apply -f service.yaml
```

You should see `service/fastapi-service created`

Let's inspect our new service

```bash
kubectl get service fastapi-service
```

You should see something like this

```text
NAME            TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
fastapi-service   LoadBalancer   10.96.231.152   <pending>     8000:30604/TCP   24s
```


## Our first K8s Deployment 🛰

Within Kubernetes, a container runs in a pod, which can be represented as **one instance of a running service**.

Pods are ephemeral and not self-healing, which makes them fragile. 🤕

They can go down when an interruption occurs on the server, during a brief network problem, or due to a minimal memory issue — and it can bring down your entire application with it. Kubernetes deployments help to prevent this downtime. 💪

In a deployment, you can describe the desired state for your application and Kubernetes will constantly check if this state is matched.

A deployment will create `ReplicaSets` which then ensures that the desired number of pods are running. If a pod goes down due to an interruption, the `ReplicaSets` controller will notice that the desired state does not match the actual state, and a new pod will be created.

Deployments offer:

- High availability of your application (pods) by creating a `ReplicaSet`
- (Auto)scaling of pods
- Multiple strategies to deploy your application
- The possibility to rollback to an earlier revision of your deployment

Let's now create our Deployment. A Deployment runs multiple replicas of your application and automatically replaces any instances that fail or become unresponsive.

❓ Create a configuration file for the deployment - `deployment.yaml` - and copy below content into it.

```yaml
#deployment.yaml
apiVersion: apps/v1

kind: Deployment

metadata:
  name: fastapi-deployment

spec:
  replicas: 4
  selector:
    matchLabels:
      app: fastapi

  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
      - name: fastapi-container
        image: app:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
```

In the first part of the configuration, we specify that the configuration we are applying is for a Deployment resource that we call `fastapi-deployment`.

In the spec, we specify the number of replicas, here 4.
It means that we will always have 4 pods running our application.
This pods will each run a container app that we have build previously and renamed `fastapi-container` here.

We then specify the port exposed in the container, here 8000.

By Default, a Deployment will always try to pull the image from a remote registry. If you want to use a local image to build a container in the pods, you need to specify the `imagePullPolicy` to `Never`.

Run the below command to run the deployment 👇

```bash
kubectl apply -f deployment.yaml
```

you should see `deployment.apps/fastapi-deployment created`


Let's inspect our 4 pods created 👇

```bash
kubectl get pods
```

You should see 4 pods running:

```text
NAME                                READY   STATUS    RESTARTS   AGE
fastapi-deployment-746c85b46f-2sdp2   1/1     Running   0          26s
fastapi-deployment-746c85b46f-dqcxs   1/1     Running   0          26s
fastapi-deployment-746c85b46f-h5vls   1/1     Running   0          26s
fastapi-deployment-746c85b46f-rgm82   1/1     Running   0          26s
```

## Forwarding our service 🔗

If you want to see the app running we need to forward to port from the cluster to our VM!

```bash
kubectl port-forward service/fastapi-service 9000:8080
```

This command will forward the service port we defined in the `service.yaml` to 9000 on the localhost of your VM.

❓ Then forward the port 9000 again to your host machine and you should be able to see your running service!

## Using Minikube dashboard 🖼️

Minikube has an excellent UI interface to manage and visualize your clusters!
You can use it to :

- Get an overview of applications running on the K8s cluster
- Deploy containerized applications to a K8s cluster
- Debug your containerized application
- Manage cluster resources and create or change individual resources

To launch the Minikube dashboard, let's open a new terminal and run:

```bash
minikube dashboard
```

Then follow the address it gives and open it in your local browser!

## Stopping Minikube 🛑

To delete your local cluster 👇

```bash
minikube delete
```


To stop Minikube 👇

```bash
minikube stop
```

### Well done! 🙌

You've just experienced the basic building blocks of a k8s deployment - pods, nodes, containers and clusters. For a further summary of these, check out [this article 📚](https://medium.com/google-cloud/kubernetes-101-pods-nodes-containers-and-clusters-c1509e409e16).
