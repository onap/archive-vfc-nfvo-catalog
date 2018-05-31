FROM ubuntu:14.04

ARG HTTP_PROXY=${HTTP_PROXY}
ARG HTTPS_PROXY=${HTTPS_PROXY}

ENV http_proxy $HTTP_PROXY
ENV https_proxy $HTTPS_PROXY

RUN echo "mysql-server mysql-server/root_password password root" | debconf-set-selections
RUN echo "mysql-server mysql-server/root_password_again password root" | debconf-set-selections

RUN apt-get update && \
    apt-get install -y python-virtualenv && \
    apt-get install -y python-setuptools && \
    apt-get install -y python-dev && \
    apt-get install -y python-pip && \
    apt-get install -y gcc && \
    apt-get install -y libmysqlclient-dev && \
    apt-get install -y redis-server && \
    apt-get install -y mysql-server && \
    apt-get install -y mysql-client && \
    apt-get install -y wget && \
    apt-get install -y unzip && \
    apt-get install -y curl && \
    apt-get install -y build-essential && \
    apt-get install -y libssl-dev && \
    apt-get install -y libffi-dev

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

ADD . /service
WORKDIR /service

# get binary zip from nexus - vfc-nfvo-catalog
RUN wget -q -O vfc-nfvo-catalog.zip 'https://nexus.onap.org/service/local/artifact/maven/redirect?r=snapshots&g=org.onap.vfc.nfvo.catalog&a=vfc-nfvo-catalog&v=LATEST&e=zip' && \
    unzip vfc-nfvo-catalog.zip && \
    rm -rf vfc-nfvo-catalog.zip

RUN sed -i "s|bind-address.*|# bind-address = 127.0.0.1|" /etc/mysql/my.cnf

VOLUME /var/lib/mysql

WORKDIR /service/vfc/nfvo/catalog
RUN pip install --pre -r requirements.txt

EXPOSE 8806
EXPOSE 3306
EXPOSE 6379

WORKDIR /service
ENTRYPOINT vfc/nfvo/catalog/docker/docker-entrypoint.sh
