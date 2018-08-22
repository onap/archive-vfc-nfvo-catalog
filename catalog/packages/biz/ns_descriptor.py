# Copyright 2017 ZTE Corporation.
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
from catalog.pub.utils import fileutil
from catalog.pub.utils.values import ignore_case_get
from catalog.pub.database.models import NSPackageModel, VnfPackageModel
from catalog.pub.exceptions import CatalogException

logger = logging.getLogger(__name__)


def create(data):
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
        operationalState=data['nsdOperationalState'],
        usageState=data['nsdUsageState'],
        userDefinedData=data['userDefinedData']
    ).save()
    return data


def query_multiple():
    ns_pkgs = NSPackageModel.objects.all()
    if not ns_pkgs:
        raise CatalogException('NS descriptors do not exist.')
    response_data = []
    for ns_pkg in ns_pkgs:
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
            'nsdOnboardingState': 'CREATED',
            'onboardingFailureDetails': None,  # TODO
            'nsdOperationalState': ns_pkg.operationalState,
            'nsdUsageState': ns_pkg.usageState,
            'userDefinedData': {},
            '_links': None  # TODO
        }

        if ns_pkg.nsdModel:
            data['nsdOnboardingState'] = 'ONBOARDED'
        elif ns_pkg.localFilePath:  # TODO: strip()
            data['nsdOnboardingState'] = 'PROCESSING'
        elif ns_pkg.nsdId:
            data['nsdOnboardingState'] = 'UPLOADING'
            data['nsdOnboardingState'] = 'CREATED'

        if ns_pkg.nsdModel:
            nsd_model = json.JSONDecoder().decode(ns_pkg.nsdModel)
            vnf_pkg_ids = []
            for vnf in nsd_model['vnfs']:
                vnfd_id = vnf["properties"]["id"]
                pkgs = VnfPackageModel.objects.filter(vnfdId=vnfd_id)
                for pkg in pkgs:
                    vnf_pkg_ids.append(pkg.vnfPackageId)
            data['vnfPkgIds'] = vnf_pkg_ids

        if ns_pkg.userDefinedData:
            user_defined_data = json.JSONDecoder().decode(ns_pkg.userDefinedData)
            data['userDefinedData'] = user_defined_data

        response_data.append(data)
    return response_data


def query_single(nsd_info_id):
    ns_pkgs = NSPackageModel.objects.filter(nsPackageId=nsd_info_id)
    if not ns_pkgs.exists():
        raise CatalogException('NS descriptors(%s) does not exist.' % nsd_info_id)
    data = {
        'id': ns_pkgs[0].nsPackageId,
        'nsdId': ns_pkgs[0].nsdId,
        'nsdName': ns_pkgs[0].nsdName,
        'nsdVersion': ns_pkgs[0].nsdVersion,
        'nsdDesigner': ns_pkgs[0].nsdDesginer,
        'nsdInvariantId': None,  # TODO
        'vnfPkgIds': [],
        'pnfdInfoIds': [],  # TODO
        'nestedNsdInfoIds': [],  # TODO
        'nsdOnboardingState': 'CREATED',
        'onboardingFailureDetails': None,  # TODO
        'nsdOperationalState': ns_pkgs[0].operationalState,
        'nsdUsageState': ns_pkgs[0].usageState,
        'userDefinedData': {},
        '_links': None  # TODO
    }

    if ns_pkgs[0].nsdModel:
        ns_pkgs[0]['nsdOnboardingState'] = 'ONBOARDED'
    elif ns_pkgs[0].localFilePath:  # TODO: strip()
        ns_pkgs[0]['nsdOnboardingState'] = 'PROCESSING'
    elif ns_pkgs[0].nsdId:
        ns_pkgs[0]['nsdOnboardingState'] = 'UPLOADING'
        ns_pkgs[0]['nsdOnboardingState'] = 'CREATED'

    if ns_pkgs[0].nsdModel:
        nsd_model = json.JSONDecoder().decode(ns_pkgs[0].nsdModel)
        vnf_pkg_ids = []
        for vnf in nsd_model['vnfs']:
            vnfd_id = vnf["properties"]["id"]
            pkgs = VnfPackageModel.objects.filter(vnfdId=vnfd_id)
            for pkg in pkgs:
                vnf_pkg_ids.append(pkg.vnfPackageId)
        data['vnfPkgIds'] = vnf_pkg_ids

    if ns_pkgs[0].userDefinedData:
        user_defined_data = json.JSONDecoder().decode(ns_pkgs[0].userDefinedData)
        data['userDefinedData'] = user_defined_data

    return data


def delete_single(nsd_info_id):
    ns_pkgs = NSPackageModel.objects.filter(nsPackageId=nsd_info_id)
    if not ns_pkgs.exists():
        raise CatalogException('The NS descriptor (%s) does not exist.' % nsd_info_id)
    if not ns_pkgs[0].nsdModel:
        raise CatalogException('The NS descriptor (%s) is not ONBOARDED.' % nsd_info_id)
    if ns_pkgs[0].operationalState != 'DISABLED':
        raise CatalogException('The NS descriptor (%s) is not DISABLED.' % nsd_info_id)
    if ns_pkgs[0].usageState != 'NOT_IN_USE':
        raise CatalogException('The NS descriptor (%s) is not NOT_IN_USE.' % nsd_info_id)
    ns_pkgs.delete()


def upload(files, nsd_info_id):
    remote_files = files
    for remote_file in remote_files:
        local_file_name = remote_file.name
        local_file_dir = os.path.join(CATALOG_ROOT_PATH, nsd_info_id)
        local_file_name = os.path.join(local_file_dir, local_file_name)
        if not os.path.exists(local_file_dir):
            fileutil.make_dirs(local_file_dir)
        with open(local_file_name, 'wb') as local_file:
            if remote_file.multiple_chunks(chunk_size=None):
                for chunk in remote_file.chunks():
                    local_file.write(chunk)
            else:
                data = remote_file.read()
                local_file.write(data)


def fill_resp_data(ns_pkg):
    pass
