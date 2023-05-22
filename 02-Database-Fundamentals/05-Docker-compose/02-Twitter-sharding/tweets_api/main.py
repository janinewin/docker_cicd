from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from tweets_api import crud, schemas
from tweets_api.database import SessionLocal

tags = [
    {"name": "tweets", "description": "Operations with tweets"},
]

app = FastAPI(title="Twitter Database", openapi_tags=tags)


def get_db():
    """Helper function which opens a connection to the database and also manages closing the connection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# App landing page
@app.get("/")
def read_root():
    return {"Le Wagon Twitter app": "Running"}


####### Tweets section #######


@app.post("/tweets/", response_model=schemas.Tweet, tags=["tweets"])
def create_tweet_for_user(tweet: schemas.TweetCreate, db: Session = Depends(get_db)):
    """post endpoint to create a new tweet for a given user id"""
    return crud.create_tweet(db=db, tweet=tweet)


@app.get("/tweets/", response_model=List[schemas.Tweet], tags=["tweets"])
def read_tweets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """get endpoint to read all the the tweets"""
    tweets = crud.read_tweets(db, skip=skip, limit=limit)
    return tweets
