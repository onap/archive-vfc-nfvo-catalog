# Copyright (c) 2019, CMCC Technologies. Co., Ltd.
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
import traceback

from coverage.xmlreport import os

from catalog.packages.biz.service_descriptor import ServiceDescriptor
from catalog.pub.config.config import CATALOG_ROOT_PATH, REG_TO_MSB_REG_PARAM, CATALOG_URL_PATH
from catalog.pub.database.models import ServicePackageModel, VnfPackageModel, PnfPackageModel
from catalog.pub.exceptions import CatalogException, PackageNotFoundException, \
    PackageHasExistsException
from catalog.pub.msapi import sdc
from catalog.pub.utils import fileutil, toscaparser

logger = logging.getLogger(__name__)


class ServicePackage(object):
    """
    Actions for sdc service package.
    """

    def __init__(self):
        pass

    def on_distribute(self, csar_id):
        if ServicePackageModel.objects.filter(servicePackageId=csar_id):
            raise PackageHasExistsException("Service CSAR(%s) already exists." % csar_id)

        try:
            service = sdc.get_asset(sdc.ASSETTYPE_SERVICES, csar_id)
            # check if the related resources exist
            resources = service.get('resources', None)
            if resources:
                for resource in resources:
                    if not VnfPackageModel.objects.filter(vnfPackageId=resource['resourceUUID']) and \
                            not PnfPackageModel.objects.filter(pnfPackageId=resource['resourceUUID']):
                        logger.error("Resource [%s] is not distributed.", resource['resourceUUID'])
                        raise CatalogException("Resource (%s) is not distributed." % resource['resourceUUID'])

            # download csar package
            local_path = os.path.join(CATALOG_ROOT_PATH, csar_id)
            csar_name = "%s.csar" % service.get("name", csar_id)
            local_file_name = sdc.download_artifacts(service["toscaModelURL"], local_path, csar_name)
            if local_file_name.endswith(".csar") or local_file_name.endswith(".zip"):
                fileutil.unzip_file(local_file_name, local_path, "")
            data = {
                'userDefinedData': {}
            }
            serviced = ServiceDescriptor()
            serviced.create(data, csar_id)
            serviced.parse_serviced_and_save(csar_id, local_file_name)

        except Exception as e:
            logger.error(traceback.format_exc())
            if ServicePackageModel.objects.filter(servicePackageId=csar_id):
                ServicePackage().delete_csar(csar_id)
            raise e

    def delete_csar(self, csar_id):
        serviced = ServiceDescriptor()
        serviced.delete_single(csar_id)

    def get_csars(self):
        csars = []
        packages = ServicePackageModel.objects.filter()
        for package in packages:
            csar = self.get_csar(package.servicePackageId)
            csars.append(csar)
        return csars

    def get_csar(self, csar_id):
        package_info = {}
        csars = ServicePackageModel.objects.filter(servicePackageId=csar_id)
        if csars:
            package_info["servicedId"] = csars[0].servicedId
            package_info["servicePackageId"] = csars[0].servicePackageId
            package_info["servicedProvider"] = csars[0].servicedDesigner
            package_info["servicedVersion"] = csars[0].servicedVersion
            package_info["csarName"] = csars[0].servicePackageUri
            package_info["servicedModel"] = csars[0].servicedModel
            package_info["servicedInvariantId"] = csars[0].invariantId
            package_info["downloadUrl"] = "http://%s:%s/%s/%s/%s" % (
                REG_TO_MSB_REG_PARAM[0]["nodes"][0]["ip"],
                REG_TO_MSB_REG_PARAM[0]["nodes"][0]["port"],
                CATALOG_URL_PATH,
                csar_id,
                csars[0].servicePackageUri)
        else:
            error_message = "Service package[%s] not Found." % csar_id
            logger.error(error_message)
            raise PackageNotFoundException(error_message)

        return {"csarId": csar_id, "packageInfo": package_info}

    def parse_serviced(self, csar_id, inputs):
        service_pkg = ServicePackageModel.objects.filter(servicePackageId=csar_id)
        if not service_pkg:
            raise PackageNotFoundException("Service CSAR(%s) does not exist." % csar_id)

        try:
            csar_path = service_pkg[0].localFilePath
            ret = {"model": toscaparser.parse_sd(csar_path, inputs)}
            return ret
        except CatalogException as e:
            logger.error(e.args[0])
            raise e
        except Exception as e:
            logger.error(e.args[0])
            logger.error(traceback.format_exc())
            raise e
