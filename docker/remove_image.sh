#!/bin/bash

function remove_catalog_container {
    docker container stop vfc-catalog
    docker container rm vfc-catalog
}

function remove_catalog_image {
    docker image rm vfc-catalog
}

remove_catalog_container
