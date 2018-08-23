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

import logging
import os
import sys
import threading
import traceback
import urllib2
import uuid

from catalog.pub.config.config import CATALOG_ROOT_PATH
from catalog.pub.database.models import VnfPackageModel
from catalog.pub.exceptions import CatalogException
from catalog.pub.utils.values import ignore_case_get
from catalog.pub.utils import fileutil

logger = logging.getLogger(__name__)


def create_vnf_pkg(data):
    user_defined_data = ignore_case_get(data, "userDefinedData")
    vnfPkgId = str(uuid.uuid4())
    VnfPackageModel.objects.create(
        vnfPackageId=vnfPkgId,
        onboardingState="CREATED",
        operationalState="DISABLED",
        usageState="NOT_IN_USE",
        userDefinedData=user_defined_data
    )
    data = {
        "id": vnfPkgId,
        "onboardingState": "CREATED",
        "operationalState": "DISABLED",
        "usageState": "NOT_IN_USE",
        "userDefinedData": user_defined_data,
        "_links": None
    }
    return data


def query_multiple():
    pkgs_info = []
    nf_pkgs = VnfPackageModel.objects.filter()
    if not nf_pkgs.exists():
        raise CatalogException('VNF packages do not exist.')
    for nf_pkg in nf_pkgs:
        ret = query_single(nf_pkg.vnfPackageId)
        pkgs_info.append(ret)
    return pkgs_info


def query_single(vnfPkgId):
    pkg_info = {}
    nf_pkg = VnfPackageModel.objects.filter(vnfPackageId=vnfPkgId)
    if not nf_pkg.exists():
        raise CatalogException('VNF package(%s) does not exist.' % vnfPkgId)
    pkg_info["id"] = nf_pkg[0].vnfPackageId
    pkg_info["vnfdId"] = nf_pkg[0].vnfdId
    pkg_info["vnfdProvider"] = nf_pkg[0].vnfVendor
    pkg_info["vnfProductName"] = nf_pkg[0].vnfdProductName
    pkg_info["vnfSoftwareVersion"] = nf_pkg[0].vnfSoftwareVersion
    pkg_info["vnfdVersion"] = nf_pkg[0].vnfdVersion
    pkg_info["checksum"] = nf_pkg[0].checksum
    pkg_info["softwareImages"] = ""  # TODO
    pkg_info["additionalArtifacts"] = ""  # TODO
    pkg_info["onboardingState"] = nf_pkg[0].onboardingState
    pkg_info["operationalState"] = nf_pkg[0].operationalState
    pkg_info["usageState"] = nf_pkg[0].usageState
    pkg_info["userDefinedData"] = nf_pkg[0].userDefinedData
    pkg_info["_links"] = ""  # TODO
    return pkg_info


def delete_vnf_pkg(vnfPkgId):
    vnf_pkg = VnfPackageModel.objects.filter(vnfPackageId=vnfPkgId)
    if not vnf_pkg.exists():
        logger.debug('VNF package(%s) is deleted.' % vnfPkgId)
        return
    if vnf_pkg[0].onboardingState != "CREATED":
        raise CatalogException("The VNF package (%s) is not on-boarded" % vnfPkgId)
    if vnf_pkg[0].operationalState != "DISABLED":
        raise CatalogException("The VNF package (%s) is not disabled" % vnfPkgId)
    if vnf_pkg[0].usageState != "NOT_IN_USE":
        raise CatalogException("The VNF package (%s) is in use" % vnfPkgId)
    vnf_pkg.delete()
    vnf_pkg_path = os.path.join(CATALOG_ROOT_PATH, vnfPkgId)
    fileutil.delete_dirs(vnf_pkg_path)


class VnfpkgUploadThread(threading.Thread):
    def __init__(self, data, vnfPkgId):
        threading.Thread.__init__(self)
        self.vnfPkgId = vnfPkgId
        self.data = data

    def run(self):
        try:
            self.upload_vnfPkg_from_uri()
        except CatalogException as e:
            logger.error(e.message)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            logger.error(str(sys.exc_info()))

    def upload_vnfPkg_from_uri(self):
        logger.debug("UploadVnf %s" % self.vnfPkgId)
        uri = ignore_case_get(self.data, "addressInformation")
        upload_path = os.path.join(CATALOG_ROOT_PATH, self.vnfPkgId)
        if not os.path.exists(upload_path):
            os.makedirs(upload_path, 0o777)
        r = urllib2.Request(uri)
        req = urllib2.urlopen(r)

        upload_file_name = os.path.join(upload_path, os.path.basename(uri))
        save_file = open(upload_file_name, "wb")
        save_file.write(req.read())
        save_file.close()
        req.close()
