# Multistage builds

## 1️⃣ Build single stage image

```bash
docker build -f Dockerfile-single-stage -t single-stage .
```

This image builds an api which runs on port `8080` so we can run it with

```bash
docker run -p 8080:8080 single-stage
```

Lets explore the image with dive!

```bash
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest single-stage
```

Lets see what benefits we get with a multistage build!

<br>

## 2️⃣ Build multi stage image

```bash
docker build -f Dockerfile-multi-stage -t multi-stage .
```

Run our new image

```bash
docker run -p 8080:8080 multi-stage
```

Once you've verified that it works the same its time to dive in and explore the image!

```bash
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest multi-stage
```

🤯 This is quite an extreme example but you can see the power of multistage docker builds especiall when we use a compiled language!
