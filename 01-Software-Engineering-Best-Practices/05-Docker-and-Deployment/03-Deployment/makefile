include ../../../make.inc

build_docker_image:
    # build the container using DOCKER_IMAGE_NAME
		docker build -t $(DOCKER_IMAGE_NAME):$(IMAGE_TAG) -f Dockerfile .

run_docker_image:
    # run the container using DOCKER_IMAGE_NAME
		docker run --rm -it -e PORT=$(PORT) -p $(PORT):$(PORT) $(DOCKER_IMAGE_NAME):$(IMAGE_TAG)

push_docker_image:
    # push the container using DOCKER_IMAGE_NAME
		docker tag "$(DOCKER_IMAGE_NAME):$(IMAGE_TAG)" "$(HOSTNAME)/$(PROJECT_ID)/$(REPOSITORY)/$(DOCKER_IMAGE_NAME):$(IMAGE_TAG)"
		docker push "$(HOSTNAME)/$(PROJECT_ID)/$(REPOSITORY)/$(DOCKER_IMAGE_NAME):$(IMAGE_TAG)"

deploy_docker_image:
		deploy "$(HOSTNAME)/$(PROJECT_ID)/$(REPOSITORY)/$(DOCKER_IMAGE_NAME):$(IMAGE_TAG)"
