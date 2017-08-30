--
-- Copyright  2017 ZTE Corporation.
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

use nfvocatalog;

DROP TABLE IF EXISTS NFVO_JOB;
CREATE TABLE NFVO_JOB (
  `JOBID` varchar(255) NOT NULL PRIMARY KEY,
  `JOBTYPE` varchar (255) NOT NULL,
  `JOBACTION` varchar(255) NOT NULL,
  `RESID` varchar(255) NOT NULL,
  `STATUS` integer NULL,
  `STARTTIME` varchar(255) NULL,
  `ENDTIME` varchar(255) NULL,
  `PROGRESS` integer NULL,
  `USER` varchar(255) NULL,
  `PARENTJOBID` varchar(255) NULL,
  `RESNAME` varchar(255) NULL
);

DROP TABLE IF EXISTS NFVO_JOB_STATUS;
CREATE TABLE NFVO_JOB_STATUS (
  `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `INDEXID` integer NOT NULL,
  `JOBID` varchar(255) NOT NULL,
  `STATUS` varchar(255) NOT NULL,
  `PROGRESS` integer NULL,
  `DESCP` longtext NOT NULL,
  `ERRCODE` varchar(255) NULL,
  `ADDTIME` varchar(255) NULL
);


DROP TABLE IF EXISTS NFVO_NFPACKAGE;
CREATE TABLE NFVO_NFPACKAGE (
  `UUID` varchar(255) NOT NULL PRIMARY KEY,
  `NFPACKAGEID` varchar(200) NOT NULL,
  `VNFDID` varchar(255) NOT NULL,
  `VENDOR` varchar(255) NOT NULL,
  `VNFDVERSION` varchar(255) NOT NULL,
  `VNFVERSION` varchar(255) NOT NULL,
  `VNFDMODEL` longtext NULL,
  `VNFDPATH` varchar(300) NULL
);

DROP TABLE IF EXISTS NFVO_NSPACKAGE;
CREATE TABLE NFVO_NSPACKAGE (
  `ID` varchar(200) NOT NULL PRIMARY KEY,
  `NSDID` varchar(200) NOT NULL,
  `NAME` varchar(200) NOT NULL,
  `VENDOR` varchar(200) NULL,
  `DESCRIPTION` varchar(200) NULL,
  `VERSION` varchar(200) NULL,
  `NSDMODEL` longtext NULL,
  `NSDPATH` varchar(300) NULL
);


DROP TABLE IF EXISTS NFVO_NFPACKAGEFILE;
CREATE TABLE NFVO_NFPACKAGEFILE (
  `ID` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `NFPACKAGEID` varchar(50) NOT NULL,
  `FILENAME` varchar(100) NOT NULL,
  `FILETYPE` varchar(2) NOT NULL,
  `IMAGEID` varchar(50) NOT NULL,
  `VIMID` varchar(50) NOT NULL,
  `VIMUSER` varchar(50) NOT NULL,
  `TENANT` varchar(50) NOT NULL,
  `PURPOSE` varchar(1000) NOT NULL,
  `STATUS` varchar(10) NOT NULL
);

