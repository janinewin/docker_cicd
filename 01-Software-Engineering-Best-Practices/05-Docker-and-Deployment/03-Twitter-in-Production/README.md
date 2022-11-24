🎯 We would like to have
- our **Twitter api** running in a container in the cloud (**[Google Cloud Run](https://cloud.google.com/run)**)
- ...accessing our **production database**, which is running on a managed SQL instance in the cloud(**[Google Cloud SQL](https://cloud.google.com/sql)**)


✅ We have given you the solution to the `twitter_api` package as well as the associated `alembic` migration you built in unit 04 as starting point.


# 1️⃣ Setup a Google cloud sql instance

First copy the `.env.sample` into a new `.env`. You will notice we have a few extra environment variables than our original twitter app! You can start just by filling out `POSTGRES_PASSWORD` with the password you want.

Run this command to create a cloud sql instance, it will take a little while to provision so read what the options are below! Note that you could have done everything from the [console UI](https://console.cloud.google.com/sql/choose-instance-engine) instead

```bash
gcloud sql instances create twitter-prod \
--database-version=POSTGRES_14 \
--region=europe-west1 \
--root-password=$POSTGRES_PASSWORD \
--no-assign-ip \
--network=default \
--cpu=2 \
--memory=8GiB
```

- The first argument after create is the name for instance we want to create in this case `twitter-prod`.

- `--database-version` tells cloud sql the version of SQL we want to run.

- --region is where we want to run the instance, here we are placing it in the same region as our virtual machine for fast access. We should make sure to place our api here as well!

- --root-password is the password for the `postgres` user on the new sql instance.

- --no-assign-ip tells GCP not to give a public ip to our database, there is no need for anyone external to be able to access the database directly except through the api. This way even if we somehow leak our password no-one can connect without also breaking into GCP.

- --network tells GCP where to host it privately, given that we don't want it exposed with a public ip. Here we picked default as it is the same network across all your current GCP project's services (which includes your beloved VM). We could equally have created a separate private network just for the app for even more isolation!

# 2️⃣ Setup the tables

## 2.1) Connection

Lets connect! **We need the private ip** of our sql instance so we can run, so that the DB is not accessible through anyone on with the IP on public internet.

```bash
gcloud sql instances describe twitter-prod | grep ipAddress
```

and now you have the ip address to populate into your `.env` `$POSTGRES_IP` as well (+`direnv reload`)!


Now connect with `psql`, as usual via the default "postgres" user and db

```bash
psql "hostaddr=$POSTGRES_IP port=5432 user=postgres dbname=postgres password=$POSTGRES_PASSWORD"
```
☝️ We used the string syntax instead of the usual `psql --host=$POSTGRES_IP --port=...` but it doesn't matter

 🎉 You are now inside the newly created cloud sql instance
- Here, connecting via DBeaver from our local machine is not so easy as it is outside our google project virtual private network (whereas your VM is).
- Hopefully, `psql` should be plenty in order to verify the creation of our tables!

## 2.2) Database creation

If we try to create our database in `psql` it won't work. For `cloud sql`, we have to create our database via gcloud as well. Run the command below it says to create a `twitter-prod-db` database on the `twitter-prod` instance:

```bash
gcloud sql databases create twitter-prod-db --instance=twitter-prod
```

Add this new DB name `twitter-prod-db` to your `.env` at `$POSTGRES_DATABASE_NAME`

## 2.3) Table creation

Now we have our twitter-prod-db database in our twitter postgres instance! **We can use alembic to create the tables we created locally yesterday directly onto our new cloud sql instance.**. As in previous unit 04, we already have a revision history (the revisions will also populate a few rows in each table), and populated `alembic/env.py` file so as to connect it to your $POSTGRES_DATABASE_URL (line:23)

❓ Now apply the migration to the database and connect and check with `psql` that the databases look how you would expect.


<details>
<summary markdown='span'>🎁 Solution</summary>
Simply run:
```bash
alembic upgrade head
```

</details>

❗️ Now you should see the utility of alembic keeping track of all your migration files: Being able to replicate our setup from our local `dev` environment we were on yesterday, to our `prod` database today, is super powerful!


# 3️⃣ Containerize API

🎯 We want to be able to call our twitter API from our local machine's chrome app --> through our VM --> through our container inside the VM --> to Google cloud SQL !

❓Create a new `Dockerfile` and bring the code over.
- You have a great re-usable framework for a docker container from the previous exercise if you need inspiration
- The image needs to build well from the challenge root folder
```bash
docker build --tag=twitter .
```
- And the container should run well too, launching twitter via uvicorn, listening on port 8000 on your localhost, and exposing the port 8000 to your local machine too!
```bash
docker run twitter
```

❗️ You may see an error: This is because in your container (and contrary to your VM), the `.envrc` is not activating and therefore not loading the `.env` file into shell ENV variables. We could install direnv in the container, but it makes more sense to use docker to populate the environment only at run time:

```bash
docker run --env-file=.env twitter
```

☝️ Now that we are populating the environment at run time, we don't need the `.env` to be copied into the container, nor do we want it to be for security reason anyway

Here is where the concept of a `.Dockerignore` file becomes useful create one and it functions like a `.gitignore`. For example create one with the following and rebuild and rerun the container, if you attach a shell to the container you should see no `.env` files but the environment variables from it still available!

```bash
alembic
.env
.env.sample
.envrc
.alembic.ini
.README.md
```
☝️ Always try to keep your image as lean as possible

Now lets publish the port to make our api available

```bash
docker run --env-file=.env -p 8010:8000 twitter
```

We are mapping 8010 on our vm to 8000 inside the container. If we forward the port to our host machine we can now check out our running twitter app. All looks good, try an endpoint. Amazing we are plugged to our hosted database! Lets go one step further and run our api on cloud run.

🎉 **You should be able to read the list of all tweets by calling `GET /tweets` from your local machine's chrome app --> through your VM --> through your container --> to Google cloud SQL !**


# 4️⃣ Put your app in production through Google Cloud Run

🎯 Final step, we want to get rid of our VM entirely and run our app on Google Cloud Run!
🎯 We want to call our twitter API from our local machine's chrome app --> pinging our container directly inside Google Cloud Run --> pinging Google cloud SQL !

### Push to cloud run

First lets populate our related values in our `.env` file:

```bash
LOCATION=<USE_SAME_ZONE_THAN_YOUR_G_CLOUD_SQL>
HOSTNAME=$LOCATION-docker.pkg.dev
PROJECT_ID=<INSERT_YOUR_GCP_PROJECT_ID>
REPOSITORY=docker-hub
IMAGE_NAME=twitter
IMAGE_TAG=prod
IMAGE_FULL_TAG=$HOSTNAME/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:$IMAGE_TAG
```

❓ Now tag and push our image on cloud run

<details>
<summary markdown='span'>🎁 solution</summary>

```bash
docker tag twitter $IMAGE_FULL_TAG
docker push $IMAGE_FULL_TAG
```

</details>

### Create a Virtual Private Connection (VPC)

Here there is one additional complexity: we need to create a vpc connector to describe to cloud run where to route internal traffic.
So far, our VM was in the same VPC than your GCloud SQL, but for Cloud Run it's different:

Here is the gcloud command below to create a VPC named "twitter-connector":

```bash
gcloud compute networks vpc-access connectors create twitter-connector \
--region=europe-west1 \
--range=10.9.0.0/28 # CIDR range of internal addresses that are reserved for this connector.
```
### Deploy on Cloud Run

📚 Take a minute to read the [docs](https://cloud.google.com/run/docs/deploying)

You should see the couple of extra arguments from the lecture we'll have to use:

- `add-cloudsql-instances`: Speak by itself !
- `vpc-connector`: Needed when our cloudsql instance is on a Private IP network as we have [docs](https://cloud.google.com/sql/docs/mysql/connect-run?authuser=1#private-ip)
- `allow-unauthenticated`: We want our Twitter API to be publicly available (just for this challenge)
- `set-env-vars`: We need to pass the same env variable than when locally running Docker. However, gcloud does not accept "--env-file=.env" syntax, so we can either pass each variable manually, or create a yml with env variable. We decided to pass the required variables manually.


```bash
gcloud run deploy twitter-prod \
--image $IMAGE_FULL_TAG \
--vpc-connector=twitter-connector \
--region=europe-west1 \
--add-cloudsql-instances=twitter-prod \
--allow-unauthenticated \
--set-env-vars POSTGRES_DATABASE_URL=$POSTGRES_DATABASE_URL
```

The region we are putting our database, cloud run and database in the same region to minimise latency!

❗️ This still won't work: Try to see if you can spot the error message:
> _The user-provided container failed to start and listen on the port defined provided by the PORT=8080 environment variable_

<details>
<summary markdown='span'>💡 Hint to the failure</summary>

Cloud run needs our api to start on the `$PORT`, a special env variable that will be injected by cloud run at runtime. You need to update your Dockerfile with $PORT instead of hard-coding the port number.


</details>

🏁 Once you have fixed everything locally push and re-reun the deploy command you should be able to access your api managed by cloud run connected to your managed database!

# 5️⃣ Shut down everything that costs money
Go to [console.cloud.google.com](console.cloud.google.com) and try to shutdown the following services using the web user interface

- Your Cloud Run twitter-prod instance
- Your Cloud SQL twitter-prod database
- Your [VPC](https://console.cloud.google.com/networking/connectors/) twitter-connector
