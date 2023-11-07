## Setting up ci and cd!

### Setup a repo and cd!

1. Duplicate the previous challenge to a new repo outside of the challenges
2. Push all of the code up!
3. Go to your cloud run service

a. Cloud run service click setup continuous deployment

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D5/cloud-run-service.png">

b. Select your repo

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D5/cloud-run-select-repo.png" width=500>

c. Select the branch you want to deploy and the name of your dockefile

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D5/cloud-run-build-config.png" width=500>


4. Go to the code and make a change to the response of the api


5. Push the code and go and view your repo and you will see the ci/cd pipeline in action automatically as an action!

<img src="https://wagon-public-datasets.s3.amazonaws.com/data-engineering/W0D5/repo-action.png">

Cloud Run and Cloud Build offer some safeguards against deploying broken containers:

- Cloud Build: Compiles your source code and builds the container image. If the build process fails, it stops there, preventing a faulty image from being pushed.

- Cloud Run: Only deploys successfully built containers. If a container fails to start, it won't replace the currently running version, maintaining uptime.

Both mechanisms offer a safety net by ensuring only functional containers make it to production, even in the absence of a full-fledged CI system.

We want to be robust through so lets setup ci!


### Setting up ci

Create an action using the template below most of the code is already written for you!


```yml
name: FastAPI CI and Lint

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  lint:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Run Hadolint
      uses: hadolint/hadolint-action@v1.5.0
      with:
        dockerfile: Dockerfile

  build-and-test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Build Docker image
      run: docker build -t my_fastapi_app .

    - name: Run Docker container
      run: docker run --name test_container -d -p 8000:8000 -e PORT=8000 my_fastapi_app

    - name: Wait for FastAPI to start
      run: sleep 10

    - name: Test API
      run: curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ | grep 200

    - name: Save Docker image
      run: docker save my_fastapi_app:latest > my_fastapi_app.tar

    - name: Upload Docker image as artifact
      uses: actions/upload-artifact@v2
      with:
        name: my_fastapi_app
        path: my_fastapi_app.tar

  security-scan:
    needs: build-and-test
    runs-on: ubuntu-latest
    steps:
    - name: Download Docker image from artifact
      uses: actions/download-artifact@v2
      with:
        name: my_fastapi_app

    - name: Load Docker image
      run: docker load < my_fastapi_app.tar

    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'my_fastapi_app:latest'
        format: 'table'
        exit-code: '1'

```

Try to add and push the action what breaks?

Fix it and checkout the output of the actions!

They will probably fail but give interesting insights in improving your containers!


### Advanced cd

Sometimes you don't want cloud build to automatically build and deploy the containers but you still want it pushed to the artifact registry.

If you checkout this article you can attempt to do just that but it gets a little tricky!:

https://gist.github.com/palewire/12c4b2b974ef735d22da7493cf7f4d37
