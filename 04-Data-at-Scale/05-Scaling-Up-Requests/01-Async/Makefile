include ../../../make.inc

test: pytest-and-write-output

test_sayhi:
	poetry run pytest tests/test_sayhi.py

run-server:
	poetry run uvicorn lwasync.server:app --port 8080


# A name for your Docker image
TAG=lewagon/serverless:0.1

# Insert the Docker registry prefix here, remove the trailing slash /
REGISTRYPREFIX=

# Build the Docker image
build:
	docker build -t $(TAG) .

# Tag the Docker image with the Docker registry prefix
tag:
	docker tag $(TAG) $(REGISTRYPREFIX)/$(TAG)

# Push the image to your remote Docker registry
push:
	docker push $(REGISTRYPREFIX)/$(TAG)
