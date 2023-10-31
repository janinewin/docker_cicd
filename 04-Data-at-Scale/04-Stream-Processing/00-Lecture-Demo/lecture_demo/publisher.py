from google.cloud import pubsub_v1
import os
import time
from random import choice
from datetime import datetime

PROJECT_ID = os.getenv("PROJECT_ID")
TOPIC_NAME = os.getenv("TOPIC_NAME")


publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)

while True:
    time.sleep(choice((0.5, 1, 1.5)))
    timestamp = datetime.now().strftime("%d/%b/%Y:%H:%M:%S")
    ec = choice((307, 500, 200))
    message = f'{timestamp} 172.19.0.4:40606 - "GET /sentry/ HTTP/1.1" {ec}'
    job = publisher.publish(topic_path, data=message.encode("utf-8"))
    job.result()
