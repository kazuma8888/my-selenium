FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update -y

RUN mkdir -p /var/www
COPY . /var/www
RUN pip install -r /var/www/requirements.txt

WORKDIR /var/www