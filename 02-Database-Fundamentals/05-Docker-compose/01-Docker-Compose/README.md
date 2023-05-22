## Engineering context - Real life use
This exercise builds on top of work we did with single docker containers. Often times you will need to assemble together multiple services offering different features.
A perfect example as a data scientist, is a backend stack composed of:
- a backend server (API, ORM, Migration tools), such as fastAPI+SQLAlchemy+Alembic or Django which is an all in one web framework.
- a database which it is relational (PostgreSQL, MySQL) or NoSQL (Redis, MongoDB,...) or timeseries (InfluxDB, TimescaleDB)
- a workflow manager (Airflow, Dagster, Celery+RabbitMQ)
- a reverse proxy to handle SSL termination and various ingress rules (Traefik, NGinx, HAProxy)

Trying to do so in a piecewise manner is a hard project, usually distributed systems engineers or now more commonly called platform engineers would tackle this.

This is where orchestration comes to rescue us. Contrary to the previous challenge where you worked on a single docker container to build a single service (the Tweeter API), you can now build complex services by putting together those standalone services and have them collaborate.

Docker compose let's you do that with a simple `docker-compose.yaml` file properly configured.

This way you don't need a platform expert to spin up your experiment platform, you can stand it up yourself and be self-sufficient.

## End goal 🎯

This exercise aims at validating the docker compose fundamentals necessary to stand up and operate a multi-container applications.
To do so we will teach you how to:
- Pull a docker image remotely built
- Mount volumes to share data into a container
- Create a docker network to allow the containers to communicate between them
- Create multiple services SQL DB + Web server
- Configure those services via environement variables
- Use the docker-compose CLI

## Prerequisite

- The previously created `base-image-fastapi:dev` image stored in your Google container registry.
- Or you can also use this base image
`europe-west1-docker.pkg.dev/data-engineering-students/student-images/base-image-fastapi:dev`


# 1️⃣ - Services 🤲
This first task consists in creating your first service in your multi-container application. We will spin up the web API service that relies on the fastapi base image you previously built.
We also want to mount a directory inside the container that will point to our app directory so that we can simply update our server's code and reload it right away without having to tear down and rebuild the stack.

**❓ Create the web API service**

1. Open the `docker-compose-1.yml` file
1. Create a docker compose service named `webapi` with a [container name](https://docs.docker.com/compose/compose-file/#container_name) `fastapi` building the docker file included in this exercise named `dockerfile-fastapi`
1. Adjust the [restart policy](https://docs.docker.com/config/containers/start-containers-automatically/) to be `on-failure`
1. Expose the [port](https://docs.docker.com/compose/compose-file/#ports) 8000 so you can access your container from outside
1. Create a [volume](https://docs.docker.com/compose/compose-file/#volumes) mounting the directory `./api-no-database` into the container's directory `/app/api`
1. Override the container's command adding the `--reload` flag to restart the fastapi server on file changes
    ```bash
    uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
    ```
1. Build and run the docker compose stack
    ```bash
    # Validate the dockerfile
    docker-compose -f docker-compose-1.yml config
    docker-compose -f docker-compose-1.yml build
    docker-compose -f docker-compose-1.yml up
    docker container ls
    ```
1. Access your webserver, it should display a new `hello world`
1. Teardown the stack
    ```bash
    docker-compose -f docker-compose-1.yml down
    ```
    **🧪 Test your code with `make testTask1`**

    **💾 Save your work in progress on GitHub**
1. Now replace the local dockerfile used to build the stack by the remote [image](https://docs.docker.com/compose/compose-file/#image) you previously built `base-image-fastapi:dev`, remember to use the proper url to reference it.
1. Repeat steps 6&&
1. Enjoy!

**🧪 Test your code with `make testTask1`**

**💾 Save your work in progress on GitHub**

# 2️⃣ - Networking 🌉
When creating a docker compose stack, by default Docker will create a single network of type bridge associated with your docker compose stack with a name `<app_directory>_default`. Each container part of this network can reach out to each other using their container name (if absent use the service name).
At times you can end up needing multiple networks in a docker compose stack to isolate services from each other or to allow external services to access your internal stack networks.
Remember that in networking (in or outside of docker) you should be very conservative in your choice to reduce the exposure area of your stack.

**❓Create a docker network of type bridge and have our webapi service be part of this network.**

1. Copy the content of `docker-compose-1.yml` into `docker-compose-2.yml`
1. Create a custom [network](https://docs.docker.com/compose/compose-file/#networks) named `backend`
1. Assign the type bridge to the [driver](https://docs.docker.com/compose/networking/)
1. Update the webapi service to connect to the newly created network
1. Build and run the docker-compose stack
    ```bash
    #Validate the docker file
    docker-compose -f docker-compose-2.yml config
    docker-compose -f docker-compose-2.yml build
    docker-compose -f docker-compose-2.yml up
    docker container ls
    docker network ls
    docker inspect <network-id>
    ```
1. Access your webserver, it should display a new `hello world`
1. Teardown the stack
    ```bash
    docker-compose -f docker-compose-2.yml down
    ```

**🧪 Test your code with `make testTask2`**

**💾 Save your work in progress on GitHub**

# 3️⃣ - Database Service 🗄
Now that you have a solid backbone for the docker compose stack we can start adding one more service, a database service based on PostgreSQL.
We want to achieve two goals here:
- Configure the database properly by setting up a user, password and an actual database inside the container, using environment variables or a `.env` file
- Connect the server and the database by properly assigning the database to the network, creating a dependency on the web server with the database, properly constructing the url to reach the database inside the docker compose stack

**❓ 3.1) Add a database service**

1. Copy the content of `docker-compose-2.yml` into `docker-compose-3.yml`
1. We are now using the `app` folder instead of `api-no-database`, change the mounted dir accordingly in the docker compose file
1. Create a second service for the relational database, based on the postgreSQL 14.2 image
1. As described in the [image docs](https://hub.docker.com/_/postgres#:~:text=The%20only%20variable%20required%20is%20POSTGRES_PASSWORD%2C%20the%20rest%20are%20optional.), add the only mandatory env variable for this image: the superuser password
    ```yml
    environment:
      - POSTGRES_PASSWORD=postgres
    ```
1. Set the restart policy to `on-failure`
1. Let's add a small [health check](https://docs.docker.com/compose/compose-file/#healthcheck) to periodically check if our DB is alive, we'll use a small command to so do relying on [pg_isready](https://www.postgresql.org/docs/current/app-pg-isready.html). Adjust the parameters to **run it every 5s with a 5s timeout and 5 retries**
    ```bash
    # Check if postgres is ready
    pg_isready -U postgres
    ```
1. We prepared a small `01-init.sh` script for you to create a new custom DB using your env vars. 
    - To use it mount the volume `./database` into the following container dir `/docker-entrypoint-initdb.d/`
    - Why this specific dir ? The postgres image will run the scripts contained in this specific dir at [initialization time](https://hub.docker.com/_/postgres)
    - Change the script's permission to make it executable on your system `chmod +x database/01-init.sh`

1. Add the the [environment](https://docs.docker.com/compose/compose-file/#environment) variables required by `01-init.sh`:
    ```yaml

    - APP_DB_USER=lewagon
    - APP_DB_PASS=password
    - APP_DB_NAME=movies

    ```
1. [Map port](https://docs.docker.com/compose/compose-file/#expose) port 5432 of your container (where postgres runs by default) into port 5433 of your host (the VM). Why 5433? Just to make you think more deeply about which one means what 😈

1. Add network called `backend` of type `bridge` that links both `webapi` and `database`.

1. Finally, we need to set a [`depends_on` instruction](https://docs.docker.com/compose/compose-file/#depends_on) to the `webapi` service so it depends on the `database` service

🚀 Build and run the docker compose stack
```bash
# Validate the docker file
docker-compose -f docker-compose-3.yml config
docker-compose -f docker-compose-3.yml build
docker-compose -f docker-compose-3.yml up
```

```bash
# Inspect outcome
docker container ls
docker network ls
```

❓**3.2) Try to access your webserver**

🐛 It should not work and scream at you because can't connect to the DB!

Can you figure out why? Try to solve it if you can 🏋🏽‍♂️!

<details>
  <summary markdown='span'>💡 Hints</summary>

The API needs to have postgres POSTGRES_DATABASE_URL (which includes passwords etc...) see `database.py` line 6!

👉 Update your `docker-compose-3.yml` with the correct connection URL

    ```yml
    environment:
        - POSTGRES_DATABASE_URL=...# postgresql+psycopg2://<username>:<pwd>@<hostname>:<PORT>/<db_name>
    ```

💡 `+psycopg2` (the connection type) is not mandatory as its the default one, yet it's interesting to name it explicitly.

💡 What you your `<hostname>` in the context of docker-compose ? Give it a deep thought! 

</details>

Then, down and up again your docker-compose3.yml, and you should now have access again the endpoint! 

Voila! ✨


# 4️⃣ - Connect to the database 🗄

**❓ Connect to the database**

1. First check which port you forwarded in the docker compose or if you did not add it now! For example:
```yml
ports:
  - 5432:5432
```
1. Make sure that port is then also forwarded to your host machine!
1. Connect with dbeaver now using the enviroment variables you set in the docker-compose!

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W1D1/dockercompose-dbeaver.png" width=700>

1. Make sure you can interact with it and create a table!


## 🏁 When both DBeaver and fast API (on localhost:8000) are accessible from your local computer...

🧪 Store `test_ouput.txt`
```bash
make test
```

Push it for kitt to track your progress
```bash
git add .
git commit -m "finalized challenge 020101"
ggpush
```

Then `docker-compose down` to free-up ports for the next challenge!
