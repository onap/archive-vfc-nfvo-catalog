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

from catalog.pub.config.config import CATALOG_ROOT_PATH
from catalog.pub.database.models import NSPackageModel, VnfPackageModel
from catalog.pub.exceptions import CatalogException
from catalog.pub.msapi import nfvolcm
from catalog.pub.msapi import sdc
from catalog.pub.utils import fileutil
from catalog.pub.utils import toscaparser
from rest_framework import status

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
    return fmt_ns_pkg_rsp(STATUS_SUCCESS, ret[1], "")


def ns_delete_csar(csar_id, force_delete):
    ret = None
    nsinstances = []
    try:
       if force_delete:
           ret = NsPackage().delete_csar(csar_id)
           return fmt_ns_pkg_rsp(STATUS_SUCCESS, ret[1], "")
       nsinstances = nfvolcm.get_nsInstances(csar_id)
       if nsinstances:
          if len(nsinstances) > 0:
              return fmt_ns_pkg_rsp(STATUS_FAILED, "NS instances using the CSAR exists!",status.HTTP_412_PRECONDITION_FAILED)
       ret = NsPackage().delete_csar(csar_id)
       return fmt_ns_pkg_rsp(STATUS_SUCCESS, ret[1], "")
    except CatalogException as e:
        return fmt_ns_pkg_rsp(STATUS_FAILED, e.message)
    except:
        logger.error(traceback.format_exc())
        return fmt_ns_pkg_rsp(STATUS_FAILED, str(sys.exc_info()))


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
    except:
        logger.error(traceback.format_exc())
        return [1, str(sys.exc_info())]
    return ret

def parser_NSPackageModel(csar_id,inputs):
    ret= None
    try:
        nf_pkg = NSPackageModel.objects.filter(nsPackageId=csar_id)

        if nf_pkg:
            for pkg in nf_pkg:
                csar_path = pkg.localFilePath
                ret={"model":toscaparser.parse_nsd(csar_path,inputs)}
                continue
    except CatalogException as e:
        return [1, e.message]
    except:
        logger.error(traceback.format_exc())
        return [1, str(sys.exc_info())]
    return [0,ret]


class NsPackage(object):
    """
    Actions for sdc ns package.
    """

    def __init__(self):
        pass

    def on_distribute(self, csar_id):
        if NSPackageModel.objects.filter(nsPackageId=csar_id):
            raise CatalogException("NS CSAR(%s) already exists." % csar_id)

        nsd,local_file_name,nsd_json = self.get_nsd(csar_id)

        nsd_id = nsd["metadata"]["id"]
        if NSPackageModel.objects.filter(nsdId=nsd_id):
            raise CatalogException("NSD(%s) already exists." % nsd_id)

        for vnf in nsd["vnfs"]:
            vnfd_id = vnf["properties"]["id"]
            pkg = VnfPackageModel.objects.filter(vnfdId = vnfd_id)
            if not pkg:
                raise CatalogException("VNF package(%s) is not distributed." % vnfd_id)

        NSPackageModel(
            nsPackageId=csar_id,
            nsdId=nsd_id,
            nsdName=nsd["metadata"].get("name", nsd_id),
            nsdDesginer=nsd["metadata"].get("vendor", "undefined"),
            nsdDescription=nsd["metadata"].get("description", ""),
            nsdVersion=nsd["metadata"].get("version", "undefined"),
            nsPackageUri=local_file_name,
            sdcCsarId=csar_id,
            localFilePath=local_file_name,
            nsdModel=nsd_json
            ).save()

        return [0, "CSAR(%s) distributed successfully." % csar_id]

    def get_nsd(self, csar_id):
        artifact = sdc.get_artifact(sdc.ASSETTYPE_SERVICES, csar_id)
        local_path = os.path.join(CATALOG_ROOT_PATH, csar_id)
        local_file_name = sdc.download_artifacts(artifact["toscaModelURL"], local_path)

        nsd_json = toscaparser.parse_nsd(local_file_name)
        nsd = json.JSONDecoder().decode(nsd_json)

        return nsd,local_file_name,nsd_json

    def delete_csar(self, csar_id):
        '''
        if force_delete:
            NSInstModel.objects.filter(nspackage_id=csar_id).delete()
        else:
            if NSInstModel.objects.filter(nspackage_id=csar_id):
                raise CatalogException("CSAR(%s) is in using, cannot be deleted." % csar_id)
        '''
        #nfvolcm.delete_ns_inst_mock()
        NSPackageModel.objects.filter(nsPackageId=csar_id).delete()
        return [0, "Delete CSAR(%s) successfully." % csar_id]


    def get_csars(self):
        csars = []
        nss = NSPackageModel.objects.filter()
        for ns in nss:
            csars.append({
                "csarId": ns.nsPackageId,
                "nsdId": ns.nsdId
            })
        return [0,csars]

    def get_csar(self, csar_id):
        package_info = {}
        csars = NSPackageModel.objects.filter(nsPackageId=csar_id)
        if csars:
            package_info["nsdId"] = csars[0].nsdId
            package_info["nsdProvider"] = csars[0].nsdDesginer
            package_info["nsdVersion"] = csars[0].nsdVersion

        #nss = NSInstModel.objects.filter(nspackage_id=csar_id)
        nss = nfvolcm.get_nsInstances(csar_id)
        ns_instance_info = [{
            "nsInstanceId": ns["nsInstanceId"],
            "nsInstanceName": ns["nsName"]} for ns in nss]

        return [0, {"csarId": csar_id, 
            "packageInfo": package_info, 
            "nsInstanceInfo": ns_instance_info}]

    def delete_catalog(self, csar_id):
        local_path = os.path.join(CATALOG_ROOT_PATH, csar_id)
        fileutil.delete_dirs(local_path)
