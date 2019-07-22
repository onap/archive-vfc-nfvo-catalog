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

from catalog.pub.config.config import SDC_BASE_URL, SDC_USER, SDC_PASSWD
from catalog.pub.exceptions import CatalogException
from catalog.pub.utils import fileutil
from catalog.pub.utils import restcall

logger = logging.getLogger(__name__)

ASSETTYPE_RESOURCES = "resources"
ASSETTYPE_SERVICES = "services"
DISTRIBUTED = "DISTRIBUTED"


def call_sdc(resource, method, content=''):
    additional_headers = {
        'X-ECOMP-InstanceID': 'VFC',
    }
    return restcall.call_req(base_url=SDC_BASE_URL,
                             user=SDC_USER,
                             passwd=SDC_PASSWD,
                             auth_type=restcall.rest_no_auth,
                             resource=resource,
                             method=method,
                             content=content,
                             additional_headers=additional_headers)


"""
sample of return value
[
    {
        "uuid": "c94490a0-f7ef-48be-b3f8-8d8662a37236",
        "invariantUUID": "63eaec39-ffbe-411c-a838-448f2c73f7eb",
        "name": "underlayvpn",
        "version": "2.0",
        "toscaModelURL": "/sdc/v1/catalog/resources/c94490a0-f7ef-48be-b3f8-8d8662a37236/toscaModel",
        "category": "Volte",
        "subCategory": "VolteVF",
        "resourceType": "VF",
        "lifecycleState": "CERTIFIED",
        "lastUpdaterUserId": "jh0003"
    }
]
"""


def get_artifacts(asset_type):
    resource = "/sdc/v1/catalog/{assetType}"
    resource = resource.format(assetType=asset_type)
    ret = call_sdc(resource, "GET")
    if ret[0] != 0:
        logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        raise CatalogException("Failed to query artifacts(%s) from sdc." % asset_type)
    return json.JSONDecoder().decode(ret[1])


def get_artifact(asset_type, csar_id):
    artifacts = get_artifacts(asset_type)
    for artifact in artifacts:
        if artifact["uuid"] == csar_id:
            if asset_type == ASSETTYPE_SERVICES and \
                    artifact.get("distributionStatus", None) != DISTRIBUTED:
                raise CatalogException("The artifact (%s,%s) is not distributed from sdc." % (asset_type, csar_id))
            else:
                return artifact
    raise CatalogException("Failed to query artifact(%s,%s) from sdc." % (asset_type, csar_id))


def get_asset(asset_type, uuid):
    resource = "/sdc/v1/catalog/{assetType}/{uuid}/metadata".format(assetType=asset_type, uuid=uuid)
    ret = call_sdc(resource, "GET")
    if ret[0] != 0:
        logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        raise CatalogException("Failed to get asset(%s, %s) from sdc." % (asset_type, uuid))
    asset = json.JSONDecoder().decode(ret[1])
    if asset.get("distributionStatus", None) != DISTRIBUTED:
        raise CatalogException("The asset (%s,%s) is not distributed from sdc." % (asset_type, uuid))
    else:
        return asset


def delete_artifact(asset_type, asset_id, artifact_id):
    resource = "/sdc/v1/catalog/{assetType}/{uuid}/artifacts/{artifactUUID}"
    resource = resource.format(assetType=asset_type, uuid=asset_id, artifactUUID=artifact_id)
    ret = call_sdc(resource, "DELETE")
    if ret[0] != 0:
        logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        raise CatalogException("Failed to delete artifacts(%s) from sdc." % artifact_id)
    return json.JSONDecoder().decode(ret[1])


def download_artifacts(download_url, local_path, file_name):
    additional_headers = {
        'X-ECOMP-InstanceID': 'VFC',
        'accept': 'application/octet-stream'
    }
    ret = restcall.call_req(base_url=SDC_BASE_URL,
                            user=SDC_USER,
                            passwd=SDC_PASSWD,
                            auth_type=restcall.rest_no_auth,
                            resource=download_url,
                            method="GET",
                            additional_headers=additional_headers)
    if ret[0] != 0:
        logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
        raise CatalogException("Failed to download %s from sdc." % download_url)
    fileutil.make_dirs(local_path)
    local_file_name = os.path.join(local_path, file_name)
    local_file = open(local_file_name, 'wb')
    local_file.write(ret[1])
    local_file.close()
    return local_file_name
