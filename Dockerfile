FROM centos:7
MAINTAINER Karim Boumedhel <karimboumedhel@gmail.com>

RUN yum -y install git epel-release && yum -y install python-pip && yum clean all && rm -rf /var/cache/yum
RUN pip install git+git://github.com/kubernetes-incubator/client-python.git
ADD controller.py /tmp
ADD guitar.yml /tmp

ENTRYPOINT  ["python", "/tmp/controller.py"]
