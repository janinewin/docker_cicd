from pydantic import BaseModel

# User section


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


# Tweet section


class TweetBase(BaseModel):
    text: str


class TweetCreate(TweetBase):
    pass


class Tweet(TweetBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# Like section


class LikeBase(BaseModel):
    tweet_id: int


class LikeCreate(LikeBase):
    pass


class Like(LikeBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
