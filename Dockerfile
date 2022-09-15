FROM python:3.6
RUN apt-get update
RUN mkdir /driveApp
WORKDIR /driveApp
COPY . /driveApp
RUN pip install -r requirements.txt
ENV FLASK_ENV="docker"
EXPOSE 80