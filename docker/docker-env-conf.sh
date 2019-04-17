#!/bin/bash

config_env(){

    sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
    apk --no-cache update
    apk --no-cache add bash curl gcc wget mysql-client openssl-dev
    apk --no-cache add python-dev libffi-dev musl-dev py2-virtualenv

    # get binary zip from nexus - vfc-nfvo-catalog
    wget -q -O vfc-nfvo-catalog.zip 'https://nexus.onap.org/service/local/artifact/maven/redirect?r=snapshots&g=org.onap.vfc.nfvo.catalog&a=vfc-nfvo-catalog&v=LATEST&e=zip' && \
    unzip vfc-nfvo-catalog.zip && \
    rm -rf vfc-nfvo-catalog.zip && \
    pip install --upgrade setuptools pip && \
    pip install --no-cache-dir --pre -r  /service/vfc/nfvo/catalog/requirements.txt
}

add_onap(){

    apk --no-cache add sudo
    addgroup -g 1000 -S onap && \
    adduser onap -D -G onap -u 1000 && \
    chmod u+w /etc/sudoers && \
    sed -i '/User privilege/a\\onap    ALL=(ALL:ALL) NOPASSWD:ALL' /etc/sudoers && \
    chmod u-x /etc/sudoers && \
    chown onap:onap -R /service
}

clean_env(){

    rm -rf /var/cache/apk/*
    rm -rf /root/.cache/pip/*
    rm -rf /tmp/*
}

config_env
wait
add_onap
clean_env



