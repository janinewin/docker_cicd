# Week 1 Day 1: Docker Advanced


## Engineering context - Real life use
This exercise builds on top of the previous exercise about single docker containers. Often times you will need to assemble together multiple services offering different features.
A perfect example as a data scientist, is a backend stack composed of:
- a backend server (API, ORM, Migration tools), such as fastAPI+SQLAlchemy+Alembic or Django which is an all in one web framework.
- a database which it is relational (PostgreSQL, MySQL) or NoSQL (Redis, MongoDB,...) or timeseries (InfluxDB, TimescaleDB)
- a workflow manager (Airflow, Dagster, Celery+RabbitMQ)
- a reverse proxy to handle SSL termination and various ingress rules (Traefik, NGinx, HAProxy)

Trying to do so in a piecewise manner is a hard project, usually distributed systems engineers or now more commonly called platform engineers would tackle this.

This is where orchestration comes to rescue us, with the previous exercise where you worked on a single docker container - a single service (usually), you can now build complex services by putting together those standalone services and have them collaborate.
Docker compose let's you do that with a simple yaml file properly configured.

This way you don't need a platform expert to spin up your experiment platform, you can stand it up yourself and be self-sufficient. You'll be a strong independent data scientist (hopefully!)

## Background
This exercise aims at validating the docker compose fundamentals necessary to stand up and operate a multi-container applications.
To do so we will teach you how to:
- Pull a docker image remotely built
- Mount volumes to share data into a container
- Create a docker network to allow the container's to communicate between them 
- Create multiple services SQL DB + Web server
- Configure those services via environement variables
- Use the docker compose CLI

## End goal

By the end of this exercise you should be able to:

- Understand the concept of docker compose
- Understand the concept of volumes
- Understand the concept of networking
- Know how to create a functional docker compose stack
- Be familiar with the docker compose CLI


## Setup

For this exercise you will need:

- Working docker installation

Run the following command
```
$ docker run hello-world 
```

Expected output:

```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
7050e35b49f5: Pull complete
Digest: sha256:80f31da1ac7b312ba29d65080fddf797dd76acfb870e677f390d5acba9741b17
Status: Downloaded newer image for hello-world:latest
Hello from Docker!
This message shows that your installation appears to be working correctly.
```
- Text/Code editor - VSCode
- Working github setup
- Working GCP setup with docker authentication
    1. Enable container registry: [Link](https://cloud.google.com/container-registry/docs/enable-service)
    2. Authentication using gcloud credentials helper: [Link](https://cloud.google.com/container-registry/docs/advanced-authentication#gcloud-helper)
- The previously created `base-fastapi:dev` image stored in your Google container registry


# Task 1: Services
This first task consists in creating your first service in your multi-container application. We will spin up the webapi service that relies on the fastapi base image you previously built.
we also want to mount a directory inside the container that will point to our app directory so that we can simply update our server's code and reload it right away without having to tear down and rebuild the stack.

Please do the following:
1. Create a docker compose service named `webapi` with a container name `fastapi` building the docker file included in this exercise named `dockerfile-fastapi`
2. Adjust the [restart policy](https://docs.docker.com/config/containers/start-containers-automatically/) to be `on-failure`
3. Expose the port 8000 so you can access your container from outside 
4. Create a volume mounting the directory `./app-no-database` into the container's directory `/server/app`
5. Override the container's command adding the `--reload` flag to restart the fastapi server on file changes 
```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
6. Build and run the docker compose stack
```
Validate the docker file
docker compose -f docker-compose-1.yml config
docker compose -f docker-compose-1.yml build
docker compose -f docker-compose-1.yml up
docker container ls
```
7. Access your webserver it should display a new `hello world`
8. Teardown the stack 
```
docker compose -f docker-compose-1.yml down
```
9. Now replace the local dockerfile used to build the stack by the remote image you previously built `base-fastapi:dev`, remember to use the proper url to reference it.
10. Repeat steps 6&&
11. Enjoy!



# Task 2: Networking
When creating a docker compose stack, by default Docker will create a single network of type bridge associated with your docker compose stack with a name `<app_directory>_default`. Each container part of this network can reach out to each other using their container name (if absent use the service name).
At times you can end up needing multiple networks in a docker compose stack to isolate services from each other or to allow external services to access your internal stack networks.
Remember that in networking (in or outside of docker) you should be very conservative in your choice to reduce the exposure area of your stack

For this task we'll create a docker network of type bridge and have our webapi service be part of this network.

1. Create a custom network named `backend`
2. Assign the type bridge to the driver
3. Update the webapi service to connect to the newly created network
4. Build and run the docker compose stack
```
Validate the docker file
docker compose -f docker-compose-2.yml config
docker compose -f docker-compose-2.yml build
docker compose -f docker-compose-2.yml up
docker container ls
docker network ls
```
5. Access your webserver it should display a new `hello world`
6. Teardown the stack 
```
docker compose -f docker-compose-2.yml down
```

# Task 3: Database Service
Now that you have a solid backbone for the docker compose stack we can start adding one more service, a database service based on PostgreSQL. 
We want to achieve two goals here:
- Configure the database properly by setting up a user, password and an actual database inside the container, using environement variables or a `.env` file
- Connect the server and the database by properly assigning the database to the network, creating a dependency on the web server with the database, properly constructing the url to reach the database inside the docker compose stack

Please do the following:
1. Create a second service for the relational database, based on the postgreSQL 14.2 image
2. Set the restart policy to `on-failure` 
3. Let's add a small health check to periodically check if our DB is alive, we'll use a small command to so do relying on [pg_isready](https://www.postgresql.org/docs/current/app-pg-isready.html). Adjust the parameters to **run it every 5s with a 5s timeout and 5 retries**
```
    # Check if postgres is ready
    pg_isready -U postgres
```
4. We prepared a small script for you to create a new custom DB using your env vars. To use it mount the volume `./database` into the following container dir `/docker-entrypoint-initdb.d/` why this specific dir ? The postgres image will run the scripts contained in this specific dir at [initializtion time](https://hub.docker.com/_/postgres)
5. Setup the environment variables, postgres has default credentials, we will use them to create our own admin user and our own database
```
    - POSTGRES_USER=postgres
    - POSTGRES_PASSWORD=postgres
    - APP_DB_USER=goldenspice
    - APP_DB_PASS=whatsupdawg
    - APP_DB_NAME=gangstadb
```
6. Expose port 5432
7. Add network `backend` to the service
8. We need to set a dependency order, to do so add a `depends_on` instruction to the webapi service, so it depends on the database service

9. Build and run the docker compose stack
```
Validate the docker file
docker compose -f docker-compose-3.yml config
docker compose -f docker-compose-3.yml build
docker compose -f docker-compose-3.yml up
docker container ls
docker network ls
```
10. Access your webserver it should not work and scream at you because can't connect to the DB
11. While the stack is running, update the `database.py` file with the right connection string, save the file ( it will reload the server ), now access again the endpoint. Voila!