# APIs, JSON + HTTP versus Protobuf + gRPC 

❗️ It's required to at least read until `Loading it with Pandas` from the `Serialization` exercise.

## Introduction

First of all, let's remember what an API is.

Here's a scenario

- I've written some code that does something useful for the world.
- Let's say it's written in Python.
- I'd like to make this code available and useful for other people than me.
- Even people who don't know Python.

**⁉️ How do I do that?**

<details>
  <summary markdown='span'>💡 Hint</summary>

  They keyword is `interface`.
</details>

That's what APIs are for. [API](https://en.wikipedia.org/wiki/API) stands for `application programming interface`, or sometimes `application programming interface`, which is as valid in the spirit.

An API is here to delimit the bits of your code that you'd like to expose to the rest of the world 🌐.

And ideally, it's language-agnostic, meaning it's accessible from Python, Go, Rust, C++, Java, Javascript, etc. And even web browsers, apps like Postman (but that's because they use one of the programming languages mentioned earlier 👈  of course).

In the `Serialization` exercise, we've talked about two dualities:

- CSV and Parquet -- and we've played with both.
- JSON and Protobuf. In this exercise, we'll play with both and expose JSON data, and Protobuf data, in their respective APIs.
  - For JSON, it will be a HTTP API using the [popular and modern FastAPI library](https://fastapi.tiangolo.com/). You may have heard of [Flask](https://flask.palletsprojects.com/en/2.1.x/), it's similar but for modern, typed, asynchronous Python 3.x.
  - For Protobuf, it will be a [gRPC](https://grpc.io/) API. Note we'll use Protobuf version 3 for the record.

We'll build simple APIs, then more complex ones, for both formats.

### Let's discover the Python packages we'll use

Open the `pyproject.toml` file. We use Poetry for Python packages management. If you haven't already, [read up about the pyproject.toml file](https://python-poetry.org/docs/pyproject/). 

In this exercise, we care mostly about these lines:

```
pandas = "^1.4.2"
```
to load CSVs (cf. `Serialization` exercise).

```
fastapi = "^0.78.0"
uvicorn = {extras = ["standard"], version = "^0.17.6"}
```
for the JSON HTTP API.

```
grpcio-tools = "^1.46.3"
```
for the Protobuf + gRPC part.

## Let's write our JSON HTTP API ⛏️

Let's start simple, we want to return the current hour `h`, minute `m`, second `s`, broken down in a JSON that looks like this.

```json
{
  "h": 10,
  "m": 3,
  "s": 1
}
```

**First, how do we get the current time in Python?**

<details>
  <summary markdown='span'>💡 Hint</summary>

  Check out the [datetime](https://docs.python.org/3/library/datetime.html) package of the standard library.
</details>

Then, hook this function to an endpoint.

**Follow the [example app](https://fastapi.tiangolo.com/#example) to create the endpoint `/time`**

<details>
  <summary markdown='span'>💡 Hint</summary>

  Check out the `def read_root():` bit, but change the path in `@app.get("/")` to be `@app.get("/time")`.
</details>

**Run the API**

The answer to run the app [lies here](https://fastapi.tiangolo.com/#run-it), but you need to adapt the code to your path.

<details>
  <summary markdown='span'>💡 Hint</summary>

  The tutorial suggests `uvicorn main:app --reload`, because it's
  - a variable `app`, like us
  - in a file `main.py`, ❗ we don't have this file, we have a file `jsonrpc.py` in a directory `lwapi`. A little bit of help here: `uvicorn` reads that as `lwapi.jsonrpc`
  - `--reload` simply says it'll reload the app whenever there is a code change, which is handy in development mode.
</details>

Once this is running, run `curl http://localhost:8000` in your terminal, what do you see?

<details>
  <summary markdown='span'>💡 Hint</summary>

  This should be `{"h":22,"m":23,"s":40}` with your current hour, minute, second.
</details>

## Now Protobuf + gRPC 🔧

TODO protobuf + gRPC.

## Pimp your APIs! 🍕

This part is a bonus if you feel like a Proto-boss 🤦. Are you up for the challenge? It uses your work from the `Serialization` exercise, so you'll need that completed first. At the very least, do the first part of that exercise, until the CSV data is downloaded and in the `./data` directory. To keep you going in this `APIs` exercise, the code you need to play with the rural CSV data is in the file `lwapi/rural.py`.

Let's start by creating a `data` directory here, and copying the `API-rural.csv` file from the `Serialization` exercise under this `./data/` directory.

### One more endpoint in FastAPI

In your FastAPI app, add a `GET` endpoint `GET /country/:country/year/:year` that returns the `Rural population (% of total population)` for a given country and year.

<details>
  <summary markdown='span'>💡 Hint</summary>

  Check out the documentation about [path parameters in FastAPI](https://fastapi.tiangolo.com/tutorial/path-params/) and how to get them.
</details>

### And now in gRPC

- Add 2 Protobuf messages
  - A query `RuralQuery` that has a `Country` and `Year` field
  - And a response `RuralResponse` that has one field `RuralPopulationPercentage`
- Add an `rpc` endpoint in the `service Lewagon` that takes the `RuralQuery` as input and returns a `RuralResponse`
- Now implement the request in Python.

TODO protobuf + gRPC.
