--
-- Copyright 2018 ZTE Corporation.
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

DROP TABLE IF EXISTS CATALOG_JOB;
DROP TABLE IF EXISTS CATALOG_JOB_STATUS;
DROP TABLE IF EXISTS CATALOG_NSPACKAGE;
DROP TABLE IF EXISTS CATALOG_SOFTWAREIMAGEMODEL;
DROP TABLE IF EXISTS CATALOG_VNFPACKAGE;
DROP TABLE IF EXISTS CATALOG_PNFPACKAGE;

--
-- Create model JobModel
--
CREATE TABLE `CATALOG_JOB` (`JOBID` varchar(255) NOT NULL PRIMARY KEY, `JOBTYPE` varchar(255) NOT NULL, `JOBACTION` varchar(255) NOT NULL, `RESID` varchar(255) NOT NULL, `STATUS` integer NULL, `STARTTIME` varchar(255) NULL, `ENDTIME` varchar(255) NULL, `PROGRESS` integer NULL, `USER` varchar(255) NULL, `PARENTJOBID` varchar(255) NULL, `RESNAME` varchar(255) NULL);
--
-- Create model JobStatusModel
--
CREATE TABLE `CATALOG_JOB_STATUS` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `INDEXID` integer NOT NULL, `JOBID` varchar(255) NOT NULL, `STATUS` varchar(255) NOT NULL, `PROGRESS` integer NULL, `DESCP` longtext NOT NULL, `ERRCODE` varchar(255) NULL, `ADDTIME` varchar(255) NULL);
--
-- Create model NSPackageModel
--
CREATE TABLE `CATALOG_NSPACKAGE` (`NSPACKAGEID` varchar(50) NOT NULL PRIMARY KEY, `NSPACKAGEURI` varchar(300) NULL, `CHECKSUM` varchar(50) NULL, `SDCCSARID` varchar(50) NULL, `ONBOARDINGSTATE` varchar(20) NULL, `OPERATIONALSTATE` varchar(20) NULL, `USAGESTATE` varchar(20) NULL, `DELETIONPENDING` varchar(20) NULL, `NSDID` varchar(50) NULL, `NSDNAME` varchar(50) NULL, `NSDDESIGNER` varchar(50) NULL, `NSDDESCRIPTION` varchar(100) NULL, `NSDVERSION` varchar(20) NULL, `USERDEFINEDDATA` longtext NULL, `LOCALFILEPATH` varchar(300) NULL, `NSDMODEL` longtext NULL, `INVARIANTID` varchar(50) NULL);
--
-- Create model SoftwareImageModel
--
CREATE TABLE `CATALOG_SOFTWAREIMAGEMODEL` (`IMAGEID` varchar(50) NOT NULL PRIMARY KEY, `CONTAINERFORMAT` varchar(20) NOT NULL, `DISKFORMAT` varchar(20) NOT NULL, `MINDISK` varchar(20) NOT NULL, `MINRAM` varchar(20) NOT NULL, `USAERMETADATA` varchar(1024) NOT NULL, `VNFPACKAGEID` varchar(50) NOT NULL, `FILEPATH` varchar(300) NOT NULL, `STATUS` varchar(10) NOT NULL, `VIMID` varchar(50) NOT NULL);
--
-- Create model VnfPackageModel
--
CREATE TABLE `CATALOG_VNFPACKAGE` (`VNFPACKAGEID` varchar(50) NOT NULL PRIMARY KEY, `VNFPACKAGEURI` varchar(300) NULL, `SDCCSARURI` varchar(300) NULL, `CHECKSUM` varchar(50) NULL, `ONBOARDINGSTATE` varchar(20) NULL, `OPERATIONALSTATE` varchar(20) NULL, `USAGESTATE` varchar(20) NULL, `DELETIONPENDING` varchar(20) NULL, `VNFDID` varchar(50) NULL, `VENDOR` varchar(50) NULL, `VNFDPRODUCTNAME` varchar(50) NULL, `VNFDVERSION` varchar(20) NULL, `VNFSOFTWAREVERSION` varchar(20) NULL, `USERDEFINEDDATA` longtext NULL, `LOCALFILEPATH` varchar(300) NULL, `VNFDMODEL` longtext NULL);
--
-- Create model PnfPackageModel
--
CREATE TABLE `CATALOG_PNFPACKAGE` (`PNFPACKAGEID` varchar(50) NOT NULL PRIMARY KEY, `PNFPACKAGEURI` varchar(300) NULL, `SDCCSARURI` varchar(300) NULL, `CHECKSUM` varchar(50) NULL, `ONBOARDINGSTATE` varchar(20) NULL, `USAGESTATE` varchar(20) NULL, `DELETIONPENDING` varchar(20) NULL, `PNFDID` varchar(50) NULL, `VENDOR` varchar(50) NULL, `PNFDPRODUCTNAME` varchar(50) NULL, `PNFDVERSION` varchar(20) NULL, `PNFSOFTWAREVERSION` varchar(20) NULL, `USERDEFINEDDATA` longtext NULL, `LOCALFILEPATH` varchar(300) NULL, `PNFDMODEL` longtext NULL, `PNFDNAME` varchar(100) NULL);
