FROM karmab/client-python-kubernetes
MAINTAINER Karim Boumedhel <karimboumedhel@gmail.com>

ADD controller.py /tmp
ADD guitar.yml /tmp

ENTRYPOINT  ["python", "-u", "/tmp/controller.py"]
