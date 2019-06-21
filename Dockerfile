FROM python:3-slim

RUN mkdir -p /niu-api

RUN apt-get update
#RUN pip3 install --no-cache-dir prometheus_client
RUN pip3 install --no-cache-dir requests

WORKDIR /niu-api

COPY niu-api.py /niu-api/
RUN chmod +x niu-api.py

expose 8345

#ENTRYPOINT [ "python", "-u", "./niu-api.py"]
