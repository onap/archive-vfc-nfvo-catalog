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


class NSDModel(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=200)
    nsd_id = models.CharField(db_column='NSDID', max_length=200)
    name = models.CharField(db_column='NAME', max_length=200)
    vendor = models.CharField(db_column='VENDOR', max_length=200, null=True, blank=True)
    description = models.CharField(db_column='DESCRIPTION', max_length=200, null=True, blank=True)
    version = models.CharField(db_column='VERSION', max_length=200, null=True, blank=True)
    nsd_model = models.TextField(db_column='NSDMODEL', max_length=65535, null=True, blank=True)
    nsd_path = models.CharField(db_column='NSDPATH', max_length=300, null=True, blank=True)

    class Meta:
        db_table = 'NFVO_NSPACKAGE'

class NfPackageModel(models.Model):
    uuid = models.CharField(db_column='UUID', primary_key=True, max_length=255)
    nfpackageid = models.CharField(db_column='NFPACKAGEID', max_length=200)
    vnfdid = models.CharField(db_column='VNFDID', max_length=255)
    vendor = models.CharField(db_column='VENDOR', max_length=255)
    vnfdversion = models.CharField(db_column='VNFDVERSION', max_length=255)
    vnfversion = models.CharField(db_column='VNFVERSION', max_length=255)
    vnfdmodel = models.TextField(db_column='VNFDMODEL', max_length=65535, blank=True, null=True)
    vnfd_path = models.CharField(db_column='VNFDPATH', max_length=300, null=True, blank=True)

    class Meta:
        db_table = 'NFVO_NFPACKAGE'


class VnfPackageFileModel(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    vnfpid = models.CharField(db_column='NFPACKAGEID', max_length=50)
    filename = models.CharField(db_column='FILENAME', max_length=100)
    filetype = models.CharField(db_column='FILETYPE', max_length=2)
    imageid = models.CharField(db_column='IMAGEID', max_length=50)
    vimid = models.CharField(db_column='VIMID', max_length=50)
    vimuser = models.CharField(db_column='VIMUSER', max_length=50)
    tenant = models.CharField(db_column='TENANT', max_length=50)
    purpose = models.CharField(db_column='PURPOSE', max_length=1000)
    status = models.CharField(db_column='STATUS', max_length=10)

    class Meta:
        db_table = 'NFVO_NFPACKAGEFILE'


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
        db_table = 'NFVO_JOB'

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
        db_table = 'NFVO_JOB_STATUS'

    def toJSON(self):
        import json
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))

