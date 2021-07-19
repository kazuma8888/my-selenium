FROM python:3.7-alpine

ENV PYTHONIOENCODING utf-8
ENV PYTHONUNBUFFERED 1
WORKDIR /app

RUN apk add --update \
    wget \
    # Add chromium and dependences
    udev \
    ttf-freefont \
    chromium \
    chromium-chromedriver \
    gcc \
    libc-dev \
    libxml2-dev \
    libxslt-dev

COPY ./requirements.txt /app/
RUN pip3 install -r requirements.txt

COPY . /app/