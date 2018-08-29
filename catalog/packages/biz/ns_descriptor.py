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

from catalog.pub.config.config import CATALOG_ROOT_PATH
from catalog.pub.database.models import NSPackageModel, PnfPackageModel, VnfPackageModel
from catalog.pub.exceptions import CatalogException, ResourceNotFoundException
from catalog.pub.utils import fileutil, toscaparser
from catalog.pub.utils.values import ignore_case_get

logger = logging.getLogger(__name__)


def create(data):
    logger.info('Start to create a NSD...')
    user_defined_data = ignore_case_get(data, 'userDefinedData')
    data = {
        'id': str(uuid.uuid4()),
        'nsdOnboardingState': 'CREATED',
        'nsdOperationalState': 'DISABLED',
        'nsdUsageState': 'NOT_IN_USE',
        'userDefinedData': user_defined_data,
        '_links': None  # TODO
    }
    NSPackageModel(
        nsPackageId=data['id'],
        onboardingState=data['nsdOnboardingState'],
        operationalState=data['nsdOperationalState'],
        usageState=data['nsdUsageState'],
        userDefinedData=data['userDefinedData']
    ).save()
    logger.info('A NSD(%s) has been created.' % data['id'])
    return data


def query_multiple():
    ns_pkgs = NSPackageModel.objects.all()
    response_data = []
    for ns_pkg in ns_pkgs:
        data = fill_resp_data(ns_pkg)
        response_data.append(data)
    return response_data


def query_single(nsd_info_id):
    ns_pkgs = NSPackageModel.objects.filter(nsPackageId=nsd_info_id)
    if not ns_pkgs.exists():
        logger.error('NSD(%s) does not exist.' % nsd_info_id)
        raise ResourceNotFoundException('NSD(%s) does not exist.' % nsd_info_id)
    return fill_resp_data(ns_pkgs[0])


def delete_single(nsd_info_id):
    logger.info('Start to delete NSD(%s)...' % nsd_info_id)
    ns_pkgs = NSPackageModel.objects.filter(nsPackageId=nsd_info_id)
    if not ns_pkgs.exists():
        logger.info('NSD(%s) has been deleted.' % nsd_info_id)
        return
    '''
    if ns_pkgs[0].operationalState != 'DISABLED':
        logger.error('NSD(%s) shall be DISABLED.' % nsd_info_id)
        raise CatalogException('NSD(%s) shall be DISABLED.' % nsd_info_id)
    if ns_pkgs[0].usageState != 'NOT_IN_USE':
        logger.error('NSD(%s) shall be NOT_IN_USE.' % nsd_info_id)
        raise CatalogException('NSD(%s) shall be NOT_IN_USE.' % nsd_info_id)
    '''
    ns_pkgs.delete()
    ns_pkg_path = os.path.join(CATALOG_ROOT_PATH, nsd_info_id)
    fileutil.delete_dirs(ns_pkg_path)
    logger.info('NSD(%s) has been deleted.' % nsd_info_id)


def upload(remote_file, nsd_info_id):
    logger.info('Start to upload NSD(%s)...' % nsd_info_id)
    ns_pkgs = NSPackageModel.objects.filter(nsPackageId=nsd_info_id)
    if not ns_pkgs.exists():
        logger.info('NSD(%s) does not exist.' % nsd_info_id)
        raise CatalogException('NSD(%s) does not exist.' % nsd_info_id)

    ns_pkgs.update(onboardingState='UPLOADING')
    local_file_name = remote_file.name
    local_file_dir = os.path.join(CATALOG_ROOT_PATH, nsd_info_id)
    local_file_name = os.path.join(local_file_dir, local_file_name)
    if not os.path.exists(local_file_dir):
        fileutil.make_dirs(local_file_dir)
    with open(local_file_name, 'wb') as local_file:
        for chunk in remote_file.chunks(chunk_size=1024 * 8):
            local_file.write(chunk)
    logger.info('NSD(%s) content has been uploaded.' % nsd_info_id)
    return local_file_name


def parse_nsd_and_save(nsd_info_id, local_file_name):
    logger.info('Start to process NSD(%s)...' % nsd_info_id)
    ns_pkgs = NSPackageModel.objects.filter(nsPackageId=nsd_info_id)
    ns_pkgs.update(onboardingState='PROCESSING')
    nsd_json = toscaparser.parse_nsd(local_file_name)
    nsd = json.JSONDecoder().decode(nsd_json)

    nsd_id = nsd["metadata"]["id"]
    if nsd_id and NSPackageModel.objects.filter(nsdId=nsd_id):
        logger.info('NSD(%s) already exists.' % nsd_id)
        raise CatalogException("NSD(%s) already exists." % nsd_id)

    for vnf in nsd["vnfs"]:
        vnfd_id = vnf["properties"]["id"]
        pkg = VnfPackageModel.objects.filter(vnfdId=vnfd_id)
        if not pkg:
            logger.error("VNFD is not distributed.")
            raise CatalogException("VNF package(%s) is not distributed." % vnfd_id)

    ns_pkgs.update(
        nsdId=nsd_id,
        nsdName=nsd["metadata"].get("name", nsd_id),
        nsdDesginer=nsd["metadata"].get("vendor", "undefined"),
        nsdDescription=nsd["metadata"].get("description", ""),
        nsdVersion=nsd["metadata"].get("version", "undefined"),
        onboardingState="ONBOARDED",
        operationalState="ENABLED",
        usageState="NOT_IN_USE",
        nsPackageUri=local_file_name,
        sdcCsarId=nsd_info_id,
        localFilePath=local_file_name,
        nsdModel=nsd_json
    )
    logger.info('NSD(%s) has been processed.' % nsd_info_id)


def download(nsd_info_id):
    logger.info('Start to download NSD(%s)...' % nsd_info_id)
    ns_pkgs = NSPackageModel.objects.filter(nsPackageId=nsd_info_id)
    if not ns_pkgs.exists():
        logger.error('NSD(%s) does not exist.' % nsd_info_id)
        raise ResourceNotFoundException('NSD(%s) does not exist.' % nsd_info_id)
    
    if ns_pkgs[0].onboardingState != 'ONBOARDED':
        logger.error('NSD(%s) is not ONBOARDED.' % nsd_info_id)
        raise CatalogException('NSD(%s) is not ONBOARDED.' % nsd_info_id)
    local_file_path = ns_pkgs[0].localFilePath
    local_file_name = local_file_path.split('/')[-1]
    local_file_name = local_file_name.split('\\')[-1]
    logger.info('NSD(%s) has been downloaded.' % nsd_info_id)
    return local_file_path, local_file_name, os.path.getsize(local_file_path)


def fill_resp_data(ns_pkg):
    data = {
        'id': ns_pkg.nsPackageId,
        'nsdId': ns_pkg.nsdId,
        'nsdName': ns_pkg.nsdName,
        'nsdVersion': ns_pkg.nsdVersion,
        'nsdDesigner': ns_pkg.nsdDesginer,
        'nsdInvariantId': None,  # TODO
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
            vnfd_id = vnf["properties"]["id"]
            pkgs = VnfPackageModel.objects.filter(vnfdId=vnfd_id)
            for pkg in pkgs:
                vnf_pkg_ids.append(pkg.vnfPackageId)
        data['vnfPkgIds'] = vnf_pkg_ids

        pnf_info_ids = []
        for pnf in nsd_model['pnfs']:
            pnfd_id = pnf["properties"]["id"]
            pkgs = PnfPackageModel.objects.filter(pnfdId=pnfd_id)
            for pkg in pkgs:
                pnf_info_ids.append(pkg.pnfPackageId)
        data['pnfInfoIds'] = pnf_info_ids  # TODO: need reconfirming

    if ns_pkg.userDefinedData:
        user_defined_data = json.JSONDecoder().decode(ns_pkg.userDefinedData)
        data['userDefinedData'] = user_defined_data

    return data


def handle_upload_failed(nsd_info_id):
    ns_pkg = NSPackageModel.objects.filter(nsPackageId=nsd_info_id)
    ns_pkg.update(onboardingState="CREATED")
