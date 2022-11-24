# Google Cloud Platform 101

## Objective

In this series of challenges, you will learn how to deploy your container-hosted application to **Google Cloud Platform** (GCP).

There are three steps in order to enable the developers from anywhere around the world to use your app:

- **Build** your Docker image locally
- Push this image online to **Google Container Registry**
- Deploy a container on **Google Cloud Run**

The role of **Container Registry** is to act as a storage for our Docker images.
The role of **Cloud Run** will be to run a Docker container instantiated from our image.

In the first challenge, we will set up your account and ship our first image to Google Cloud Registry!

🚨 If you have not yet done the GCP setup instruction, follow the instruction below :

## GCP Set-up

Let's install `gcloud`, Google Cloud command line interface tool.

for **MacOs**:

```
brew install --cask google-cloud-SDK
```

Then you can:

```
$(brew --prefix)/Caskroom/google-cloud-sdk/latest/google-cloud-sdk/install.sh
```

for **Windows**:

```bash
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt-get install apt-transport-https ca-certificates gnupg
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt-get update && sudo apt-get install google-cloud-sdk
sudo apt-get install google-cloud-sdk-app-engine-python
```

for **Linux**:

```bash
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt-get install apt-transport-https ca-certificates gnupg
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt-get update && sudo apt-get install google-cloud-sdk
sudo apt-get install google-cloud-sdk-app-engine-python
```

Now that `gcloud` is installed on your computer, you can log in to your Google account by running the following command. Please use your github email address.

```
gcloud auth login
```

Running the command will open a new window in your browser; click on `authorize` to allow gcloud and Google SDK.

<center>
<img src="https://github.com/lewagon/fullstack-images/blob/master/reboot-python/gcp-login.png?raw=true" height=300/>
</center>

If everything goes well, you should be able to access the [google cloud console dashboard](<https://console.cloud.google.com/>).
If yes, good job! Otherwise, please call a TA for help.

For this week, you will use with your colleagues one of Le Wagon GCP's shared project: `wagon-devops-day-5`.
It means that you don't need to activate your account on Google Cloud as it would requires you to activate a billing account and add a valid credit card. Instead you will access Google Cloud through Le Wagon and you will only be able to use the tool from GCP that we are going to use during the day.

Please, **don't** click on the button on top of the console like in the screenshot below to activate your account.

<center>
  <img src="https://github.com/lewagon/fullstack-images/blob/master/reboot-python/gcp-activation-bar.png?raw=true" />
</center>

Let's now make the `wagon-devops-day-5` project the default project on our computer so that whenever we interact with GCP through the terminal or python, we will do it on this `wagon-devops-day-5` project specifically.

```
gcloud config set project wagon-devops-day-5
```

## Push an image to Google Container Registry

**Google Container Registry** is a service storing Docker images on the cloud to allow Cloud Run or Kubernetes Engine to serve them.

It is similar to GitHub, allowing you to store your git repositories in the cloud (except for the lack of a dedicated user interface and additional services such as forks and pull requests).
It is a warehouse of docker images. From this library, you can run as many containers as you wish from google cloud run or google cloud Kubernetes.

In this challenge, we have provided you with a `Dockerfile` to run a dummy flask app.
Let's build our first image.

```bash
docker build -t api .
```

Let's run a container locally to check that everything works well so that we avoid spending time on pushing an image to the cloud that is not working.

```bash
docker run -p 8000:8000 api
```

Everything should work well, we can now push our image to Google Container Registry.

Let's rename our image correctly so that docker knows where to push it.

You can rename an image in docker with the `docker tag` command.

Remember, to push our image to Google Container Registry, we need to:

- specify in which google data center we want to send it: `eu.gcr.io` for Europe for example
- then, we specify the project in which we want to deploy our image: `wagon-devops-day-5`
- then, we specify our image name. Please use your github_name as your image name for practical reasons. Since all students work on the same project, it is crucial to keep this naming convention to ease our work.

```bash
docker tag api eu.gcr.io/wagon-devops-day-5/<user.github_nickname>
```

## GCR

Let's now push our image to GCR

```bash
docker push eu.gcr.io/wagon-devops-day-5/<user.github_nickname>
```

If the command runs successfully, you will be able to see your image [here](<https://console.cloud.google.com/gcr>)

Congrats! Let's go to the second challenge of the day to discover how to deploy our container with Google Cloud Run!
