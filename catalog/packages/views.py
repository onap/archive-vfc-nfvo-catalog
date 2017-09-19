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
from catalog.packages import nf_package
from catalog.packages import ns_package


logger = logging.getLogger(__name__)


@api_view(http_method_names=['POST', 'GET'])
def nspackages_rc(request, *args, **kwargs):
    logger.debug("Enter %s, method is %s", fun_name(), request.method)
    ret, normal_status = None, None

    if request.method == 'GET':
        # Gets ns package list
        ret = ns_package.ns_get_csars()
        normal_status = status.HTTP_200_OK
    elif request.method == 'POST':
        # Distributes the package accroding to the given csarId
        csar_id = ignore_case_get(request.data, "csarId")
        logger.debug("csar_id is %s", csar_id)
        ret = ns_package.ns_on_distribute(csar_id)
        normal_status = status.HTTP_202_ACCEPTED
    logger.debug("Leave %s, Return value is %s", fun_name(), ret)
    if ret[0] != 0:
        return Response(data={'error': ret[1]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=normal_status)


@api_view(http_method_names=['POST', 'GET'])
def nfpackages_rc(request, *args, **kwargs):
    logger.debug("Enter %s%s, method is %s", fun_name(), request.data, request.method)
    ret, normal_status = None, None
    if request.method == 'GET':
        ret = nf_package.nf_get_csars()
        normal_status = status.HTTP_200_OK
    elif request.method == 'POST':
        csar_id = ignore_case_get(request.data, "csarId")
        vim_ids = ignore_case_get(request.data, "vimIds")
        lab_vim_id = ignore_case_get(request.data, "labVimId")
        job_id = str(uuid.uuid4())
        nf_package.NfDistributeThread(csar_id, vim_ids, lab_vim_id, job_id).start()
        ret = [0, {"jobId": job_id}]
        normal_status = status.HTTP_202_ACCEPTED
    logger.debug("Leave %s, Return value is %s", fun_name(), ret)
    if ret[0] != 0:
        return Response(data={'error': ret[1]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=normal_status)


@api_view(http_method_names=['DELETE', 'GET'])
def ns_rd_csar(request, *args, **kwargs):
    csar_id = ignore_case_get(kwargs, "csarId")
    logger.info("Enter %s, method is %s, csar_id is %s", fun_name(), request.method, csar_id)
    ret, normal_status = None, None
    if request.method == 'GET':
        ret = ns_package.ns_get_csar(csar_id)
        normal_status = status.HTTP_200_OK
    elif request.method == 'DELETE':
        force_delete = csar_id.endswith("force")
        if force_delete:
            csar_id = csar_id[:-5]
        ret = ns_package.ns_delete_csar(csar_id, force_delete)
        normal_status = status.HTTP_202_ACCEPTED
    logger.info("Leave %s, Return value is %s", fun_name(), ret)
    if ret[0] != 0:
        return Response(data={'error': ret[1]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=normal_status)


@api_view(http_method_names=['DELETE', 'GET'])
def nf_rd_csar(request, *args, **kwargs):
    csar_id = ignore_case_get(kwargs, "csarId")
    logger.info("Enter %s, method is %s, csar_id is %s", fun_name(), request.method, csar_id)
    ret, normal_status = None, None
    if request.method == 'GET':
        ret = nf_package.nf_get_csar(csar_id)
        normal_status = status.HTTP_200_OK
    elif request.method == 'DELETE':
        force_delete = csar_id.endswith("force")
        if force_delete:
            csar_id = csar_id[:-5]
        job_id = str(uuid.uuid4())
        nf_package.NfPkgDeleteThread(csar_id, job_id, force_delete).start()
        ret = [0, {"jobId": job_id}]
        normal_status = status.HTTP_202_ACCEPTED
    logger.info("Leave %s, Return value is %s", fun_name(), ret)
    if ret[0] != 0:
        return Response(data={'error': ret[1]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=normal_status)


@api_view(http_method_names=['POST'])
def ns_model_parser(request, *args, **kwargs):
    csar_id = ignore_case_get(request.data, "csarId")
    inputs = ignore_case_get(request.data, "inputs")
    logger.debug("Enter %s, csar_id=%s, inputs=%s", fun_name(), csar_id, inputs)
    ret = ns_package.parser_NSPackageModel(csar_id, inputs)
    logger.info("Leave %s, Return value is %s", fun_name(), ret)
    if ret[0] != 0:
        return Response(data={'error': ret[1]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=status.HTTP_202_ACCEPTED)


@api_view(http_method_names=['POST'])
def vnf_model_parser(request, *args, **kwargs):
    csar_id = ignore_case_get(request.data, "csarId")
    inputs = ignore_case_get(request.data, "inputs")
    logger.debug("Enter %s, csar_id=%s, inputs=%s", fun_name(), csar_id, inputs)
    nf_package.parser_vnfdmodel(csar_id, inputs)
    logger.info("Leave %s, Return value is %s", fun_name(), ret)
    if ret[0] != 0:
        return Response(data={'error': ret[1]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=status.HTTP_202_ACCEPTED)
