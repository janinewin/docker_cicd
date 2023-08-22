# Import the RabbitMQ client library
import pika


EXCHANGE_NAME = "chat"


def get_connection(host: str, port: int, username: str, password: str):
    """
    Create a RabbitMQ connection given a host, a port, username and password.
    """
    credentials = pika.PlainCredentials(username, password)
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=host, port=port, credentials=credentials)
    )
