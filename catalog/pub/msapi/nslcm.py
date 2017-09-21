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
from catalog.pub.utils.restcall import req_by_msb

logger = logging.getLogger(__name__)

# ASSETTYPE_RESOURCES = "resources"
# ASSETTYPE_SERVICES = "services"


# def call_lcm(resource, method, content=''):
#     return restcall.call_req(base_url=NFVOLCM_BASE_URL,
#         user="",
#         passwd="",
#         auth_type=restcall.rest_no_auth,
#         resource=resource,
#         method=method,
#         content=content)


def get_nsInstances(csarid):
    ret=req_by_msb("/nslcm/v1/ns?nsPackageId=%s"% csarid, "GET")
    if ret[0] != 0:
        logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        raise CatalogException("Failed to query NS Instances(%s) from NSLCM." % csarid)
    return json.JSONDecoder().decode(ret[1])


def get_vnfInstances(csarid):
    ret=req_by_msb("/nslcm/v1/vnfs?vnfPackageId=%s"% csarid, "GET")
    if ret[0] != 0:
        logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        raise CatalogException("Failed to query VNF Instances(%s) from NSLCM." % csarid)
    return json.JSONDecoder().decode(ret[1])

def delete_all_nsinst(csarid):
    nsinstances = get_nsInstances(csarid)
    for ns in nsinstances:
        nsInstanceId = ns["nsInstanceId"]
        ret=req_by_msb("/nslcm/v1/ns/%s" % nsInstanceId,"delete")
        if ret[0] != 0:
            logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
            raise CatalogException("Failed to delete NS Instances(%s) from NSLCM." % nsInstanceId)

    return [0,'success']

def delete_nf_inst(csar_id):
    #vnf_instance = get_vnfInstances(csar_id)
    # REST API from nslcm to delete nf instance is not implemented
    # ret=req_by_msb("/nslcm/v1/nf/%s" % csar_id,"delete")
    return [0,'success']

# def delete_ns(asset_type):
#     resource = "/nfvolcm/v1/ns/"
#     resource = resource.format(assetType=asset_type)
#     ret = req_by_msb(resource, "DELETE")
#     if ret[0] != 0:
#         logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
#         raise CatalogException("Failed to query artifacts(%s) from sdc." % asset_type)
#     return json.JSONDecoder().decode(ret[1])
