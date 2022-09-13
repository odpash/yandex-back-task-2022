FROM python:3

RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN mkdir /api
COPY . /api/
WORKDIR /api

ENTRYPOINT ["python", "main.py"]
