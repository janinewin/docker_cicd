🎯 The purpose of this exercise is to:

* guide you through common `docker` CLI commands
* while giving some details about them and the associated Docker concepts

**⏩ Feel free to skip to next challenge (DockerFile) if you are already familiar with this**

## 1) Docker Hub 💻

#### Sign up
Docker Hub is a hosted repository service provided by Docker for finding and sharing container images with your team. Once you create a Docker ID (a user), you will be able to pull and push images to the Hub.

Create a personal account 👉  [here](https://hub.docker.com/signup).

#### Login 🔑

Open a terminal and type:
```bash
docker login
```

You will be prompted for your username and password:
<p><img src="https://github.com/lewagon/fullstack-images/blob/master/reboot-python/docker-login.png?raw=true" width="500"></p>

When successful, your terminal should tell you "Login Succeeded" 🙌!

---

## 2) Hello-World ! 👋

Let's validate our Docker installation by running our first container: `hello-world`. To do so, run the following in your terminal:

```bash
docker run hello-world
```

Since you do not have any docker images on your VM (as you just installed docker),

* it will first pull the `hello-world` image from the Hub
* then run a container from this image

This container _only_ prints a message
```bash
Hello from Docker!
```


#### To see the containers you have running on your VM 👀:

```
docker ps
```

You don't see any 🤔 ? That's normal !
Your `hello-world` container is not running anymore: it exited as soon as it was done. Its job was simply to print a message.

In fact, the `docker ps` command can take arguments

#### To view all containers (even non-running ones), run:
```
docker ps -a
```

You should see a container here. What is its name ? Which image was used to run it ? What is its state ?

#### To view images on your host:
```
docker images
```

You should see your `hello-world` image, freshly pulled. You also have access to other details such as

* the image ID,
* the image tag (used to convey important information about the image. By default, the tag is "latest",
* the image size

---

## 3) Common Docker commands 🎹

### 3.1) Run a container

The [**`docker run`**](https://docs.docker.com/engine/reference/run/) command is used to run a container from an image: you should pass the image name to it, like
```bash
docker run <SOME_IMAGE>
```

- Docker will use the image from the host (your machine) if it exists
- If the image is not present on the host, it will go to the Docker Hub and pull the image for you 👌!

👉 For instance, run a container from the `postgres` image. You can see [here](https://hub.docker.com/_/postgres) that the postgres image is available on the Hub !

```bash
docker run postgres
```
this will break...👇

```bash
Error: Database is uninitialized and superuser password is not specified.
   You must specify POSTGRES_PASSWORD to a non-empty value for the
   superuser. For example, "-e POSTGRES_PASSWORD=password" on "docker run".
```

👉 Message is quite explicit: try to fix your command and run it!

The `-e` flag in `docker run -e ...` stands for environment variable. Here, we just created a password for the database superuser, and passed it to the `docker run` command
</details>

🍾 That's it! **No need for a complex installer, no conflicts on your laptop, no long hours scrolling tech forums to fix your problem** : you have a running database in a single command. Running locally is very stable on the virtual machine but often you want to use a database without having to spin up a whole virtual machine.


Now, you should see an output in your terminal: it looks like your database is initialized and ready to accept connections!


👉 Stop the container by hitting CTRL-C.

---

### 3.2) Run a container in the background

One other thing you can do, is run a container in the background (using the "detached" mode). This way, your terminal prompt will be available.

👉 Try run a new postgres container in detached mode, and give it a name: `pg`. `docker un --help` or `tldr docker run` are your best friends!

<details><summary markdown='span'>💡 solution</summary>

```bash
docker run -d -e POSTGRES_PASSWORD=password --name=pg postgres
```
</details>

You should see it running in `docker ps`
(FYI, docker generates some random names for us if we do not pass any)

---

### 3.3) Access the Postgres database

Now that your container is running, you might want to run a SQL query.
Let's first get a bash shell in the container:

👉 Run
```
docker exec -it pg /bin/bash
```

What have we done here 🤔 ? We have asked Docker to run a command (`/bin/bash`: to get a bash shell) in the container, passing the flags:
* `-i` flag for "interactive" mode: it gets us a standard input **stdin** (by default, a container runs in a non-interactive mode: it does not listen for input from your side). To provide an input, you need to pass this `-i` flag.
* the `-t` flag stands for "tty", which is a Unix-like operating system command: with this flag, you will get a command prompt.

So the combination of these two flags give us access to a "terminal", in the container 🎉 !

We can now access our DB using the `psql` CLI:

👉 Run ```psql --username postgres```

It gives you access to the Postgresql command line, where you could write SQL.

<p><img src="https://github.com/lewagon/fullstack-images/blob/master/reboot-python/psql-docker.png?raw=true" width="500"></p>

👉 Exit the `psql` prompt: `\q` + **Enter**
👉 Exit the container bash shell: `exit` + **Enter**

### 4) Clean up 🧹

#### stop & remove containers

To stop a container, use the [`docker stop`](https://docs.docker.com/engine/reference/commandline/stop/) command. You will need to pass the container ID, or the container name.

👉 Stop your `pg` container, and check the list of running containers, and the list of non-running containers.

```bash
docker stop <CONTAINER_ID>
```

And list running and exited containers:
```bash
docker ps
docker ps --filter "status=exited"
```

You should see that your container changed state, from `running` to `exited`, but it is still here ! To remove it from your host, run the `docker rm` command.

👉 Remove your postgres container

```bash
docker rm pg
```

#### 🧹 remove an image

So you have stopped and removed your postgres container, but how about the postgres image that your host initially pulled from the Docker Hub.

👉 Do you remember how to list docker images ?

<details><summary markdown='span'>View solution</summary>

```bash
docker images
```

</details>

👉 Try to remove the `postgres` image using [`docker rmi`](https://docs.docker.com/engine/reference/commandline/rmi/) and double check it worked

<details><summary markdown='span'>View solution</summary>

```bash
docker rmi postgres
docker images
```
</details>

If you have other containers on your host using the `postgres` image, you will not be able to remove the image... Get rid of the containers first ! You already know how to do so !

**💡 Cheatsheet: docker cleaning**

```bash
# Containers
docker stop $(docker ps -q) # Stop all running containers
docker container prune # Remove all stopped containers

# Images
docker rmi image_name

# Big Clean: Remove container & images
docker system prune
```

🏁 Congratulation! `make test`, commit and push your code so we can track your progress!
