from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "From the cloud! We managed the continuous deployment! whoop whoop!"}
