FROM python:3.7-alpine

RUN adduser -D blog_api_user

WORKDIR /home/api

# RUN apk add --no-cache build-base libxml2 libxml2-dev libxslt-dev
RUN apk upgrade --update
RUN apk add libffi-dev gcc musl-dev

RUN python -m venv venv

COPY app app
COPY requirements.txt run.py shellscripts/run.sh ./

RUN venv/bin/pip install -r requirements.txt

RUN chown -R blog_api_user:blog_api_user ./
USER blog_api_user

ENV PYTHONPATH /home

CMD sh run.sh