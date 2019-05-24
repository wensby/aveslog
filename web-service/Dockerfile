FROM python:3.7-alpine

RUN apk update && apk add libpq
RUN apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev

COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN apk del .build-deps

COPY src/ /src
WORKDIR /src

ENV FLASK_APP=birding

CMD ["flask", "run", "--host=0.0.0.0", "--port=3002"]
