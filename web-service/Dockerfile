FROM python:3.7-alpine

COPY requirements.txt /

RUN pip install -r /requirements.txt

COPY src/ /app
WORKDIR /app
VOLUME /data

ENTRYPOINT ["python"]
CMD ["app.py"]
