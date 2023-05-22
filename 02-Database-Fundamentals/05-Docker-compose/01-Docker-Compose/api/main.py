from fastapi import Depends, FastAPI
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from .database import SessionLocal

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
        return {"DB Status": f"{res} Ok"}
    else:
        return {"DB Status: Not Ok"}
