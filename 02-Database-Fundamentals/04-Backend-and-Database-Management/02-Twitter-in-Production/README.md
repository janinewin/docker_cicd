🎯 In this exercise, we would like to get
- our **Twitter API** running in a container in the cloud (**[Google Cloud Run](https://cloud.google.com/run)**)
- ...accessing our **production database**, which is running on a managed SQL instance on the cloud(**[Google Cloud SQL](https://cloud.google.com/sql)**)


We have given you the solution to the `twitter_api` package as well as the associated `alembic` migration you previouslt built as our starting point.


# Setup a Google cloud SQL instance

First, copy the `.env.sample` into a new `.env`. You will notice we have a few extra environment variables than our original twitter app! Fill:
- `POSTGRES_PASSWORD` with the password you want.
- `LOCATION` where your VM is located (e.g. europe-west1)

Then, go to [gcp console UI - SQL section](https://console.cloud.google.com/sql/choose-instance-engine), and create a DB with the following properties
- instanceID=twitter-prod
- root-password=$POSTGRES_PASSWORD
- database-version=POSTGRES_14
- region=$LOCATION
- connections:
    - Private IP
    - Default network
    - Allocated IP range: Use the automatically assigned IP range

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D5/cloudSQL.png" width=500>

**About networks ☝️**

- Here, we tell the GCP not to assign any public IP address to our database: there is no need for anyone external to be able to access the database directly except through the API. This way, even if we somehow leak our password, no-one will be able to connect without breaking into our GCP first 🔐

- We picked the "default" option because it is the same network as all your other GCP project's services (which include your beloved VM). We could have created a separate private network just for the app if we wanted even more isolation!

# Setup the tables

## Connection

Let's connect! **We need the private IP** of our SQL instance, so we can run it, and so the DB isn't accessible through a public internet's IP address.

```bash
gcloud sql instances describe twitter-prod | grep ipAddress
```

and, now, you have the IP address to populate into your `.env` `$POSTGRES_IP` as well as (+`direnv reload`)!


Now, connect with `psql`, as usual via the default "postgres" user and DB

```bash
psql "hostaddr=$POSTGRES_IP port=5432 user=postgres dbname=postgres password=$POSTGRES_PASSWORD"
```
☝️ We used the string syntax instead of the usual `psql --host=$POSTGRES_IP --port=...` but it doesn't matter

 🎉 You are now inside the newly created cloud SQL instance
- Here, connecting via DBeaver from our local machine is not as easy as it is outside our google project virtual private network (whereas your VM is).
- Hopefully, `psql` should be sufficient to verify the creation of our tables!

## Database creation

If we try to create our database in `psql`, it won't work. For `cloud sql`, we have to create our database via gcloud as well. Run the command below. It says to create a `twitter-prod-db` database on the `twitter-prod` instance:

```bash
gcloud sql databases create twitter-prod-db --instance=twitter-prod
```

Add this new DB name `twitter-prod-db` to your `.env` at `$POSTGRES_DATABASE_NAME`

## Table creation

Now, we have our `twitter-prod-db` database in our twitter postgres instance! **We can use alembic to create the yesterday's tables directly onto our new cloud SQL instance.**. As in unit 04, we already have a revision history (the revisions will also populate a few rows in each table), and populated `alembic/env.py` file so as to connect it to your `$POSTGRES_DATABASE_URL` (line:23)

❓ Now apply the migration to the database and connect and check with `psql` that the databases look the way you would expect.


<details>
<summary markdown='span'>🎁 Solution</summary>
Simply run:
```bash
alembic upgrade head
```

</details>

❗️ Now you should see how alembic helps you to keep track of all your migration files: Being able to replicate our setup from yesterday's local `dev` environment to our `prod` database today is super powerful!


# Containerize API

🎯 We want to be able to call our twitter API from our local machine's chrome app --> through our VM --> through our container inside the VM --> to Google cloud SQL !

❓Create a new `Dockerfile` and bring the code over.
- You have a great re-usable framework for a Docker container from the previous exercise if you need inspiration
- The image needs to build well from the challenge root folder
```bash
docker build --tag=twitter .
```
- And the container should run well too, launching twitter via uvicorn, listening on port 8000 on your localhost, and exposing the port 8000 to your local machine too!
```bash
docker run twitter
```

❗️ You may see an error: This is because in your container (and contrary to your VM), the `.envrc` is not activating and therefore not loading the `.env` file into shell ENV variables. We could install direnv in the container, but it makes more sense to use Docker to populate the environment only at run time:

```bash
docker run --env-file=.env twitter
```

☝️ Now that we are populating the environment at run time, we don't need the `.env` to be copied into the container, nor do we want it to be there for security reasons

Here is where the concept of a `.Dockerignore` file becomes useful (it functions like a `.gitignore`). For example, create one with the following, and rebuild, and rerun the container. If you attached a shell to the container, you should see no `.env` files, yet its environment variables will still be available!

```bash
alembic
.env
.env.sample
.envrc
.alembic.ini
.README.md
```
☝️ Always try to keep your image as lean as possible

Now, let's publish the port to make our API available

```bash
docker run --env-file=.env -p 8010:8000 twitter
```

We are mapping 8010 on our VM to 8000 inside the container. If we forward the port to our host machine, we can now check out our running Twitter app. When all looks good, try an endpoint.

Amazing, we are now plugged into our hosted database! Let's go one step further and run our API on cloud run.

🎉 **You should be able to read the list of all tweets by calling `GET /tweets` from your local machine's chrome app --> through your VM --> through your container --> to Google cloud SQL !**


# Put your app in production through Google Cloud Run

🎯 Final step - we want to get rid of our VM entirely and run our app on Google Cloud Run!
🎯 We want to call our twitter API from our local machine's chrome app --> pinging our container directly inside the Google Cloud Run --> pinging Google cloud SQL !

### Push to cloud run

First, let's populate our related values in our `.env` file:

```bash
LOCATION=<USE_SAME_ZONE_THAN_YOUR_G_CLOUD_SQL>
HOSTNAME=$LOCATION-docker.pkg.dev
PROJECT_ID=<INSERT_YOUR_GCP_PROJECT_ID>
REPOSITORY=docker-hub
IMAGE_NAME=twitter
IMAGE_TAG=prod
IMAGE_FULL_TAG=$HOSTNAME/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:$IMAGE_TAG
```

❓ Now, tag and push our image on cloud run

<details>
<summary markdown='span'>🎁 solution</summary>

```bash
docker tag twitter $IMAGE_FULL_TAG
docker push $IMAGE_FULL_TAG
```

</details>

### Create a Virtual Private Connection (VPC)

Now comes one additional complexity: we need to create a VPC connector to describe to the cloud run where to route the internal traffic.
So far, our VM has been in the same VPC as your GCloud SQL, but it's different for Cloud Run:

Here is the gcloud command below to create a VPC named "twitter-connector":

```bash
gcloud compute networks vpc-access connectors create twitter-connector \
--region=europe-west1 \
--range=10.9.0.0/28 # CIDR range of internal addresses that are reserved for this connector.
```
### Deploy on Cloud Run

📚 Take a minute to read the [docs](https://cloud.google.com/run/docs/deploying)

You should see a couple of extra arguments from the lecture we'll have to use:

- `add-cloudsql-instances`: Speaks by itself!
- `vpc-connector`: Needed when our cloudsql instance is on a Private IP network as we have [docs](https://cloud.google.com/sql/docs/mysql/connect-run?authuser=1#private-ip)
- `allow-unauthenticated`: We want our Twitter API to be publicly available (just for this challenge)
- `set-env-vars`: We need to pass the same env variable as when locally running Docker. However, gcloud does not accept "--env-file=.env" syntax, so we can either pass each variable manually or create a yml with env variable. We decided to pass the required variables manually.


```bash
gcloud run deploy twitter-prod \
--image $IMAGE_FULL_TAG \
--vpc-connector=twitter-connector \
--region=europe-west1 \
--add-cloudsql-instances=twitter-prod \
--allow-unauthenticated \
--set-env-vars POSTGRES_DATABASE_URL=$POSTGRES_DATABASE_URL
```

For the region, we put cloud run and the database in the same region to minimise latency!

❗️ This still won't work: Try to see if you can spot the error message:
> _The user-provided container failed to start and listen on the port defined provided by the PORT=8080 environment variable_

<details>
<summary markdown='span'>💡 Hint to the failure</summary>

Cloud run needs our API to start on the `$PORT`, a special env variable that will be injected by cloud run at runtime. You need to update your Dockerfile with `$PORT` instead of hard-coding the port number.


</details>

🏁 Once you have fixed everything locally, push and re-reun the deploy command. You should be able to access your API managed by cloud run connected to your managed database!

# Shut down everything that costs money
Go to [console.cloud.google.com](console.cloud.google.com) and try to shutdown the following services using the web user interface

- Your Cloud Run twitter-prod instance
- Your Cloud SQL twitter-prod database
- Your [VPC](https://console.cloud.google.com/networking/connectors/) twitter-connector
