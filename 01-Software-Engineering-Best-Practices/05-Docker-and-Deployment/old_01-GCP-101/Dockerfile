
FROM python:3.8-buster

COPY wsgi.py /wsgi.py

COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Notice here the port parameter, it is required by google cloud run
CMD flask run --host 0.0.0.0 --port $PORT
