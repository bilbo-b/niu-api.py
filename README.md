# niu-api.py

API wrapper for access to the data of your NIU electric scooter in python

inspired and parts borrowed from https://github.com/volkerschulz/NIU-API (php) and https://github.com/BlueAndi/niu-cloud-cli (node)

projects originated from https://www.elektroroller-forum.de/viewtopic.php?f=63&t=6227 [German]

needs the following shell environment variables for credentials (set them before running niu.py)

export NIU_EMAIL="mymail@domain.com"  
export NIU_PASSWORD="secret"  
export NIU_COUNTRYCODE="49"  


DOCKER-Container with Prometheus Exporter
=========================================

in case you want to run it in a container (and have docker already installed),
create a file named "env" with following content in current folder:

NIU_EMAIL=mymail@domain.com  
NIU_PASSWORD=secret  
NIU_COUNTRYCODE=49  

then run

docker build -t niu .  
docker run -it -p 8777:8777 --env-file env niu
./niu.py  

now includes a Prometheus exporter (I want the stats in my Grafana Dashboard)
had to rename cli-version to niu.py (no dash allowed when you import)
The exporter is named niu_exporter.py and will be run automatically when the docker container is run

To chose a different port-number, change the variable in the niu_exporter.py file, the Dockerfile and 
the cli-command to start it accordingly
