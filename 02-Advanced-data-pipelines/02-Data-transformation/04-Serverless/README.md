# Serverless processing

In this exercise we'll build and deploy an application to a cloud provider's serverless framework for Docker containers.

- GCP: [Cloud Run](https://cloud.google.com/run).
- Amazon: [Fargate](https://aws.amazon.com/en/fargate/).
- Azure: [Container instances](https://azure.microsoft.com/en-us/services/container-instances/)

If your cloud isn't here, or if you'd prefer to go agnostic, adapt this exercise with an open source serverless framework. We recommend to install [OpenFaas through faasd](https://docs.openfaas.com/deployment/faasd/) in a separate server from the server you'll use to build your Docker images.

In the exercise below, we'll assume you're on GCP.

## Exploring Cloud Run

## Build a Docker image

- We'll build a small FastAPI application
- Two endpoints, one fast, one small (`time.sleep` with random values picked from different distributions)

## Deploy the Docker image to the Artifact registry

## Deploy the image to Cloud Run

- Settings to a concurrency of 20 per image
- 0 instance minimum, 3 instances maximum

## Run tests

- Set your API URL as an environment variable
- Call the API once
- Call the API asynchronously 100 times and notice how many instances are spawn, as well as latency per call
  - For each call, we'll give it a unique auto-incrementing ID, measure response time and store it

## Analytics

- Let's do some analytics on response times with Pandas and Matplotlib
- Is that expected?
