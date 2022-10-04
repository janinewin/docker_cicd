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
RUN poetry install --only main

# Copy this package's Python files last
COPY ./ ./

# Set a default PORT environment variable to 8080
ENV PORT 8080

# Run the `FastAPI` application on port 8080
CMD poetry run uvicorn lwserverless.app:app --host 0.0.0.0 --port $PORT
```

**Then run `make build` to build the Docker image locally**.

## 3/5 Set up the Artifact Registry

**Note: if you've already set one up in the bootcamp, reuse it ♻️ and skip this step!**

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

- Run `make test`. **Note: it is expected that `test_runtimes_concurrency` fails, you'll make this one pass in the "App analytics" section later**
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
- Authentication: choose `Allow unauthenticated invocations`, this allows you to call this API from anywhere on the internet.
- Open `Container, Variables & Secrets, Connections, Security`
  - What should the container port be? Hint 💡 : what is the port the FastAPI app runs on? Check the `Makefile`, `run` target.
  - Keep the capacity at its lowest values, our app doesn't do much 🦶.
  - Maximum requests per container: **set it to 5**.
  - In the environment variables, set `HOME` to `/root`. By default, Google Cloud Run has a [strange behaviour](https://chanind.github.io/2021/09/27/cloud-run-home-env-change.html) we need to override.
- We're good to go! Click `CREATE` and let the magic happen. Once up and running (which can take up to 5 minutes), you'll get a URL for your service.

## App analytics

To understand the internals of Cloud Run, we are going to
- make a lot of requests to our app
- check on which instance of the app the request was made
- run some analytics on load time
- root cause why we're getting these statistics!

We've written some code for you that will generate statistics, given

- the Cloud Run API URL: type `https://serverless-something-ew.a.run.app/fast-run` and replace `serverless-something-ew.a.run.app` with your own URL
- the number of calls to the API you're making. It defaults to 25.

### The experiment

- Open an IPython interactive shell by just typing `ipython` in your terminal. Jupyter works too if you prefer.
- Import the function `generate_statistics` from the `lwserverless.statistics` package.
- Save your API URL in a variable called `api_url=...`. **Note: make sure you end the URL with /fast-run, we need the full API URL, not just the root**
- Let's run the following calls:

  ```python
  # Run a first "cold" call of 25
  stats_first_run_25, duration_first_run_25 = generate_statistics(api_url, 25)

  # Run the exact same call a second time
  stats_second_run_25, duration_second_run_25 = generate_statistics(api_url, 25)

  # Run a call for 15
  stats_run_15, duration_run_15 = generate_statistics(api_url, 15)

  # Run a call for 12
  stats_run_12, duration_run_12 = generate_statistics(api_url, 12)
  ```

You should notice that:

- The first call of 25 takes longer than the second call of 25. Why?

<details>
  <summary markdown='span'>💡 Hint</summary>

  We've set the minimum value of instances to 0. So when the instances aren't running, the first one needs to do a [cold start](https://cloud.google.com/run/docs/tips/general?hl=en#using_minimum_instances_to_reduce_cold_starts).
</details>

- How many different `app_instance_id` values are there? Look into `stats_second_run_25` by just typing it and evaluating it in the console.

<details>
  <summary markdown='span'>💡 Hint</summary>

  As many as the number of instances in Cloud Run! Check by doing `len(set(stats_second_run_25["app_instance_id"]))`
</details>

- Look into `stats_second_run_25` by just typing it and evaluating it in the console. What do you notice for the last 10 calls?

<details>
  <summary markdown='span'>💡 Hint</summary>

  We have a maximum of 3 (number of instances) x 5 (allowed concurrency of each instance) = 15 calls to our instances that can happen simultaneously to our cloud instances at most.

  Once the first 15 are filled, the following will have to wait for them to complete.
</details>

- Finally, what differences do you see in total runtime of the 15 versus 12 runs? Does it make sense?

<details>
  <summary markdown='span'>💡 Hint</summary>

  The calls all happen concurrently on 3 instances which can each accept 5 concurrent requests. Therefore running 2 requests or 5 requests on one instance shouldn't have a significant impact on the total runtime.
</details>

Once you're done, fill in the runtimes that you got in the previous exercise into the `lwserverless/runs.py` file and run `make test` to check your results.

**Well done! 🔆**
