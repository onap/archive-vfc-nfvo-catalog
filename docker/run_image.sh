#!/bin/bash

function run_catalog {
    docker run -it --name vfc-catalog -p 3306:3306 -p 8403:8403 -e MSB_ADDR=127.0.0.1 onap/vfc/catalog
}

run_catalog