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
import uuid

from catalog.packages.biz.common import parse_file_range, read, save
from catalog.packages.const import PKG_STATUS
from catalog.pub.config.config import CATALOG_ROOT_PATH
from catalog.pub.database.models import NSPackageModel, PnfPackageModel, VnfPackageModel
from catalog.pub.exceptions import CatalogException, ResourceNotFoundException
from catalog.pub.utils import fileutil, toscaparser
from catalog.pub.utils.values import ignore_case_get

logger = logging.getLogger(__name__)

METADATA = "metadata"


class NsDescriptor(object):

    def __init__(self):
        pass

    def create(self, data, id=None):
        logger.info('Start to create a NSD...')
        user_defined_data = ignore_case_get(data, 'userDefinedData', {})
        data = {
            'id': id if id else str(uuid.uuid4()),
            'nsdOnboardingState': PKG_STATUS.CREATED,
            'nsdOperationalState': PKG_STATUS.DISABLED,
            'nsdUsageState': PKG_STATUS.NOT_IN_USE,
            'userDefinedData': user_defined_data,
            '_links': None  # TODO
        }
        NSPackageModel.objects.create(
            nsPackageId=data['id'],
            onboardingState=data['nsdOnboardingState'],
            operationalState=data['nsdOperationalState'],
            usageState=data['nsdUsageState'],
            userDefinedData=json.dumps(user_defined_data)
        )
        logger.info('A NSD(%s) has been created.' % data['id'])
        return data

    def query_multiple(self, nsdId=None):
        if nsdId:
            ns_pkgs = NSPackageModel.objects.filter(nsdId=nsdId)
        else:
            ns_pkgs = NSPackageModel.objects.all()
        response_data = []
        for ns_pkg in ns_pkgs:
            data = self.fill_resp_data(ns_pkg)
            response_data.append(data)
        return response_data

    def query_single(self, nsd_info_id):
        ns_pkgs = NSPackageModel.objects.filter(nsPackageId=nsd_info_id)
        if not ns_pkgs.exists():
            logger.error('NSD(%s) does not exist.' % nsd_info_id)
            raise ResourceNotFoundException('NSD(%s) does not exist.' % nsd_info_id)
        return self.fill_resp_data(ns_pkgs[0])

    def delete_single(self, nsd_info_id):
        logger.info('Start to delete NSD(%s)...' % nsd_info_id)
        ns_pkgs = NSPackageModel.objects.filter(nsPackageId=nsd_info_id)
        if not ns_pkgs.exists():
            logger.info('NSD(%s) has been deleted.' % nsd_info_id)
            return
        '''
        if ns_pkgs[0].operationalState != PKG_STATUS.DISABLED:
            logger.error('NSD(%s) shall be DISABLED.' % nsd_info_id)
            raise CatalogException('NSD(%s) shall be DISABLED.' % nsd_info_id)
        if ns_pkgs[0].usageState != PKG_STATUS.NOT_IN_USE:
            logger.error('NSD(%s) shall be NOT_IN_USE.' % nsd_info_id)
            raise CatalogException('NSD(%s) shall be NOT_IN_USE.' % nsd_info_id)
        '''
        ns_pkgs.delete()
        ns_pkg_path = os.path.join(CATALOG_ROOT_PATH, nsd_info_id)
        fileutil.delete_dirs(ns_pkg_path)
        logger.info('NSD(%s) has been deleted.' % nsd_info_id)

    def upload(self, nsd_info_id, remote_file):
        logger.info('Start to upload NSD(%s)...' % nsd_info_id)
        ns_pkgs = NSPackageModel.objects.filter(nsPackageId=nsd_info_id)
        if not ns_pkgs.exists():
            logger.error('NSD(%s) does not exist.' % nsd_info_id)
            raise CatalogException('NSD(%s) does not exist.' % nsd_info_id)
        ns_pkgs.update(onboardingState=PKG_STATUS.UPLOADING)

        local_file_name = save(remote_file, nsd_info_id)
        logger.info('NSD(%s) content has been uploaded.' % nsd_info_id)
        return local_file_name

    def download(self, nsd_info_id, file_range):
        logger.info('Start to download NSD(%s)...' % nsd_info_id)
        ns_pkgs = NSPackageModel.objects.filter(nsPackageId=nsd_info_id)
        if not ns_pkgs.exists():
            logger.error('NSD(%s) does not exist.' % nsd_info_id)
            raise ResourceNotFoundException('NSD(%s) does not exist.' % nsd_info_id)
        if ns_pkgs[0].onboardingState != PKG_STATUS.ONBOARDED:
            logger.error('NSD(%s) is not ONBOARDED.' % nsd_info_id)
            raise CatalogException('NSD(%s) is not ONBOARDED.' % nsd_info_id)

        local_file_path = ns_pkgs[0].localFilePath
        start, end = parse_file_range(local_file_path, file_range)
        logger.info('NSD(%s) has been downloaded.' % nsd_info_id)
        return read(local_file_path, start, end)

    def parse_nsd_and_save(self, nsd_info_id, local_file_name, isETSI=True):
        logger.info('Start to process NSD(%s)...' % nsd_info_id)
        ns_pkgs = NSPackageModel.objects.filter(nsPackageId=nsd_info_id)
        ns_pkgs.update(onboardingState=PKG_STATUS.PROCESSING)

        nsd_json = toscaparser.parse_nsd(local_file_name, isETSI)
        logger.debug("%s", nsd_json)
        nsd = json.JSONDecoder().decode(nsd_json)

        nsd_id = nsd.get("ns", {}).get("properties", {}).get("descriptor_id", "")
        nsd_name = nsd.get("ns", {}).get("properties", {}).get("name", "")
        nsd_version = nsd.get("ns", {}).get("properties", {}).get("version", "")
        nsd_designer = nsd.get("ns", {}).get("properties", {}).get("designer", "")
        invariant_id = nsd.get("ns", {}).get("properties", {}).get("invariant_id", "")
        if nsd_id == "":
            raise CatalogException("nsd_id(%s) does not exist in metadata." % nsd_id)
        if NSPackageModel.objects.filter(nsdId=nsd_id):
            raise CatalogException("NSD(%s) already exists." % nsd_id)

        for vnf in nsd["vnfs"]:
            vnfd_id = vnf["properties"].get("descriptor_id", "undefined")
            if vnfd_id == "undefined":
                vnfd_id = vnf["properties"].get("id", "undefined")
            pkg = VnfPackageModel.objects.filter(vnfdId=vnfd_id)
            if not pkg:
                vnfd_name = vnf.get("vnf_id", "undefined")
                logger.error("[%s] is not distributed.", vnfd_name)
                raise CatalogException("VNF package(%s) is not distributed." % vnfd_id)

        for pnf in nsd["pnfs"]:
            pnfd_id = pnf["properties"].get("descriptor_id", "undefined")
            if pnfd_id == "undefined":
                pnfd_id = pnf["properties"].get("id", "undefined")
            pkg = PnfPackageModel.objects.filter(pnfdId=pnfd_id)
            if not pkg:
                pnfd_name = pnf.get("vnf_id", "undefined")
                logger.error("[%s] is not distributed.", pnfd_name)
                raise CatalogException("VNF package(%s) is not distributed." % pnfd_name)

        ns_pkgs.update(
            nsdId=nsd_id,
            nsdName=nsd_name,
            nsdDesginer=nsd_designer,
            nsdDescription=nsd.get("description", ""),
            nsdVersion=nsd_version,
            invariantId=invariant_id,
            onboardingState=PKG_STATUS.ONBOARDED,
            operationalState=PKG_STATUS.ENABLED,
            usageState=PKG_STATUS.NOT_IN_USE,
            nsPackageUri=local_file_name,
            sdcCsarId=nsd_info_id,
            localFilePath=local_file_name,
            nsdModel=nsd_json
        )
        logger.info('NSD(%s) has been processed.' % nsd_info_id)

    def fill_resp_data(self, ns_pkg):
        data = {
            'id': ns_pkg.nsPackageId,
            'nsdId': ns_pkg.nsdId,
            'nsdName': ns_pkg.nsdName,
            'nsdVersion': ns_pkg.nsdVersion,
            'nsdDesigner': ns_pkg.nsdDesginer,
            'nsdInvariantId': ns_pkg.invariantId,
            'vnfPkgIds': [],
            'pnfdInfoIds': [],  # TODO
            'nestedNsdInfoIds': [],  # TODO
            'nsdOnboardingState': ns_pkg.onboardingState,
            'onboardingFailureDetails': None,  # TODO
            'nsdOperationalState': ns_pkg.operationalState,
            'nsdUsageState': ns_pkg.usageState,
            'userDefinedData': {},
            '_links': None  # TODO
        }

        if ns_pkg.nsdModel:
            nsd_model = json.JSONDecoder().decode(ns_pkg.nsdModel)
            vnf_pkg_ids = []
            for vnf in nsd_model['vnfs']:
                vnfd_id = vnf["properties"].get("descriptor_id", "undefined")
                if vnfd_id == "undefined":
                    vnfd_id = vnf["properties"].get("id", "undefined")
                pkgs = VnfPackageModel.objects.filter(vnfdId=vnfd_id)
                for pkg in pkgs:
                    vnf_pkg_ids.append(pkg.vnfPackageId)
            data['vnfPkgIds'] = vnf_pkg_ids

            pnf_info_ids = []
            for pnf in nsd_model['pnfs']:
                pnfd_id = pnf["properties"].get("descriptor_id", "undefined")
                if pnfd_id == "undefined":
                    pnfd_id = pnf["properties"].get("id", "undefined")
                pkgs = PnfPackageModel.objects.filter(pnfdId=pnfd_id)
                for pkg in pkgs:
                    pnf_info_ids.append(pkg.pnfPackageId)
            data['pnfInfoIds'] = pnf_info_ids  # TODO: need reconfirming

        if ns_pkg.userDefinedData:
            user_defined_data = json.JSONDecoder().decode(ns_pkg.userDefinedData)
            data['userDefinedData'] = user_defined_data

        return data

    def handle_upload_failed(self, nsd_info_id):
        ns_pkg = NSPackageModel.objects.filter(nsPackageId=nsd_info_id)
        ns_pkg.update(onboardingState=PKG_STATUS.CREATED)
