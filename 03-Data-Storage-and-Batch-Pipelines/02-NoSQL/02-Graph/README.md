Our goal today is to load a local instance of the Neo4j database using Docker Compose, and do Neo4j's official [movie graph tutorial](https://neo4j.com/developer/cypher/guide-cypher-basics/#cypher-movie-find). By the end, you'll be familiar with the power of graph databases for highly connected data, and how non-SQL query languages can help express graph / tree 🌳 patterns.

## 1️⃣ Run Neo4j in Docker Compose

Based on
- how we ran Postgres in previous days and exercises
- Neo4j's recommendations on [how to run their Docker image locally](https://neo4j.com/developer/docker/), which should give you hints on the used ports and environment variables. Use the following image: `neo4j:4.2.18-community`.


**❓Write a `docker-compose.yml` file to mimic what this Docker command does.**  
- 💡 Why bother with docker-compose when we can use a simple docker run ? Saving setup instructions explicitely in a yml file is much easier than remembering the docker command by heart. You'll be happy to find such "ready to work" template challenges later on !

<details>
  <summary markdown='span'>💡 Hints</summary>

- To connect, type `neo4j` as the username and `s3cr3t` as the password, that's how we interpret their `NEO4J_AUTH=neo4j/s3cr3t` environment variable
- 💯 Did you create a `.env` file to store the `NEO4J_AUTH` environment variable value? Or did you hardcode it in the `docker-compose.yml` 😡. If the latter, modify your `docker-compose.yml` file and create a `.env` file based on the template from the `env-template`!
- Do not forget to also open the 7687 port❗ This port handles the communication between the database and Neo4j, and for example handles the database connection.

</details>

🧪 docker-compose up the service, make sure you understand the logs, then open up [http://localhost:7474/browser/](http://localhost:7474/browser/) in your browser, does it work?

## 2️⃣ Play with Movies dataset
Type `:play movie graph` 🎥 and be guided directly in the browser! 💻


## 3️⃣ More Neo4j please! (Optional)

This [tutorial about building a recommendation engine](https://neo4j.com/developer/cypher/guide-build-a-recommendation-engine/) comes next for the bravest 😱.

<br> 

## 4️⃣ DGraph (Optional)

Want to try another graph database and exercise all the concepts seen so far ?

Let's try [DGraph](https://dgraph.io/)! DGraph is a modern, [open source](https://github.com/dgraph-io/dgraph) distributed graph database, written in Go.

They have fantastic documentation. It's a great opportunity to play more with a scalable graph database, as well as practice your Protobuf + gRPC game as their serialization layer uses Protobufs all the way. You'll notice that accessing the database is done through gRPC.

**Task** Add DGraph services to Docker-Compose and follow the tutorial below.

The documentation isn't always up to date, so to save you time, we give you the Docker Compose services below. We use the [Docker Compose setup](https://dgraph.io/docs/deploy/single-host-setup/#run-using-docker-compose-on-single-aws-instance) and add the web browser interface (Ratel).

```yml
  zero:
    image: dgraph/dgraph:v21.12.0
    volumes:
      - /tmp/data:/dgraph
    ports:
      - 5080:5080
      - 6080:6080
    restart: on-failure
    command: dgraph zero --my=zero:5080
  alpha:
    image: dgraph/dgraph:v21.12.0
    volumes:
      - /tmp/data:/dgraph
    ports:
      - 8080:8080
      - 9080:9080
    restart: on-failure
    command: dgraph alpha --my=alpha:7080 --zero=zero:5080 --security whitelist=0.0.0.0/0
  ratel:
    image: dgraph/ratel:v21.12.0
    ports:
      - 8000:8000
    command: dgraph-ratel
```

Follow the [Get started with DGraph](https://dgraph.io/docs/tutorials/) tutorial, from the introduction all the way to native geolocation features. 🚀.
