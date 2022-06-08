# Week 1 Day 1: Docker Advanced


## Engineering context - Real life use
This exercise perfectly illustrates the general way of starting a new project or new experiments. 

As data scientist or data engineers packaging your code and infrastructure using docker is essential to ensure portability and reproducibility of your results on different hosts. 

Docker is the perfect antidote to the famous catchphrase: “But it works on my machine! &copy;”
Creating clean and extensible docker images will also help the work downstream of infrastructure/DevOps engineers responsible to run& test them inside CI/CD systems and in production
(Docker swarm, virtual instances, kubernetes)


## Background
This exercise aims at validating the docker fundamentals necessary to stand up and operate a docker container.
To do so we will teach you how to:
- Create a Dockerfile leveraging all the best practices
- Build & tag a docker image
- Analyse the content and construction of a docker image
- Spin up/down containers
- Access containers & execute commands inside containers using the CLI
- Push images to remote docker hubs (DockerHub, GCP image registry)

## End goal

By the end of this exercise you should be able to:

- Understand the concept of a base image
- Understand the concept of layers 
- Know how to create a functional & lean docker image, leveraging the concepts of caching, multi stage builds
- Be familiar with the concept of a docker image & a docker container
- Build, run & push docker images
- Use GCP container registry


## Setup

For this exercise you will need:

- Working docker installation

Run the following command
```
$ docker run hello-world 
```

Expected output:

```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
7050e35b49f5: Pull complete
Digest: sha256:80f31da1ac7b312ba29d65080fddf797dd76acfb870e677f390d5acba9741b17
Status: Downloaded newer image for hello-world:latest
Hello from Docker!
This message shows that your installation appears to be working correctly.
```
- Text/Code editor - VSCode
- Working github setup
- Working GCP setup with docker authentication
    1. Enable container registry: [Link](https://cloud.google.com/artifact-registry/docs/docker/authentication)
    2. Authentication using gcloud credentials helper: [Link](https://cloud.google.com/artifact-registry/docs/docker/authentication#gcloud-helper)



## Task 1: Layers
This task illustrates the concept of layers. We will purposely write a bad Dockerfile to highlight the internal structure of an image.


**Only for the following exercise use separate “RUN” for each command you write.**

Write a single Dockerfile with the following requirements:

1. Based on ubuntu 20.04
2. Add `ARG DEBIAN_FRONTEND=noninteractive` note: **Do not use ENV as this would persist after the build and would impact your containers, children images**
3. Add `ENV PYTHONUNBUFFERED 1` this forces the stdout and stderr streams to be unbuffered. [Explanation](https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file)
3. Installing python 3.8.12 from deadsnake ppa
```
#install required dependencies
apt-get -y install software-properties-common
# Add PPA to system's source list
add-apt-repository ppa:deadsnakes/ppa
# Upgrade package list to take into account new PPA
apt-get update
#install python 3.8
apt-get install -y python3.8
```
4. Installing pip
```
apt-get install python3-pip
```
5. Install fastapi (0.78.0), SQLAchemy (1.4.36) and, Alembic (1.7.7), uvicorn[standard] (0.17.6)
6. Create `WORKDIR` server
7. Copying the complete dir into the workdir /server˚
8. Expose port 8000 to be able to access the server from outside of the container
9. Create an `ENTRYPOINT` for `uvicorn`
8. Create a `CMD` to run fastapi via uvicorn, listening on all interfaces `0.0.0.0` and on port `8000`
```
app.main:app --host 0.0.0.0 --port 8000
```
9. Build image using the tag `base-image-fastapi-ubuntu-fat:test`
10. Run container to make sure it’s functional -- it should start the fastapi server listening on the localhost interface and port 8000
11. Head to localhost:8000 you should see `Hello World`
12. Inspect size and layers using [dive](https://github.com/wagoodman/dive)
```
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest <your_image_name:tag>
```
13. Inspect the layers, check the image size, check the wasted space.
14. Push image to remote hub: [Link](https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling)
    1. Retag the image with the registry name
    ```
    docker tag <source-image> <LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY/image:tag>
    ```
    2. Push retagged image to container registry
    ```
    docker push <hostname/project-id/image:tag>
    ```
    3. Check image is present in the registry
    ```
    gcloud container images list-tags  <hostname/project-id/image:tag>
    ```

## Task 2: Caching - easy wins

This tasks illustrates the concept of caching and unwanted dependencies installed via regular commands. When doing a simple `apt install` or `pip install` by default those package managers install quality of life dependencies to make any developement work easy. To reduce the size of a docker image, one can easily trim down the fat by installing **only** what's necessary and using as fewer layers as possible.

Using the Dockerfile written in task 1

1. Refactor the Dockerfile to use a single layer to install your dependencies
2. Disable the installation of recommended packages when using `apt install` using the flag `--no-install-recommends` [Link to apt documentation](https://manpages.ubuntu.com/manpages/xenial/man8/apt-get.8.html)
3. Disable the installation of  when using `pip install` with the flag `--no-cache-dir` [Link to pip caching documentation](https://pip.pypa.io/en/stable/topics/caching/)
4. Clean up apt lists using the following command `rm -rf /var/lib/apt/lists/*` [Link to apt-get documentation](https://manpages.ubuntu.com/manpages/xenial/man8/apt-get.8.html)
5. Build image using the tag `base-image-fastapi-ubuntu:test`
6. Run container to make sure it’s functional -- it should start the fastapi server listening on the localhost interface and port 8000 - Head to localhost:8000 you should see `Hello World`
7. Inspect size and layers using [dive](https://github.com/wagoodman/dive)
```
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest <your_image_name:tag>
```
8. Inspect the layers, check the image size, check the wasted space.
9. Push image to remote hub



## Task 3: The importance of a base image

This tasks elaborates on the concept of a base image and how it can be used in real life scenarios to spin up images/containers easily and efficiently.
Previously we installed our own version of python, pip and other dependencies. The community already built many robusts base images. Using the right base image can save time, space and headaches.
Using the previous Dockerfile in task 2 do the following:

1. Update the Dockerfile to use python:3.8.12 as a base image, you may need to remove some of the installations you’ve done in it, since now python and pip come with it.
2. We are going to use [poetry](https://python-poetry.org/) to handle all the dependencies and package management for python, instead of using the traditional `pip` and `requirements.txt` to install our packages.
To do so in the `RUN` 
```
#add the following lines
    pip install --no-cache-dir poetry \ 
    poetry install --no-dev \

#Remove all of the manual python package installations via pip
```
3. Change the `ENTRYPOINT` to use poetry
```
poetry run
```
4. Change the `CMD` to
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
5. Build image using the tag `base-image-fastapi-fat:test`
6. Run container to make sure it’s functional -- it should start the fastapi server listening on the localhost interface and port 8000 - Head to localhost:8000 you should see `Hello World`
7. Inspect size and layers using [dive](https://github.com/wagoodman/dive)
```
docker run --rm -it /var/run/docker.sock:/var/run/docker.soc wagoodman/dive:latest <your_image_name:tag>
```
8. Inspect the layers, check the image size, check the wasted space.

9. Now switch to python:3.8.12-slim
10. Build image using the tag `base-image-fastapi:dev`
11. Inspect size and layers using [dive](https://github.com/wagoodman/dive)
```
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest <your_image_name:tag>
```
12. Inspect the layers, check the image size, check the wasted space.

13. Push the slim image to remote hub


## Interesting tools:
https://github.com/hadolint/hadolint


https://github.com/GoogleContainerTools/container-structure-test


https://github.com/wagoodman/dive


https://github.com/asottile/dockerfile