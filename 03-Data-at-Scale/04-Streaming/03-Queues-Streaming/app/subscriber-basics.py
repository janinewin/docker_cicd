from google.cloud import pubsub_v1
import os
import sys


def callback(message):
	print(f"Received {message}.")
	message.ack()

def run(SUBSCRIPTION_NAME, PROJECT_ID):
	subscriber = pubsub_v1.SubscriberClient()
	subscription_path = subscriber.subscription_path(PROJECT_ID,SUBSCRIPTION_NAME)
	streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
	print(f"Listening for messages on {subscription_path}..\n")

	with subscriber:
	 	try:
       			streaming_pull_future.result()
	 	except TimeoutError:
				streaming_pull_future.cancel()


if __name__ == "__main__":


	project_id=os.environ["PROJECT_ID"]
	subscription_name = os.environ["SUBSCRIPTION_NAME"]



	try:
		run(
		subscription_name,
		project_id
		)
	except KeyboardInterrupt:
		print('Interrupted : Stopped Subscribing messages')
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
