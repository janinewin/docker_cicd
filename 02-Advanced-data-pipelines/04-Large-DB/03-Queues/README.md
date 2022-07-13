# Queues, PubSub

When there is too much data to handle for our workers, when data flow needs to be managed, or processing scheduled, queues come to the rescue.

To decouple our applications, it is good practice to have them talk to one another through messages, and to have these messages managed by a queue 🚥.

A fun way to practice with queues is to replace machines by humans and build a chat application 🐦.

> Humans are underrated.

Source: [Twitter](https://twitter.com/elonmusk/status/984882630947753984).

We'll build that in three steps:

1. We'll start with the open source, rock-solid message broker [RabbitMQ](https://www.rabbitmq.com/). Each student will build their own chat server and clients.

**V1 with RabbitMQ**

<img src="https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/assets/chat-rabbitmq.png" width=600>

2. One of the students will open up their chat server for everyone else. When you'll connect to it you'll get subscribed to messages from everyone else!
3. We'll replace our RabbitMQ implementation with a cloud service, like GCP PubSub.

**V2 with PubSub**

<img src="https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/assets/chat-pubsub.png" width=600>

## Our RabbitMQ server

Surprise surprise, we'll use Docker Compose to easily deploy RabbitMQ.

Follow the [Docker Hub documentation](https://hub.docker.com/_/rabbitmq) to add `rabbitmq:3.10.6-management` to the `docker-compose.yml`.

**Instructions:**

- We'll need to map ports 5672 and 15672.
- Set the environment variables `RABBITMQ_DEFAULT_USER` to `rmq` and `RABBITMQ_DEFAULT_PASS` must be read from the `.env`.
- Mount the volumes `./data/rabbitmq/data:/var/lib/rabbitmq/` and `./data/rabbitmq/log:/var/log/rabbitmq`.

Then run the server in the background with `docker-compose up -d`.

You can check that it's up and running by going to the port 15672 in your web browser. Installing the `-management` plugin brings a management dashboard for our RabbitMQ server.

## Client and server code

Now that we've got our RabbitMQ instance running and accessible, let's work on the files `lwqueue/rabbitmq.py` to receive messages from the queue (ie. our chat).

The code is heavily inspired by the [official tutorial](https://www.rabbitmq.com/tutorials/tutorial-three-python.html), which you're encouraged to read. That being said our code is cleaner and better structured and more documented.

By the end of this section we should be able to run:

```bash
python lwqueue/rabbitmq.py --host localhost --port 5672 --mode print
```

to receive messages sent to our chat and print them out to the terminal.

We'll also add the file `lwqueue/rabbitmq_send_message.py` to send a message using

```bash
python lwqueue/rabbitmq_send_message.py --host localhost --port 5672 --username <your name> --message "<your message here>"
```

## Next, add a cool UI to it

The basic terminal is pretty boring isn't it? Let's display nicely messages we're receiving from other chatters using [Rich](https://rich.readthedocs.io/en/stable/live.html).

## Now, chat with your group!

We'll need a bit of coordination here 🤸 🤸‍♂️. We need one person per group OR per bootcamp (depending on the setup), to make their RabbitMQ server, and credentials, accessible to the rest of the students.

Here is a simple rule, if noone has claimed to have opened their server on the Slack / Zoom / Teams chat, claim it 👋. Otherwise, wait for credentials from that person to be shared.

If you've reached this point, this means you've got RabbitMQ in a Docker network on port 5672, mapped to your host's port 5672. You can't share this port outside your host just yet because the firewall is blocking requests from outside it.

### Allow a port on GCP

- Go to the service `VPC Network`
- Click on `Firewall` on the left menu
- Click `CREATE FIREWALL RULE` (right next to `CREATE FIREWALL POLICY`)
  - Give it a name
  - Give it the target tag `rabbitmq`
  - Source IPv4 ranges: `0.0.0.0/0` which means any IP can access it
  - Protocol and ports. On the internet, search whether the RabbitMQ protocol (AMQP) uses TCP or UDP (😄 can't give you all the answers!)
  - Once you've found the protocol and checked it, type `5672` in the `Ports` input
  - Click `CREATE`
- Now go back to your virtual machine and click `EDIT`
  - The target tag `rabbitmq` given to your firewall rule above corresponds to a network target tag. Now look for `Network tags` and type `rabbitmq`
  - Then click `SAVE` which will update your instance

Your RabbitMQ server should be open to the world!

Share the following with your mates (in Slack / Zoom / Teams):
- Your server IP address
- The RabbitMQ password over [Password Pusher](https://pwpush.com/), make sure you increase the number of views to 100 for everyone to be able to see it.

Now, are you receiving messages from your peers? No trash talking allowed... officially 😉!

## Bonus. GCP specific: Google PubSub

- Replace your RabbitMQ implementation with a shared Google PubSub project
- Talk to your peers over a shared PubSub!
