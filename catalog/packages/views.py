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
from catalog.serializers import NsPackagesSerializer
from catalog.serializers import NfPackagesSerializer
from catalog.serializers import NfPackageDistributeRequestSerializer
from catalog.serializers import PostJobResponseSerializer
from catalog.serializers import ParseModelRequestSerializer
from catalog.serializers import ParseModelResponseSerializer
from catalog.serializers import InternalErrorRequestSerializer

from drf_yasg import openapi
from drf_yasg.utils import no_body, swagger_auto_schema


logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method='POST',
    operation_description="On distribute NS package",
    request_body=no_body,
    responses={
        status.HTTP_202_ACCEPTED: openapi.Response(
            'return code',
            openapi.Schema(
                type=openapi.TYPE_STRING,
                pattern='CSAR(\w+) distributed successfully.')),
        status.HTTP_500_INTERNAL_SERVER_ERROR: InternalErrorRequestSerializer})
@swagger_auto_schema(
    method='GET',
    operation_description="Query NS packages",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: NsPackagesSerializer,
        status.HTTP_500_INTERNAL_SERVER_ERROR: InternalErrorRequestSerializer})
@api_view(http_method_names=['POST', 'GET'])
def nspackages_rc(request, *args, **kwargs):
    logger.debug("Enter %s, method is %s", fun_name(), request.method)
    ret, normal_status, validation_error = None, None, None

    if request.method == 'GET':
        # Gets ns package list
        ret = ns_package.ns_get_csars()
        normal_status = status.HTTP_200_OK
        responseSerializer = NsPackagesSerializer(data=ret[1])

        if not responseSerializer.is_valid():
            validation_error = handleValidatonError(
                responseSerializer, False)
    elif request.method == 'POST':
        # Distributes the package accroding to the given csarId
        csar_id = ignore_case_get(request.data, "csarId")
        logger.debug("csar_id is %s", csar_id)
        ret = ns_package.ns_on_distribute(csar_id)
        normal_status = status.HTTP_202_ACCEPTED

    if validation_error:
        return validation_error

    logger.debug("Leave %s, Return value is %s", fun_name(), ret)
    if ret[0] != 0:
        return Response(
            data={
                'error': ret[1]},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=normal_status)


@swagger_auto_schema(
    method='POST',
    operation_description="On distribute Nf package",
    request_body=NfPackageDistributeRequestSerializer(),
    responses={
        status.HTTP_202_ACCEPTED: PostJobResponseSerializer,
        status.HTTP_500_INTERNAL_SERVER_ERROR: InternalErrorRequestSerializer})
@swagger_auto_schema(
    method='GET',
    operation_description="Query Nf packages",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: NfPackagesSerializer,
        status.HTTP_500_INTERNAL_SERVER_ERROR: InternalErrorRequestSerializer})
@api_view(http_method_names=['POST', 'GET'])
def nfpackages_rc(request, *args, **kwargs):
    logger.debug(
        "Enter %s%s, method is %s",
        fun_name(),
        request.data,
        request.method)
    ret, normal_status, validation_error = None, None, None
    if request.method == 'GET':
        ret = nf_package.nf_get_csars()
        normal_status = status.HTTP_200_OK
        response = Response(data=ret[1], status=normal_status)
        response_serializer = NfPackagesSerializer(data=response.data)
        if not response_serializer.is_valid():
            validation_error = handleValidatonError(response_serializer, False)
            return validation_error
    elif request.method == 'POST':
        request_serivalizer = NfPackageDistributeRequestSerializer(
            data=request.data)
        if not request_serivalizer.is_valid():
            validation_error = handleValidatonError(request_serivalizer, True)
            return validation_error

        csar_id = ignore_case_get(request_serivalizer.data, "csarId")
        vim_ids = ignore_case_get(request_serivalizer.data, "vimIds")
        lab_vim_id = ignore_case_get(request_serivalizer.data, "labVimId")
        job_id = str(uuid.uuid4())
        nf_package.NfDistributeThread(
            csar_id, vim_ids, lab_vim_id, job_id).start()
        ret = [0, {"jobId": job_id}]
        normal_status = status.HTTP_202_ACCEPTED

        response = Response(data=ret[1], status=normal_status)
        response_serializer = PostJobResponseSerializer(data=response.data)
        if not response_serializer.is_valid():
            validation_error = handleValidatonError(response_serializer, False)
            return validation_error
    logger.debug("Leave %s, Return value is %s", fun_name(), ret)

    if ret[0] != 0:
        return Response(
            data={
                'error': ret[1]},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=response_serializer.data, status=normal_status)


@api_view(http_method_names=['DELETE', 'GET'])
def ns_rd_csar(request, *args, **kwargs):
    csar_id = ignore_case_get(kwargs, "csarId")
    logger.info("Enter %s, method is %s, csar_id is %s",
                fun_name(), request.method, csar_id)
    ret, normal_status = None, None
    if request.method == 'GET':
        ret = ns_package.ns_get_csar(csar_id)
        normal_status = status.HTTP_200_OK
    elif request.method == 'DELETE':
        ret = ns_package.ns_delete_csar(csar_id)
        normal_status = status.HTTP_202_ACCEPTED
    logger.info("Leave %s, Return value is %s", fun_name(), ret)
    if ret[0] != 0:
        return Response(
            data={
                'error': ret[1]},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=normal_status)


@api_view(http_method_names=['DELETE', 'GET'])
def nf_rd_csar(request, *args, **kwargs):
    csar_id = ignore_case_get(kwargs, "csarId")
    logger.info("Enter %s, method is %s, csar_id is %s",
                fun_name(), request.method, csar_id)
    ret, normal_status = None, None
    if request.method == 'GET':
        ret = nf_package.nf_get_csar(csar_id)
        normal_status = status.HTTP_200_OK
    elif request.method == 'DELETE':
        job_id = str(uuid.uuid4())
        nf_package.NfPkgDeleteThread(csar_id, job_id).start()
        ret = [0, {"jobId": job_id}]
        normal_status = status.HTTP_202_ACCEPTED
    logger.info("Leave %s, Return value is %s", fun_name(), ret)
    if ret[0] != 0:
        return Response(
            data={
                'error': ret[1]},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=normal_status)


@swagger_auto_schema(
    method='POST',
    operation_description="Parse NS model",
    request_body=ParseModelRequestSerializer,
    responses={
        status.HTTP_202_ACCEPTED: ParseModelResponseSerializer,
        status.HTTP_500_INTERNAL_SERVER_ERROR: InternalErrorRequestSerializer})
@api_view(http_method_names=['POST'])
def ns_model_parser(request, *args, **kwargs):
    csar_id = ignore_case_get(request.data, "csarId")
    inputs = ignore_case_get(request.data, "inputs")
    logger.debug(
        "Enter %s, csar_id=%s, inputs=%s",
        fun_name(),
        csar_id,
        inputs)
    ret = ns_package.parse_nsd(csar_id, inputs)
    logger.info("Leave %s, Return value is %s", fun_name(), ret)
    if ret[0] != 0:
        return Response(
            data={
                'error': ret[1]},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=status.HTTP_202_ACCEPTED)


@swagger_auto_schema(
    method='POST',
    operation_description="Parse Nf model",
    request_body=ParseModelRequestSerializer,
    responses={
        status.HTTP_202_ACCEPTED: ParseModelResponseSerializer,
        status.HTTP_500_INTERNAL_SERVER_ERROR: InternalErrorRequestSerializer})
@api_view(http_method_names=['POST'])
def vnf_model_parser(request, *args, **kwargs):
    csar_id = ignore_case_get(request.data, "csarId")
    inputs = ignore_case_get(request.data, "inputs")
    logger.debug(
        "Enter %s, csar_id=%s, inputs=%s",
        fun_name(),
        csar_id,
        inputs)
    ret = nf_package.parse_vnfd(csar_id, inputs)
    logger.info("Leave %s, Return value is %s", fun_name(), ret)
    if ret[0] != 0:
        return Response(
            data={
                'error': ret[1]},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=status.HTTP_202_ACCEPTED)


def handleValidatonError(base_serializer, is_request):
    errormessage = base_serializer.errors
    logger.error(errormessage)

    if is_request:
        message = 'Invalid request'
    else:
        message = 'Invalid response'
    logger.error(message)

    return Response(data={'error': errormessage},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
