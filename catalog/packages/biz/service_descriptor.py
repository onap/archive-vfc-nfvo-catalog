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

import json
import logging
import os
import uuid

from catalog.packages.const import PKG_STATUS
from catalog.pub.config.config import CATALOG_ROOT_PATH
from catalog.pub.database.models import ServicePackageModel, VnfPackageModel, PnfPackageModel
from catalog.pub.exceptions import CatalogException, PackageNotFoundException
from catalog.pub.utils import toscaparser, fileutil
from catalog.pub.utils.values import ignore_case_get

logger = logging.getLogger(__name__)


class ServiceDescriptor(object):
    """
    Action for Service Descriptor
    """

    def __init__(self):
        pass

    def create(self, data, csar_id=None):
        logger.info('Start to create a ServiceD...')
        user_defined_data = ignore_case_get(data, 'userDefinedData', {})
        data = {
            'id': csar_id if csar_id else str(uuid.uuid4()),
            'servicedOnboardingState': PKG_STATUS.CREATED,
            'servicedOperationalState': PKG_STATUS.DISABLED,
            'servicedUsageState': PKG_STATUS.NOT_IN_USE,
            'userDefinedData': user_defined_data,
            '_links': None  # TODO
        }
        ServicePackageModel.objects.create(
            servicePackageId=data['id'],
            onboardingState=data['servicedOnboardingState'],
            operationalState=data['servicedOperationalState'],
            usageState=data['servicedUsageState'],
            userDefinedData=json.dumps(user_defined_data)
        )
        logger.info('A ServiceD(%s) has been created.' % data['id'])
        return data

    def parse_serviced_and_save(self, serviced_info_id, local_file_name):
        logger.info('Start to process ServiceD(%s)...' % serviced_info_id)
        service_pkgs = ServicePackageModel.objects.filter(servicePackageId=serviced_info_id)
        service_pkgs.update(onboardingState=PKG_STATUS.PROCESSING)

        serviced_json = toscaparser.parse_sd(local_file_name)
        serviced = json.JSONDecoder().decode(serviced_json)

        serviced_id = serviced.get("service", {}).get("properties", {}).get("descriptor_id", "")
        serviced_name = serviced.get("service", {}).get("properties", {}).get("name", "")
        serviced_version = serviced.get("service", {}).get("properties", {}).get("version", "")
        serviced_designer = serviced.get("service", {}).get("properties", {}).get("designer", "")
        invariant_id = serviced.get("service", {}).get("properties", {}).get("invariant_id", "")
        if serviced_id == "":
            raise CatalogException("serviced_id(%s) does not exist in metadata." % serviced_id)
        other_nspkg = ServicePackageModel.objects.filter(servicedId=serviced_id)
        if other_nspkg and other_nspkg[0].servicePackageId != serviced_info_id:
            logger.warn("ServiceD(%s,%s) already exists.", serviced_id, other_nspkg[0].servicePackageId)
            raise CatalogException("ServiceD(%s) already exists." % serviced_id)

        for vnf in serviced["vnfs"]:
            vnfd_id = vnf["properties"].get("descriptor_id", "undefined")
            if vnfd_id == "undefined":
                vnfd_id = vnf["properties"].get("id", "undefined")
            pkg = VnfPackageModel.objects.filter(vnfdId=vnfd_id)
            if not pkg:
                pkg = VnfPackageModel.objects.filter(vnfPackageId=vnfd_id)
            if not pkg:
                vnfd_name = vnf.get("vnf_id", "undefined")
                logger.error("[%s] is not distributed.", vnfd_name)
                raise CatalogException("VNF package(%s) is not distributed." % vnfd_id)

        for pnf in serviced["pnfs"]:
            pnfd_id = pnf["properties"].get("descriptor_id", "undefined")
            if pnfd_id == "undefined":
                pnfd_id = pnf["properties"].get("id", "undefined")
            pkg = PnfPackageModel.objects.filter(pnfdId=pnfd_id)
            if not pkg:
                pkg = PnfPackageModel.objects.filter(pnfPackageId=pnfd_id)
            if not pkg:
                pnfd_name = pnf.get("pnf_id", "undefined")
                logger.error("[%s] is not distributed.", pnfd_name)
                raise CatalogException("PNF package(%s) is not distributed." % pnfd_name)

        service_pkgs.update(
            servicedId=serviced_id,
            servicedName=serviced_name,
            servicedDesigner=serviced_designer,
            servicedDescription=serviced.get("description", ""),
            servicedVersion=serviced_version,
            invariantId=invariant_id,
            onboardingState=PKG_STATUS.ONBOARDED,
            operationalState=PKG_STATUS.ENABLED,
            usageState=PKG_STATUS.NOT_IN_USE,
            servicePackageUri=local_file_name,
            sdcCsarId=serviced_info_id,
            localFilePath=local_file_name,
            servicedModel=serviced_json
        )
        logger.info('ServiceD(%s) has been processed.' % serviced_info_id)

    def delete_single(self, serviced_info_id):
        logger.info('Start to delete ServiceD(%s)...' % serviced_info_id)
        service_pkgs = ServicePackageModel.objects.filter(servicePackageId=serviced_info_id)
        if not service_pkgs.exists():
            logger.warn('ServiceD(%s) not found.' % serviced_info_id)
            raise PackageNotFoundException("Service package[%s] not Found." % serviced_info_id)
        service_pkgs.delete()
        service_pkg_path = os.path.join(CATALOG_ROOT_PATH, serviced_info_id)
        fileutil.delete_dirs(service_pkg_path)
        logger.info('ServiceD(%s) has been deleted.' % serviced_info_id)
