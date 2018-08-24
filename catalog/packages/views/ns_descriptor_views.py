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
import traceback

from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import FileResponse

from catalog.packages.biz.ns_descriptor import create, query_multiple, query_single, delete_single, upload, download
from catalog.packages.serializers.create_nsd_info_request import \
    CreateNsdInfoRequestSerializer
from catalog.packages.serializers.nsd_info import NsdInfoSerializer
from catalog.packages.serializers.nsd_infos import NsdInfosSerializer
from catalog.pub.exceptions import CatalogException

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method='GET',
    operation_description="Query an individual NS descriptor resource",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: NsdInfoSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete an individual NS descriptor resource",
    request_body=no_body,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['GET', 'DELETE'])
def ns_info_rd(request, nsdInfoId):
    if request.method == 'GET':
        try:
            data = query_single(nsdInfoId)
            nsd_info = NsdInfoSerializer(data=data)
            if not nsd_info.is_valid():
                raise CatalogException
            return Response(data=nsd_info.data, status=status.HTTP_200_OK)
        except CatalogException:
            logger.error(traceback.format_exc())
            return Response(
                data={'error': 'Query of an individual NS descriptor resource failed.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    if request.method == 'DELETE':
        try:
            data = delete_single(nsdInfoId)
            return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except CatalogException:
            logger.error(traceback.format_exc())
            return Response(
                data={'error': 'Deletion of an individual NS descriptor resource failed.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@swagger_auto_schema(
    method='POST',
    operation_description="Create an individual NS descriptor resource",
    request_body=CreateNsdInfoRequestSerializer(),
    responses={
        status.HTTP_201_CREATED: NsdInfoSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@swagger_auto_schema(
    method='GET',
    operation_description="Query multiple NS descriptor resources",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: NsdInfosSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['POST', 'GET'])
def ns_descriptors_rc(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            create_nsd_info_requst = CreateNsdInfoRequestSerializer(data=request.data)
            if not create_nsd_info_requst.is_valid():
                raise CatalogException
            data = create(create_nsd_info_requst.data)
            nsd_info = NsdInfoSerializer(data=data)
            if not nsd_info.is_valid():
                raise CatalogException
            return Response(data=nsd_info.data, status=status.HTTP_201_CREATED)
        except CatalogException:
            logger.error(traceback.format_exc())
            return Response(data={'error': 'Creating nsd info failed.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'GET':
        try:
            data = query_multiple()
            nsd_infos = NsdInfosSerializer(data=data)
            if not nsd_infos.is_valid():
                raise CatalogException
            return Response(data=nsd_infos.data, status=status.HTTP_200_OK)
        except CatalogException:
            logger.error(traceback.format_exc())
            return Response(
                data={'error': 'Query of multiple NS descriptor resources failed.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@swagger_auto_schema(
    method='PUT',
    operation_description="Upload NSD content",
    request_body=no_body,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@swagger_auto_schema(
    method='GET',
    operation_description="Fetch NSD content",
    request_body=no_body,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['PUT', 'GET'])
def nsd_content_ru(request, *args, **kwargs):
    nsd_info_id = kwargs.get("nsdInfoId")
    if request.method == 'PUT':
        files = request.FILES.getlist('file')
        try:
            upload(files[0], nsd_info_id)
            return Response(data={}, status=status.HTTP_204_NO_CONTENT)
        except IOError:
            logger.error(traceback.format_exc())
            raise CatalogException
            return Response(data={'error': 'Uploading nsd content failed.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'GET':
        try:
            file_path = download(nsd_info_id)
            file_name = file_path.split('/')[-1]
            file_name = file_name.split('\\')[-1]
            response = FileResponse(open(file_path, 'rb'), status=status.HTTP_200_OK)
            response['Content-Disposition'] = 'attachment; filename=%s' % file_name.encode('utf-8')
            return response
        except IOError:
            logger.error(traceback.format_exc())
            raise CatalogException
            
