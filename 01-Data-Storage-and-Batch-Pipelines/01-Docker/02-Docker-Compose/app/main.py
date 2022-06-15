from typing import List

from fastapi import Depends, FastAPI, HTTPException
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from sqlalchemy import select, text

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root(db: Session = Depends(get_db)):
    res = db.execute(select(text("1")))
    if res:
        return {"DB Status": f'{res} Ok'}
    else:
        return {"DB Status: Not Ok"}
