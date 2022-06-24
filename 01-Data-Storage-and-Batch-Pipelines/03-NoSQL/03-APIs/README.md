# APIs, JSON + HTTP versus Protobuf + gRPC 

❗️ Before you begin this exercise, it is required to _at least_ read until `4. Load it with Pandas` from the `Serialization` exercise.

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

### Before we start, let's discover the Python packages we'll use

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

## First off, let's write our JSON HTTP API ⛏️

Let's start simple, we want to return the current hour `h`, minute `m`, second `s`, broken down in a JSON that looks like this.

```json
{
  "h": 10,
  "m": 3,
  "s": 1
}
```

**How do we get the current time in Python?**

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

Once this is running, run `curl http://localhost:8000/time` in your terminal, what do you see?

<details>
  <summary markdown='span'>💡 Hint</summary>

  This should be `{"h":22,"m":23,"s":40}` with your current hour, minute, second.
</details>

## Now Protobuf + gRPC 🔧

Protobuf, by its "compiled" nature, is a different beast 🐈.

🚸 **I thought Python wasn't compiled, what are you talking about?**

Here, by compilation, we mean there is an extra step required to go from the `.proto` file definition to Python code. Take a look at the generated files

- `lwapi/api_pb2.py` which contains the Protobuf structures
- `lwapi/api_pb2_grpc.py` which contains the gRPC services.

That probably doesn't make sense just yet. Let's deconstruct the pieces. For the record, we're following our own simpler version of the [gRPC Python tutorial](https://grpc.io/docs/languages/python/basics/). You might want to take a look anyways, as that is the official reference.

### It starts with a `proto` file

All the messages exchanged within our gRPC service are Protobuf messages. And these messages are defined in the `protos/api.proto` file (pre-filled for you), in the `message <> {...}` blocks.

An example from the official doc
```proto
// Points are represented as latitude-longitude pairs in the E7 representation
// (degrees multiplied by 10**7 and rounded to the nearest integer).
// Latitudes should be in the range +/- 90 degrees and longitude should be in
// the range +/- 180 degrees (inclusive).
message Point {
  int32 latitude = 1;
  int32 longitude = 2;
}
```

These protobuf messages define what are the inputs and outputs of any API that uses them.

Now, we also define the API endpoints in the protobuf message, by defining a `service` block, with `rpc` lines. Each `rpc` line is like a new function that can be called on the API. Here is an example from [the official tutorial](https://github.com/grpc/grpc/blob/v1.46.3/examples/protos/helloworld.proto).

```proto
// The greeting service definition.
service Greeter {
  // Sends a greeting
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}
```

Once the protobuf file is well defined, we need to compile it into actual "semi-finished" code. We've written this for you, run `make compile-proto`.

This compilation step 
1. writes the message definitions to be used by Python
2. writes the API glue code

Cool 👌.

**There is one last step, fill in the logic!**

And for that, look at these instructions 👇.

<details>
  <summary markdown='span'>💡 Hint</summary>

  If you need extra explanations, take the time to read the [official "Introduction to gRPC"](https://grpc.io/docs/what-is-grpc/introduction/).
  Even after finishing this exercise, it's worth a second read.
</details>


### Back to the code

Then, like we defined an API service signature for the FastAPI app, we define

- the endpoint: `/time` for the the HTTP API, here this is the `rpc` service name
- the input type: here this is an empty message `TimeRequest` already filled out
- the response type: a JSON dictionary for the HTTP API, here the `TimeResponse` message you have to fill out.

**Task: fill out the `TimeResponse` message**

<details>
  <summary markdown='span'>💡 Hint</summary>

  - It needs to map what you've done in the return of `def time():`.
  - Except that you need to give a type `int64` to each of the fields.
  - Tip: each field needs to have a unique number, which increments every time. Check the `message Point` above, note the `=1`, then `=2`, then `=3`.
</details>

**Task: fill out the `GetTime` service endpoint**

<details>
  <summary markdown='span'>💡 Hint</summary>

  - Look at how this is done in the [official tutorial](https://github.com/grpc/grpc/blob/v1.46.3/examples/protos/route_guide.proto#L25)
  - Something like `rpc GetTime(...) returns (...) {}`
</details>

**Task: recompile the protos**

We've already added the command for that in the `Makefile`: `make compile-proto`.

**Task: fill out the service code!**

In `lwapi/protorcp.py`, you'll need to fill out the `GetTime(...)` method of the `Api` class. Again, this mimics what we've done earlier in the HTTP API ; just this time it's a `TimeResponse` instance that is returned.

**Task: test it!**

To put this all together, we've created the server and client code for you to test.

- In one terminal, run `python protorpc_server.py`, this runs a server on a default port 50051.
- In a second terminal, run `python protorpc_client.py`, this tests a client against this server ✌️.

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

If you've reached this part, congratulations. You should have all the ingredients to make your gRPC API fancier. A few steps to follow, as a guide:

1. **Task 1**. Add 2 Protobuf messages
  - A query `RuralRequest` that has a `country` and a `year` field.
  - And a response `RuralResponse` that has one field `value`.

2. **Task 2**. Still in the `protos/api.proto` file. Add an `rpc` endpoint in the `service Api` that takes the `RuralRequest` as input and returns a `RuralResponse`.

3. **Task 3**. Recompile the Protobuf code with `make compile-proto` to generate the latest stubs (the 2 `lwapi/api_pb2*.py` files)

4. **Task 4**. Now implement the request in Python in `lwapi/protorpc.py`.

5. **Task 5**. Run the new server.

6. **Task 6**. Adapt the `protorpc_client.py` file to test the request. 👏
