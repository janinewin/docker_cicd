# Load Testing, Logging, Monitoring

The goal of this exercise is to give you the necessary tools to load test, log, monitoring your systems.
This way, you'll be able to understand where your system is the most likely to break using load testing.
You'll also be able to collect the logs, so no information is lost in the void. Finally, you'll set up a simple monitoring system that will alert you and keep track of all your system malfunctions.

For this exercise, we'll only scratch the surface as this is a complex and time-consuming topic. We'll rely on some already provided snippets and codebase.

## Setup
All you need for this exercise is a working docker setup

## Task 1: Load testing & server scaling

Let's start by load testing the fastapi server included with this exercise in the app folder. Disclaimer this server is buggy, and we'll see how to address those issues during this exercise. So don't worry if this is not working flawlessly. This will be your job!

In order to load test, we'll use a package named [Locust](https://locust.io/). We'll create a docker compose stack to run our server and locust and create a small locust file that will simulate a user's behavior.

### Create the docker compose stack
in the `docker-compose-task-1.yml` please do the following:

**1. API Service**
1. Add the API service, running the fastapi server (we'll keep things on your local file system for this one).
 - create a service named: `webapi`
 - Building the docker image `Dockerfile-fastapi`
 - With a `on-failure` restart policy (we'll actually see it in action today!)
 - Expose ports 8000
 - Mount the `./app` dir into the `/app/app` container dir
 - Command: `["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]`


**2. Locust Service**

[Documentation](https://docs.locust.io/en/stable/running-in-docker.html)

Using the documentation, add the following snippet to your docker compose file. It creates a master and worker node to run your load test. We won't need more.
```
  master:
    image: locustio/locust
    ports:
     - "8089:8089"
    volumes:
      - ./:/mnt/locust
    command: -f /mnt/locust/locust.py --master -H http://01-load-testing-webapi-1:8000

  worker:
    image: locustio/locust
    volumes:
      - ./:/mnt/locust
    command: -f /mnt/locust/locust.py --worker --master-host master
```
You can adjust the host `-H http://01-load-testing-webapi-1:8000` as needed for Locust depending on your container and service name


**3. Build and test**
- Build the stack `docker-compose -f docker-compose-task-1.yml build`
- Run the stack `docker-compose -f docker-compose-task-1.yml up`
- If you head to http://localhost:8000 you should see hello world
- If you head to http://localhost:8089 you should see the locust homepage

**3. Creating a load testing scenario**
We now need to set up the load test. To do so let's refer Locust's [documentation](https://docs.locust.io/en/stable/writing-a-locustfile.html).
The `locust.py` at the root of the folder defines the load testing scenarios and configuration.
It simply defines the simulated user behavior for locust to use.

In the `WagonFakeUser` class
- Configure the wait time to be between 1,5; the user will wait between 1 & 5 seconds before firing a new request.
```
    wait_time = between(1, 5)
```
- Add 4 tasks to hit the 4 endpoints of our server:
```
task: index - GET /
task: compute_addition - POST /addNumbers/ JSON Body: { "a": <random Int>[-1000, 1000], "b": <random Int>[-1000, 1000]}
task: compute_fib - POST /computeFib/ JSON Body: { "iteration": <random Int>[0, 30]}
task: kill_the_server - GET /oom/
```
- Adjust each task priority with a `@task(<PRIORITY>)` decorator. The higher the relative number, the most likely the simulated user will run it.


**4. Load testing**
- Build and run the docker compose stack
- Head to localhost:8000 -> you should see `hello world`
- Head to localhost:8089 -> This is the locust interface
- Configure the load test host. It should be in the form of:
```
http://01-load-testing-webapi-1:8000
http://<your-service-name>:<export_port>
```
Let's find the server breaking point; API failures are expected since the logic has an issue on purpose.
(depending on your machine, the breaking point will be different)
- Simulate 1 user and observe the test; the server should handle it fine; click the stop button
- Simulate 10 users with a spawning rate of 1
- Simulate 50 users with a spawning rate of 3
- Simulate 100 users with a spawning rate of 10

It should probably be broken by now; congrats! i.e., the server is stalling, and nothing happens anymore in the logs, and the service is defaulting; if it is not stalling, keep going to infinity and beyond.
You should also notice the restart policy kicking in when the server crashes.

The reason is that the server is running a single node and is not capable of handling all the users we throw at it; we need to create more nodes/workers to be able to handle the load.

## Task 2: Handling more load
To solve the problem we faced in task 1, we'll introduce [Gunicorn](https://gunicorn.org/) a WSGI HTTP server that will help us create more uvicorn workers and manage them.


Gunicorn will act as a process manager for our uvicorn+fastAPI server basically it will handle the whole lifecycle of our server [you should read more about it here](https://www.uvicorn.org/deployment/#using-a-process-manager)

Fortunately for us, the FastAPI team already provided the resources to run this production-like setup on our machine; let's use that.

**1. Switch up the stack**

We will rely on this [docker image](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker#uvicorn-gunicorn-fastapi) - It is a performance auto-tuned gunicorn-uvicorn-fastapi stack (lots of unicorns here).


For this task, use the docker-compose-task-2.yml

**1. Update the webapi service**

- Change the dockerfile built to `Dockerfile-gunicorn-poetry`, a multistage build for poetry, our dependencies and relying on the unicorn image.
- Add restart policy: `on-failure`
- Export port `8000:8000`
- Map the volume `./app` to `/app/app`
- Add the following env vars
```
      - PORT=8000
      - PYTHONBUFFERED=1
```
- Build and run the stack - You should see a lot more output and notice the different uvicorn workers. it's almost magical (it just means someone made it magical for us)
What we just did is called **horizontal scaling** - we added more replicas without adding more resources
- Re-run the previous load testing scenarios; the breaking point should be pushed a lot further - you will hit one eventually because your machine can't infinitely scale vertically - you can use Kubernetes for that.
Some workers will get killed in the process due to our server code, and you should see how they are spawned back up by gunicorn
Our job here is done.


Also, a few numbers:
1 RPS = 1 Request per second
if you have a service receiving 1 RPS - it adds to 86400 requests a day (it is a successful service here)

20 RPS - 1.7 million requests a day

Ikea.com had 161 Million visits in May 2022 [link](https://www.similarweb.com/website/ikea.com/#overview); this is equivalent to 62 RPS.


## Task 3: Logging
Now let's try to get some more logging going to debug our issues. Logging is a fairly complex topic and requires some attention to setup properly when using different systems together.
For us, we are using FastAPI -> Uvicorn -> Gunicorn, which means we have to propagate and handle the logs properly between each layer to be able to get them.

Here we'll start from an already existing configuration and extend it. They are many ways of doing that, such as creating a [gunicorn config file](https://docs.gunicorn.org/en/stable/settings.html), a dict config or setting it in the code. We choose to do a specific logging file to isolate the logging configuration from the rest of the system.

We aim to log all the incoming requests and errors to a file for a later inspection.

Head to the `logging.conf` file
we'll rely on the python documentation to create the basic section [documentation](https://docs.python.org/3/library/logging.config.html#configuration-file-format)


**1. Sections**
- Create the following sections
1. `loggers` with 3 loggers `root`, `gunicorn.error`, `gunicorn.access`
2. `handlers` with 3 handlers `console`, `error_file`, `access_file`
3. `formatters` with 2 formatters `generic`, `access`

**2. Configuration**

_Loggers_

Each logger must define a default configuration composed of a `level`, a `handler` and the `propagate=1`
```
[logger_<name>]
level=
handlers=
propagate=
```
Root Logger

```
- Debug level
- console handler
```

gunicorn.error logger
```
- Debug level
- handlers error_file and console
- Propagate to true (1)
- qualname=gunicorn.error

```

gunicorn.access logger
```
- Debug level
- handlers error_file and console
- Propagate to true (1)
- qualname=gunicorn.access
```

_Formatters_

Add the following formatters - they define the format of the output and can be finicky to adjust
```
[formatter_generic]
format=%(asctime)s [%(process)d] [%(levelname)s] %(message)s
datefmt=%Y-%m-%d %H:%M:%S
class=logging.Formatter

[formatter_access]
format=%(message)s
datefmt=%Y-%m-%d %H:%M:%S
class=logging.Formatter
```

_Handlers_

Our handlers are responsible for redirecting the log object to the appropriate output

console handler
```
Class: StreamHandler
formatter: generic
args: (sys.stdout,)
```

error_file handler
```
Class: logging.FileHandler
formatter: generic
args: ('/app/app/logs/error.log',) -> this is where our error log file will be output
```

access_file handler
```
Class: logging.FileHandler
formatter: access
args: ('/app/app/logs/access.log',) -> this is where our access log file will be output
```

Your logging configuration should now be ready to be used.

**3. Configuration update**
To use this configuration for our stack, we need to pass the location of our config file as a command argument to do so
Add 2 more environment vars to the docker compose file

``` - LOG_LEVEL=DEBUG
    - GUNICORN_CMD_ARGS=--log-config /app/app/logging.conf
```

This will adjust the logging level to `DEBUG` and tell Gunicorn where to find our logs

- Run the stack, and trigger a load test; you should see the logs file in your local file system in the logs directory
You can also add a few lines of code in your main.py to test the log output
```
logger.info("this is an info message")
logger.warning("this is a warning message")
logger.error("this is an error message")
```

**4. Grep**

now that we have our logs, we can use one of the most useful commands while groveling through the logs: `grep`
>grep searches the input files for lines containing a match to a given pattern list. When it finds a match in a line, it copies the line to standard output (by default), or whatever other sort of output you have requested with options.

1. Find all the errors in the log file, sort them
```
grep "STR_TO_LOOK_FOR" <file> | sort
```
2. Find all the failing requests in the access log (status code != 200) OR find the most frequently called endpoint
```
    grep -v -e 200  <file> # -v is invert match and -e is pattern matching
```

## Task 4: Monitoring

Now that we have our load test & logging, we want to make sure that we'll get alerted and have a trace when things go bad when we are away.
To do so, we'll introduce [Sentry](https://sentry.io/welcome/) a convenient and easy monitoring tool. In this task, we'll setup Sentry using a `.env` file and a small settings class in fastAPI
We'll also use Postman to test that our integration is working. [Postman](https://www.postman.com/) is a convenient tool to send requests; it's a UI around `curl` or `wget`

**1. Creating the Settings class**

[FastAPI setting documentation](https://fastapi.tiangolo.com/advanced/settings/)
- Head to the `config.py` file and add a class member `sentry_key: str`. We'll use this var to store our very secret sentry key.
- At the root of this exercise dir, create a .env file with the key `SENTRY_KEY`. We'll populate it later.
- Update the docker compose file in the webapi service to have docker read the env fileit will automatically load the .env and populate it as an env var inside our container - [Documentation](https://docs.docker.com/compose/environment-variables/#the-env-file)
```
    env_file:
      - .env
```
- Head to `main.py` and add the following snippet after the FastAPI app creation `app = FastAPI()`
```
@functools.lru_cache()
def get_settings():
    return Settings()
```
Our settings should be ready to go.

**2. Create a sentry account**
- Create a sentry account to get the key; it's free for devs.

**3. Sentry integration**
we are going to use the [ASGI Middleware](https://docs.sentry.io/platforms/python/guides/asgi/) plugin since we are using FastAPI
- Create your first project in sentry
- Choose the `asgi` integration
- Copy and paste the key in the `dsn=` to the .env file. It's an API token that allows you to communicate to your sentry project
```
https://examplePublicKey@o0.ingest.sentry.io/0"
```
- Add the following snippet of code below the settings section in `main.py` to integrate sentry
```
sentry_sdk.init(
    dsn=get_settings().sentry_key,
    traces_sample_rate=1.0,
)
app.add_middleware(SentryAsgiMiddleware)
```

**4.Testing**
- Stop and relaunch your docker stack
- Open Postman and do a query
```
GET - http://localhost:8000/sentry
```
Sentry propagates any exception your system encounters to your sentry dashboard.
- Check that you have this exception in your dashboard
- Run a load test and watch the dashboard fill up


Congrats, you have now all the tools to properly debug an app in production and understand its breaking points

## Task 5: Fix the server

**1. addNumbers**

Find out why this simple addition is not working and correct it. The goal is to either only allow some numbers to be added or to allow any numbers to be added.

**2. computeFib**

Find out why the Fibonacci endpoint is slow for high iterations (>20). Try to fix it using memoization (i.e., caching). hint: You can find a fast Fibonacci implemtation in the Fibonacci class

**3. oom**

The logic in this endpoint is not fixable; it is simply designed to quickly saturate the memory and make python crash. Fun!
