from pydantic import BaseModel

# Tweet section


class TweetBase(BaseModel):
    text: str


class TweetCreate(TweetBase):
    owner_id: int
    location: str
    like_count: int


class Tweet(TweetBase):
    id: int

    class Config:
        orm_mode = True
