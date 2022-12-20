from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    """Class to represent the users table"""

    # Table name
    pass  # YOUR CODE HERE

    # Columns
    pass  # YOUR CODE HERE

    # Relationships
    pass  # YOUR CODE HERE


class Tweet():  # YOUR CODE HERE: Please add "Base" inheritence to this class when you start working on this class, to allow `alembic revision --autogenerate` to take into account this model
    """Class to represent the tweets table"""

    # Table name
    pass  # YOUR CODE HERE

    # Columns
    pass  # YOUR CODE HERE

    # Relationships
    pass  # YOUR CODE HERE


class Like():  # YOUR CODE HERE: Please add "Base" inheritence to this class when you start working on Like to allow running `alembic revision --autogenerate` to take into account this model
    """Class to represent the likes table"""

    # Table name
    pass  # YOUR CODE HERE

    # Columns
    pass  # YOUR CODE HERE

    # Relationships
    pass  # YOUR CODE HERE
