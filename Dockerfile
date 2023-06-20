FROM python:3.9-alpine

# Install Google Cloud SDK dependencies
RUN apk add --no-cache curl && \
    apk add --no-cache bash

# Download and install Google Cloud SDK
RUN curl https://sdk.cloud.google.com | bash && \
    /root/google-cloud-sdk/install.sh --quiet

# Set the working directory
WORKDIR /Escape_IT

# Copy your application files
COPY service-account-key.json /service-account-key.json
COPY ./requirements.txt /requirements.txt
COPY ./Escape_IT /Escape_IT
COPY ./static /static

# Install application dependencies
RUN python -m venv /py && \
    apk add --no-cache build-base && \
    apk add --no-cache libffi-dev && \
    /py/bin/pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home django-user && \
    /py/bin/python manage.py makemigrations && \
    /py/bin/python manage.py migrate

# Set the environment variables
ENV PATH="/py/bin:/root/google-cloud-sdk/bin:$PATH"
ENV GOOGLE_APPLICATION_CREDENTIALS="/service-account-key.json"

# Set the user
USER root