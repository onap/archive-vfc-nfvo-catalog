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

from catalog.packages.biz.pnf_descriptor import create, upload
from catalog.packages.serializers.create_pnfd_info_request import \
    CreatePnfdInfoRequestSerializer
from catalog.packages.serializers.pnfd_info import PnfdInfoSerializer
from catalog.pub.exceptions import CatalogException

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    responses={
        # status.HTTP_200_OK: Serializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
# @api_view(http_method_names=['GET'])
def query_multiple_pnfds(self, request):
    # TODO
    return None


@swagger_auto_schema(
    responses={
        # status.HTTP_200_OK: Serializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
# @api_view(http_method_names=['GET'])
def query_single_pnfd(self, request):
    # TODO
    return None


@swagger_auto_schema(
    method='POST',
    operation_description="Create an individual PNF descriptor resource",
    request_body=CreatePnfdInfoRequestSerializer(),
    responses={
        status.HTTP_201_CREATED: PnfdInfoSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['POST'])
def pnf_descriptors_rc(request, *args, **kwargs):
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
        return Response(data={'error': 'Uploading pnfd content failed.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
