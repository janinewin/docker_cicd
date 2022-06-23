# Graph databases

You've made it to the bonus exercise of the day, 💪 🧠 ! This means you don't need as much guidance as in the previous exercises.

Our goal today is to load a local instance of the Neo4j database using Docker Compose, and do Neo4j's official [movie graph tutorial](https://neo4j.com/developer/cypher/guide-cypher-basics/#cypher-movie-find). By the end, you'll be familiar with the power of graph databases for highly connected data, and how non-SQL query languages can help express graph / tree patterns.

## Run Neo4j in Docker Compose

Based on
- how we ran Postgres in previous days and exercises
- Neo4j's recommendations on [how to run their Docker image locally](https://neo4j.com/developer/docker/), which should give you hints on the used ports and environment variables

Write a `docker-compose.yml` file to mimic what this Docker command does.

Open up [http://localhost:7474/browser/](http://localhost:7474/browser/) in your browser, does it work?

To connect, type `neo4j` as the username and `s3cr3t` as the password, that's how we interpret their `NEO4J_AUTH=neo4j/s3cr3t` environment variable

## Best practice

Did you create a `.env` file to store the `NEO4J_AUTH` environment variable value? Or did you hardcode it in the `docker-compose.yml`. If the latter, modify your `docker-compose.yml` file and create a `.env` file based on the template from the `env-template`!

## Load the dataset

Type `:play movie graph` and be guided directly in the browser!


## More Neo4j please!

This [tutorial about building a recommendation engine](https://neo4j.com/developer/cypher/guide-build-a-recommendation-engine/) comes next for the bravest.
