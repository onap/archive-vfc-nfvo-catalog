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
import os

from catalog.pub.config.config import CATALOG_ROOT_PATH
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from catalog.pub.exceptions import CatalogException
from catalog.packages.serializers.upload_vnf_pkg_from_uri_req import UploadVnfPackageFromUriRequestSerializer
from catalog.packages.serializers.create_vnf_pkg_info_req import CreateVnfPkgInfoRequestSerializer
from catalog.packages.serializers.vnf_pkg_info import VnfPkgInfoSerializer
from catalog.packages.serializers.vnf_pkg_infos import VnfPkgInfosSerializer
from catalog.packages.biz.vnf_package import create_vnf_pkg, query_multiple, VnfpkgUploadThread, \
    query_single, delete_single

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
            query_serializer = VnfPkgInfosSerializer(data=res)
            if not query_serializer.is_valid():
                raise CatalogException
            return Response(data=query_serializer.data, status=status.HTTP_200_OK)
        except CatalogException:
            logger.error(traceback.format_exc())
            return Response(data={'error': 'Query vnfPkg failed.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
            return Response(data={'error': 'Create vnfPkg failed.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            return Response(data={'error': 'unexpected exception'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='PUT',
    operation_description="Upload VNF package content",
    request_body=no_body,
    responses={
        status.HTTP_202_ACCEPTED: "Successfully",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['PUT'])
def upload_vnf_pkg_content(request, vnfPkgId):
    logger.debug("UploadVnf %s" % vnfPkgId)
    file_object = request.FILES.get('file')
    upload_path = os.path.join(CATALOG_ROOT_PATH, vnfPkgId)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path, 0o777)
    try:
        upload_file_name = os.path.join(upload_path, file_object.name)
        with open(upload_file_name, 'wb+') as dest_file:
            for chunk in file_object.chunks():
                dest_file.write(chunk)
    except Exception as e:
        logger.error("File upload exception.[%s:%s]" % (type(e), str(e)))
        logger.error("%s", traceback.format_exc())
    return Response(None, status.HTTP_202_ACCEPTED)


@swagger_auto_schema(
    method='POST',
    operation_description="Upload VNF package content from uri",
    request_body=UploadVnfPackageFromUriRequestSerializer,
    responses={
        status.HTTP_202_ACCEPTED: "Successfully",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['POST'])
def upload_vnf_pkg_from_uri(request, vnfPkgId):
    try:
        req_serializer = UploadVnfPackageFromUriRequestSerializer(data=request.data)
        if not req_serializer.is_valid():
            raise CatalogException
        VnfpkgUploadThread(req_serializer.data, vnfPkgId).start()
        return Response(None, status=status.HTTP_202_ACCEPTED)
    except CatalogException:
        logger.error(traceback.format_exc())
        return Response(data={'error': 'Upload vnfPkg failed.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error(e.message)
        logger.error(traceback.format_exc())
        return Response(data={'error': 'unexpected exception'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='GET',
    operation_description="Query an individual VNF package resource",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: VnfPkgInfoSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete an individual VNF package resource",
    request_body=no_body,
    responses={
        status.HTTP_204_NO_CONTENT: None,
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['GET', 'DELETE'])
def vnf_package_rd(request, vnfPkgId):
    if request.method == 'GET':
        logger.debug("Query an individual VNF package> %s" % request.data)
        try:
            res = query_single(vnfPkgId)
            query_serializer = VnfPkgInfoSerializer(data=res)
            if not query_serializer.is_valid():
                raise CatalogException
            return Response(data=query_serializer.data, status=status.HTTP_200_OK)
        except CatalogException:
            logger.error(traceback.format_exc())
            return Response(data={'error': 'Query an individual VNF package failed.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            return Response(data={'error': 'unexpected exception'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'DELETE':
        logger.debug("Delete an individual VNF package> %s" % request.data)
        try:
            delete_single(vnfPkgId)
            return Response(data=None, status=status.HTTP_204_NO_CONTENT)
        except CatalogException:
            logger.error(traceback.format_exc())
            return Response(data={'error': 'Delete an individual VNF package failed.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            return Response(data={'error': 'unexpected exception'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
