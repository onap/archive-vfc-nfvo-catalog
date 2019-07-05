# Copyright 2018 ZTE Corporation.
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

from django.http import StreamingHttpResponse
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from catalog.packages.biz.pnf_descriptor import PnfDescriptor
from catalog.packages.serializers.create_pnfd_info_request import CreatePnfdInfoRequestSerializer
from catalog.packages.serializers.pnfd_info import PnfdInfoSerializer
from catalog.packages.serializers.pnfd_infos import PnfdInfosSerializer
from catalog.packages.views.common import validate_data
from catalog.packages.serializers.catalog_serializers import ParseModelRequestSerializer
from catalog.packages.serializers.catalog_serializers import ParseModelResponseSerializer
from catalog.packages.serializers.catalog_serializers import InternalErrorRequestSerializer
from catalog.packages.serializers.response import ProblemDetailsSerializer
from catalog.pub.utils.syscomm import fun_name
from catalog.pub.utils.values import ignore_case_get
from .common import view_safe_call_with_log

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method='GET',
    operation_description="Query a PNFD",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: PnfdInfoSerializer(),
        status.HTTP_404_NOT_FOUND: ProblemDetailsSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: ProblemDetailsSerializer()
    }
)
@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete a PNFD",
    request_body=no_body,
    responses={
        status.HTTP_204_NO_CONTENT: "No content",
        status.HTTP_500_INTERNAL_SERVER_ERROR: ProblemDetailsSerializer()
    }
)
@api_view(http_method_names=['GET', 'DELETE'])
@view_safe_call_with_log(logger=logger)
def pnfd_info_rd(request, **kwargs):  # TODO
    pnfd_info_id = kwargs.get('pnfdInfoId')
    if request.method == 'GET':
        logger.debug("Query an individual PNF descriptor> %s" % request.data)
        data = PnfDescriptor().query_single(pnfd_info_id)
        pnfd_info = validate_data(data, PnfdInfoSerializer)
        return Response(data=pnfd_info.data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        logger.debug("Delete an individual PNFD resource> %s" % request.data)
        PnfDescriptor().delete_single(pnfd_info_id)
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    method='POST',
    operation_description="Create a  PNFD",
    request_body=CreatePnfdInfoRequestSerializer(),
    responses={
        status.HTTP_201_CREATED: PnfdInfoSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: ProblemDetailsSerializer()
    }
)
@swagger_auto_schema(
    method='GET',
    operation_description="Query multiple PNFDs",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: PnfdInfosSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: ProblemDetailsSerializer()
    }
)
@api_view(http_method_names=['POST', 'GET'])
@view_safe_call_with_log(logger=logger)
def pnf_descriptors_rc(request):
    if request.method == 'POST':
        create_pnfd_info_request = validate_data(request.data, CreatePnfdInfoRequestSerializer)
        data = PnfDescriptor().create(create_pnfd_info_request.data)
        validate_data(data, PnfdInfoSerializer)
        return Response(data=data, status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        data = PnfDescriptor().query_multiple(request)
        validate_data(data, PnfdInfosSerializer)
        return Response(data=data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='PUT',
    operation_description="Upload PNFD content",
    request_body=no_body,
    responses={
        status.HTTP_204_NO_CONTENT: "No content",
        status.HTTP_500_INTERNAL_SERVER_ERROR: ProblemDetailsSerializer()
    }
)
@swagger_auto_schema(
    method='GET',
    operation_description="Fetch PNFD content",
    request_body=no_body,
    responses={
        status.HTTP_204_NO_CONTENT: 'PNFD file',
        status.HTTP_404_NOT_FOUND: ProblemDetailsSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: ProblemDetailsSerializer()
    }
)
@api_view(http_method_names=['PUT', 'GET'])
@view_safe_call_with_log(logger=logger)
def pnfd_content_ru(request, **kwargs):
    pnfd_info_id = kwargs.get("pnfdInfoId")
    if request.method == 'PUT':
        files = request.FILES.getlist('file')
        try:
            local_file_name = PnfDescriptor().upload(files[0], pnfd_info_id)
            PnfDescriptor().parse_pnfd_and_save(pnfd_info_id, local_file_name)
            return Response(data=None, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            PnfDescriptor().handle_upload_failed(pnfd_info_id)
            raise e

    if request.method == 'GET':
        file_iterator = PnfDescriptor().download(pnfd_info_id)
        return StreamingHttpResponse(file_iterator, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='POST',
    operation_description="Parse PNF model",
    request_body=ParseModelRequestSerializer,
    responses={
        status.HTTP_202_ACCEPTED: ParseModelResponseSerializer,
        status.HTTP_500_INTERNAL_SERVER_ERROR: InternalErrorRequestSerializer})
@api_view(http_method_names=['POST'])
def pnf_model_parser(request, *args, **kwargs):
    csar_id = ignore_case_get(request.data, "csarId")
    inputs = ignore_case_get(request.data, "inputs")
    logger.debug(
        "Enter %s, csar_id=%s, inputs=%s",
        fun_name(),
        csar_id,
        inputs)
    ret = PnfDescriptor().parse_pnfd(csar_id, inputs)
    logger.info("Leave %s, Return value is %s", fun_name(), ret)
    if ret[0] != 0:
        return Response(data={'error': ret[1]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    response = validate_data(ret[1], ParseModelResponseSerializer)
    return Response(data=response.data, status=status.HTTP_202_ACCEPTED)
