from google.cloud import pubsub_v1
import os
import sys


def callback(message: pubsub_v1.types.message):
    '''
    Define the action to perform when receiving a message:
    print it and ack the received message.
    '''
    #$CHALLENGIFY_BEGIN
    print(f"Received {message}.")
    message.ack()
    #$CHALLENGIFY_END

def run(SUBSCRIPTION_NAME, PROJECT_ID):

    # 1. Instantiate a pubsub SubscriberClient Class named `subscriber`
    subscriber = None
    #$CHALLENGIFY_BEGIN
    subscriber = pubsub_v1.SubscriberClient()
    #$CHALLENGIFY_END

    # 2. Construct the subscription path using the method `subscription_path` of subscriber inside the variable sub
    subscription_path = None
    #$CHALLENGIFY_BEGIN
    subscription_path = subscriber.subscription_path(PROJECT_ID,SUBSCRIPTION_NAME)
    #$CHALLENGIFY_END

    with subscriber:
        # use the method `subscribe` to create the subscriber with the `callback` function triggered at each message
        streaming_pull_future=None
        #$CHALLENGIFY_BEGIN
        streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
        #$CHALLENGIFY_END

        print(f"Listening for messages on {subscription_path}..\n")

        # streaming_pull_future is a Thread in background that listens to Pub/sub.
        # To await the future callback, the method `result` needs to be called
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
