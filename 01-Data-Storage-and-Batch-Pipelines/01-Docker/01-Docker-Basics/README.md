## Engineering context - Real life use
This exercise perfectly illustrates the general way of starting a new project or new experiments.

As data scientist or data engineers packaging your code and infrastructure using docker is essential to ensure portability and reproducibility of your results on different hosts.

Docker is the perfect antidote to the famous catchphrase: “But it works on my machine! &copy;”
Creating clean and extensible docker images will also help the work downstream of infrastructure/DevOps engineers responsible to run & test them inside CI/CD systems and in production (Docker swarm, virtual instances, kubernetes).


## Background
This exercise aims at validating the docker fundamentals necessary to stand up and operate a docker container.
To do so we will teach you how to:
- Create a `Dockerfile` leveraging all the best practices
- Build & tag a docker image
- Analyse the content and construction of a docker image
- Spin up/down containers
- Access containers & execute commands inside containers using the CLI
- Push images to remote docker hubs (DockerHub, GCP Artifact Registry)

## End goal
By the end of this exercise you should be able to:
- Understand the concept of a base image
- Understand the concept of layers
- Know how to create a functional & lean docker image, leveraging the concepts of caching, multi stage builds
- Be familiar with the concept of a docker image & a docker container
- Build, run & push docker images
- Use GCP container registry

## Task 1 - Layers 🥞
This task illustrates the concept of layers. We will purposely write a bad Dockerfile to highlight the internal structure of an image.

**❗️Only for the following exercise use separate “RUN” for each command you write.**

**❓Write a single Dockerfile with the following requirements:**

1. Based on ubuntu 20.04
1. Add `ARG DEBIAN_FRONTEND=noninteractive` note: **Do not use ENV as this would persist after the build and would impact your containers, children images**
1. Add `ENV PYTHONUNBUFFERED 1` this forces the stdout and stderr streams to be unbuffered. [Explanation](https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file)
1. Installing python 3.8.12 from [deadsnake ppa](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa)
    ```dockerfile
    #install required dependencies
    apt-get -y install software-properties-common
    # Add PPA to system's source list
    add-apt-repository ppa:deadsnakes/ppa
    # Upgrade package list to take into account new PPA
    apt-get update
    #install python 3.8
    apt-get install -y python3.8
    ```
1. Installing pip
    ```dockerfile
    apt-get install -y python3-pip
    ```
1. Install fastapi (0.78.0), SQLAchemy (1.4.36) and, Alembic (1.7.7), uvicorn[standard] (0.17.6)
1. Create `WORKDIR` server
1. Copying the complete current directory into the working directory `/server`
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
1. Head to [localhost:8000](http://localhost:8000) you should see `Hello World`
1. Inspect size and layers using [dive](https://github.com/wagoodman/dive)
    ```bash
    docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest base-image-fastapi-ubuntu-fat:test
    ```
1. Inspect the layers, check the image size, check the wasted space.
    <details>
      <summary markdown='span'>💡 Hint</summary>

    You could save space deleting the files and directories in `/var/lib/apt/lists/`.
    </details>
1. Push image to [Artifact Registry](https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling)
    1. Set the following variables with your own:
        ```bash
        LOCATION=europe-west1
        HOSTNAME="$LOCATION-docker.pkg.dev"
        PROJECT_ID=kevin-bootcamp
        REPOSITORY=docker-hub
        IMAGE_NAME=base-image-fastapi-ubuntu-fat
        IMAGE_TAG=test
        ```
    1. Retag the image with the registry name
        ```bash
        docker tag "$IMAGE_NAME:$IMAGE_TAG" "$HOSTNAME/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:$IMAGE_TAG"
        ```
    1. Push retagged image to container registry
        ```bash
        docker push "$HOSTNAME/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:$IMAGE_TAG"
        ```
    1. Check image is present in the registry
        ```bash
        gcloud container images list-tags  "$HOSTNAME/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME"
        ```
    <details>
      <summary markdown='span'>💡 Hint</summary>

    - Find your repo `LOCATION` with `cat ~/.docker/config.json`
    - Find your `PROJECT_ID` with `gcloud projects list`
    - Find your repo name with `gcloud artifacts repositories list`
    - Find your `IMAGE_NAME` and `IMAGE_TAG` with `docker images`
    </details>

**🧪 Test your code with `make testTask1`**

**🏁 Save your work in progress on GitHub**

<details>
  <summary markdown='span'>💡 Hint</summary>

```bash
git status
git add dockerfile-task-1
git commit --message 'complete task 1'
git push origin main
```

</details>

## Task 2 - Caching 👻 - easy wins

This tasks illustrates the concept of caching and unwanted dependencies installed via regular commands. When doing a simple `apt install` or `pip install` by default those package managers install quality of life dependencies to make any developement work easy. To reduce the size of a docker image, one can easily trim down the fat by installing **only** what's necessary and using as fewer layers as possible.

Using the Dockerfile written in task 1

1. Refactor the Dockerfile to use a single layer to install your dependencies
1. Disable the installation of recommended packages when using `apt-get install` using the flag `--no-install-recommends` [Link to apt documentation](https://manpages.ubuntu.com/manpages/xenial/man8/apt-get.8.html)
1. Disable the caching of packaging downloads and builds when using `pip install` with the flag `--no-cache-dir` [Link to pip caching documentation](https://pip.pypa.io/en/stable/topics/caching/)
1. Clean up apt lists using the following command `rm -rf /var/lib/apt/lists/*` [Link to apt-get documentation](https://manpages.ubuntu.com/manpages/xenial/man8/apt-get.8.html)
1. Build image using the tag `base-image-fastapi-ubuntu:test`
1. Run container to make sure it’s functional -- it should start the fastapi server listening on the localhost interface and port 8000 - Head to localhost:8000 you should see `Hello World`
1. Inspect size and layers using [dive](https://github.com/wagoodman/dive)
    ```bash
    docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest <your_image_name:tag>
    ```
1. Inspect the layers, check the image size, check the wasted space.
1. Push image to remote hub



## Task 3 - The importance of a base image 🖼

This tasks elaborates on the concept of a base image and how it can be used in real life scenarios to spin up images/containers easily and efficiently.
Previously we installed our own version of python, pip and other dependencies. The community already built many robusts base images. Using the right base image can save time, space and headaches.
Using the previous Dockerfile in task 2 do the following:

1. Update the Dockerfile to use python:3.8.12 as a base image, you may need to remove some of the installations you’ve done in it, since now python and pip come with it.
1. We are going to use [poetry](https://python-poetry.org/) to handle all the dependencies and package management for python, instead of using the traditional `pip` and `requirements.txt` to install our packages. To do so:
    1. Replace all the previously added pip packages using poetry
        ```dockerfile
        poetry add <package>
        ```
        This will generete 2 files a `poetry.toml` & `poetry.lock` defining your dependency tree
    1. Update the `RUN` command:
        ```dockerfile
        #add the following lines
        pip install --no-cache-dir poetry \
        poetry install --no-dev \

        #Remove all of the manual python package installations via pip
        ```
1. Change the `ENTRYPOINT` to use poetry
    ```dockerfile
    poetry run
    ```
1. Change the `CMD` to
    ```dockerfile
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```
1. Build image using the tag `base-image-fastapi-fat:test`
1. Run container to make sure it’s functional -- it should start the fastapi server listening on the localhost interface and port 8000 - Head to localhost:8000 you should see `Hello World`
1. Inspect size and layers using [dive](https://github.com/wagoodman/dive)
    ```bash
    docker run --rm -it /var/run/docker.sock:/var/run/docker.soc wagoodman/dive:latest <your_image_name:tag>
    ```
1. Inspect the layers, check the image size, check the wasted space.
1. Now switch to python:3.8.12-slim
1. Build image using the tag `base-image-fastapi:dev`
1. Inspect size and layers using [dive](https://github.com/wagoodman/dive)
    ```
    docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest <your_image_name:tag>
    ```
1. Inspect the layers, check the image size, check the wasted space.
1. Push the slim image to remote hub


## Interesting tools
✨ https://github.com/hadolint/hadolint

🛠 https://github.com/GoogleContainerTools/container-structure-test

🤿 https://github.com/wagoodman/dive

🍰 https://github.com/asottile/dockerfile
