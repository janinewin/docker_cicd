include ../../../make.inc

# Update the tag to 0.2 once the lwface/pages/Webcam.py code has been activated
TAG=lewagon/serverless:0.1

# Insert the Docker registry prefix here, remove the trailing slash /
REGISTRYPREFIX=

test: pytest

run:
	poetry run uvicorn lwserverless.app:app --port 8080

# Build the Docker image
build:
	docker build -t $(TAG) .

# Tag the Docker image with the Docker registry prefix
tag:
	docker tag $(TAG) $(REGISTRYPREFIX)/$(TAG)

# Push the image to your remote Docker registry
push:
	docker push $(REGISTRYPREFIX)/$(TAG)
