# Asynchronous programming in Python is managed by the `asyncio` library
import asyncio

from typing  import Any, Dict, List
import time

# The library to make asynchronous HTTP requests
import aiohttp

from lwasync import argument_parser


async def make_one_call(session: aiohttp.ClientSession) -> Dict[str, Any]:
    """
    Make one call to the API
    """
    response = None
    # Replace `None` by a call to the API, using the `aiohttp` library
    # Follow the Client example here: https://docs.aiohttp.org/en/stable/#client-example
    # in the function `async def main``
    # Note that you only need a bit of the code, given that the `session` is already given as an argument of `make_one_call`
    # YOUR CODE HERE
    return response


async def make_many_calls(n: int) -> List[Dict[str, Any]]:
    """
    Runs n asynchronous calls to the local server and returns all the responses in a list
    We provide this code documented, as you'll notice it's not as straightforward as the synchronous version
    """
    t0 = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(make_one_call(session)) for _ in range(n)]
        responses = await asyncio.gather(*tasks)

    tf = time.time()
    print(f"It took {tf-t0} seconds to run the {n} asynchronous calls!")
    return responses


def main():
    """
    The main function to run this file as a standalone program
    """
    # First we get the command line arguments, check
    args = argument_parser.parse_args()
    # Then, there is an additional intermediate step when running an asynchronous program, we need to create an event loop!
    loop = asyncio.get_event_loop()
    # Then, instead of simply calling the function we're interested in, we let the event loop run it for us
    # So instead of calling `make_many_calls(...)` we do:
    return loop.run_until_complete(make_many_calls(args.number))

if __name__ == "__main__":
    # Here we simply call `main()` when this file is run as a program and not imported as a library
    main()
