import pymongo
from pymongo_get_database import get_database

db = get_database()

customers = None
# create a new collection called "customers"
# assign it to the variable "customers"
pass  # YOUR CODE HERE

# Insert the documents into the "customers" collection
def ingest_data(customers):
    """Ingest data into the customers collection.

    Args:
        customers (pymongo.collection.Collection): The customers collection.
    """
    # Create a collection named `customers` and insert the documents from
    # the readme
    pass  # YOUR CODE HERE

if __name__ == "__main__":
    ingest_data(customers)

    # Count the number of documents in the "customers" collection
    total_customer = None
    pass  # YOUR CODE HERE
    print(f"There are now {total_customer} customers in the collection.")
