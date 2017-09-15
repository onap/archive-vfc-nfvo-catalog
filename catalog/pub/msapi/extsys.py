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

import json
import logging
import uuid

from catalog.pub.config.config import AAI_BASE_URL, AAI_USER, AAI_PASSWD
from catalog.pub.exceptions import NSLCMException
from catalog.pub.utils import restcall
from catalog.pub.utils.restcall import req_by_msb
from catalog.pub.utils.values import ignore_case_get

logger = logging.getLogger(__name__)


def call_aai(resource, method, content=''):
    additional_headers = {
        'X-FromAppId': 'VFC-NFVO-LCM',
        'X-TransactionId': str(uuid.uuid1())
    }

    return restcall.call_req(AAI_BASE_URL,
                             AAI_USER,
                             AAI_PASSWD,
                             restcall.rest_no_auth,
                             resource,
                             method,
                             content,
                             additional_headers)


# def get_vims():
#     ret = req_by_msb("/api/extsys/v1/vims", "GET")
#     if ret[0] != 0:
#         logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
#         raise NSLCMException("Failed to query vims from extsys.")
#     return json.JSONDecoder().decode(ret[1])

def get_vims():
    ret = call_aai("/cloud-infrastructure/cloud-regions?depth=all", "GET")
    if ret[0] != 0:
        logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        raise NSLCMException("Failed to query vims from extsys.")
    # convert vim_info_aai to internal vim_info
    vims_aai = json.JSONDecoder().decode(ret[1])
    vims_aai = ignore_case_get(vims_aai, "cloud-region")
    vims_info = []
    for vim in vims_aai:
        vim = convert_vim_info(vim)
        vims_info.append(vim)
    return vims_info

def split_vim_to_owner_region(vim_id):
    split_vim = vim_id.split('_')
    cloud_owner = split_vim[0]
    cloud_region = "".join(split_vim[1:])
    return cloud_owner, cloud_region

def convert_vim_info(vim_info_aai):
    vim_id = vim_info_aai["cloud-owner"] + "_" + vim_info_aai["cloud-region-id"]
    esr_system_info = ignore_case_get(ignore_case_get(vim_info_aai, "esr-system-info-list"), "esr-system-info")
    # tenants = ignore_case_get(vim_info_aai, "tenants")
    vim_info = {
        "vimId": vim_id,
        "name": vim_id,
        "url": ignore_case_get(esr_system_info[0], "service-url"),
        "userName": ignore_case_get(esr_system_info[0], "user-name"),
        "password": ignore_case_get(esr_system_info[0], "password"),
        # "tenant": ignore_case_get(tenants[0], "tenant-id"),
        "tenant": ignore_case_get(esr_system_info[0], "default-tenant"),
        "vendor": ignore_case_get(esr_system_info[0], "vendor"),
        "version": ignore_case_get(esr_system_info[0], "version"),
        "description": "vim",
        "domain": "",
        "type": ignore_case_get(esr_system_info[0], "type"),
        "createTime": "2016-07-18 12:22:53"
    }
    return vim_info


# def get_vim_by_id(vim_id):
#     ret = req_by_msb("/api/extsys/v1/vims/%s" % vim_id, "GET")
#     if ret[0] != 0:
#         logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
#         raise NSLCMException("Failed to query vim(%s) from extsys." % vim_id)
#     return json.JSONDecoder().decode(ret[1])

def get_vim_by_id(vim_id):
    cloud_owner, cloud_region = split_vim_to_owner_region(vim_id)
    ret = call_aai("/cloud-infrastructure/cloud-regions/cloud-region/%s/%s?depth=all"
                   % (cloud_owner, cloud_region), "GET")
    if ret[0] != 0:
        logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        raise NSLCMException("Failed to query vim(%s) from extsys." % vim_id)
    # convert vim_info_aai to internal vim_info
    vim_info_aai = json.JSONDecoder().decode(ret[1])
    vim_info = convert_vim_info(vim_info_aai)
    return vim_info


def get_sdn_controller_by_id(sdn_ontroller_id):
    ret = req_by_msb("/api/extsys/v1/sdncontrollers/%s" % sdn_ontroller_id, "GET")
    if ret[0] != 0:
        logger.error("Failed to query sdn ontroller(%s) from extsys. detail is %s.", sdn_ontroller_id, ret[1])
        raise NSLCMException("Failed to query sdn ontroller(%s) from extsys." % sdn_ontroller_id)
    return json.JSONDecoder().decode(ret[1])


def get_vnfm_by_id(vnfm_inst_id):
    uri = '/api/extsys/v1/vnfms/%s' % vnfm_inst_id
    ret = req_by_msb(uri, "GET")
    if ret[0] > 0:
        logger.error('Send get VNFM information request to extsys failed.')
        raise NSLCMException('Send get VNFM information request to extsys failed.')
    return json.JSONDecoder().decode(ret[1])

def select_vnfm(vnfm_type, vim_id):
    uri = '/api/extsys/v1/vnfms'
    ret = req_by_msb(uri, "GET")
    if ret[0] > 0:
        logger.error("Failed to call %s: %s", uri, ret[1])
        raise NSLCMException('Failed to get vnfms from extsys.')
    vnfms = json.JSONDecoder().decode(ret[1])
    for vnfm in vnfms:
        if vnfm["type"] == vnfm_type and vnfm["vimId"] == vim_id:
            return vnfm
    raise NSLCMException('No vnfm found with %s in vim(%s)' % (vnfm_type, vim_id))

