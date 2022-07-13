import os

# Import the RabbitMQ client library
# IMPORT YOUR PACKAGES HERE


RABBITMQ_USERNAME = "rmq"
EXCHANGE_NAME = "chat"


def get_connection(host: str, port: int):
    """
    Create a RabbitMQ connection given a host, a port
    The username in the constant `RABBITMQ_USERNAME` above should be fixed
    The password should be taken from the environment variable `RABBITMQ_DEFAULT_PASS`, don't forget it!
    """
    pass  # YOUR CODE HERE
