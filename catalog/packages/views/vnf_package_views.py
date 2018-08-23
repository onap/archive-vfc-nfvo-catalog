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

import traceback
import logging
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from catalog.pub.exceptions import CatalogException
from catalog.packages.serializers.create_vnf_pkg_info_req import CreateVnfPkgInfoRequestSerializer
from catalog.packages.serializers.vnf_pkg_info import VnfPkgInfoSerializer
from catalog.packages.biz.nf_package import create_vnf_pkg, query_multiple

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method="GET",
    operation_description="Query multiple VNF package resource",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: VnfPkgInfoSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@swagger_auto_schema(
    method="POST",
    operation_description="Create an individual VNF package resource",
    request_body=CreateVnfPkgInfoRequestSerializer,
    responses={
        status.HTTP_201_CREATED: VnfPkgInfoSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=["GET", "POST"])
def vnf_packages_rc(request):
    if request.method == 'GET':
        logger.debug("Query VNF Packages> %s" % request.data)
        try:
            res = query_multiple()
            query_serializer = VnfPkgInfoSerializer(data=res)
            if not query_serializer.is_valid():
                raise CatalogException
            return Response(data=query_serializer.data, status=status.HTTP_200_OK)
        except CatalogException:
            logger.error(traceback.format_exc())
            return Response(data={'error': 'Querying vnfPkg failed.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            return Response(data={'error': 'unexpected exception'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    if request.method == 'POST':
        logger.debug("CreateVnfPkg> %s" % request.data)
        try:
            req_serializer = CreateVnfPkgInfoRequestSerializer(data=request.data)
            if not req_serializer.is_valid():
                raise CatalogException
            res = create_vnf_pkg(req_serializer.data)
            create_vnf_pkg_resp_serializer = VnfPkgInfoSerializer(data=res)
            if not create_vnf_pkg_resp_serializer.is_valid():
                raise CatalogException
            return Response(data=create_vnf_pkg_resp_serializer.data, status=status.HTTP_201_CREATED)
        except CatalogException:
            logger.error(traceback.format_exc())
            return Response(data={'error': 'Creating vnfPkg failed.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            return Response(data={'error': 'unexpected exception'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
