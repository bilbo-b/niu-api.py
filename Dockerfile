FROM python:3-slim

RUN mkdir -p /niu-api

RUN apt-get update
RUN pip3 install --no-cache-dir prometheus_client
RUN pip3 install --no-cache-dir requests

WORKDIR /niu-api

COPY niu.py niu_exporter.py /niu-api/
RUN chmod +x niu.py niu_exporter.py

expose 8777

ENTRYPOINT [ "python", "-u", "./niu_exporter.py"]
