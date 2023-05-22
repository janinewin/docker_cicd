from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from twitter_api import crud, schemas
from twitter_api.database import SessionLocal

tags = [
    {"name": "users", "description": "Operations with users"},
    {"name": "tweets", "description": "Operations with tweets"},
    {"name": "likes", "description": "Operations with likes"},
]

app = FastAPI(title="Twitter Database", openapi_tags=tags)


def get_db():
    """Helper function which opens a connection to the database and also manages closing the connection
    See https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
    """

    db = SessionLocal()
    try:
        yield db  # yield statement suspends the function’s execution and sends db value back to the caller, but retains enough state to enable the function to resume where it left off as soon as the caller has finished executing.
    finally:
        db.close()


# App landing page
@app.get("/")
def read_root():
    return {"Le Wagon Twitter app": "Running"}


####### Users section #######


@app.get("/users/{user_id}", response_model=schemas.User, tags=["users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    """get endpoint to read a given user"""
    db_user = crud.read_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/", response_model=List[schemas.User], tags=["users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """get endpoint to read all the the users"""
    pass  # YOUR CODE HERE


@app.post("/users/", response_model=schemas.User, tags=["users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """post endpoint to create a new user for a given email"""
    pass  # YOUR CODE HERE


####### Tweets section #######


@app.post("/users/{user_id}/tweets/", response_model=schemas.Tweet, tags=["tweets"])
def create_tweet_for_user(
    user_id: int, tweet: schemas.TweetCreate, db: Session = Depends(get_db)
):
    """post endpoint to create a new tweet for a given user id"""
    pass  # YOUR CODE HERE


@app.get("/tweets/", response_model=List[schemas.Tweet], tags=["tweets"])
def read_tweets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """get endpoint to read all the the tweets"""
    pass  # YOUR CODE HERE


@app.get(
    "/users/{user_id}/tweets/", response_model=List[schemas.Tweet], tags=["tweets"]
)
def read_users_tweets(user_id: int, db: Session = Depends(get_db)):
    pass  # YOUR CODE HERE


####### Likes section #######


@app.post("/users/{user_id}/likes/", response_model=schemas.Like, tags=["likes"])
def create_like(user_id: int, like: schemas.LikeCreate, db: Session = Depends(get_db)):
    """post endpoint to create a new like for given user id given that they have not already liked the tweet"""
    pass  # YOUR CODE HERE


@app.get("/users/{user_id}/likes/", response_model=List[schemas.Like], tags=["likes"])
def read_user_likes(user_id: int, db: Session = Depends(get_db)):
    """get endpoint to read all the the likes for a given user id"""
    pass  # YOUR CODE HERE


@app.get(
    "/users/{user_id}/liked_tweets/", response_model=List[schemas.Tweet], tags=["likes"]
)
def read_user_liked_tweets(user_id: int, db: Session = Depends(get_db)):
    """get endpoint to read all liked_tweets from a user"""
    pass  # YOUR CODE HERE
