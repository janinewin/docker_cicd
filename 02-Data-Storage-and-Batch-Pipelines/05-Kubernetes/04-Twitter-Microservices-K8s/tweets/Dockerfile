FROM python:3.8-buster

COPY models.py /models.py
COPY routes.py /routes.py
COPY wsgi.py /wsgi.py
COPY tweet.db /tweet.db
COPY migrations /migrations

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD flask run --host 0.0.0.0
