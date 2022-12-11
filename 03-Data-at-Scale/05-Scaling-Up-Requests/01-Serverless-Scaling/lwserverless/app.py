import asyncio
from datetime import datetime
import random

from fastapi import FastAPI

app = FastAPI()

# Add a unique app_instance_id, which changes every time the app is started
app_instance_id = str(datetime.utcnow())

FAST_WAIT_TIME = 1
SLOW_WAIT_TIME = 4

async def make_payload(average_wait: float, wait_variation: float):
    """Return the `app_instance_id` after waiting a bunch of time"""

    # We'll create a random wait time, of around `average_wait` seconds
    wait_s = max(0.5, random.gauss(average_wait, wait_variation))

    # Store the `app_instance_id` in a map
    payload = {"app_instance_id": app_instance_id}
    await asyncio.sleep(wait_s)
    return payload

@app.get("/fast-run")
async def fast_run():
    payload = await make_payload(FAST_WAIT_TIME, 0.1)
    return payload

@app.get("/slow-run")
async def slow_run():
    payload = await make_payload(SLOW_WAIT_TIME, 0.5)
    return payload
