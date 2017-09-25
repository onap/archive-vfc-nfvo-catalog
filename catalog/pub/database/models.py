# Copyright 2016 ZTE Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.db import models


class NSPackageModel(models.Model):
    nsPackageId = models.CharField(db_column='NSPACKAGEID', primary_key=True, max_length=50)
    nsPackageUri = models.CharField(db_column='NSPACKAGEURI', max_length=300, null=True, blank=True)
    checksum = models.CharField(db_column='CHECKSUM', max_length=50, null=True, blank=True)  # checksum
    sdcCsarId = models.CharField(db_column='SDCCSARID', max_length=50, null=True, blank=True)  # SdcCSARUri
    operationalState = models.CharField(db_column='OPERATIONALSTATE', max_length=20, blank=True,null=True)  # operationalState
    usageState = models.CharField(db_column='USAGESTATE', max_length=20, blank=True, null=True)  # usageState
    deletionPending = models.CharField(db_column='DELETIONPENDING', max_length=20, blank=True, null=True)  # deletionPending
    nsdId = models.CharField(db_column='NSDID', max_length=50,blank=True, null=True)
    nsdName = models.CharField(db_column='NSDNAME', max_length=50,blank=True, null=True)
    nsdDesginer = models.CharField(db_column='NSDDESIGNER', max_length=50, null=True, blank=True)
    nsdDescription = models.CharField(db_column='NSDDESCRIPTION', max_length=100, null=True, blank=True)
    nsdVersion = models.CharField(db_column='NSDVERSION', max_length=20, null=True, blank=True)
    userDefinedData = models.TextField(db_column='USERDEFINEDDATA', max_length=1024, blank=True, null=True)  # userDefinedData
    localFilePath = models.CharField(db_column='LOCALFILEPATH', max_length=300, null=True, blank=True)
    nsdModel = models.TextField(db_column='NSDMODEL', max_length=65535, null=True, blank=True)

    class Meta:
        db_table = 'CATALOG_NSPACKAGE'


class VnfPackageModel(models.Model):
    # uuid = models.CharField(db_column='UUID', primary_key=True, max_length=255)
    vnfPackageId = models.CharField(db_column='VNFPACKAGEID', primary_key=True, max_length=50)   # onboardedVnfPkgInfoId
    vnfPackageUri = models.CharField(db_column='VNFPACKAGEURI', max_length=300, null=True, blank=True)  # downloadUri
    SdcCSARUri = models.CharField(db_column='SDCCSARURI', max_length=300, null=True, blank=True)  # SdcCSARUri
    checksum = models.CharField(db_column='CHECKSUM', max_length=50, null=True, blank=True)  # checksum
    operationalState = models.CharField(db_column='OPERATIONALSTATE', max_length=20, blank=True,null=True)  # operationalState
    usageState = models.CharField(db_column='USAGESTATE', max_length=20, blank=True, null=True)  # usageState
    deletionPending = models.CharField(db_column='DELETIONPENDING', max_length=20, blank=True, null=True)  # deletionPending
    vnfdId = models.CharField(db_column='VNFDID', max_length=50,blank=True, null=True)                # vnfdId
    vnfVendor = models.CharField(db_column='VENDOR', max_length=50,blank=True, null=True)  # vnfProvider
    vnfdProductName = models.CharField(db_column='VNFDPRODUCTNAME', max_length=50,blank=True, null=True)  # vnfProductName
    vnfdVersion = models.CharField(db_column='VNFDVERSION', max_length=20,blank=True, null=True)     # vnfdVersion
    vnfSoftwareVersion = models.CharField(db_column='VNFSOFTWAREVERSION', max_length=20,blank=True, null=True)   # vnfSoftwareVersion
    userDefinedData = models.TextField(db_column='USERDEFINEDDATA', max_length=1024, blank=True, null=True)  # userDefinedData
    localFilePath = models.CharField(db_column='LOCALFILEPATH', max_length=300, null=True, blank=True)
    vnfdModel = models.TextField(db_column='VNFDMODEL', max_length=65535, blank=True, null=True)  # vnfd

    class Meta:
        db_table = 'CATALOG_VNFPACKAGE'


class SoftwareImageModel(models.Model):
    imageid = models.CharField(db_column='IMAGEID', primary_key=True, max_length=50)
    containerFormat = models.CharField(db_column='CONTAINERFORMAT', max_length=20)
    diskFormat = models.CharField(db_column='DISKFORMAT', max_length=20)
    mindisk = models.CharField(db_column='MINDISK', max_length=20)
    minram = models.CharField(db_column='MINRAM', max_length=20)
    usermetadata = models.CharField(db_column='USAERMETADATA', max_length=1024)
    vnfPackageId = models.CharField(db_column='VNFPACKAGEID', max_length=50)
    filePath = models.CharField(db_column='FILEPATH', max_length=300)
    status = models.CharField(db_column='STATUS', max_length=10)
    vimid = models.CharField(db_column='VIMID', max_length=50)
    # filetype = models.CharField(db_column='FILETYPE', max_length=2)
    # vimuser = models.CharField(db_column='VIMUSER', max_length=50)
    # tenant = models.CharField(db_column='TENANT', max_length=50)
    # purpose = models.CharField(db_column='PURPOSE', max_length=1000)

    class Meta:
        db_table = 'CATALOG_SOFTWAREIMAGEMODEL'


class JobModel(models.Model):
    jobid = models.CharField(db_column='JOBID', primary_key=True, max_length=255)
    jobtype = models.CharField(db_column='JOBTYPE', max_length=255)
    jobaction = models.CharField(db_column='JOBACTION', max_length=255)
    resid = models.CharField(db_column='RESID', max_length=255)
    status = models.IntegerField(db_column='STATUS', null=True, blank=True)
    starttime = models.CharField(db_column='STARTTIME', max_length=255, null=True, blank=True)
    endtime = models.CharField(db_column='ENDTIME', max_length=255, null=True, blank=True)
    progress = models.IntegerField(db_column='PROGRESS', null=True, blank=True)
    user = models.CharField(db_column='USER', max_length=255, null=True, blank=True)
    parentjobid = models.CharField(db_column='PARENTJOBID', max_length=255, null=True, blank=True)
    resname = models.CharField(db_column='RESNAME', max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'CATALOG_JOB'

    def toJSON(self):
        import json
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))


class JobStatusModel(models.Model):
    indexid = models.IntegerField(db_column='INDEXID')
    jobid = models.CharField(db_column='JOBID', max_length=255)
    status = models.CharField(db_column='STATUS', max_length=255)
    progress = models.IntegerField(db_column='PROGRESS', null=True, blank=True)
    descp = models.TextField(db_column='DESCP', max_length=65535)
    errcode = models.CharField(db_column='ERRCODE', max_length=255, null=True, blank=True)
    addtime = models.CharField(db_column='ADDTIME', max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'CATALOG_JOB_STATUS'

    def toJSON(self):
        import json
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))
