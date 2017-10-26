FROM karmab/client-python-kubernetes
MAINTAINER Karim Boumedhel <karimboumedhel@gmail.com>

ADD initializer.py /tmp
ADD initializer_deployments.yml /tmp

ENTRYPOINT  ["python", "-u", "/tmp/initializer.py"]
