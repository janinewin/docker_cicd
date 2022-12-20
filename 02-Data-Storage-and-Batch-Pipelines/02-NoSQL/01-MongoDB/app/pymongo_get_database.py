from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load your username and password from the .env file
pass  # YOUR CODE HERE

def get_database() -> MongoClient:
    """
    Returns a database connection to the food database.

    :return: a PyMongo Client object representing the connection to the MongoDB server
    using the restaurant database
    """
    CONNECTION_STRING = None
    # Use your username and password to log in to MongoDB
    # it should be in the following format: mongodb://username:password@localhost:27017/
    pass  # YOUR CODE HERE
    # Create a connection using MongoClient
    client = MongoClient(CONNECTION_STRING)
    return client['random']



if __name__ == "__main__":
    # Print the database connection
    print(get_database())
    print("Database connection successful!")
