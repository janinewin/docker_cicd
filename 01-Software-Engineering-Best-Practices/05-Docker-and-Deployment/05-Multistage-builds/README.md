# Multi-stage Builds

## Build a single-stage image

First, run:

```bash
docker build -f Dockerfile-single-stage -t single-stage .
```

This image builds an API which runs on the port `8080`. We can run it with:

```bash
docker run -p 8080:8080 single-stage
```

Let's explore the image with dive!

```bash
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest single-stage
```

Now, let's see what benefits we get with a multistage build!

<br>

## Build a multi-stage image

Build your multi-stage image:

```bash
docker build -f Dockerfile-multi-stage -t multi-stage .
```

Run it on your 8080 port.

```bash
docker run -p 8080:8080 multi-stage
```

Once you've verified that it works the same, dive in and explore the image!

```bash
docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive:latest multi-stage
```

This is quite an extreme example. Now imagine the power of multi-stage Docker builds when using a compiled language...
