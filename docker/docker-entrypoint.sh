#!/bin/bash

if [ -z "$SERVICE_IP" ]; then
    export SERVICE_IP=`hostname -i`
fi
echo "SERVICE_IP=$SERVICE_IP"

if [ -z "$MSB_ADDR" ]; then
    echo "Missing required variable MSB_ADDR: Microservices Service Bus address <ip>:<port>"
    exit 1
fi
echo "MSB_ADDR=$MSB_ADDR"

if [ -z "$MYSQL_ADDR" ]; then
    echo "Missing required variable MYSQL_ADDR: <ip>:<port>"
    exit 1
fi
echo "MYSQL_ADDR=$MYSQL_ADDR"

if [ -z "$SDC_USER" ]; then
    echo "Missing required variable SDC_USER"
    exit 1
fi
echo "SDC_USER=$SDC_USER"

if [ -z "$SDC_PASSWD" ]; then
    echo "Missing required variable SDC_PASSWD"
    exit 1
fi
echo "SDC_PASSWD=$SDC_PASSWD"

# Wait for MSB initialization
echo "Wait for MSB initialization"
for i in {1..5}; do
    curl -sS -m 1 $MSB_ADDR > /dev/null && break
    sleep $i
done

# Wait for DB initialization
echo "Wait for DB initialization"
for i in {1..5}; do
    curl -sS -m 1 $MYSQL_ADDR > /dev/null && break
    sleep $i
done

# Configure service based on docker environment variables
vfc/nfvo/catalog/docker/instance_config.sh

# microservice-specific one-time initialization
vfc/nfvo/catalog/docker/instance_init.sh

date > init.log

# Start the microservice
vfc/nfvo/catalog/docker/instance_run.sh
