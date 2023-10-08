# Import the pymongo library
import pymongo
from pymongo.collection import Collection
from app.pymongo_get_database import get_database
from typing import List, Dict


def customer_below_age(customers: Collection, max: int) -> List[Dict]:
    """
    Finds customers below a certain age.
    :return: list of dictionaries representing the customers who are at most the given minimum age
    """
    customer_below_age = list(customers.find({"age": {"$lt": max}}))
    # 💡 By default the pymongo functionalities return a `pymongo.cursor.Cursor`,
    # because it allows for the efficient iteration over a large number of results.
    # To see the values that are in the cursor, you can simply use the `list()` function

    return customer_below_age


def customer_above_age(customers: Collection, min_age: int) -> List[Dict]:
    """
    Finds customers with minimum age.
    :return: list of dictionaries representing the customers who are at least the given minimum age
    """
    pass  # YOUR CODE HERE


def calculate_avg_age_per_gender(customers: Collection) -> List:
    """
    Calculates average age of customers per gender.
    :return: [{'_id': 'female', 'avg_age': xxx}, {'_id': 'male', 'avg_age': xxx}]
    """
    pass  # YOUR CODE HERE


def update_customers_membership(customers: Collection, membership: str):
    """
    Updates all customers with a new "membership" field.
    :param membership: string representing the value to set the "membership" field to
    """
    pass  # YOUR CODE HERE


def customers_sorted_by_age(customers: Collection) -> List[Dict]:
    """
    Finds customers and sorts them by age in descending order.

    :return: list of dictionaries representing the customers sorted by their age in descending order
    """
    pass  # YOUR CODE HERE


if __name__ == "__main__":
    db = get_database()
    customers = db["customers"]

    # Example: Use the find command to search for customers who are below 36 years old
    results = customer_below_age(customers, 36)
    print(results, " \n ----- \n")

    # Use the find command to search for customers who are 36 years old or older
    results = customer_above_age(customers, 36)
    print(results, " \n ----- \n")

    # Use the aggregate command to calculate the average age of the customers in the collection
    results = calculate_avg_age_per_gender(customers)
    print(results, " \n ----- \n")

    # Use the updateMany command to update all customers with a new field called "membership" that has a value of "gold"
    update_customers_membership(customers, "gold")
    print(" \n ----- \n")

    # Use the find command with the sort modifier to search for customers and sort the results by their age in descending order
    results = customers_sorted_by_age(customers)
    print(results, " \n ----- \n")
