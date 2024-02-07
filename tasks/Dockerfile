FROM python:3.9-slim

RUN pip install celery
RUN pip install pymongo

ADD /tasks /tasks
ADD constants.py /tasks
WORKDIR /tasks

ENTRYPOINT celery -A tasks worker --loglevel=info
