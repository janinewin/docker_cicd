from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
import os

Base = declarative_base()


class Tweet(Base):
    """Class to represent the tweets table"""

    # Table name
    # __tablename__ =
    pass  # YOUR CODE HERE

    # Columns
    id = Column(Integer, primary_key=True)
    location = Column(String, nullable=False)
    text = Column(String, nullable=False)
    owner_id = Column(Integer, nullable=False)
    like_count = Column(Integer, default=0, nullable=False)
