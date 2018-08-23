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
    # TODO
    data = {
        "id": "1",
        "onboardingState": "CREATED",
        "operationalState": "DISABLED",
        "usageState": "NOT_IN_USE",
        "userDefinedData": "1",
        "_links": None
    }
    return data


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
