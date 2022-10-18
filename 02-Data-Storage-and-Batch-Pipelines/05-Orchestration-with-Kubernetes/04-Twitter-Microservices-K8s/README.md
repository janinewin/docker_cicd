# 04 - Deploy Twitter Microservices with K8s

Welcome to this new challenge!
This exercise aims to deploy a single cluster of pods with Kubernetes that will run our day **04 Microservices Twitter app**!

To do so, let's start with a quick reminder about our application.

It contains two services :

- A **tweet service** that contains our Twitter REST API where we can read, create, delete and update tweets, along with a simple sqlite database
- A **user service** that contains a user sqlite database with four basic endpoints :
  - create users
  - list all users
  - get all tweets from one user
  - a tweet timeline to recommend ten tweets per user

Yesterday, we put our microservices application into containers thanks to `docker compose`, so we had one container per service.

Today, we will deploy our microservices into **clusters of pods** so that each service can get runned by many pods / containers !

To do so, we will use a fantastic tool that helps ease the transition between docker compose and k8s, **Kompose**.

[Kompose](<https://kompose.io/user-guide/>) is a conversion tool for **Docker Compose** to container orchestrators such as Kubernetes.

## Start

First, let's start by launching **Minikube**, which we will use to use our local machine as if it was a cluster of servers.

```bash
minikube start
```

Let's now build our docker image that contains our tweet and user microservices.
After making them, don't forget to run some containers to check that everything works well before starting to use K8s.
It is always crucial to **test your containers before** putting them into clusters, as it would save you a crucial amount of troubleshooting time!

We will start by configuring docker to use the docker daemon inside Minikube to build and run containers.

Let's build our image.

```bash
docker compose -f docker-compose.yaml build
```

And let's launch our two containers.

```bash
docker compose -f docker-compose.yaml up
```

Please check that your containers work. Everything should work well. If not please call a TA for help.

## From docker compose to K8s

Let's stop our running containers. You can list all your docker containers with the `docker ps` command and delete them by typing `docker stop container_id`

Remember, as for now, we only build and run our containers locally using our computer docker daemon.
If we want to deploy these containers into a cluster through Minikube, we will need to send them to Minikube's VM.

Well, let's do it.

```bash
 eval $(minikube docker-env)
 ```

 ```bash
docker compose -f docker-compose.yaml build
```

Let's rename our images for better readability.

```bash
docker tag 04-twitter-microservices-k8s_user-service  user-service
docker tag 04-twitter-microservices-k8s_tweet-service  tweet-service
```

Let's start the actual work, shifting from docker compose to Kubernetes.
The good news is that we already did a considerable part of the hard work yesterday with our `docker-compose.yml`.

We need now to adapt this configuration file into multiple ones for Kubernetes :
- one **service configuration** file for our user service
- one **deployment configuration** file for our user service
- one **service configuration** file for our tweet service
- one **deployment configuration** file for our tweet service
- one **volume configuration** file for our user service so that our pods can store the evolution of our sqlite database
- one **volume configuration** file for our tweet service so that our pods can keep the evolution of our sqlite database

Looks complex, repetitive and painful, right?

Well, the good news is that Kompose was invented to solve this issue as it makes it way easier to transit from docker compose to K8s. Kompose will do most of the job for you and turn your docker-compose.yaml file into multiples configuration files adapted for kubernetes!

Let's install **Kompose** by following this [link](<https://kompose.io/installation/>)

To convert a docker compose config file to K8s, let's run the following command :

```bash
kompose convert -f docker-compose.yaml
```

As you can see six files were created :

```txt
INFO Kubernetes file "tweet-service-service.yaml" created
INFO Kubernetes file "user-service-service.yaml" created
INFO Kubernetes file "tweet-service-deployment.yaml" created
INFO Kubernetes file "tweeterapp-persistentvolumeclaim.yaml" created
INFO Kubernetes file "user-service-deployment.yaml" created
INFO Kubernetes file "userapp-persistentvolumeclaim.yaml" created
```


Boom, magic! We got our **services & deployments files** which describes how we wanna deploy our app!
By default with Kompose our microservices will be deployed into one pod each.
We also got some **volume configuration files** to create volumes that will store our sqlite databases so that we don't lose the evolution of the database even if we create or kill multiple pods. Please, go over this [explanation](<https://kubernetes.io/docs/concepts/storage/persistent-volumes/>) to better understand the volumes configuration files we set up

Let's launch our deployment, resources, and volumes.

```bash
kubectl apply -f .
```

Let's inspect our new pods :
```
kubectl get pods -o wide
```

Ohoh, you should see that your pods failed to run your container with an `ImagePullBackOff` status.
The status `ImagePullBackOff` means that a container could not start because Kubernetes could not pull a container image for reasons such as invalid image name, or pulling from a private registry without imagePullSecret.
The BackOff part indicates that Kubernetes will keep trying to pull the image, with an increasing back-off delay.

You can inspect in-depth the log of the error by running the following command :

```bash
kubectl describe pods
```

Here, it happens because we did not specify to kubectl that the docker image we want to use in our pods is from our local machine and not a remote repository like google container registery! Indeed, **by default, kubectl will always try to pull an image from a registery and not from a local machine**!

Let's update our `tweet-service-deployment.yaml` and `user-service-deployment.yaml` by adding the argument `imagePullPolicy: Never` to fix the issue.


```yaml
# in user-service-deployment.yaml AND tweet-service-deployment.yaml

# [...]
 containers:
        - image: user-service
          name: user-service
          imagePullPolicy: Never
          ports:
          #[...]
```

Let's update our services

```bash
kubectl apply -f user-service-deployment.yaml, tweeter-service-deployment.yaml
```

Let's check again our pods :

```bash
kubectl get pods
```
Tadam! After a few seconds, you should see your pods working well.

Let's now do one last thing, update our services to be `Load Balancer`.
By default with K8s, all services are ClusterIP.


Let's update the `user-service-service.yaml` and `tweet-service-service.yaml`

```yaml
# in user-service-service.yaml AND tweet-service-service.yaml

# [...]
spec:
  type: LoadBalancer
  ports:

# [...]
```

Let's update our services.
```bash
kubectl apply -f user-service-service.yaml, tweet-service-service.yaml
```

Let's launch a tunnel

```bash
minikube tunnel
```

Tada! You can access your app through <http://localhost:5000/> and <http://localhost:5000/>

Play with the app and add some new tweets in your database!

You can now change the configuration of our deployment and update the number of **replicas to have more pods running your container**. Change the number of replicas in the deployments files so that you get 2 for the tweets services and 4 for the users services.

Apply the changes :

```bash
kubectl apply -f user-service-deployment.yaml, tweeter-service-deployment.yaml
```

Check you new pods :

```bash
kubectl get pods -o wide
```


Start the tunnel again
```bash
kubectl minikube
```

Boom, good job! You should be able to see that even if you add or delete pods, the database will still get updated, thanks to the volume resource! 🔥
You can use the Minikube dashboard to investigate your resources.

```bash
minikube dashboard
```
