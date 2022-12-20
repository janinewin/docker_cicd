# Asynchronous programming in Python is managed by the `asyncio` library
import asyncio

import pandas as pd

from typing import Any, Dict, List
import time

# The library to make asynchronous HTTP requests
import aiohttp


async def make_one_call(session: aiohttp.ClientSession, api_url: str, index: int) -> Dict[str, Any]:
    """
    Make one call to the API
    """
    response = None
    # Replace `None` by a call to the API, using the `aiohttp` library
    # Follow the Client example here: https://docs.aiohttp.org/en/stable/#client-example
    # in the function `async def main``
    # Note that you only need a bit of the code, given that the `session` is already given as an argument of `make_one_call`
    t0 = time.time()
    async with session.get(api_url) as response:
        if response.status >= 400:
            raise ValueError(f"Status error! The response status in `make_one_call` is {response.status}, is your API URL correct? It needs to be the full API URL ending with /fast-run, not just the API root.")
        response = await response.json()
    duration_seconds = time.time() - t0

    return {**response, "index": index, "duration_seconds": duration_seconds}


async def make_many_calls(api_url: str, n: int) -> List[Dict[str, Any]]:
    """
    Runs n asynchronous calls to the local server and returns all the responses in a list
    We provide this code documented, as you'll notice it's not as straightforward as the synchronous version
    """
    t0 = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(make_one_call(session, api_url, index)) for index in range(n)]
        responses = await asyncio.gather(*tasks)

    duration_seconds = time.time() - t0
    print(f"It took {duration_seconds} seconds to run the {n} asynchronous calls!")
    return pd.DataFrame(responses), duration_seconds


def generate_statistics(api_url: str, number: int = 25):
    """
    The main function to run this file as a standalone program
    """
    # First we get the command line arguments, check
    # Then, there is an additional intermediate step when running an asynchronous program, we need to create an event loop!
    loop = asyncio.get_event_loop()
    # Then, instead of simply calling the function we're interested in, we let the event loop run it for us
    # So instead of calling `make_many_calls(...)` we do:
    return loop.run_until_complete(make_many_calls(api_url, number))
