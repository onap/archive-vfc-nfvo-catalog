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

from drf_yasg import openapi
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from catalog.packages.biz import vnfpackage, nspackage
from catalog.packages.serializers.catalog_serializers import InternalErrorRequestSerializer
from catalog.packages.serializers.catalog_serializers import NfPackageDistributeRequestSerializer
from catalog.packages.serializers.catalog_serializers import NfPackageSerializer
from catalog.packages.serializers.catalog_serializers import NfPackagesSerializer
from catalog.packages.serializers.catalog_serializers import NsPackageDistributeRequestSerializer
from catalog.packages.serializers.catalog_serializers import NsPackageDistributeResponseSerializer
from catalog.packages.serializers.catalog_serializers import NsPackageSerializer
from catalog.packages.serializers.catalog_serializers import NsPackagesSerializer
from catalog.packages.serializers.catalog_serializers import ParseModelRequestSerializer
from catalog.packages.serializers.catalog_serializers import ParseModelResponseSerializer
from catalog.packages.serializers.catalog_serializers import PostJobResponseSerializer
from catalog.pub.utils.syscomm import fun_name
from catalog.pub.utils.values import ignore_case_get

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method='POST',
    operation_description="On distribute NS package",
    request_body=NsPackageDistributeRequestSerializer,
    responses={
        status.HTTP_202_ACCEPTED: NsPackageDistributeResponseSerializer,
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
    ret, normal_status, response_serializer, validation_error = None, None, None, None

    if request.method == 'GET':
        # Gets ns package list
        ret = nspackage.ns_get_csars()
        normal_status = status.HTTP_200_OK

        if ret[0] == 0:
            response_serializer = NsPackagesSerializer(data=ret[1])
            validation_error = handleValidatonError(
                response_serializer, False)
            if validation_error:
                return validation_error
    elif request.method == 'POST':
        # Distributes the package accroding to the given csarId
        request_serializer = NsPackageDistributeRequestSerializer(data=request.data)
        validation_error = handleValidatonError(request_serializer, True)
        if validation_error:
            return validation_error

        csar_id = ignore_case_get(request.data, "csarId")
        logger.debug("csar_id is %s", csar_id)
        ret = nspackage.ns_on_distribute(csar_id)
        normal_status = status.HTTP_202_ACCEPTED

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
    ret, normal_status, response_serializer, validation_error = None, None, None, None
    if request.method == 'GET':
        ret = vnfpackage.nf_get_csars()
        normal_status = status.HTTP_200_OK
        response_serializer = NfPackagesSerializer(data=ret[1])
    elif request.method == 'POST':
        request_serivalizer = NfPackageDistributeRequestSerializer(
            data=request.data)
        validation_error = handleValidatonError(
            request_serivalizer, True)
        if validation_error:
            return validation_error

        csar_id = ignore_case_get(request_serivalizer.data, "csarId")
        vim_ids = ignore_case_get(request_serivalizer.data, "vimIds")
        lab_vim_id = ignore_case_get(request_serivalizer.data, "labVimId")
        job_id = str(uuid.uuid4())
        vnfpackage.NfDistributeThread(
            csar_id, vim_ids, lab_vim_id, job_id).start()
        ret = [0, {"jobId": job_id}]
        normal_status = status.HTTP_202_ACCEPTED

        response_serializer = PostJobResponseSerializer(data=ret[1])
    logger.debug("Leave %s, Return value is %s", fun_name(), ret)

    if ret[0] != 0:
        return Response(
            data={
                'error': ret[1]},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    validation_error = handleValidatonError(
        response_serializer, False)
    if validation_error:
        return validation_error

    return Response(data=response_serializer.data, status=normal_status)


@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete one NS package",
    request_body=no_body,
    manual_parameters=[
        openapi.Parameter(
            'csarId',
            openapi.IN_QUERY,
            "csarId",
            type=openapi.TYPE_STRING)],
    responses={
        status.HTTP_200_OK: NsPackageDistributeResponseSerializer,
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            'error message',
            openapi.Schema(
                type=openapi.TYPE_STRING))})
@swagger_auto_schema(
    method='GET',
    operation_description="Query one NS package",
    request_body=no_body,
    manual_parameters=[
        openapi.Parameter(
            'csarId',
            openapi.IN_QUERY,
            "csarId",
            type=openapi.TYPE_STRING)],
    responses={
        status.HTTP_200_OK: NsPackageSerializer,
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            'error message',
            openapi.Schema(
                type=openapi.TYPE_STRING))})
@api_view(http_method_names=['DELETE', 'GET'])
def ns_rd_csar(request, *args, **kwargs):
    csar_id = ignore_case_get(kwargs, "csarId")
    logger.info("Enter %s, method is %s, csar_id is %s",
                fun_name(), request.method, csar_id)
    ret, normal_status, response_serializer, validation_error = None, None, None, None
    if request.method == 'GET':
        ret = nspackage.ns_get_csar(csar_id)
        normal_status = status.HTTP_200_OK
        if ret[0] == 0:
            response_serializer = NsPackageSerializer(data=ret[1])
            validation_error = handleValidatonError(response_serializer, False)
            if validation_error:
                return validation_error
    elif request.method == 'DELETE':
        ret = nspackage.ns_delete_csar(csar_id)
        normal_status = status.HTTP_200_OK
    logger.info("Leave %s, Return value is %s", fun_name(), ret)
    if ret[0] != 0:
        return Response(
            data={
                'error': ret[1]},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=normal_status)


@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete one Nf package",
    request_body=no_body,
    manual_parameters=[
        openapi.Parameter(
            'csarId',
            openapi.IN_QUERY,
            "csarId",
            type=openapi.TYPE_STRING)],
    responses={
        status.HTTP_202_ACCEPTED: PostJobResponseSerializer,
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            'error message',
            openapi.Schema(
                type=openapi.TYPE_STRING))})
@swagger_auto_schema(
    method='GET',
    operation_description="Query one Nf package",
    request_body=no_body,
    manual_parameters=[
        openapi.Parameter(
            'csarId',
            openapi.IN_QUERY,
            "csarId",
            type=openapi.TYPE_STRING)],
    responses={
        status.HTTP_200_OK: NfPackageSerializer,
        status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
            'error message',
            openapi.Schema(
                type=openapi.TYPE_STRING))})
@api_view(http_method_names=['DELETE', 'GET'])
def nf_rd_csar(request, *args, **kwargs):
    csar_id = ignore_case_get(kwargs, "csarId")
    logger.info("Enter %s, method is %s, csar_id is %s",
                fun_name(), request.method, csar_id)
    ret, normal_status, response_serializer, validation_error = None, None, None, None

    if request.method == 'GET':
        ret = vnfpackage.nf_get_csar(csar_id)
        normal_status = status.HTTP_200_OK
        response_serializer = NfPackageSerializer(data=ret[1])

    elif request.method == 'DELETE':
        job_id = str(uuid.uuid4())
        vnfpackage.NfPkgDeleteThread(csar_id, job_id).start()
        ret = [0, {"jobId": job_id}]
        normal_status = status.HTTP_202_ACCEPTED
        response_serializer = PostJobResponseSerializer(data=ret[1])

    logger.info("Leave %s, Return value is %s", fun_name(), ret)
    if ret[0] != 0:
        return Response(
            data={
                'error': ret[1]},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    validation_error = handleValidatonError(
        response_serializer, False)
    if validation_error:
        return validation_error

    return Response(data=response_serializer.data, status=normal_status)


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
    ret = nspackage.parse_nsd(csar_id, inputs)
    logger.info("Leave %s, Return value is %s", fun_name(), ret)
    if ret[0] != 0:
        return Response(
            data={
                'error': ret[1]},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response_serializer = ParseModelResponseSerializer(data=ret[1])
    validation_error = handleValidatonError(
        response_serializer, False)
    if validation_error:
        return validation_error

    return Response(data=response_serializer.data, status=status.HTTP_202_ACCEPTED)


@swagger_auto_schema(
    method='POST',
    operation_description="Parse NF model",
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
    ret = vnfpackage.parse_vnfd(csar_id, inputs)
    logger.info("Leave %s, Return value is %s", fun_name(), ret)
    if ret[0] != 0:
        return Response(
            data={
                'error': ret[1]},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response_serializer = ParseModelResponseSerializer(data=ret[1])
    validation_error = handleValidatonError(
        response_serializer, False)
    if validation_error:
        return validation_error

    return Response(data=response_serializer.data, status=status.HTTP_202_ACCEPTED)


def handleValidatonError(base_serializer, is_request):
    response = None

    if not base_serializer.is_valid():
        errormessage = base_serializer.errors
        logger.error(errormessage)

        if is_request:
            message = 'Invalid request'
        else:
            message = 'Invalid response'
        logger.error(message)
        response = Response(
            data={'error': errormessage},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
