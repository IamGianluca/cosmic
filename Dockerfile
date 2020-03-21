FROM python:3.8-alpine

RUN apk add --no-cache --virtual .build-deps gcc postgresql-dev musl-dev python3-dev
RUN apk add libpq curl

# required by cryptography (Python lib)
RUN apk add --no-cache libressl-dev musl-dev libffi-dev

RUN mkdir -p /
COPY . /

RUN pip install poetry
RUN poetry install --no-dev

RUN apk del --no-cache .build-deps

ENV FLASK_APP=cosmic/entrypoints/flask_app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
CMD poetry run flask run --host=0.0.0.0 --port=80
