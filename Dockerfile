FROM python:3.9-alpine
LABEL maintainer="Escape IT"

COPY ./requirements.txt /requirements.txt
COPY ./Escape_IT /Escape_IT
WORKDIR /Escape_IT

RUN python -m venv /py && \
    apk add --no-cache build-base && \
    apk add --no-cache libffi-dev && \
    /py/bin/pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home django-user && \
    /py/bin/python manage.py makemigrations && \
    /py/bin/python manage.py migrate

ENV PATH="/py/bin:$PATH"

USER django-user