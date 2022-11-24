# Deploy a Single Container application with Cloud Run

Let's now deploy our first container hosted application with **Google Cloud Run**!

In the previous exercice, we pushed our Docker image to **Google Container Registry**.
The image is now available for deployment by Google services such as **Cloud Run** and **Google Kubernetes Managed Services** (for massive scaling).

Cloud Run is a great tool to deploy single container application in one shell command.

Cloud Run will instantiate the image into a container and run the `CMD` instruction inside of the Dockerfile of the image.


## Deploy to Cloud Run

Let’s run the following command 🤞

```bash
gcloud run deploy -- image eu.gcr.io/wagon-devops-day-5/<user.github_nickname>
```

- You will be ask to give a name to your service, you can call it `docker-101-<your_github_name>`
- Then you will be asked to choose a data center in which you want to send your image. You can choose 125 for europe-west1
- Then you will be asked if you want to make your app public and usable by anyone. In this exercice, we want to make it public so let's says yes.
- After a few seconds, your container should be deployed

After confirmation, you should see a similar output indicating that the service is live 🎉

```txt
Service name (xxx):
Allow unauthenticated invocations to [xxx] (y/N)?  y

Deploying container to Cloud Run service [xxx] in project [le-wagon-devops-day-5] region [europe-west1]
✓ Deploying new service... Done.
  ✓ Creating Revision... Revision deployment finished. Waiting for health check to begin.
  ✓ Routing traffic...
  ✓ Setting IAM Policy...
Done.

Service [xxx] has been deployed and is serving 100 percent of traffic.
Service URL: <https://xxx.a.run.app>
```


You can access to your public app by clicking on the URL, congrats!

Any developer in the world 🌍 is now able to browse to the deployed url and make a prediction using the API 🤖!

⚠️ Keep in mind that you pay for the service as long as it is up 💸
If you want to inspect your running container, look at the logs, change the machine type that host it, you can head over to the dashboard and [have a look](<https://console.cloud.google.com/run>).
