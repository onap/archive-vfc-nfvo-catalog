#!/bin/bash

cd /service/vfc/nfvo/catalog
./run.sh

while [ ! -f logs/runtime_catalog.log ]; do
    sleep 1
done
tail -F logs/runtime_catalog.log
