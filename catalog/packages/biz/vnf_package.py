# Copyright 2018 ZTE Corporation.
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

import json
import logging
import os
import sys
import threading
import traceback
import urllib2
import uuid

from rest_framework import status
from django.http import StreamingHttpResponse
from catalog.pub.config.config import CATALOG_ROOT_PATH
from catalog.pub.database.models import VnfPackageModel
from catalog.pub.exceptions import CatalogException, ResourceNotFoundException
from catalog.pub.utils.values import ignore_case_get
from catalog.pub.utils import fileutil, toscaparser
from catalog.packages.const import PKG_STATUS


logger = logging.getLogger(__name__)


class VnfPackage(object):
    def create_vnf_pkg(self, data):
        user_defined_data = ignore_case_get(data, "userDefinedData")
        vnf_pkg_id = str(uuid.uuid4())
        VnfPackageModel.objects.create(
            vnfPackageId=vnf_pkg_id,
            onboardingState=PKG_STATUS.CREATED,
            operationalState=PKG_STATUS.DISABLED,
            usageState=PKG_STATUS.NOT_IN_USE,
            userDefinedData=user_defined_data
        )
        data = {
            "id": vnf_pkg_id,
            "onboardingState": PKG_STATUS.CREATED,
            "operationalState": PKG_STATUS.DISABLED,
            "usageState": PKG_STATUS.NOT_IN_USE,
            "userDefinedData": user_defined_data,
            "_links": None
        }
        return data

    def query_multiple(self):
        pkgs_info = []
        nf_pkgs = VnfPackageModel.objects.filter()
        for nf_pkg in nf_pkgs:
            ret = fill_response_data(nf_pkg)
            pkgs_info.append(ret)
        return pkgs_info

    def query_single(self, vnf_pkg_id):
        nf_pkg = VnfPackageModel.objects.filter(vnfPackageId=vnf_pkg_id)
        if not nf_pkg.exists():
            raise ResourceNotFoundException('VNF package(%s) does not exist.' % vnf_pkg_id)
        return fill_response_data(nf_pkg[0])

    def delete_vnf_pkg(self, vnf_pkg_id):
        vnf_pkg = VnfPackageModel.objects.filter(vnfPackageId=vnf_pkg_id)
        if not vnf_pkg.exists():
            logger.debug('VNF package(%s) is deleted.' % vnf_pkg_id)
            return
        '''
        if vnf_pkg[0].operationalState != PKG_STATUS.DISABLED:
            raise CatalogException("The VNF package (%s) is not disabled" % vnf_pkg_id)
        if vnf_pkg[0].usageState != PKG_STATUS.NOT_IN_USE:
            raise CatalogException("The VNF package (%s) is in use" % vnf_pkg_id)
        '''
        vnf_pkg.delete()
        vnf_pkg_path = os.path.join(CATALOG_ROOT_PATH, vnf_pkg_id)
        fileutil.delete_dirs(vnf_pkg_path)

    def fetch_vnf_pkg(self, request, vnf_pkg_id):
        nf_pkg = VnfPackageModel.objects.filter(vnfPackageId=vnf_pkg_id)
        if not nf_pkg.exists():
            raise ResourceNotFoundException('VNF package(%s) does not exist.' % vnf_pkg_id)
        if nf_pkg[0].onboardingState != PKG_STATUS.ONBOARDED:
            raise CatalogException("VNF package (%s) is not on-boarded" % vnf_pkg_id)
        file_path = nf_pkg[0].localFilePath
        file_name = file_path.split('/')[-1]
        file_name = file_name.split('\\')[-1]
        file_range = request.META.get('RANGE')
        if file_range:
            start_end = file_range.split('-')
            start = int(start_end[0])
            end = int(start_end[1])
            f = open(file_path, "rb")
            f.seek(start, 0)
            fs = f.read(end - start + 1)
            response = StreamingHttpResponse(fs, status=status.HTTP_200_OK)
            response['Content-Range'] = file_range
        else:
            response = StreamingHttpResponse(open(file_path, 'rb'), status=status.HTTP_200_OK)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name.encode('utf-8')
        return response


class VnfPkgUploadThread(threading.Thread):
    def __init__(self, data, vnf_pkg_id):
        threading.Thread.__init__(self)
        self.vnf_pkg_id = vnf_pkg_id
        self.data = data
        self.upload_file_name = None

    def run(self):
        try:
            self.upload_vnf_pkg_from_uri()
            parse_vnfd_and_save(self.vnf_pkg_id, self.upload_file_name)
        except CatalogException as e:
            logger.error(e.message)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            logger.error(str(sys.exc_info()))

    def upload_vnf_pkg_from_uri(self):
        logger.debug("UploadVnf %s" % self.vnf_pkg_id)
        vnf_pkg = VnfPackageModel.objects.filter(vnfPackageId=self.vnf_pkg_id)
        if vnf_pkg[0].onboardingState != PKG_STATUS.CREATED:
            raise CatalogException("VNF package (%s) is not created" % self.vnf_pkg_id)
        vnf_pkg.update(onboardingState=PKG_STATUS.UPLOADING)
        uri = ignore_case_get(self.data, "addressInformation")
        upload_path = os.path.join(CATALOG_ROOT_PATH, self.vnf_pkg_id)
        if not os.path.exists(upload_path):
            os.makedirs(upload_path, 0o777)
        r = urllib2.Request(uri)
        req = urllib2.urlopen(r)

        self.upload_file_name = os.path.join(upload_path, os.path.basename(uri))
        save_file = open(self.upload_file_name, "wb")
        save_file.write(req.read())
        save_file.close()
        req.close()


def fill_response_data(nf_pkg):
    pkg_info = {}
    pkg_info["id"] = nf_pkg.vnfPackageId
    pkg_info["vnfdId"] = nf_pkg.vnfdId
    pkg_info["vnfProductName"] = nf_pkg.vnfdProductName
    pkg_info["vnfSoftwareVersion"] = nf_pkg.vnfSoftwareVersion
    pkg_info["vnfdVersion"] = nf_pkg.vnfdVersion
    if nf_pkg.checksum:
        pkg_info["checksum"] = json.JSONDecoder().decode(nf_pkg.checksum)
    pkg_info["softwareImages"] = None  # TODO
    pkg_info["additionalArtifacts"] = None  # TODO
    pkg_info["onboardingState"] = nf_pkg.onboardingState
    pkg_info["operationalState"] = nf_pkg.operationalState
    pkg_info["usageState"] = nf_pkg.usageState
    if nf_pkg.userDefinedData:
        pkg_info["userDefinedData"] = json.JSONDecoder().decode(nf_pkg.userDefinedData)
    pkg_info["_links"] = None  # TODO
    return pkg_info


def parse_vnfd_and_save(vnf_pkg_id, vnf_pkg_path):
    vnf_pkg = VnfPackageModel.objects.filter(vnfPackageId=vnf_pkg_id)
    vnf_pkg.update(onboardingState=PKG_STATUS.PROCESSING)
    vnfd_json = toscaparser.parse_vnfd(vnf_pkg_path)
    vnfd = json.JSONDecoder().decode(vnfd_json)

    vnfd_id = vnfd["metadata"]["id"]
    if VnfPackageModel.objects.filter(vnfdId=vnfd_id):
        raise CatalogException("VNFD(%s) already exists." % vnfd_id)

    vnfd_ver = vnfd["metadata"].get("vnfd_version")
    if not vnfd_ver:
        vnfd_ver = vnfd["metadata"].get("vnfdVersion", "undefined")
    vnf_pkg.update(
        vnfPackageId=vnf_pkg_id,
        vnfdId=vnfd_id,
        vnfVendor=vnfd["metadata"].get("vendor", "undefined"),
        vnfdVersion=vnfd_ver,
        vnfSoftwareVersion=vnfd["metadata"].get("version", "undefined"),
        vnfdModel=vnfd_json,
        onboardingState=PKG_STATUS.ONBOARDED,
        operationalState=PKG_STATUS.ENABLED,
        usageState=PKG_STATUS.NOT_IN_USE,
        localFilePath=vnf_pkg_path
    )


def handle_upload_failed(vnf_pkg_id):
    vnf_pkg = VnfPackageModel.objects.filter(vnfPackageId=vnf_pkg_id)
    vnf_pkg.update(onboardingState=PKG_STATUS.CREATED)
