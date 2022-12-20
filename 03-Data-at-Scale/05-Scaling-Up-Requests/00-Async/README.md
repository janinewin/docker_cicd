# Asynchronous programming

As seen today, queues allow our programs to talk asynchronously to one another. Between them, brokers sit and allow our programs to talk to one another through messaging.

While Python is fundamentally synchronous by design, Python 3.4 and later bring a lot of ways to program asynchronously.

In the exercise below, we introduce asynchronous programming in Python. By the end, you'll have implemented a simple program that runs the same task multiple times. We'll run these tasks simultaneously, leveraging the fact that they're mostly **I/O bound, and not CPU bound**. This will improve execution time by many orders of magnitude.

Wait 🖐️, you said I/O bound and CPU bound, what does this mean?

We can split work that a computer executes into two parts:

- Computation that runs on the CPU. For instance, a program that computes new digits of Pi π or does large matrix multiplications will typically be doing these calculations on the CPU, it's just crunching numbers. **CPU bound is: if you get a faster CPU, the program runs faster 🚲 => 🛵.**
- Data exchange that is managed by the I/O (Input / Output) subsystem. There are one or more subsystems for each of the peripheral devices your computer works with: disks, terminals, printers, and.. **networks** like the Internet. A program is **I/O bound if it runs faster if the I/O subsystem was faster**.

For instance, take a program that downloads a 1GB file from the internet. Your computer is just exchanging data between two I/O subsystems: the Internet network and your computer disk. There is no computation happening per se. Using a faster CPU should not help download the file faster. **Hence, your CPU is essentially waiting for I/O to finish the data transfer**.

This dichotomy allows us to speed up programs that are **not CPU bound** by having the data transfer decoupled from the CPU cycles.

⌛ I've got a program that requires to download 20 files, I need it to go fast. What do I do?

⭐ Enter the **event loop!**

# 1️⃣ Main concepts

## Event loop ♻️

The event loop is the core of every asyncio application. Event loops run asynchronous tasks and callbacks, perform network IO operations, and run subprocesses.

In short, there is one master process called the **event loop**. You can schedule tasks on it (mainly I/O bound tasks), it will run the I/O operations in the background and "alert you" when they're done. This way, if you have many simultaneous I/O bound operations to run, scheduling them on an event loop in Python is an easy way to speed up the work.

## `async` / `await`

Python introduced in version 3+ two keywords: `async` and `await`.

Typically, here's how you use them:

- Instead of naming a function `def my_io_bound_function(...)` you name it `async def my_io_bound_function(...)`. It will "tell" the Python interpreter this function is mostly I/O bound and can be run on an event loop.
- To call this function and wait for its returned value, you don't just call it `my_io_bound_function(arg1, arg2)` but you prefix the call with `await`: `await my_io_bound_function(arg1, arg2)`.

**Task: read this [StackOverflow post](https://stackoverflow.com/a/53420574)** about differences in implementation of the `sleep` function, when `async` is used or not.

Let's do a practical example together.

# 2️⃣ First Python `async` program

The files are under the `lwasync` directory.

```bash
tree lwasync/
lwasync/
├── argument_parser.py
├── client_asynchronous.py
├── client_synchronous.py
└── server.py
```

**Objective**

We've added two files you'll use but not touch:

- `server.py` which runs a simple FastAPI HTTP server. It has one GET endpoint: `GET /say-hi` which we'll use to illustrate gains from asynchronous programming in I/O bound contexts like making an HTTP API call.
- `argument_parser.py` uses the [argparse](https://docs.python.org/3/library/argparse.html) library from the Python standard library. It helps add arguments to your program as you run it. In our case, we add the `--number` argument, which is the number of simultaneous API requests we'd like to make.

‼️ Run `make run-server` and keep the server running in a terminal window.

### A "naive" synchronous example

Synchronous code lies in the `client_synchronous.py`. Fill in the blanks in the documented code.

When you're done:
- Make sure the server is running in a terminal window. If not, open one and run `make run-server`.
- Run your code with `python lwasync/client_synchronous.py --number 10`, feel free to replace 10 by any other number. **How long did it take?**

### An asynchronous equivalent

Open the files `client_synchronous.py` and `client_asynchronous.py` side by side in VSCode (use "View: Split Editor Right"). Read through the code in `client_asynchronous.py` and notice they key differences and additions in the documented code.

<details>
  <summary markdown='span'>💡 Hint</summary>

  Try

  ```python
  async with session.get("http://localhost:8080/say-hi") as response:
        response = await response.json()
  ```
</details>

Now fill in the blanks in the `make_one_call` function.

### Let's run a comparison

1️⃣ Run your synchronous and asynchronous code with a number of 10. Which one wins? By how many multiples?
2️⃣ Double the number to 20. Is the speed factor the same or twice as good?


## BONUS. HIGHLY OPTIONAL. Skip and come back to it if you're done with everything.

This [article](https://iximiuz.com/en/posts/explain-event-loop-in-100-lines-of-code/) brillantly explains the event loop and proposes a 100 line implementation of the event loop. We highly recommend reading this article and implementing its code as an optional exercise if you'd like to understand the internals of the event loop.
