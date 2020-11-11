FROM debian:buster

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get dist-upgrade
RUN apt-get install python3 python3-pip wget unzip -y
RUN python3 -m pip install triggers

#WORKDIR /py_scan_app
#CMD ["python3", "/py_scan_app/scan.py"]