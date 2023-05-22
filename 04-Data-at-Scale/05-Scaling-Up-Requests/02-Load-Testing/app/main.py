import functools
import logging
import warnings

import numpy as np
import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.logger import logger
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.config import Settings
from app.fibonacci import Fibonacci
from app.request_models import AdditionInputModel, FibInputModel

# # Since we are running behing gunicorn we need to do some logger forwarding to be able to get the worker's logs (running uvicorn)
gunicorn_logger = logging.getLogger("gunicorn.error")
logger.handlers = gunicorn_logger.handlers

if __name__ != "__main__":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)

app = FastAPI()


# Load the Settings model with the .env file
# https://fastapi.tiangolo.com/advanced/settings/#reading-a-env-file




# Add Sentry SDK and middleware for error and performance reporting
# ⚠️ Read sentry key from .env file, don't save it in your code




@app.get("/")
async def root():
    return {"message": "Hello World!"}


# Calling this endpoint to see if the setup works. If yes, an error message will show in Sentry dashboard
@app.get("/sentry")
async def sentry():
    raise Exception("Test sentry integration")


@app.post("/addNumbers")
async def addNumbers(item: AdditionInputModel):
    with warnings.catch_warnings():
        warnings.filterwarnings("error")
        try:
            res = np.uint16(item.a) + np.uint16(item.b)
            
        except Warning as e:
            # Optional #1: to help the team (and yourself) debug this error, let's capture this event on Sentry
            
            raise e
        # json serialization doesn't recognize numpy uint8 so we need to cast it to python int
        return {"result": int(res)}


# Increasing response time
@app.post("/computeFib")
async def computeFib(item: FibInputModel):
    res = await Fibonacci().compute(item.iteration)
    # Optional #2: create an info level log of the `compute_fast` method's cache info when this endpoint is called
    
    return {"result": res}


if __name__ == "__main__":
    uvicorn.run(app)
