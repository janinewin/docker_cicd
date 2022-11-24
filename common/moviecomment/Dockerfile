FROM python:3.8.10-slim

# Do not use env as this would persist after the build and would impact your containers, children images
ARG DEBIAN_FRONTEND=noninteractive

# Force the stdout and stderr streams to be unbuffered.
ENV PYTHONUNBUFFERED 1

WORKDIR /server

COPY ./  ./

RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y gzip wget \
    && pip install --no-cache-dir poetry \
    && poetry install --only main \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /datasets \
  && cd /datasets \
  && wget https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/movies/csvs/movie_ids.csv.gz -O ./movie_ids.csv.gz \
  && wget https://storage.googleapis.com/lewagon-data-engineering-bootcamp-assets/datasets/movies/csvs/imdb_comments_dataset.csv.gz -O ./imdb_comments_dataset.csv.gz \
  && gunzip movie_ids.csv.gz \
  && gunzip imdb_comments_dataset.csv.gz

CMD ["poetry", "run", "uvicorn", "moviecomment.api:app", "--host", "0.0.0.0", "--port", "8000"]
