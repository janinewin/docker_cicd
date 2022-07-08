# Serverless processing

In this exercise we'll build and deploy an application to a cloud provider's serverless framework for Docker containers.

- GCP: [Cloud Run](https://cloud.google.com/run).
- Amazon: [Fargate](https://aws.amazon.com/en/fargate/).
- Azure: [Container instances](https://azure.microsoft.com/en-us/services/container-instances/)

If your cloud isn't here, or if you'd prefer to go agnostic, adapt this exercise with an open source serverless framework. We recommend to install [OpenFaas through faasd](https://docs.openfaas.com/deployment/faasd/) in a separate server from the server you'll use to build your Docker images.

In the exercise below, we'll assume you're on GCP. The steps are fairly similar between all Docker image serverless providers.

## Step 1/5 Write our application locally

We've built a small FastAPI application. It has two endpoints, one fast, one small (the code just artificially "sleeps" with random values picked from different distributions, to mimic its behaviour if it were doing some heavy calculations in the background)

**Update `lwserverless/app.py` and give a value to `wait_time_seconds` in the functions `fast_run` and `slow_run`**. This determines how much time you'd like each endpoint to take to respond.

<details>
  <summary markdown='span'>💡 Hint</summary>

  - A value between 0.5 and 2 for fast is good
  - A value between 2 and 5 for slow is good
</details>

Run the app locally with `make run`. Now let's check that the endpoints work:

- Run `curl http://127.0.0.1:8080/slow-run -w %{time_total}`
- Run `curl http://127.0.0.1:8080/fast-run -w %{time_total}`

You should notice four things:

1. We've added the option `-w %{time_total}` to `curl` which prints the total time the endpoint takes in seconds, that is handy as we're mimicking it taking some time!
2. Write down the amount returned by the `curl` command in both calls. Is `/slow-run` taking more time than `/fast-run`? If so, good 🙌!
3. See the `app_instance_id` returned by the app, it should be the same as we're running the same instance of the application.
4. Now stop the app and re-run it with `make run`. Make another curl call (either one above works). Is the `app_instance_id` the same? It shouldn't! We're running a new instance of the application. This will help us identify which instance of the application is running in the cloud for the purposes of this exercise. 

## Step 2/5 Build the Docker image

We've written the Docker image for you, see the `Dockerfile` contents below. Run through its lines and comments and make sure you understand each step. Then paste it into the `Dockerfile` file.

```Dockerfile
# Start from Python 3.8.10, the slim version is usually enough (stripped from packages that aren't useful for our purpose)
# and way smaller than the non-slim version
FROM python:3.8.10-slim

# Setting PYTHONUNBUFFERED to 1 is useful for logs
# See https://stackoverflow.com/a/59812588
ENV PYTHONUNBUFFERED 1

# Set a working directory that maps our data-engineering-challenges repository structure
WORKDIR /repo/02-Advanced-data-pipelines/02-Data-transformation/01-Serverless/

# Install Poetry
RUN pip3 install --upgrade --no-cache-dir pip \
    && pip3 install poetry

# Copy the installation files and local dependencies first (in this case there aren't local dependencies)
COPY poetry.lock pyproject.toml ./

# Now we are ready to install the packages
RUN poetry install --no-dev

# Copy this package's Python files last
COPY ./ ./

# Run the `FastAPI` application on port 8080
CMD ["poetry", "run", "uvicorn", "lwserverless.app:app", "--port", "8080"]
```

**Then run `make build` to build the Docker image locally**.

## 3/5 Set up the Artifact Registry

We're going to deploy our application to the artifact registry.

- Go to your browser > Cloud Console > Artifact Registry
  - Click `CREATE REPOSITORY`
  - Give it a unique name like `lw-registry-<your Github username>`
  - Format: "Docker"
  - Pick a local region. For instance, if you're in Europe, select `europe-west1`
- Now that you have a repository, click on it to go to its dedicated page, then click `SETUP INSTRUCTIONS`. This should give you a `gcloud auth configure-docker ...` command that you need to run in your terminal.
- Click on the "Copy" icon in the top right of your registry and write the value in the `Makefile`, in the `REGISTRYPREFIX` variable.

<img src="https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/assets/lw-artifact-registry-copy.png" alt="Copy" width=600>


## 4/5 Deploy the image to the artifact registry

- Run `make test`
- We're all set on the browser side, let's go back to the terminal and push our first Docker image to our remote repository now.

Let's do:
- Run `make tag`, which will tag our local image with the remote repository prefix.
- Run `make push`, which will push our image to the remote repository.

Once done with the upload, refresh your browser page, you should see a Docker image showing up in the registry.

<img src="https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/assets/lw-artifact-registry-images.png" alt="Images" width=600>

## 5/5 Deploy the application in Cloud Run

Almost there! In the browser, go to the Cloud Run service and click `CREATE SERVICE`.

<img src="https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/assets/lw-cloud-run-create.png" alt="Create" width=600>

- In "Deploy one revision from an existing container image", click `SELECT`. In the `Artifact Registry` tab, you should find your image 🤙. 
- Give it a unique service name
- Pick a local region.
- Select "CPU is only allocated during request processing" (should be selected by default).
- Autoscaling: 0 (minimum) to 3 (maximum) instances
- Open `Container, Variables & Secrets, Connections, Security`
  - What should the container port be? Hint 💡 : what is the port the FastAPI app runs on? Check the `Makefile`, `run` target.
  - Keep the capacity at its lowest values, our app doesn't do much 🦶.
  - Maximum requests per container: **set it to 5**.
- We're good to go! Click `CREATE` and let the magic happen.

## App analytics

To understand the internals of Cloud Run, we are going to
- make a lot of requests to our app
- check on which instance of the app the request was made
- run some analytics on load time

- Set your API URL as an environment variable
- Call the API once
- Call the API asynchronously 100 times and notice how many instances are spawn, as well as latency per call
  - For each call, we'll give it a unique auto-incrementing ID, measure response time and store it

