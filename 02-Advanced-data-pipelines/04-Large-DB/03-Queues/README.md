# Queues, PubSub

When there is too much data to handle for our workers, when data flow needs to be managed, or processing scheduled, queues come to the rescue.

## A simple Python queue: Huey

- Create a simple FastAPI application
- Add a periodic task
- Add a worker queue

## Queuing patterns in RabbitMQ

- Add RabbitMQ to a Docker Compose
- Write the PubSub example with a chat application that parses hashtags
  - FastAPI page with a form to publish a new message
  - Refresh the page to load newer messages, by topic
  - Select a bunch of topics that you care about

## GCP specific: Google PubSub

- Replace your RabbitMQ implementation with a shared Google PubSub project
- Talk to your peers over a shared PubSub!
s
