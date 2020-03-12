#!/bin/bash

install_sf(){

    apk --no-cache update
    apk --no-cache add bash curl gcc wget mysql-client openssl-dev
    apk --no-cache add python36-dev libffi-dev musl-dev py3-virtualenv

    # get binary zip from nexus - vfc-nfvo-catalog

    wget -q -O vfc-nfvo-catalog.zip "https://nexus.onap.org/service/local/artifact/maven/redirect?r=snapshots&g=org.onap.vfc.nfvo.catalog&a=vfc-nfvo-catalog&v=${pkg_version}-SNAPSHOT&e=zip" && \
    unzip vfc-nfvo-catalog.zip && \
    rm -rf vfc-nfvo-catalog.zip && \
    pip install --upgrade setuptools pip && \
    pip install --no-cache-dir --pre -r  /service/vfc/nfvo/catalog/requirements.txt
    find  /service -name '*.sh'|xargs chmod a+x
}

add_user(){

    addgroup -g 1000 -S onap && \
    adduser onap -D -G onap -u 1000 && \
    chown onap:onap -R /service
}

config_logdir(){

    if [ ! -d "/var/log/onap" ]; then
       mkdir /var/log/onap
    fi
    chown onap:onap -R /var/log/onap
    chmod g+s /var/log/onap
}

clean_sf_cache(){

    rm -rf /var/cache/apk/*
    rm -rf /root/.cache/pip/*
    rm -rf /tmp/*
}

install_sf
wait
add_user
config_logdir
clean_sf_cache



