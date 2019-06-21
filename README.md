# niu-api.py

API wrapper for access to the data of your NIU electric scooter in python

inspired and parts borrowed from https://github.com/volkerschulz/NIU-API (php) and https://github.com/BlueAndi/niu-cloud-cli (node)

projects originated from https://www.elektroroller-forum.de/viewtopic.php?f=63&t=6227 [German]

needs the following environment variables for credentials:

export NIU_EMAIL="mymail@domain.com"
export NIU_PASSWORD="secret"
export NIU_COUNTRYCODE="49"

DOCKER
======

in case you want to run it in a container (and have docker already installed),
create a file named "env" with following content in current folder:

NIU_EMAIL=mymail@domain.com
NIU_PASSWORD=secret
NIU_COUNTRYCODE=49

then run

docker build -t niu-api .

docker run -it --env-file env niu-api /bin/bash

./niu-api.py
