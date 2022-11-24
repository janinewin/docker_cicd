FROM python:3.8.10-slim

# Do not use env as this would persist after the build and would impact your containers, children images
ARG DEBIAN_FRONTEND=noninteractive

# Force the stdout and stderr streams to be unbuffered.
ENV PYTHONUNBUFFERED 1

WORKDIR /server

COPY ./  ./

RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y gzip wget make \
    && pip install --no-cache-dir poetry \
    && poetry install --only main \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /server

RUN make genproto

CMD ["poetry", "run", "python", "server.py"]
