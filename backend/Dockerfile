FROM python:3.9.1-alpine
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev
WORKDIR /film/film_1/film_3/backend

ENV PYTHONUNBUFFERED 1

COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
COPY . .