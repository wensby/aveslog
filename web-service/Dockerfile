FROM python:3.7-alpine

COPY requirements.txt /

RUN apk update && apk add libpq
RUN apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .build-deps

COPY src/ /app
WORKDIR /app
VOLUME /data

ENTRYPOINT ["python"]
CMD ["app.py"]
