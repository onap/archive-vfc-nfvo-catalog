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
import sys
import traceback

from catalog.pub.config.config import CATALOG_ROOT_PATH, CATALOG_URL_PATH
from catalog.pub.config.config import REG_TO_MSB_REG_PARAM
from catalog.pub.database.models import NSPackageModel, VnfPackageModel
from catalog.pub.exceptions import CatalogException
from catalog.pub.msapi import sdc
from catalog.pub.utils import fileutil
from catalog.pub.utils import toscaparser

logger = logging.getLogger(__name__)

STATUS_SUCCESS, STATUS_FAILED = "success", "failed"


def fmt_ns_pkg_rsp(status, desc, error_code="500"):
    return [0, {"status": status, "statusDescription": desc, "errorCode": error_code}]


def ns_on_distribute(csar_id):
    ret = None
    try:
        ret = NsPackage().on_distribute(csar_id)
    except CatalogException as e:
        NsPackage().delete_catalog(csar_id)
        return fmt_ns_pkg_rsp(STATUS_FAILED, e.message)
    except:
        logger.error(traceback.format_exc())
        NsPackage().delete_catalog(csar_id)
        return fmt_ns_pkg_rsp(STATUS_FAILED, str(sys.exc_info()))
    if ret[0]:
        return fmt_ns_pkg_rsp(STATUS_FAILED, ret[1])
    return fmt_ns_pkg_rsp(STATUS_SUCCESS, ret[1], "")


def ns_delete_csar(csar_id):
    ret = None
    try:
        ret = NsPackage().delete_csar(csar_id)
    except CatalogException as e:
        return fmt_ns_pkg_rsp(STATUS_FAILED, e.message)
    except:
        logger.error(traceback.format_exc())
        return fmt_ns_pkg_rsp(STATUS_FAILED, str(sys.exc_info()))
    return fmt_ns_pkg_rsp(STATUS_SUCCESS, ret[1], "")


def ns_get_csars():
    ret = None
    try:
        ret = NsPackage().get_csars()
    except CatalogException as e:
        return [1, e.message]
    except:
        logger.error(traceback.format_exc())
        return [1, str(sys.exc_info())]
    return ret


def ns_get_csar(csar_id):
    ret = None
    try:
        ret = NsPackage().get_csar(csar_id)
    except CatalogException as e:
        return [1, e.message]
    except Exception as e:
        logger.error(e.message)
        logger.error(traceback.format_exc())
        return [1, str(sys.exc_info())]
    return ret


def parse_nsd(csar_id, inputs):
    ret = None
    try:
        ns_pkg = NSPackageModel.objects.filter(nsPackageId=csar_id)
        if not ns_pkg:
            raise CatalogException("NS CSAR(%s) does not exist." % csar_id)
        csar_path = ns_pkg[0].localFilePath
        ret = {"model": toscaparser.parse_nsd(csar_path, inputs)}
    except CatalogException as e:
        return [1, e.message]
    except Exception as e:
        logger.error(e.message)
        logger.error(traceback.format_exc())
        return [1, str(sys.exc_info())]
    return [0, ret]


class NsPackage(object):
    """
    Actions for sdc ns package.
    """

    def __init__(self):
        pass

    def on_distribute(self, csar_id):
        if NSPackageModel.objects.filter(nsPackageId=csar_id):
            return [1, "NS CSAR(%s) already exists." % csar_id]

        artifact = sdc.get_artifact(sdc.ASSETTYPE_SERVICES, csar_id)
        local_path = os.path.join(CATALOG_ROOT_PATH, csar_id)
        csar_name = "%s.csar" % artifact.get("name", csar_id)
        local_file_name = sdc.download_artifacts(artifact["toscaModelURL"], local_path, csar_name)

        nsd_json = toscaparser.parse_nsd(local_file_name)
        nsd = json.JSONDecoder().decode(nsd_json)

        nsd_id = nsd["metadata"]["id"]
        if NSPackageModel.objects.filter(nsdId=nsd_id):
            raise CatalogException("NSD(%s) already exists." % nsd_id)

        for vnf in nsd["vnfs"]:
            vnfd_id = vnf["properties"]["id"]
            pkg = VnfPackageModel.objects.filter(vnfdId=vnfd_id)
            if not pkg:
                vnfd_name = vnf.get("vnf_id", "undefined")
                logger.error("[%s] is not distributed.", vnfd_name)
                raise CatalogException("VNF package(%s) is not distributed." % vnfd_id)

        NSPackageModel(
            nsPackageId=csar_id,
            nsdId=nsd_id,
            nsdName=nsd["metadata"].get("name", nsd_id),
            nsdDesginer=nsd["metadata"].get("vendor", "undefined"),
            nsdDescription=nsd["metadata"].get("description", ""),
            nsdVersion=nsd["metadata"].get("version", "undefined"),
            nsPackageUri=csar_name,
            sdcCsarId=csar_id,
            localFilePath=local_file_name,
            nsdModel=nsd_json
        ).save()

        return [0, "CSAR(%s) distributed successfully." % csar_id]

    def delete_csar(self, csar_id):
        NSPackageModel.objects.filter(nsPackageId=csar_id).delete()
        self.delete_catalog(csar_id)
        return [0, "Delete CSAR(%s) successfully." % csar_id]

    def get_csars(self):
        csars = {"csars": []}
        nss = NSPackageModel.objects.filter()
        for ns in nss:
            csars["csars"].append({
                "csarId": ns.nsPackageId,
                "nsdId": ns.nsdId,
                "nsdProvider": ns.nsdDesginer,
                "nsdVersion": ns.nsdVersion
            })
        return [0, csars]

    def get_csar(self, csar_id):
        package_info = {}
        csars = NSPackageModel.objects.filter(nsPackageId=csar_id)
        if csars:
            package_info["nsdId"] = csars[0].nsdId
            package_info["nsPackageId"] = csars[0].nsPackageId
            package_info["nsdProvider"] = csars[0].nsdDesginer
            package_info["nsdVersion"] = csars[0].nsdVersion
            package_info["csarName"] = csars[0].nsPackageUri
            package_info["nsdModel"] = csars[0].nsdModel
            package_info["downloadUrl"] = "http://%s:%s/%s/%s/%s" % (
                REG_TO_MSB_REG_PARAM["nodes"][0]["ip"],
                REG_TO_MSB_REG_PARAM["nodes"][0]["port"],
                CATALOG_URL_PATH,
                csar_id,
                csars[0].nsPackageUri)
        else:
            raise CatalogException("Ns package[%s] not Found." % csar_id)

        return [0, {"csarId": csar_id, "packageInfo": package_info}]

    def delete_catalog(self, csar_id):
        local_path = os.path.join(CATALOG_ROOT_PATH, csar_id)
        fileutil.delete_dirs(local_path)
