FROM python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
    libav-tools \
    gunicorn

COPY requirements/ /usr/src/app/requirements/
RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements/prod.txt

COPY . /usr/src/app
