include ../../../make.inc

TAG=lewagon/imgtransform:0.1

# Insert the Docker registry prefix here, remove the trailing slash /
REGISTRYPREFIX=

# Run the tests
test: pytest

# Run the application locally
run-locally:
	poetry run streamlit run lwface/face.py

# Prepare the docker "build" step
prep-build:
	@rm -rf build/
	@mkdir -p build/common/
	@cp -R ../../../common/lewagonde/ build/common/lewagonde/
	@echo "Copied common/lewagonde to build/common/lewagonde"

# Build the Docker image
build: prep-build
	docker build -t $(TAG) .

# Tag the Docker image with the Docker registry prefix
tag:
	docker tag $(TAG) $(REGISTRYPREFIX)/$(TAG)

# Push the image to your remote Docker registry
push:
	docker push $(REGISTRYPREFIX)/$(TAG)
