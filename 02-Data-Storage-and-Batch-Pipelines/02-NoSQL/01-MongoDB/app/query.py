# Import the pymongo library
import pymongo
from pymongo_get_database import get_database
from typing import List, Dict


def customer_below_age(customers: pymongo.collection.Collection, max: int) -> List[Dict]:
    """
    Finds customers below a certain age.

    :param customers: PyMongo Collection object representing the "customers" collection
    :param min_age: integer representing the maximum age of customers to find
    :return: list of dictionaries representing the customers who are at least the given minimum age
    """
    customer_below_age = list(customers.find({"age": {"$lt": max}}))
    return customer_below_age

def customer_above_age(customers: pymongo.collection.Collection, min_age: int) -> List[Dict]:
    """
    Finds customers with minimum age.

    :param customers: PyMongo Collection object representing the "customers" collection
    :param min_age: integer representing the minimum age of customers to find
    :return: list of dictionaries representing the customers who are at least the given minimum age
    """
    pass  # YOUR CODE HERE

def calculate_avg_age(customers: pymongo.collection.Collection) -> float:
    """
    Calculates average age of customers in collection.

    :param customers: PyMongo Collection object representing the "customers" collection
    :return: float representing the average age of the customers in the collection
    """
    pass  # YOUR CODE HERE


def update_customers_membership(customers: pymongo.collection.Collection, membership: str):
    """
    Updates all customers with a new "membership" field.

    :param customers: PyMongo Collection object representing the "customers" collection
    :param membership: string representing the value to set the "membership" field to
    """
    pass  # YOUR CODE HERE

def customers_sorted_by_age(customers: pymongo.collection.Collection) -> List[Dict]:
    """
    Finds customers and sorts them by age in descending order.

    :param customers: PyMongo Collection object representing the "customers" collection
    :return: list of dictionaries representing the customers sorted by their age in descending order
    """
    pass  # YOUR CODE HERE


def delete_customer(customers: pymongo.collection.Collection, name: str):
    """
    Deletes customer with given name from the collection.

    :param customers: PyMongo Collection object representing the "customers" collection
    :param name: string representing the name of the customer to delete
    """
    pass  # YOUR CODE HERE


if __name__ == "__main__":

    db = get_database()

    # Create a new collection called "customers"
    customers = db["customers"]

    # Example: Use the find command to search for customers who are below 36 years old
    results = customer_below_age(customers, 36)
    print(results)
    print(" ")
    print("-----")
    print(" ")

    # Use the find command to search for customers who are 36 years old or older
    results = customer_above_age(customers, 36)
    print(results)
    print(" ")
    print("-----")
    print(" ")

    # Use the aggregate command to calculate the average age of the customers in the collection
    avg_age = calculate_avg_age(customers)
    print("Average age:", avg_age)
    print(" ")
    print("-----")
    print(" ")

    # Use the updateMany command to update all customers with a new field called "membership" that has a value of "gold"
    update_customers_membership(customers, "gold")
    print(" ")
    print("-----")
    print(" ")

    # Use the find command with the sort modifier to search for customers and sort the results by their age in descending order
    results = customers_sorted_by_age(customers)
    print(results)
    print(" ")
    print("-----")
    print(" ")

    # Use the deleteOne command to delete the customer with the name "Jane Smith"
    delete_customer(customers, "Jane Smith")
