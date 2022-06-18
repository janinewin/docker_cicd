import sys
import functools
import warnings
import logging
import uvicorn
from fastapi import FastAPI
from fastapi.logger import logger
import numpy as np
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.config import Settings
from app.request_models import AdditionInputModel, FibInputModel
from app.fibonacci import Fibonacci

# # Since we are running behing gunicorn we need to do some logger forwarding to be able to get the worker's logs (running uvicorn)
gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers

if __name__ != "main":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)

app = FastAPI()


#Settings
# https://fastapi.tiangolo.com/advanced/settings/#reading-a-env-file



# Adding Sentry SDK for error reporting
# Read sentry key from .env file



@app.get("/")
async def root():
    return {"message": "Hello World"}

# Calling this endpoint to see if the setup works. If yes, an error message will show in Sentry dashboard
@app.get('/sentry')
async def sentry():
    raise Exception('Test sentry integration')

@app.post("/addNumbers/")
async def addNumbers(item: AdditionInputModel):
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            res = np.uint8(item.a) + np.uint8(item.b)
        except Warning as e:
            raise e
        #json serialization doesn't recognize numpy uint8 so we need to cast it to python int
        return  {"result":int(res)}

#Increasing response time
@app.post("/computeFib/")
async def computeFib(item: FibInputModel):
    res = Fibonacci.compute(item.iteration)
    return {"result": res}


#Complete python crash
@app.get("/oom/")
async def oom():
    sys.setrecursionlimit(1<<30)
    f = lambda f:f(f)
    f(f)
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run(app)