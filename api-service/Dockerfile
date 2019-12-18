FROM python:3.7-slim-buster

RUN apt-get update

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY src/ /src
WORKDIR /src

ENV FLASK_APP=aveslog

VOLUME /src/logs
CMD ["gunicorn", "-c", "gunicorn_config.py", "aveslog:create_app()"]
