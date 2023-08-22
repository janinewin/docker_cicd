# 0️⃣ Introduction

First of all, let's remember what an API is.

Here's a scenario

- I've written some code that does something useful for the world.
- Let's say it's written in Python.
- I'd like to make this code available and useful for other people than me.
- Even people who don't know Python.

**🤔 ⁉️ How do I do that?**

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

```toml
# to load CSVs
pandas = "^1.4.2"

# for the JSON HTTP API
fastapi = "^0.78.0"
uvicorn = {extras = ["standard"], version = "^0.17.6"}

# for the Protobuf + gRPC part.
grpcio-tools = "1.47.0"
```
❓ **Run poetry install** to make sure you have installed latest version in your challenge virtualenv. (we'll not use docker for this challenge).

This challenge will make heavy use of your IDE's capability (otherwise you may get lost)!
- Make sure VScode is using the correct `.venv` as Python Interpreter.
- Use "Option-Click" on your code to navigate through imports rapidly!
- Use "Command-P" to navigate through files by name
- Use "Command-Shift-R" to search for symbol globally!
- Use "View Split Editor" to view several files at once!

# 1️⃣ Warming up: A simple JSON HTTP API ⛏️

> We'll edit the file `api/rest_api.py`.

### ❓ GET /time

Let's start simple, we want to return the current hour `h`, minute `m`, second `s`, broken down in a JSON that looks something like this.

```json
{
  "h": 10,
  "m": 3,
  "s": 1
}
```

Then Run the API locally, then run `curl http://localhost:8000/time` in your terminal. You should see `{"h":22,"m":23,"s":40}` with your current hour, minute, second.

# 2️⃣ Now Protobuf + gRPC 🔧
We are now going to recreate this API using protobuf + gRPC 💪. There are 4 steps that are necessary for this:
  1. Create a `.proto` file where we define the service (function) and input/output variables (messages) to use
  2. Compile the `.proto` file into Python code that amongst others takes care of the serialization/deserialization
  3. Create the server code
  4. Create the client-side code

## 2.1) Define our `api/api.proto`

❓**Task: Create the messages and services for the `time` function that you created for the FastAPI, similarly as the example below. Do this in `api/protos/api.proto`.**

🤔 Context please? We start by defining the API that we want to create by creating a **service** in a `.proto` file. A service definition includes a **name** and a **list of methods** that the service supports. Each method has a name, a list of input parameters, and a list of output parameters.

For example, here's a `.proto` file with a service called `NumberStreamService` that has a single method called `GetNumbers`, which takes no input and returns a stream of int32 values (notice the `stream` keyword in front of `GetNumbersResponse`):

```javascript
syntax = "proto3";

// define your service
service NumberStreamService {
  rpc GetNumbers (GetNumbersRequest) returns (stream GetNumbersResponse) {}
}

// define service inputs parameters
message GetNumbersRequest {
}

// define service output parameters
message GetNumbersResponse {
  int32 value = 1;
}
```

👉 Your service should be called `TimeService` and is not a streaming one!

<details>
  <summary markdown='span'>🎁 Solution (to make sure you start correctly)</summary>

```javascript
syntax = "proto3";

// My first endpoint to get current time
service TimeService {
  rpc GetTime (TimeRequest) returns (TimeResponse) {}
}

message TimeRequest {
}

message TimeResponse {
  int64 h = 1;
  int64 m = 2;
  int64 s = 3;
}
```
</details>


---
## 2.2) Compile the `.proto` file
Use the **protoc** compiler. The protoc compiler reads the `.proto` file and generates code in the target language (in this case, Python) that provides the necessary classes and methods for interacting with the gRPC service defined in the `.proto` file.

❓ **Compile the `.proto` file with the following command** (use --help if you want to understand):

```bash
python -m grpc_tools.protoc \
--proto_path=api/protos \
--python_out=api/generated_proto \
--grpc_python_out=api/generated_proto \
api/protos/api.proto
```

Two files are created as a result.
- `api_pb2.py` containing classes for each custom **message** defined in the `.proto` file.
- `api_pb2_grpc.py` containing interfaces and classes for each **service** defined in the `.proto` file, including:
  - An **interface** for each service, with methods for each service method.
  - A **stub** class for each service that sends requests to the server and receives responses.
  - A **server** class for each service that receives requests from the client and sends responses.

It will become clearer later as you'll have to use them!

The generated code can indeed be imported into your Python code in the next step and be used to implement the server and client for your gRPC service.

<img src="https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/movies/w1d3/exercises/day-3-protobuf-grpc-parts.png" width=800 />


❓ **Fix imports** : grpc is not 100% perfect. If you look at `pb2_grpc.py` line 5 you'll see a relative import `import api_pb2 as api__pb2` that is not best practice, because it will only work if you execute the file from the same "generated_proto" folder.

Fix this by importing `api__pb2` from the `api` package instead! You can check that `api` has been "pip installed" in your virtualenv by running that `pip install | grep api` returns your package path!

👉 Let's move on to the `client` and `server` code now. We give you 2 options
- ❓**Guided-option (if you need some help)**: Follow steps 2.3) and 2.4) below
- ❓**Not guided (better learning experience)**: Try to complete the two following files and run them:
```bash
python api/proto_rpc_client.py  # Should say "Api client received: h:10 m:35 s:56"
python api/proto_rpc_server.py  # Should say "server started running"
```

---

## 2.3) Create the server code `api/proto_rpc_server.py`
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
print("start server")
server.wait_for_termination()
```

☝️ See how we are adding our service as the input to the `add_NumberStreamServiceServicer_to_server` method? Well, you should have access to the equivalent `add_TimeServiceServicer_to_server` already available to your on `api_pb2_gprc.py` 🙂

❓ **It is your turn now to create the server side of your API for the `time` method in `api/proto_rpc_server.py`**

❓ **Try to run the server by running the python file**.

```bash
python api/proto_rpc_server.py # Should say "server started running"
```

---

## 2.4) Create the client code in `api/proto_rpc_client.py`

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

❓ **Now it's your job to create the client-side code for your application!**

❓ **Try to run the server by running the python file**.

```bash
python api/proto_rpc_client.py # Should return "Api client received: h:10 m:35 s:56"
```

# 3️⃣ Add a new "Rural" end-point 🏋️‍♀️

## 3.1) Add endpoint in FastAPI

In your FastAPI app, add a `GET` endpoint `GET /country/:country/year/:year` that returns the `Rural population (% of total population)` for a given country and year. The data that is used is loaded from a `S3` bucket in `rural.py`. You need to use pandas to retrieve the value from the `Value` column given the year and country that is used as input variables for the API.

<details>
  <summary markdown='span'>💡 Hint</summary>

  Check out the documentation about [path parameters in FastAPI](https://fastapi.tiangolo.com/tutorial/path-params/) and how to get them.
</details>

## 3.2) And now in gRPC

If you've reached this part, congratulations. You should have all the ingredients to make your gRPC API fancier.

**❓ Try to code your RPC so as to achieve this (from the point of view of a client)**

```bash
python api/rural_client.py --country="Germany" --year="2017" # The share of rural population in Germany in year 2017 is 22.74%
```

Try to do everything on your own! Just know that you can add more messages to a proto file
```javascript
// My first endpoint to get current time
service TimeService{
  ...
  }

// My second endpoint to get share of rural population per country
service ...
```

<details>
  <summary markdown='span'>💡 Hints 1 (if you need guided steps) </summary>

1. **Task 1**. Start by the Protobuf messages
   - With a `CountryYearRequest` that has a `country` and a `year` field.
   - And a `CountryYearResponse` that has one field `value`.
   - And a `CountryYearService`  that takes the `CountryYearRequest` and returns th `CountryYearResponse`

2. **Task 2**. Recompile the Protobuf code

3. **Task 4**. Now implement the request in Python in `api/rural_server.py`.

4. **Task 5**. Run the new server.

5. **Task 6**. Adapt the `rural_client.py` file to test the request. 👏
</details>

<details>
  <summary markdown='span'>💡 Hints 2 (if stuck with python CLI options "--country=...")</summary>

Checkout python argparse https://docs.python.org/3/library/argparse.html
</details>
