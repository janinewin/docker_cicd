import asyncio
from datetime import datetime
import random

from fastapi import FastAPI


app = FastAPI()

# Add a unique app_instance_id, which changes every time the app is started
app_instance_id = str(datetime.utcnow())


async def make_payload(average_wait: float, wait_variation: float):
    """
    Return the `app_instance_id` after waiting a bunch of time
    """

    # We'll create a random wait time, of around `average_wait` seconds
    wait_s = max(0.5, random.gauss(average_wait, wait_variation))

    # Store the `app_instance_id` in a map 
    payload = {
        "app_instance_id": app_instance_id,
    }
    await asyncio.sleep(wait_s)
    return payload


def fast_run_wait_time_seconds():
    """
    This function simply returns the amount of time you'd like your `/fast-run` endpoint to run.
    """
    wait_time_seconds = None
    # YOUR CODE HERE
    return wait_time_seconds


@app.get("/fast-run")
async def fast_run():
    payload = await make_payload(fast_run_wait_time_seconds(), 0.1)
    return payload


def slow_run_wait_time_seconds():
    """
    This function simply returns the amount of time you'd like your `/slow-run` endpoint to run.
    """
    wait_time_seconds = None
    # YOUR CODE HERE
    return wait_time_seconds


@app.get("/slow-run")
async def slow_run():
    payload = await make_payload(slow_run_wait_time_seconds(), 0.5)
    return payload
