# APIs, JSON + HTTP versus Protobuf + gRPC

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

That's what APIs are for. [API](https://en.wikipedia.org/wiki/API) stands for `application programming interface`, or sometimes `application public interface`, which is as valid in the spirit.

An API is here to delimit the bits of your code that you'd like to expose to the rest of the world 🌐.

And ideally, it's language-agnostic, meaning it's accessible from Python, Go, Rust, C++, Java, Javascript, etc. And even web browsers, apps like Postman (but that's because they use one of the programming languages mentioned earlier 👈  of course).

We'll build simple APIs, then more complex ones, for both formats that we discussed in the lecture:
  - For JSON, it will be a HTTP API using the [popular and modern FastAPI library](https://fastapi.tiangolo.com/).
  - For protobuf, it will be a [gRPC](https://grpc.io/) API.

### Before we start, let's discover the Python packages we'll use

Open the `pyproject.toml` file. We use Poetry for Python packages management. In this exercise, we care mostly about these lines:

```
pandas = "^1.4.2"
```
to load CSVs.

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

> We'll edit the file `src/rest_api.py`.

Let's start simple, we want to return the current hour `h`, minute `m`, second `s`, broken down in a JSON that looks something like this.

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

  Check out the [datetime](https://docs.python.org/3/library/datetime.html) package of the standard library. Return the hour, minute and second using this package.
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
  - in a file `main.py`, ❗ we don't have this file, we have a file `rest_api.py` in a directory `src`. A little bit of help here: `uvicorn` reads that as `src.rest_api`
  - `--reload` simply says it'll reload the app whenever there is a code change, which is handy in development mode.
</details>

Once this is running, run `curl http://localhost:8000/time` in your terminal, what do you see?

<details>
  <summary markdown='span'>💡 Hint</summary>

  This should be `{"h":22,"m":23,"s":40}` with your current hour, minute, second.
</details>

---

## Now Protobuf + gRPC 🔧
We are now going to recreate this API using protobuf + gRPC 💪. There are 4 steps that are necessary for this:
  1. Create a `.proto` file where we define the service (function) and input/output variables (messages) to use
  2. Compile the `.proto` file into Python code that amongst others takes care of the serialization/deserialization
  3. Create the server code
  4. Create the client-side code

### 1️⃣ The proto file
We start by defining the API that we want to create by creating a **service** in a `.proto` file. A service definition includes a **name** and a **list of methods** that the service supports. Each method has a name, a list of input parameters, and a list of output parameters. For example, here's a `.proto` file with a service called `NumberStreamService` that has a single method called `GetNumbers`, which takes no input and returns a stream of int32 values (notice the `stream` keyword in front of `GetNumbersResponse`):

```proto
syntax = "proto3";

service NumberStreamService {
  rpc GetNumbers (GetNumbersRequest) returns (stream GetNumbersResponse) {}
}

message GetNumbersRequest {
}

message GetNumbersResponse {
  int32 value = 1;
}
```

In the `.proto` file, you can define messages to use as input and output parameters for your service methods. These messages are simple data structures that consist of fields, each with a name and a type. You can use the built-in types, such as `int32`, `float`, and `string`.

❓ **Task:** Create the messages and services for the `time` function that you created for the FastAPI, similarly as the example above. Do this in `src/protos/api.proto`.

---
### 2️⃣ Compile the `.proto` file
Use the **protoc** compiler. The protoc compiler reads the `.proto` file and generates code in the target language (in this case, Python) that provides the necessary classes and methods for interacting with the gRPC service defined in the `.proto` file.

❓ To compile the `.proto` file, you can use the following command:

```bash
python -m grpc_tools.protoc -I./protos --python_out=./generated_proto/ --grpc_python_out=./generated_proto/ ./protos/api.proto
```

Two files are created as a result. The generated code can then be imported into your Python code in the next step and be used to implement the server and client for your gRPC service.


<details>
  <summary markdown='span'>💡 What does this create?</summary>
  The generated code includes **two** files:

  1️⃣ A file containing classes for each custom **message** defined in the `.proto` file.

  2️⃣ A file containing interfaces and classes for each **service** defined in the `.proto` file, including:
  - An **interface** for each service, with methods for each service method.
  - A **stub** class for each service that sends requests to the server and receives responses.
  - A **server** class for each service that receives requests from the client and sends responses.

</details>


<img src="https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/movies/w1d3/exercises/day-3-protobuf-grpc-parts.png" />

---

### 3️⃣ Create the server code
To implement the **server** for this service, you will need to define a method that takes a **request** object and and **yields** the desired response objects one at a time. Here's an example of how you might implement the GetNumbers method for the NumberStreamService:

```python
import streaming_pb2
import streaming_pb2_grpc
import grpc
from concurrent import futures
import time

class NumberStreamService(number_stream_pb2_grpc.NumberStreamServiceServicer):
    def GetNumbers(self, request, context):
        for i in range(1, 6):
            yield number_stream_pb2.GetNumbersResponse(value=i)
```

💡 Here we `yield` a return as we want to return a **stream of messages**. If you are not returning a stream, then just use the `return` keyword.

Once you have implemented the **service** class, you can create a **gRPC** server and add the service to it. With the FastAPI we were using `Uvicorn` for this. Using gRPC we can utilize the classes that were created when we compiled the `.proto` file.

```python
# Create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
streaming_pb2_grpc.add_NumberStreamServiceServicer_to_server(NumberStreamService(), server)
server.add_insecure_port('[::]:50051')
server.start()
```

See how we are adding our service as the input to the `add_NumberStreamServiceServicer_to_server` method?

Finally, you will need to **start the server** and keep it running until you are ready to shut it down. You can do this using a while loop and the sleep function from the `time` module:
```python
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
```

❓ It is your turn now to create the server side of your API for the `time` method that you created in the FastAPI.

❓ Run the server by running the python file!

### 4️⃣ Create the client code
👇 Here's an example of how you might create a channel and a **stub** for the `NumberStreamService` and print the numbers received from the `GetNumbers` method:

```python
import grpc
import streaming_pb2
import streaming_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = streaming_pb2_grpc.NumberStreamServiceStub(channel)

response_iterator = stub.GetNumbers(streaming_pb2.GetNumbersRequest())

for response in response_iterator:
    print(response.value)

channel.close()
```

❓ Now it's your job to create the **client-side** code for your application!

## Pimp your APIs! 🍕

### One more endpoint in FastAPI

In your FastAPI app, add a `GET` endpoint `GET /country/:country/year/:year` that returns the `Rural population (% of total population)` for a given country and year. The data that is used is loaded from a `S3` bucket in `rural.py`. You need to use pandas to retrieve the value from the `Value` column given the year and country that is used as input variables for the API.

<details>
  <summary markdown='span'>💡 Hint</summary>

  Check out the documentation about [path parameters in FastAPI](https://fastapi.tiangolo.com/tutorial/path-params/) and how to get them.
</details>

### And now in gRPC

If you've reached this part, congratulations. You should have all the ingredients to make your gRPC API fancier. A few steps to follow, as a guide:

1. **Task 1**. Add 2 Protobuf messages
  - A query `CountryYearRequest` that has a `country` and a `year` field.
  - And a response `CountryYearResponse` that has one field `value`.

2. **Task 2**. Still in the `protos/api.proto` file. Add an `rpc` endpoint in the `service Api` that takes the `CountryYearRequest` as input and returns a `CountryYearResponse`.

3. **Task 3**. Recompile the Protobuf code with `make compile-proto` to generate the latest stubs (the 2 `generated_proto/api_pb2*.py` files)

4. **Task 4**. Now implement the request in Python in `src/rural_server.py`.

5. **Task 5**. Run the new server.

6. **Task 6**. Adapt the `rural_client.py` file to test the request. 👏
