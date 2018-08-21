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

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from catalog.packages.biz.ns_descriptor import create
from catalog.packages.serializers.create_nsd_info_request import \
    CreateNsdInfoRequestSerializer
from catalog.packages.serializers.nsd_info import NsdInfoSerializer
from catalog.pub.exceptions import CatalogException

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    responses={
        # status.HTTP_200_OK: Serializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
# @api_view(http_method_names=['GET'])
def query_ns_descriptors(self, request):
    # TODO
    return None


@swagger_auto_schema(
    method='POST',
    operation_description="Create an individual NS descriptor resource",
    request_body=CreateNsdInfoRequestSerializer(),
    responses={
        status.HTTP_201_CREATED: NsdInfoSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['POST'])
def create_ns_descriptors(request, *args, **kwargs):
    try:
        create_nsd_info_requst = CreateNsdInfoRequestSerializer(data=request.data)
        if not create_nsd_info_requst.is_valid():
            raise CatalogException
        data = create(create_nsd_info_requst.data)
        nsd_info = NsdInfoSerializer(data=data)
        if not nsd_info.is_valid():
            raise CatalogException
        return Response(data=data, status=status.HTTP_201_CREATED)
    except CatalogException:
        logger.error(traceback.format_exc())
        return Response(data={'error': 'Creating nsd info failed.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
