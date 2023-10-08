from app.pymongo_get_database import get_database
from app.query import *  # noqa: F403, F401

db = get_database()

if "customers_test" in db.list_collection_names():
    db.customers_test.drop()
customers_test = db["customers_test"]

customers_test.insert_many(
    [
        {"name": "John Doe", "age": 35, "gender": "male", "address": "123 Main St"},
        {
            "name": "Jane Smith",
            "age": 28,
            "gender": "female",
            "address": "456 Park Ave",
        },
        {
            "name": "Michael Johnson",
            "age": 41,
            "gender": "male",
            "address": "789 Oak St",
        },
    ]
)

# TODO: write tests


def test_pass():
    pass
