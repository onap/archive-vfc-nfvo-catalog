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

from catalog.packages.biz.pnf_descriptor import create, query_multiple, upload, query_single, delete_pnf
from catalog.packages.serializers.create_pnfd_info_request import \
    CreatePnfdInfoRequestSerializer
from catalog.packages.serializers.pnfd_info import PnfdInfoSerializer
from catalog.packages.serializers.pnfd_infos import PnfdInfosSerializer
from catalog.pub.exceptions import CatalogException

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method='GET',
    operation_description="Query an individual PNF descriptor resource",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: PnfdInfoSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete an individual PNF descriptor resource",
    request_body=no_body,
    responses={
        status.HTTP_204_NO_CONTENT: None,
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['GET', 'DELETE'])
def pnfd_info_rd(request, pnfdInfoId):
    if request.method == 'GET':
        logger.debug("Query an individual PNF descriptor> %s" % request.data)
        try:
            res = query_single(pnfdInfoId)
            query_serializer = PnfdInfoSerializer(data=res)
            if not query_serializer.is_valid():
                raise CatalogException
            return Response(data=query_serializer.data, status=status.HTTP_200_OK)
        except CatalogException:
            logger.error(traceback.format_exc())
            return Response(data={'error': 'Query an individual PNF descriptor failed.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            return Response(data={'error': 'unexpected exception'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'DELETE':
        logger.debug("Delete an individual PNFD resource> %s" % request.data)
        try:
            delete_pnf(pnfdInfoId)
            return Response(data=None, status=status.HTTP_204_NO_CONTENT)
        except CatalogException:
            logger.error(traceback.format_exc())
            return Response(data={'error': 'Delete an individual PNFD resource failed.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            return Response(data={'error': 'unexpected exception'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='POST',
    operation_description="Create an individual PNF descriptor resource",
    request_body=CreatePnfdInfoRequestSerializer(),
    responses={
        status.HTTP_201_CREATED: PnfdInfoSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@swagger_auto_schema(
    method='GET',
    operation_description="Query multiple PNF descriptor resources",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: PnfdInfosSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['POST', 'GET'])
def pnf_descriptors_rc(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            create_pnfd_info_request = CreatePnfdInfoRequestSerializer(data=request.data)
            if not create_pnfd_info_request.is_valid():
                raise CatalogException
            data = create(create_pnfd_info_request.data)
            pnfd_info = PnfdInfoSerializer(data=data)
            if not pnfd_info.is_valid():
                raise CatalogException
            return Response(data=pnfd_info.data, status=status.HTTP_201_CREATED)
        except CatalogException:
            logger.error(traceback.format_exc())
            return Response(data={'error': 'Creating pnfd info failed.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'GET':
        try:
            data = query_multiple()
            pnfd_infos = PnfdInfosSerializer(data=data)
            if not pnfd_infos.is_valid():
                raise CatalogException
            return Response(data=pnfd_infos.data, status=status.HTTP_200_OK)
        except CatalogException:
            logger.error(traceback.format_exc())
            return Response(
                data={'error': 'Query of multiple PNF descriptor resources failed.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@swagger_auto_schema(
    method='PUT',
    operation_description="Upload PNFD content",
    request_body=no_body,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['PUT'])
def pnfd_content_ru(request, *args, **kwargs):
    pnfd_info_id = kwargs.get("pnfdInfoId")
    files = request.FILES.getlist('file')
    try:
        upload(files, pnfd_info_id)
        return Response(data={}, status=status.HTTP_204_NO_CONTENT)
    except IOError:
        logger.error(traceback.format_exc())
        raise CatalogException
