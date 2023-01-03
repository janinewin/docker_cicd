🎯 The goal of this exercise is to put the Streamlit F1 dashboard in production on Kubernetes (k8s), deployed on Google Kubernetes Engine (GKE). Through this we will see a number of important concepts in k8s such as secrets, volumes, communication between services, and scaling! Let's do it! 🏎️

## 1️⃣ Setup 🛠️

<details>
<summary markdown='span'>Expand for steps</summary>

### 1.1) Extensions

Before you get started there are some key extensions we need for VSCode to make developing k8s a breeze. Make sure you have Kubernetes, Kubernetes templates, and YAML - all highlighted in the image below 👇.

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/extensions.png" width=700>

### 1.2) Clean Minikube cluster

We also want to start from a clean Minikube cluster, so if you did not delete yours at the end of the previous exercise, run this 👇

```bash
minikube delete
```

Then start a new cluster with 👇

```bash
minikube start
```

We can also check to make sure there are no other services by running 👇

```bash
kubectl get svc
```

which should return just:

```
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   2m12s
```

</details>

## 2️⃣ Postgres 🗄️

<details>
<summary markdown='span'>Expand for steps</summary>

### 2.1) Service

The first step for our Postgres is to define the service.

❓ Create a `postgres-service.yaml`. Then populate it with the template using `k8sService` like in the image below.

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/service-autocomplete.png" width=700>

You should get this template:

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D5/service-template.png" width=700>

❓ Now populate the template. You can hover over all of the keys and you will get an explanation of what they do! 💡

- For now you can replace `MYAPP` with `postgres`.
- The type is already `ClusterIP` which is ideal for us, as we don't need to expose Postgres outside of k8s, just to our Streamlit app.
- Then delete the keys mentioning `sessionAffinity` and `nodePort`.
- Finally set the `port` and `targetPort`. Port can be what you like, but `targetPort` needs to be `5432` to target the port Postgres runs on.

<details>
<summary markdown='span'>💡 Completed Postgres service yaml</summary>

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: default
spec:
  selector:
    app: postgres
  type: ClusterIP
  ports:
  - name: postgres
    protocol: TCP
    port: 5432
    targetPort: 5432
```

</details>

### 2.2) Volumes

Next for our Postgres we will need a volume to keep our Postgres data in the same way we needed one for docker-compose.

There are two parts to volumes on Postgres - **volumes**, and **volume claims**. Volumes are the creation of the space on the cluster. Our pod then needs to access that volume and so the volume claim describes how the pod will be accessing the volume (i.e. how much space can the pod use of the total volume).

❓ Create a new file for the volume `postgres-pv.yaml`.

Generally most users won't be making volumes, only claims, but you can still start with a k8s template by typing `Persistent Volume` in the yaml file you just created. Then, add the code below and try to hover over the keys and understand them! 🔍

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: postgres-volume
spec:
  accessModes:
    - ReadWriteOnce
  capacity:
    storage: 2Gi
  hostPath:
    path: /data/postgres
  storageClassName: standard
```

Next - the part more commonly done by developers, which is making the claim.

❓ So now make the file `postgres-pvc.yaml` and use the template `k8sPersistentVolumeClaim`.

You can delete the `storageClassName` key and update the metadata so that the name matches `postgres-volume-claim` and the app label is `postgres`.

<details>
<summary markdown='span'>💡 Completed volume claim </summary>

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-volume-claim
  namespace: default
  labels:
    app: postgres
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 2Gi
```
</details>

We now have a volume for our Postgres to store its data! 🙌

### 2.3) Secrets

We need secrets to store environment variables such as the Postgres user and password of your local Postgres services.

❓ Create another file `postgres-secret.yaml`.
You can use the `k8sSecret` template. Then set the name to `postgres-secrets`.

Now we need to fill the secrets here. The keys can be what you want as the environment variables, while the values have to be the **base64 encoding of the data**. For example for `POSTGRES_PASSWORD` set to `password`, the end result is:

```yaml
POSTGRES_PASSWORD: cGFzc3dvcmQ=
```

❓ Fill in your own `POSTGRES_USER` and `POSTGRES_PASSWORD` keys. To generate the base64 encoding you can use this 👇

```bash
printf password | base64
```

Now we have our secrets and are ready to create our Postgres pod! 🚀

### 2.4) `StatefulSet`

Finally we need to define a `StatefulSet`, which our service will use to run a pod with the Postgres container included!

❓ Create another file called `postgres-statefulset.yaml`. Populate it with the code below 👇 (there is a template for this as well, called `k8sStatefulSet`, for when you write your own).

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres-statefulset
  labels:
    app: postgres
    role: service
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
      role: service
  serviceName: postgres-service
  template:
    metadata:
      labels:
        app: postgres
        role: service
    spec:
      containers:
        - name: postgres
          image: postgres:11.4
          env:
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  key: POSTGRES_USER
                  name: postgres-secrets
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  key: POSTGRES_PASSWORD
                  name: postgres-secrets
          ports:
            - containerPort: 5432
              name: access
              protocol: TCP
          volumeMounts:
            - name: postgres-mount
              mountPath: /var/lib/postgresql/data
      volumes:
        - name: postgres-mount
          persistentVolumeClaim:
            claimName: postgres-volume-claim
```

🤯 Wow, a lot of code! Lets break down the parts you have not seen before.

To get our previously defined secrets into the environment variables of the container we use this syntax:

```yaml
env:
- name: POSTGRES_USER
    valueFrom:
    secretKeyRef:
        key: POSTGRES_USER
        name: postgres-secrets
```

Here the `name` refers to the name we set in `postgres-secret.yaml`. Along with the `key`, which is what the environment variable should be called inside the container! It might be a lot of code compared to compose but **a lot of it is boilerplate you can use over and over again! ♻️**

Then we have our ports section exposing 5432 on our container:

```yaml
ports:
- containerPort: 5432
    name: access
    protocol: TCP
```

Finally the most complicated difference is how we use our volume we created before.

```yaml
    volumeMounts:
    - name: postgres-mount
        mountPath: /var/lib/postgresql/data
volumes:
- name: postgres-mount
    persistentVolumeClaim:
    claimName: postgres-volume-claim
```

The `volumes` section brings our claim into this yaml with the name `postgres-mount`. Then inside our container definition we use `volumeMounts` to describe where the volume should be mounted inside the container!

### 2.5) Connecting it all together 🧰

Now we have all our files lets apply them to our cluster! 👇

```bash
kubectl apply -f .
```

Then lets check if our pod is running with 👇

```bash
kubectl get po
```

Once it's running, lets connect! (similar to docker exec) 👇

```bash
kubectl exec -it postgres-statefulset-0 -- psql --user=<your user>
```

❓ We are in now lets create a new db for our F1 data!

<details>
<summary markdown='span'>💡 If you forgot how to create a SQL DB</summary>

```bash
CREATE DATABASE f1;
```

</details>

Now lets get our F1 data in there! First lets redownload the data and get the `.sql` file.

```bash
curl --output f1db.sql.gz https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/f1/f1db.sql.gz && gunzip f1db.sql.gz
```

Now we can copy our file into our running pod with 👇

```bash
kubectl cp f1db.sql postgres-statefulset-0:f1db.sql
```

Finally we can use `exec` to execute the SQL script and load our new database!

```bash
kubectl exec postgres-statefulset-0 -- psql -f f1db.sql --user=<your user> <your database>
```

Then you can connect again and checkout the tables. Now we are ready to plug in Streamlit! 🧑‍🎨

</details>

## 3️⃣ Streamlit 🖼️

<details>
<summary markdown='span'>Expand for steps</summary>

### 3.1) Service

❓ Now create a `streamlit-service.yaml` and populate it with a `LoadBalancer` service, with name `streamlit-service` and selector `app: streamlit`.

<details>
<summary markdown='span'>💡 Completed service</summary>

```yaml
apiVersion: v1
kind: Service

metadata:
  name: streamlit-service

spec:
  type: LoadBalancer
  ports:
    - protocol: TCP
      port: 8501
      targetPort: 8501
  selector:
    app: streamlit
```

</details>


### 3.2) Secrets

For our secrets in the original app we used a `secrets.toml` file. In k8s we can actually mount an entire secrets file as a value in the YAML file!

❓ Create a new file `streamlit-secret.yaml`. Here for the data the keys should be the name of the files in your `.streamlit` (for example, `secrets.toml`) and the values should be the results of `base64 <file>`!

When you update the `secrets.toml` file, the host will be the `name` of the postgres service this is how services inside k8s can speak to each other with ease (don't forget to update the other params as well).

<details>
<summary markdown='span'>💡 Example completed file</summary>

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: streamlit-secrets
type: Opaque
data:
  secrets.toml: W3Bvc3Rncm ...
  config.toml: W3NlcnZlcl0 ...
```

</details>

Now we are ready to put it into the container!

### 3.3) Deployment

❓ Finally create a new `streamlit-deployment.yaml` and build the Dockerfile inside minikube. Then populate the file with the code below 👇:

<details>
<summary markdown='span'>💡 Reminder of how to build inside minikube</summary>

```bash
eval $(minikube docker-env)
docker build -t app .
```

</details>


```yaml
apiVersion: apps/v1

kind: Deployment

metadata:
  name: streamlit-deployment

spec:
  replicas: 4
  selector:
    matchLabels:
      app: streamlit

  template:
    metadata:
      labels:
        app: streamlit
    spec:
      containers:
      - name: streamlit-container
        image: app:latest
        imagePullPolicy: Never
        volumeMounts:
          - mountPath: "/app/.streamlit"
            name: streamlit-secrets
            readOnly: true
        ports:
        - containerPort: 8501
        args: ["streamlit", "run", "f1dashboard/advanced.py"]
      volumes:
        - name: streamlit-secrets
          secret:
            secretName: streamlit-secrets
      restartPolicy: Always
```

Here you can see how we have added the secrets into the container by treating them as a volume:

```yaml
volumes:
  - name: streamlit-secrets
    secret:
      secretName: streamlit-secrets
```

Then mounting it into `/app/.streamlit` where they belong!

Something else to note that can be pretty confusing with k8s vs `docker-compose` is the `args` argument is added to the entrypoint (the equivalent in compose is `command`), since `command` in k8s overrides the entrypoint ❗

### 3.4) Putting it all together 🎀

❓ Now that we have everything ready to go with the Streamlit, apply the config files and access the service!

<details>
<summary markdown='span'>💡 If you've forgotten how to access the service!</summary>

```bash
kubectl port-forward services/streamlit 8501:8501
```

</details>


</details>

## 4️⃣ GKE

<details>
<summary markdown='span'>Expand for steps</summary>

### 4.1 Creating the cluster

First we want to create a new k8s cluster on gcloud use the command below 👇

```bash
gcloud container clusters create "streamlit-f1" \
  --region "europe-west1" \
  --machine-type "e2-standard-2" \
  --disk-type "pd-standard" \
  --disk-size "30" \
  --num-nodes "1" --node-locations "europe-west1-b","europe-west1-c"
```

This will take a while 😅 so we can continue and edit some of our files while it provisions!

### 4.2 Postgres

We need to change our volume file for the cloud so go to `postgres-pv.yaml` and replace it with the code below 👇

```yaml
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: postgres-volume
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-standard
  replication-type: regional-pd
allowedTopologies:
  - matchLabelExpressions:
      - key: failure-domain.beta.kubernetes.io/zone
        values:
          - europe-west1-b
          - europe-west1-c
```

This is one of the biggest areas of change moving to the cloud try and understand it through the keys then read the explanation

<details>
<summary markdown='span'>🧑‍🏫 Explanation</summary>

Here we are describing the type of storage we want to take. Who is providing the storage in this case gcp. Then which regions we are okay with disk being provisioned on.

</details>

Then we need to change our claim in `postgres-pvc.yaml` 👇

```yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: postgres-volume-claim
spec:
  storageClassName: postgres-volume
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 200G
```

Here basically nothing has changed except we asked for `200G` of storage as this is the minimum google will dynamically provision!

Finally we need to change the code in the `postgres-statefulset.yaml` 👇

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres-statefulset
  labels:
    app: postgres
    role: service
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
      role: service
  serviceName: postgres
  template:
    metadata:
      labels:
        app: postgres
        role: service
    spec:
      containers:
        - name: postgres
          image: postgres:11.4
          env:
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  key: POSTGRES_USER
                  name: postgres-secrets
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  key: POSTGRES_PASSWORD
                  name: postgres-secrets
            - name: PGDATA
              value: /var/lib/postgresql/data/pgdata
          ports:
            - containerPort: 5432
              name: access
              protocol: TCP
          volumeMounts:
            - name: postgres-mount
              mountPath: /var/lib/postgresql/data
      volumes:
        - name: postgres-mount
          persistentVolumeClaim:
            claimName: postgres-volume-claim
```

Here our main change is how we are adding an extra `PGDATA` envrioment variable. GKE does not like us to directly put data into the root of the mount!

### 4.3 Streamlit

❓ For streamlit we can no longer use our local image, you would now build and push the container but to save time you can use ours replace these keys in `streamlit-deployment.yaml`.

```yaml
image: europe-west1-docker.pkg.dev/data-engineering-students/student-images/streamlit-f1:0.1
imagePullPolicy: "IfNotPresent"
```

Hopefully our cluster is done provisioning now!


### 4.4 Putting it all together

Lets make kubectl interact with our new cluster:

```bash
gcloud container clusters get-credentials streamlit-f1 --region europe-west1
```

Then apply all of our config files!

If everything go correctly you should see the pods running with:

```bash
kubectl get po
```

❓ Follow the steps we used earlier to put the f1 database in this new cluster.

You should be able to access your streamlit through the internet normally!

```bash
kubectl get svc
```

Then from your streamlit service go to the `external ip` + `:8501` on your browser!

🚀 In production 🚀

### 4.5 Simulating disaster

Keep your app open. Then lets find out where the database is currently running!

```bash
kubectl get pods -l app=postgres -o wide
```

Then take note of the `NODE`

```bash
kubectl cordon NODE
```

Will prevent anymore pods being provisioned on this node. Then delete the pod!

```bash
kubectl delete postgres-statefulset-0
```

Then checkout your app it should fail to connect to the database temporarily but keep refreshing and checking `kubectl get pods -l app=postgres -o wide`.

It will reprovision itself on the other node everything intact. For a complete failure like this it is incredibly impressive how fast k8s can fix everything (usually it can be seamless as most crashes you can see coming with load increasing)!

Lets cleanup so we don't spend too much:

```bash
kubectl delete -f . \
&& gcloud container clusters delete streamlit-f1 --region=europe-west1
```


🏁

</details>
