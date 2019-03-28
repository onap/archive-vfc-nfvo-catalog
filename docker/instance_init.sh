#!/bin/bash
######
# by vfc-db test
#####
# echo "No service needs init."
#MYSQL_USER=$1
######
#by duan
pip install PyMySQL==0.9.3
if [ ! -f /var/log/onap/vfc/catalog/runtime_catalog.log ]; then
    mkdir -p /var/log/onap/vfc/catalog
    touch /var/log/onap/vfc/catalog/runtime_catalog.log
else
    echo >/var/log/onap/vfc/catalog/runtime_catalog.log
fi

if [ ! -f /service/vfc/nfvo/catalog/resources/bin/logs/runtime_catalog.log ]; then
    mkdir -p /service/vfc/nfvo/catalog/resources/bin/logs
    touch /service/vfc/nfvo/catalog/resources/bin/logs/runtime_catalog.log
else
    echo >/service/vfc/nfvo/catalog/resources/bin/logs/runtime_catalog.log
fi

MYSQL_IP=`echo $MYSQL_ADDR | cut -d: -f 1`
MYSQL_PORT=`echo $MYSQL_ADDR | cut -d: -f 2`
MYSQL_USER=`echo $MYSQL_AUTH | cut -d: -f 1`
MYSQL_ROOT_PASSWORD=`echo $MYSQL_AUTH | cut -d: -f 2`

function create_database {
    cd /service/vfc/nfvo/catalog/resources/bin
    bash initDB.sh $MYSQL_USER $MYSQL_ROOT_PASSWORD $MYSQL_PORT $MYSQL_IP
    #DIRNAME=`dirname $0`
    #HOME=`cd $DIRNAME/; pwd`
    #man_path=$HOME/../
    man_path=/service/vfc/nfvo/catalog
    #tab=`mysql -u${MYSQL_USER} -p${MYSQL_PASSWORD} -P${MYSQL_PORT} -h${MYSQL_IP} -e "use vfcnfvolcm; select count(*) from vfcnfvolcm;"`
    tab=`mysql -u${MYSQL_USER} -p${MYSQL_ROOT_PASSWORD} -P${MYSQL_PORT} -h${MYSQL_IP} -e "SELECT count(TABLE_NAME) FROM information_schema.TABLES WHERE TABLE_SCHEMA='nfvocatalog';"`
    tab1=`echo $tab |awk '{print $2}'`
	echo "=========="
	echo $tab1
	echo "=========="
    if [ $tab1 -eq 0 ] ; then
	echo "============"
	echo $tab1
	echo "============"
        echo "TABLE NOT EXISTS, START MIGRATE"
        python $man_path/manage.py makemigrations database && python $man_path/manage.py migrate &
        wait
        tab2=`mysql -u${MYSQL_USER} -p${MYSQL_ROOT_PASSWORD} -P${MYSQL_PORT} -h${MYSQL_IP} -e "SELECT count(TABLE_NAME) FROM information_schema.TABLES WHERE TABLE_SCHEMA='nfvocatalog';"`
	tab3=`echo $tab2|awk '{print $2}'`
        if [ $tab3 -gt 0  ] ; then
        echo "TABLE CREATE SUCCESSFUL"
    fi
else
    echo "table already existed"
    exit 1
fi
 }

if [ ! -f /service/vfc/nfvo/catalog/docker/db.txt ]; then
    echo 1 > /service/vfc/nfvo/catalog/docker/db.txt
    echo `pwd` >> /service/vfc/nfvo/catalog/docker/db.txt
    create_database
else
    echo "database already existed"
fi
