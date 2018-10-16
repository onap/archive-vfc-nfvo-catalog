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

from catalog.packages.biz.common import parse_file_range, read, save
from catalog.pub.config.config import CATALOG_ROOT_PATH
from catalog.pub.database.models import VnfPackageModel
from catalog.pub.exceptions import CatalogException, ResourceNotFoundException
from catalog.pub.utils.values import ignore_case_get
from catalog.pub.utils import fileutil, toscaparser
from catalog.packages.const import PKG_STATUS


logger = logging.getLogger(__name__)


class VnfPackage(object):

    def __init__(self):
        pass

    def create_vnf_pkg(self, data):
        user_defined_data = ignore_case_get(data, "userDefinedData", {})
        vnf_pkg_id = str(uuid.uuid4())
        VnfPackageModel.objects.create(
            vnfPackageId=vnf_pkg_id,
            onboardingState=PKG_STATUS.CREATED,
            operationalState=PKG_STATUS.DISABLED,
            usageState=PKG_STATUS.NOT_IN_USE,
            userDefinedData=json.dumps(user_defined_data)
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
            logger.error('VNF package(%s) does not exist.' % vnf_pkg_id)
            raise ResourceNotFoundException('VNF package(%s) does not exist.' % vnf_pkg_id)
        return fill_response_data(nf_pkg[0])

    def delete_vnf_pkg(self, vnf_pkg_id):
        vnf_pkg = VnfPackageModel.objects.filter(vnfPackageId=vnf_pkg_id)
        if not vnf_pkg.exists():
            logger.debug('VNF package(%s) has been deleted.' % vnf_pkg_id)
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
        logger.info('VNF package(%s) has been deleted.' % vnf_pkg_id)

    def upload(self, vnf_pkg_id, remote_file):
        logger.info('Start to upload VNF package(%s)...' % vnf_pkg_id)
        vnf_pkg = VnfPackageModel.objects.filter(vnfPackageId=vnf_pkg_id)
        if vnf_pkg[0].onboardingState != PKG_STATUS.CREATED:
            logger.error("VNF package(%s) is not CREATED" % vnf_pkg_id)
            raise CatalogException("VNF package(%s) is not CREATED" % vnf_pkg_id)
        vnf_pkg.update(onboardingState=PKG_STATUS.UPLOADING)

        local_file_name = save(remote_file, vnf_pkg_id)
        logger.info('VNF package(%s) has been uploaded.' % vnf_pkg_id)
        return local_file_name

    def download(self, vnf_pkg_id, file_range):
        logger.info('Start to download VNF package(%s)...' % vnf_pkg_id)
        nf_pkg = VnfPackageModel.objects.filter(vnfPackageId=vnf_pkg_id)
        if not nf_pkg.exists():
            logger.error('VNF package(%s) does not exist.' % vnf_pkg_id)
            raise ResourceNotFoundException('VNF package(%s) does not exist.' % vnf_pkg_id)
        if nf_pkg[0].onboardingState != PKG_STATUS.ONBOARDED:
            raise CatalogException("VNF package (%s) is not on-boarded" % vnf_pkg_id)

        local_file_path = nf_pkg[0].localFilePath
        start, end = parse_file_range(local_file_path, file_range)
        logger.info('VNF package (%s) has been downloaded.' % vnf_pkg_id)
        return read(local_file_path, start, end)


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
        logger.info("Start to upload VNF packge(%s) from URI..." % self.vnf_pkg_id)
        vnf_pkg = VnfPackageModel.objects.filter(vnfPackageId=self.vnf_pkg_id)
        if vnf_pkg[0].onboardingState != PKG_STATUS.CREATED:
            logger.error("VNF package(%s) is not CREATED" % self.vnf_pkg_id)
            raise CatalogException("VNF package (%s) is not created" % self.vnf_pkg_id)
        vnf_pkg.update(onboardingState=PKG_STATUS.UPLOADING)

        uri = ignore_case_get(self.data, "addressInformation")
        request = urllib2.Request(uri)
        response = urllib2.urlopen(request)

        local_file_dir = os.path.join(CATALOG_ROOT_PATH, self.vnf_pkg_id)
        self.upload_file_name = os.path.join(local_file_dir, os.path.basename(uri))
        if not os.path.exists(local_file_dir):
            fileutil.make_dirs(local_file_dir)
        with open(self.upload_file_name, "wb") as local_file:
            local_file.write(response.read())
        response.close()
        logger.info('VNF packge(%s) has been uploaded.' % self.vnf_pkg_id)


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
    logger.info('Start to process VNF package(%s)...' % vnf_pkg_id)
    vnf_pkg = VnfPackageModel.objects.filter(vnfPackageId=vnf_pkg_id)
    vnf_pkg.update(onboardingState=PKG_STATUS.PROCESSING)
    vnfd_json = toscaparser.parse_vnfd(vnf_pkg_path)
    vnfd = json.JSONDecoder().decode(vnfd_json)

    vnfd_id = vnfd["metadata"]["id"]
    if VnfPackageModel.objects.filter(vnfdId=vnfd_id):
        logger.error("VNF package(%s) already exists." % vnfd_id)
        raise CatalogException("VNF package(%s) already exists." % vnfd_id)

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
    logger.info('VNF package(%s) has been processed.' % vnf_pkg_id)


def handle_upload_failed(vnf_pkg_id):
    vnf_pkg = VnfPackageModel.objects.filter(vnfPackageId=vnf_pkg_id)
    vnf_pkg.update(onboardingState=PKG_STATUS.CREATED)
