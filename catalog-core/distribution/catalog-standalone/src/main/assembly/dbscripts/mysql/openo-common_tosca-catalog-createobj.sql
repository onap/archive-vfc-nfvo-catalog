--
-- Copyright 2016 ZTE Corporation.
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--     http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.
--

/******************drop old database and user***************************/
use mysql;
drop database IF  EXISTS catalog;
delete from user where User='catalog';
FLUSH PRIVILEGES;

/******************create new database and user***************************/
create database catalog CHARACTER SET utf8;

GRANT ALL PRIVILEGES ON catalog.* TO 'catalog'@'%' IDENTIFIED BY 'catalog' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON mysql.* TO 'catalog'@'%' IDENTIFIED BY 'catalog' WITH GRANT OPTION;

GRANT ALL PRIVILEGES ON catalog.* TO 'catalog'@'localhost' IDENTIFIED BY 'catalog' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON mysql.* TO 'catalog'@'localhost' IDENTIFIED BY 'catalog' WITH GRANT OPTION;
FLUSH PRIVILEGES;

use catalog;
set Names 'utf8';
/******************delete old table and create new***************************/
use catalog;
DROP TABLE IF EXISTS catalog_package_table;

CREATE TABLE catalog_package_table (
	CSARID                   VARCHAR(200)       NOT NULL,	
	DOWNLOADURI              VARCHAR(200)       NULL,
	SIZE                     VARCHAR(100)       NULL,
	FORMAT                   VARCHAR(100)       NULL,
	CREATETIME               VARCHAR(100)       NULL,
	DELETIONPENDING          VARCHAR(100)       NULL,
	MODIFYTIME               VARCHAR(100)       NULL,
	OPERATIONALSTATE         VARCHAR(100)       NULL,
	USAGESTATE               VARCHAR(100)       NULL,
	ONBOARDSTATE             VARCHAR(100)       NULL,
	NAME                     VARCHAR(100)       NULL,
	VERSION                  VARCHAR(20)        NULL,
	PROVIDER                 VARCHAR(300)       NULL,   
	TYPE                     VARCHAR(300)       NULL,  
    PROCESSSTATE             VARCHAR(100)       NULL,
    CONSTRAINT CATALOG_PACKAGE_TABLE_OID PRIMARY KEY(CSARID)
);

DROP TABLE IF EXISTS catalog_service_template_table;
CREATE TABLE catalog_service_template_table (
	SERVICETEMPLATEID       VARCHAR(200)       NOT NULL,
	TEMPLATENAME            VARCHAR(100)       NULL,
	TYPE                    VARCHAR(50)        NULL,
	VENDOR                  VARCHAR(100)       NULL,
	VERSION                 VARCHAR(20)        NULL,
	CSARID                  VARCHAR(100)       NULL,	
	INPUTS                  LONGTEXT           NULL,
	ROWDATA                 LONGTEXT           NULL,
	OPERATIONS              LONGTEXT           NULL,
    DOWNLOADURI             VARCHAR(200)       NULL,
	SERVICETEMPLATEORIGINALID  VARCHAR(100)    NULL,
    METADATA                LONGTEXT           NULL,	

    CONSTRAINT CATALOG_SERVICE_TEMPLATE_TABLE_OID PRIMARY KEY(SERVICETEMPLATEID)
);

DROP TABLE IF EXISTS catalog_node_template_table;
CREATE TABLE catalog_node_template_table (
	NODETEMPLATEID          VARCHAR(200)       NOT NULL,
	NAME                    VARCHAR(100)       NULL,
	SERVICETEMPLATEID       VARCHAR(200)       NOT NULL,
	TYPE                    VARCHAR(50)        NULL,
	PROPERTIES              LONGTEXT           NULL,
	RELATIONSHIPS           LONGTEXT           NULL,
	
    CONSTRAINT catalog_node_template_table PRIMARY KEY(NODETEMPLATEID,SERVICETEMPLATEID)
);
DROP TABLE IF EXISTS catalog_model_substitution_mapping_table;
CREATE TABLE catalog_model_substitution_mapping_table (
	MAPPINGID               VARCHAR(200)       NOT NULL,
	NODETYPE                VARCHAR(100)       NULL,
	SERVICETEMPLATEID       VARCHAR(200)       NULL,
	REQUIREMENTS            LONGTEXT           NULL,
	CAPABILITIES            LONGTEXT           NULL,
	
    CONSTRAINT catalog_model_substitution_mapping_table PRIMARY KEY(MAPPINGID)
);

