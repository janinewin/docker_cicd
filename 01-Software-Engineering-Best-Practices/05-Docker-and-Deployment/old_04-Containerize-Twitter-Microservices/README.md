Welcome in this new challenge!

The goal of this exercise is too containerize our twitter microservices basic application.
You are provived with the solution, you will need to container each micro service & link them thanks to `docker compose`.

Quick remember about the previous exercice.
There are 2 services:
- The service `tweets` which is a basic REST API in which we can CREATE, READ, UPDATE AND DELETE tweets on a sqlite database
- The service `users` where we have a basic `users` back-end structure in which we  we can add users, access to their tweets and look at their tweet timeline.

## Tweets Microservice

First, let's navigate to the right folder

```bash
cd ~/code/<user.github_nickname>/04-Microservices-and-Containers/04-Containerize-Twitter-Microservices
code .
```


Let`s start by containerizing our first service tweets.

``` bash

cd tweets

```

Let's create our `Dockerfile`.

``` bash

touch Dockerfile

```

Let`s store all our python dependencies within a requirements.txt

``` bash

pipenv lock -r > requirements.txt

```

Time to fill your Dockerfile! What file do you need to put in your in image ?

Remember all the step you need to create a docker image.

1 - Choose an image within the docker hub, based on your python version
2 - Copy all the files you need in your image
3 - Install everything you need in your container
4 - Don`t forget about the last command we need to put in our file..which will be the last command our container will run!

Please, don`t hesitate to go back to this morning and really try to find the solution before looking at the hints below


```hints

FROM python:3.8-buster

COPY models.py /models.py
COPY routes.py /routes.py
COPY wsgi.py /wsgi.py
COPY user.db /user.db
COPY migrations /migrations

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD flask run --host 0.0.0.0


```

Good job!
Now time to create our image with

```hints
docker build -t tweet_container .
```

Let`s launch a container to check that everything works:

```hints
docker run -p 5000:5000 tweet_container
```


## Users Microservices

Let`s now work on our users microservices.

``` bash

cd ../users

```

Let`s create our `Dockerfile`.

``` bash

touch Dockerfile

```

Let`s store all our python dependencies within a requirements.txt

``` bash

pipenv lock -r > requirements.txt

```

Now let`s fill our Dockerfile.


```hints
docker build -t user_container .
```

Let`s launch a container to check that everything works:

```hints
docker run -p 5000:5000 user_container
```

If you wanna access to your tweets timeline and your users/tweets endpoints, well, we would need to link both our containers properly...let`s see how to do it

## Linking both Microservices with Docker Compose

Let`s finish the work and link properly how 2 micro services with `docker compose`

Let`s create our file

``` bash
cd .. &&
touch docker-compose.yml
```


the first thing we need to add is the version.

```yml
version: "3.8"
```

We will add then some volumes for data persistense so that our databases will kept being updated even if our countainers get killed.

```yml
volumes:
  userapp:
  tweeterapp:
```

Let`s now create our first service with the `services` argument:
```yml
version: "3.8"

volumes:
  userapp:
  tweeterapp:

services:
  tweeter-service:
    container_name: tweet-service
    build:
      context: tweets
    ports:
      - "5002:5000"
    volumes:
      - tweeterapp:/tweeterapp
    restart: always

     user-service:
    container_name: users-service
    build:
      context: users
    ports:
      - "5000:5000"
    volumes:
      - userapp:/userapp
    restart: always

```

Good job!

Last thing we need to do is to replace the TWEETER_API_URL in the `users/routes.py` with our new url.
Replace `http://localhost:5002` with `http://tweet-service:5002`


Game over! Now we can instanciate and launch our containers in one command:

```bash

docker compose -f docker-compose.yml build
```


And to launch our containers :

```bash

docker compose -f docker-compose.yml up
```

Good job!


## Bonus - Implementing Postgres DB

Let's replace our dummy SQLite database  with a production ready database.

To do so, for each of our microservice, we will plug a postgres container to host our database.


### Step 1 - Removing sqlite db

Start by removing our `tweet.db` and `user.db` file database, as well as the `migrations` folders we created previously.


### Step 2 - Updating Tweet service

Let's add the following code in the `docker-compose.yml`

```yaml
version: "3.8"
services:
  tweet-db:
    image: postgres:14-alpine
    container_name: tweet-db
    networks:
      - default
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_PASSWORD=password
  tweet-service:
    container_name: tweet-service
    build: .
    networks:
      - default
    depends_on:
      - tweet-db
    ports:
      - 5001:5000
    volumes:
      - .:/code
    environment:
      - DATABASE_URL=postgresql://postgres:password@tweet-db:5432/twitter_db
      - FLASK_RUN_HOST=0.0.0.0
      - FLASK_ENV=development
volumes:
  postgres_data:
```

Here, we are adding a new `tweet-db` service which contains a postgres container that will run our database.

Notice how we link the two containers in the `environment` section.

Let's also update the content of the Dockerfile.


```dockerfile
FROM python:3.8-buster

RUN pip install --upgrade pip

WORKDIR /code
COPY . /code

RUN pip install -r requirements.txt

EXPOSE 5001

ENV FLASK_APP wsgi.py

CMD flask run --host 0.0.0.0
```

We are here exposing the port 5001 from our container.

Let's now build our two containers.

```bash
cd tweets && docker compose build
```

Let's run our containers in the background

```bash

docker compose up -d

```

Double check it actually launched your tech stack: run `docker ps` to see the containers running on your host.

<details><summary markdown='span'>View solution</summary>

You should see your `tweet-service` and `tweet-db` containers running.

</details>

 Let's create our database

- connect to the `tweet-db` container: `docker exec -it tweet-db psql -U postgres`
- create databases for development and test environments: in the `psql` prompt, type:
  - `CREATE DATABASE twitter_db;`
  - Exit the `psql` prompt: `\q` + **Enter**

Eventually, run your migrations:
 ```bash
docker-compose run tweet-service flask db init
docker-compose run tweet-service flask db migrate
docker-compose run tweet-service flask db upgrade
```

<details><summary markdown='span'>View solution</summary>

You should get an output like this:

```bash
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 3812f6776f12, Create tweets table
```

Let's now launch our containers and test your app!

```bash

docker compose up
```

And go to http://localhost:5001/tweets

TADAM! You can now add some tweets to your database using the `create` endpoints and redo exactly the same steps for the users service!


<details><summary markdown='span'>View solution</summary>

Let's add the following code in the `docker-compose.yml`

```yaml
version: "3.8"


services:
  user-db:
    image: postgres:14-alpine
    container_name: user-db
    networks:
      - default
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_PASSWORD=password

  user-service:
    container_name: user-service
    build:
      context: .
    networks:
      - default
    depends_on:
      - user-db
    volumes:
      - .:/code
    ports:
      - 5000:5000
    environment:
      - DB_URL=postgresql://postgres:password@user-db:5432/user_service
      - FLASK_RUN_HOST=0.0.0.0
      - FLASK_ENV=development

volumes:
  postgres_data:

```

Here, we are adding a new `user-db` service which contains a postgres container that will run our database.

Notice how we link the two containers in the `environment` section.

Let's also update the content of the Dockerfile.

```dockerfile
FROM python:3.8-buster

RUN pip install --upgrade pip

WORKDIR /code
COPY . /code

RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP wsgi.py

CMD flask run --host 0.0.0.0
```

We are here exposing the port 5001 from our container.

Let's now build our two containers.

```bash
cd users && docker compose build
```

Let's run our containers in the background

```bash

docker compose up -d

```

Double check it actually launched your tech stack: run `docker ps` to see the containers running on your host.

<details><summary markdown='span'>View solution</summary>

You should see your `user-service` and `user-db` containers running.

</details>

 Let's create our database

- connect to the `user-db` container: `docker exec -it user-db psql -U postgres`
- create databases for development and test environments: in the `psql` prompt, type:
  - `CREATE DATABASE user_service;`
  - Exit the `psql` prompt: `\q` + **Enter**

Eventually, run your migrations:

 ```bash
docker-compose run user-service flask db init
docker-compose run user-service flask db migrate
docker-compose run user-service flask db upgrade
```

<details><summary markdown='span'>View solution</summary>

You should get an output like this:

```bash
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 3812f6776f12, Create users table
```

Let's now launch our containers and test your app!

```bash

docker compose up
```

And go to <http://localhost:5000/user/all>

TADAM! You can now add some users to your database using the `create` endpoints.
