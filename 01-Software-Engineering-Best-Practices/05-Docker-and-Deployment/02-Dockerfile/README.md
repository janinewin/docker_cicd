## Engineering context - Real life use
This exercise perfectly illustrates the general way of starting a new project or new experiments.

As data scientist or data engineers packaging your code and infrastructure using docker is essential to ensure portability and reproducibility of your results on different hosts.

Docker is the perfect antidote to the famous catchphrase: “But it works on my machine! &copy;”
Creating clean and extensible docker images will also help the work downstream of infrastructure/DevOps engineers responsible to run & test them inside CI/CD systems and in production (Docker swarm, virtual instances, kubernetes).


## Goal 🎯
This exercise aims at validating the docker fundamentals necessary to stand up and operate a docker container.
To do so we will teach you how to:
- Create a `Dockerfile` leveraging all the best practices
- Build & tag a docker image
- Analyse the content and construction of a docker image
- Spin up/down containers
- Access containers & execute commands inside containers using the CLI
- Push images to remote docker hubs (DockerHub, GCP Artifact Registry)

By the end of this exercise you should be able to:
- Understand the concept of a base image
- Understand the concept of layers
- Know how to create a functional & lean docker image, leveraging the concepts of caching, multi stage builds
- Be familiar with the concept of a docker image & a docker container
- Build, run & push docker images
- Use GCP container registry

---

## Task 1️⃣ - Layers 🥞
This task illustrates the concept of layers. We will purposely write a bad Dockerfile to highlight the internal structure of an image.

**❓Write a single Dockerfile (use `dockerfile-task-1`) with the following requirements:**

1. Based on ubuntu 20.04
1. Add `ARG DEBIAN_FRONTEND=noninteractive` note: **Do not use ENV as this would persist after the build and would impact your containers, children images**
1. Add `ENV PYTHONUNBUFFERED 1` this forces the stdout and stderr streams to be unbuffered. [Explanation](https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file)
1. Install python 3.8.10 from [deadsnake ppa](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa)
    ```dockerfile
    # Upgrade package list
    apt-get -y update
    #install required dependencies
    apt-get -y install software-properties-common
    # Add PPA to system's source list
    add-apt-repository ppa:deadsnakes/ppa
    # Upgrade package list to take into account new PPA
    apt-get -y update
    #install python 3.8
    apt-get install -y python3.8
    ```
1. Install pip
    ```dockerfile
    apt-get install -y python3-pip
    ```
1. Install fastapi (0.78.0), SQLAlchemy (1.4.36), Alembic (1.7.7) and, uvicorn[standard] (0.17.6)
1. Create `WORKDIR` server
1. Copy the complete current directory into the working directory `/server`
1. Expose port 8000 to be able to access the server from outside of the container
1. Create an `ENTRYPOINT` for `uvicorn`
1. Create a `CMD` to run fastapi via uvicorn, listening on all interfaces `0.0.0.0` and on port `8000`
    ```dockerfile
    app.main:app --host 0.0.0.0 --port 8000
    ```
1. Build image using the tag `base-image-fastapi-ubuntu-fat:test`
    <details>
      <summary markdown='span'>💡 Hint</summary>

    We provided you with the `make buildTask1` command (cf `Makefile`)
    </details>
1. Run container to make sure it’s functional -- it should start the fastapi server listening on the localhost interface and port 8000
    <details>
      <summary markdown='span'>💡 Hint</summary>

    Look at your `Makefile`, you should easily find a command to do so.
    </details>
1. Head to [localhost:8000](http://localhost:8000) you should see `Hello World`.
    <details>
    <summary markdown='span'>💡 Hints</summary>

    If it doesn't work, check that you have forwarded port from your VM to your local machine.
    <img src='https://wagon-public-datasets.s3.amazonaws.com/data-engineering/port_forwarding_vs_code.png' width=400>
    </details>
1. Inspect size and layers using [dive](https://github.com/wagoodman/dive)
    ```bash
    docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest base-image-fastapi-ubuntu-fat:test
    ```
1. Inspect the layers, check the image size, check the wasted space.
    <details>
      <summary markdown='span'>💡 Hint</summary>

    You could save space deleting the files and directories in `/var/lib/apt/lists/`.
    </details>
1. Push image to [Google Artifact Registry](https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling)
    - Set the following variables in your terminal:
        ```bash
        LOCATION=europe-west1
        HOSTNAME="$LOCATION-docker.pkg.dev"
        PROJECT_ID=<INSERT_YOUR_GCP_PROJECT_ID_HERE>
        REPOSITORY=docker-hub
        IMAGE_NAME=base-image-fastapi-ubuntu-fat
        IMAGE_TAG=test
        ```
    - Retag the image with the registry name
        ```bash
        docker tag "$IMAGE_NAME:$IMAGE_TAG" "$HOSTNAME/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:$IMAGE_TAG"
        ```
    - Push retagged image to container registry
        ```bash
        docker push "$HOSTNAME/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:$IMAGE_TAG"
        ```
    - Check image is present in the registry
        ```bash
        gcloud container images list-tags  "$HOSTNAME/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME"
        ```
    <details>
      <summary markdown='span'>💡 Hints</summary>

    - Find your repo `LOCATION` with `cat ~/.docker/config.json`
    - Find your `PROJECT_ID` with `gcloud projects list`
    - Find your repo name with `gcloud artifacts repositories list`
    - Find your `IMAGE_NAME` and `IMAGE_TAG` with `docker images`
    </details>
1. Tear down the server by using the shortcut `CTRL` + `c`

**🧪 Test your code with `make testTask1`**

---

## Task 2️⃣ - Caching 👻 - easy wins

This tasks illustrates the concept of caching and unwanted dependencies installed via regular commands. When doing a simple `apt install` or `pip install` by default those package managers install quantity of life dependencies to make any development work easy. To reduce the size of a docker image, one can easily trim down the fat by installing **only** what's necessary and using as fewer layers as possible.

**❓ Refactor the Dockerfile written in task 1 to save some space**

1. Copy the content of `dockerfile-task-1` into `dockerfile-task-2`
1. Refactor the `dockerfile-task-2` to use a single layer to install your dependencies
    <details>
      <summary markdown='span'>💡 Hints</summary>

    Instead of running these 2 instructions separately:
    ```dockerfile
    RUN apt-get -y update
    RUN apt-get -y upgrade
    ```
    You have to combine them into a single instruction:
    ```dockerfile
    RUN apt-get -y update && apt-get -y upgrade
    ```
    You can also launch use `\ &&` to break up the instruction in several lines:
    ```dockerfile
    RUN apt-get -y update \
        && apt-get -y upgrade
    ```
    </details>
1. Disable the installation of recommended packages when using `apt-get install` using the flag `--no-install-recommends` 👉 [apt documentation](https://manpages.ubuntu.com/manpages/xenial/man8/apt-get.8.html)
1. Disable the caching of packaging downloads and builds when using `pip install` with the flag `--no-cache-dir` 👉 [pip caching documentation](https://pip.pypa.io/en/stable/topics/caching/)
1. Clean up apt lists using the following command `rm -rf /var/lib/apt/lists/*`
1. Build image using the tag `base-image-fastapi-ubuntu:test`
    <details>
      <summary markdown='span'>💡 Hint</summary>
        Use the docker command or look at your `Makefile`, you should easily find a command to do so.
    </details>
1. Run container to make sure it’s functional -- it should start the fastapi server listening on the localhost interface and port 8000 - Head to [localhost:8000](http://localhost:3000) you should see `Hello World`
1. Inspect size and layers using `dive`
    ```bash
    docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest base-image-fastapi-ubuntu:test
    ```
1. Inspect the layers, check the image size, check the wasted space.
1. Push image to remote hub
    <details>
      <summary markdown='span'>💡 Hint</summary>
        Be careful, the image name differs from task 1
    </details>

**🧪 Test your code with `make testTask2`**

---

## Task 3️⃣ - The importance of a base image 🖼

This task elaborates on the concept of a base image and how it can be used in real life scenarios to spin up images/containers easily and efficiently.
Previously we installed our own version of python, pip and other dependencies. The community already built many robust base images. Using the right base image can save time, space and headaches.

**❓ Enhance the performance of your image**

1. Using the content of `dockerfile-task-2` do the following tasks in `dockerfile-task-3-1`
1. Update the `dockerfile-task-3` to use python:3.8.10 as a base image, you may need to remove some of the installations you’ve done in it, since now python and pip come with it.
1. We are going to use [poetry](https://python-poetry.org/) to handle all the dependencies and package management for python, instead of using the traditional `pip` and `requirements.txt` to install our packages. To do so:
    1. Replace all the previously added pip packages using poetry running in your terminal
        ```bash
        poetry add <package>
        ```
        This will generate 2 files `pyproject.toml` & `poetry.lock` defining your dependency tree
        <details>
          <summary markdown='span'>ℹ️</summary>

        You should get a `No dependencies to install or update` message, because we already provide you with the 2 configuration files `pyproject.toml` & `poetry.lock` 👌.
        </details>
    1. Update the `RUN` command:
        ```dockerfile
        #add the following lines
        pip install --no-cache-dir poetry
        poetry install --only main

        #Remove all of the manual python package installations via pip
        ```
        ☝️ `--only main` is equivalent to `--without dev` and skip `pyproject.toml` [tool.poetry.dev-dependencies] category
1. Change the `ENTRYPOINT` to use poetry
    ```dockerfile
    poetry run
    ```
1. Change the `CMD` to
    ```dockerfile
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```
1. Build image using the tag `base-image-fastapi-fat:test`
1. Run container to make sure it’s functional -- it should start the fastapi server listening on the localhost interface and port 8000 - Head to [localhost:8000](http:localhost:8000) you should see `Hello World`
1. Inspect size and layers using `dive`
    ```bash
    docker run --rm -it /var/run/docker.sock:/var/run/docker.soc wagoodman/dive:latest <your_image_name:tag>
    ```
1. Inspect the layers, check the image size, check the wasted space.

**🧪 Test your code with `make testTask3-1`**

---

**❓ Shrink your image size**

1. Copy the content of `dockerfile-task-3-1` into `dockerfile-task-3-2`
1. Now switch to `python:3.8.10-slim` base image
1. Build image using the tag `base-image-fastapi:dev`
1. Run container to make sure it’s functional
1. Inspect size and layers using dive
    ```bash
    docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest <your_image_name:tag>
    ```
1. Inspect the layers, check the image size, check the wasted space.
1. Push the slim image to remote hub

**🧪 Test your code with `make testTask3-2`**

<br>

---

## Task 4️⃣ - Inspect what's inside a running container!

So far, we've been focusing on inspecting built **images** with dive.
Let's now *run* an image and inspect what's insider a running container!

1. 🆚 Install [VS Code Docker extension](https://code.visualstudio.com/docs/containers/overview)
1. Run your latest `base-image-fastapi:dev` image with interactive shell control:
```bash
docker run --rm -it -p 8000:8000 base-image-fastapi:dev /bin/bash
```
1. Inspect where you are located with `pwd`, and what's inside with `ls`. You should be able to find your local files copied inside the container!
1. Touch a new file `toto.py`. Check that it's there with `ls`, then use VS Code docker extension to navigate there too!
<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/docker_extension_vs_code.png" width=200>
1. Now, exit the container (exit, or ctrl-D), so that the container is stopped (`docker ps` is empty). Run again your container, and try to find `toto.py`? It's gone! Containers are running instances of `images`, and only contains additional variables in memory during the time the container is running! You will see soon how to "persist" data inside a container...


### 🏁 Congratulation for completing the challenge!
- 🧪 Run the final `make test`
- 💾 Save your work in progress on GitHub so we can track your progress

---

## Some cool tools (to keep for later)!

✨ [Haskell Dockerfile Linter](https://github.com/hadolint/hadolint)

🛠 [Container Structure Tests](https://github.com/GoogleContainerTools/container-structure-test)

🤿 [dive](https://github.com/wagoodman/dive)

🍰 [dockerfile parsing API](https://github.com/asottile/dockerfile)
