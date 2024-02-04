FROM python:3.10
MAINTAINER Zourka

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt/ requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY . /app

CMD python manage.py wait_for_db && python manage.py migrate && python manage.py runserver 0.0.0.0:8000