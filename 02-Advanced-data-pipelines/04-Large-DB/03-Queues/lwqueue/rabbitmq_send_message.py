import argparse
import json
import random
import time

import requests

from lwqueue import rabbitmq

RABBITMQ_USERNAME = "rmq"


def send_message(host: str, port: int, username: str, message: str):
    connection = rabbitmq.get_connection(host=host, port=port)
    channel = connection.channel()

    channel.exchange_declare(exchange=rabbitmq.EXCHANGE_NAME, exchange_type="fanout")

    body = {"username": username, "message": message}
    channel.basic_publish(exchange=rabbitmq.EXCHANGE_NAME, routing_key="", body=json.dumps(body))
    print(f" [x] Sent {message}")
    connection.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", required=True, type=int)
    parser.add_argument("--username", required=True)
    parser.add_argument("--message", required=True)
    parser.add_argument("--bot", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.bot:
        # In "bot" mode, send a message
        while True:
            message = requests.get("https://api.chucknorris.io/jokes/random").json()["value"]
            send_message(
                host=args.host,
                port=args.port,
                username=f"bot::chuck-norris::{args.username}",
                message=message,
            )
            sleep_s = random.randint(45, 120)
            print(f"-- Sleeping {sleep_s} seconds")
            time.sleep(sleep_s)  
    else:
        send_message(
            host=args.host,
            port=args.port,
            username=args.username,
            message=args.message,
        )


if __name__ == "__main__":
    main()
