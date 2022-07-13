import os

# Import the RabbitMQ client library
# IMPORT YOUR PACKAGES HERE


RABBITMQ_USERNAME = "rmq"
EXCHANGE_NAME = "chat"


def get_connection(host: str, port: int):
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, os.environ["RABBITMQ_DEFAULT_PASS"])
    return pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, credentials=credentials))
