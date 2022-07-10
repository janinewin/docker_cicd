import asyncio
import time

from fastapi import FastAPI


app = FastAPI()


@app.get("/say-hi")
async def root():
    await asyncio.sleep(0.2)
    return {"message": "Hello World", "time": time.time()}
