from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    """Class to represent the users table"""

    # Table name
    __tablename__ = "users"

    # Columns
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationships
    tweets = relationship("Tweet", back_populates="owner")
    likes = relationship("Like", back_populates="owner")


class Tweet(Base):
    """Class to represent the tweets table"""

    # Table name
    __tablename__ = "tweets"

    # Columns
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    like_count = Column(Integer, default=0, nullable=False)

    # Relationships
    owner = relationship("User", back_populates="tweets")
    likes = relationship("Like", back_populates="tweet")


class Like(Base):
    """Class to represent the likes table"""

    # Table name
    __tablename__ = "likes"

    # Columns
    id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=False)

    # Relationships
    owner = relationship("User", back_populates="likes")
    tweet = relationship("Tweet", back_populates="likes")
