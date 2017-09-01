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
from catalog.pub.exceptions import CatalogException
from catalog.pub.utils import restcall
from catalog.pub.config.config import NFVOLCM_BASE_URL,NFVOLCM_USER,NFVOLCM_PASSWD

logger = logging.getLogger(__name__)

ASSETTYPE_RESOURCES = "resources"
ASSETTYPE_SERVICES = "services"


def call_lcm(resource, method, content=''):
    return restcall.call_req(base_url=NFVOLCM_BASE_URL,
        user=NFVOLCM_USER,
        passwd=NFVOLCM_PASSWD,
        auth_type=restcall.rest_no_auth,
        resource=resource,
        method=method,
        content=content)

# Mock code because the REST API from nfvolcm to delete ns instance is not implemented
def delete_ns_inst_mock():
    return [0,'success']

# Mock code because the REST API from nfvolcm to delete nf instance is not implemented
def delete_nf_inst_mock():
    return [0,'success']

def delete_ns(asset_type):
    resource = "/nfvolcm/v1/ns/"
    resource = resource.format(assetType=asset_type)
    ret = call_lcm(resource, "DELETE")
    if ret[0] != 0:
        logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        raise CatalogException("Failed to query artifacts(%s) from sdc." % asset_type)
    return json.JSONDecoder().decode(ret[1])

def getNsInsts_mock():
    return [
        {
            "nsInstanceId":1,
            "nsInstanceName":"vnf1"
        },
        {
            "nsInstanceId": 2,
            "nsInstanceName": "vnf2"
        }]

def getNfInsts_mock():
    return [
        {
            "vnfInstanceId":1,
            "vnfInstanceName":"vnf1"
        },
        {
            "vnfInstanceId": 2,
            "vnfInstanceName": "vnf2"
        }]