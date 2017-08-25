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

import logging
import uuid
from catalog.pub.utils.syscomm import fun_name
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from catalog.pub.utils.values import ignore_case_get


logger = logging.getLogger(__name__)

@api_view(http_method_names=['POST', 'GET'])
def nspackage_get(request, *args, **kwargs):
    logger.debug("Enter %s, method is %s", fun_name(), request.method)
    ret, normal_status = None, None
    if request.method == 'GET':
        ret = get_ns_csars()
        normal_status = status.HTTP_200_OK
    else:
        csar_id = ignore_case_get(request.data, "csarId")
        logger.debug("csar_id is %s", csar_id)
        ret = ns_on_distribute(csar_id)
        normal_status = status.HTTP_202_ACCEPTED
    logger.debug("Leave %s, Return value is %s", fun_name(), ret)
    if ret[0] != 0:
        return Response(data={'error': ret[1]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=normal_status)

@api_view(http_method_names=['POST', 'GET'])
def nfpackage_get(request, *args, **kwargs):
    logger.debug("Enter %s%s, method is %s", fun_name(), request.data, request.method)
    ret, normal_status = None, None
    if request.method == 'GET':
        ret = get_nf_csars()
        normal_status = status.HTTP_200_OK
    else:
        csar_id = ignore_case_get(request.data, "csarId")
        vim_ids = ignore_case_get(request.data, "vimIds")
        lab_vim_id = ignore_case_get(request.data, "labVimId")
        job_id = str(uuid.uuid4())
        nf_on_distribute(csar_id, vim_ids, lab_vim_id, job_id)
        ret = [0, {"jobId": job_id}]
        normal_status = status.HTTP_202_ACCEPTED
    logger.debug("Leave %s, Return value is %s", fun_name(), ret)
    if ret[0] != 0:
        return Response(data={'error': ret[1]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=normal_status)

@api_view(http_method_names=['DELETE', 'GET'])
def ns_rd_csar():
    return [0,0]

@api_view(http_method_names=['DELETE', 'GET'])
def nf_rd_csar():
    return [0,0]

def get_ns_csars():
    return [0,0]


def get_nf_csars():
    return [0,0]


def ns_on_distribute(csarId):
    return [0,0]

def nf_on_distribute(csar_id, vim_ids, lab_vim_id, job_id):
    return [0,0]