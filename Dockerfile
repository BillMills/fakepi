FROM python:3.7

RUN apt-get update
RUN apt-get install -y nano
RUN pip install flask

WORKDIR /app
COPY . .

ENV FLASK_APP=api
CMD flask run --host=0.0.0.0
