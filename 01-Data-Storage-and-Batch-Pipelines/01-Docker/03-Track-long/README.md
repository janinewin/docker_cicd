# Basic Docker stack

After doing the `02-Docker-Compose` exercise, you should by now have a good understanding of a Docker Compose stack, and how to use it to set up a standard web app with a database and a FastAPI web server.
You should by now have a good understanding of a Docker Compose stack, and how to use it to set up a standard web app with a database and a FastAPI web server.

## Desired outcome

We are going to reuse these skills to set up a basic Docker Compose file `docker-compose.yml`. This file should have:

- a **Postgres** container with the data volume mapped, and environment variables set up.
- a **FastAPI** app container (OPTIONAL: with the code volume mapped and hot reload).
- an **Adminer** Docker container, configured to be connected to Postgres.

We'll reuse this Docker Compose in the second unit of the bootcamp to start loading a schema and data into this DB.
