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
import traceback

from django.http import StreamingHttpResponse
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from catalog.packages.biz.ns_descriptor import NsDescriptor
from catalog.packages.serializers.create_nsd_info_request import CreateNsdInfoRequestSerializer
from catalog.packages.serializers.nsd_info import NsdInfoSerializer
from catalog.packages.serializers.nsd_infos import NsdInfosSerializer
from catalog.packages.views.common import validate_data
from catalog.pub.exceptions import CatalogException, ResourceNotFoundException

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method='GET',
    operation_description="Query a NSD",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: NsdInfoSerializer(),
        status.HTTP_404_NOT_FOUND: 'NSDs do not exist',
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete a NSD",
    request_body=no_body,
    responses={
        status.HTTP_204_NO_CONTENT: None,
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['GET', 'DELETE'])
def ns_info_rd(request, **kwargs):
    nsd_info_id = kwargs.get("nsdInfoId")
    if request.method == 'GET':
        try:
            data = NsDescriptor().query_single(nsd_info_id)
            nsd_info = validate_data(data, NsdInfoSerializer)
            return Response(data=nsd_info.data, status=status.HTTP_200_OK)
        except ResourceNotFoundException as e:
            logger.error(e.message)
            error_data = {'error': e.message}
            error_code = status.HTTP_404_NOT_FOUND
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_data = {'error': 'Query of NSD(%s) failed.' % nsd_info_id}
            error_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(data=error_data, status=error_code)

    if request.method == 'DELETE':
        try:
            NsDescriptor().delete_single(nsd_info_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_data = {'error': 'Deletion of NSD(%s) failed.' % nsd_info_id}
        return Response(data=error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='POST',
    operation_description="Create a NSD",
    request_body=CreateNsdInfoRequestSerializer(),
    responses={
        status.HTTP_201_CREATED: NsdInfoSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@swagger_auto_schema(
    method='GET',
    operation_description="Query multiple NSDs",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: NsdInfosSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['POST', 'GET'])
def ns_descriptors_rc(request):
    if request.method == 'POST':
        try:
            create_nsd_info_request = validate_data(request.data, CreateNsdInfoRequestSerializer)
            data = NsDescriptor().create(create_nsd_info_request.data)
            nsd_info = validate_data(data, NsdInfoSerializer)
            return Response(data=nsd_info.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_data = {'error': 'Creating a NSD failed.'}
        return Response(data=error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'GET':
        try:
            data = NsDescriptor().query_multiple()
            nsd_infos = validate_data(data, NsdInfosSerializer)
            return Response(data=nsd_infos.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_data = {'error': 'Query of multiple NSDs failed.'}
        return Response(data=error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='PUT',
    operation_description="Upload NSD content",
    request_body=no_body,
    responses={
        status.HTTP_204_NO_CONTENT: 'PNFD file',
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@swagger_auto_schema(
    method='GET',
    operation_description="Download NSD content",
    request_body=no_body,
    responses={
        status.HTTP_204_NO_CONTENT: None,
        status.HTTP_404_NOT_FOUND: 'NSD does not exist.',
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['PUT', 'GET'])
def nsd_content_ru(request, **kwargs):
    nsd_info_id = kwargs.get("nsdInfoId")
    if request.method == 'PUT':
        files = request.FILES.getlist('file')
        try:
            local_file_name = NsDescriptor().upload(nsd_info_id, files[0])
            NsDescriptor().parse_nsd_and_save(nsd_info_id, local_file_name)
            return Response(data=None, status=status.HTTP_204_NO_CONTENT)
        except CatalogException as e:
            NsDescriptor().handle_upload_failed(nsd_info_id)
            logger.error(e.message)
            error_data = {'error': e.message}
        except Exception as e:
            NsDescriptor().handle_upload_failed(nsd_info_id)
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_data = {'error': 'Uploading NSD(%s) failed.'}
        return Response(data=error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'GET':
        try:
            file_range = request.META.get('RANGE')
            file_iterator = NsDescriptor().download(nsd_info_id, file_range)
            return StreamingHttpResponse(file_iterator, status=status.HTTP_200_OK)
        except ResourceNotFoundException as e:
            logger.error(e.message)
            error_data = {'error': e.message}
            error_code = status.HTTP_404_NOT_FOUND
        except CatalogException as e:
            logger.error(e.message)
            error_data = {'error': e.message}
            error_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_data = {'error': 'Downloading NSD(%s) failed.' % nsd_info_id}
            error_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(data=error_data, status=error_code)
