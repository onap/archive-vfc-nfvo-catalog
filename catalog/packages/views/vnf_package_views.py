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
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from catalog.packages.serializers.upload_vnf_pkg_from_uri_req import UploadVnfPackageFromUriRequestSerializer
from catalog.packages.serializers.create_vnf_pkg_info_req import CreateVnfPkgInfoRequestSerializer
from catalog.packages.serializers.vnf_pkg_info import VnfPkgInfoSerializer
from catalog.packages.serializers.vnf_pkg_infos import VnfPkgInfosSerializer
from catalog.packages.biz.vnf_package import VnfPackage
from catalog.packages.biz.vnf_package import VnfPkgUploadThread
from catalog.packages.biz.vnf_package import parse_vnfd_and_save
from catalog.packages.biz.vnf_package import handle_upload_failed
from .common import validate_data
from .common import view_safe_call_with_log

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method="GET",
    operation_description="Query multiple VNF package resource",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: VnfPkgInfosSerializer(),
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
@view_safe_call_with_log(logger=logger)
def vnf_packages_rc(request):
    if request.method == 'GET':
        logger.debug("Query VNF packages> %s" % request.data)
        data = VnfPackage().query_multiple()
        validate_data(data, VnfPkgInfosSerializer)
        return Response(data=data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        logger.debug("Create VNF package> %s" % request.data)
        create_vnf_pkg_info_request = validate_data(request.data,
                                                    CreateVnfPkgInfoRequestSerializer)
        data = VnfPackage().create_vnf_pkg(create_vnf_pkg_info_request.data)
        validate_data(data, VnfPkgInfoSerializer)
        return Response(data=data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='PUT',
    operation_description="Upload VNF package content",
    request_body=no_body,
    responses={
        status.HTTP_202_ACCEPTED: "Successfully",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@swagger_auto_schema(
    method="GET",
    operation_description="Fetch VNF package content",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: VnfPkgInfosSerializer(),
        status.HTTP_404_NOT_FOUND: "VNF package does not exist",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=["PUT", "GET"])
@view_safe_call_with_log(logger=logger)
def package_content_ru(request, **kwargs):
    vnf_pkg_id = kwargs.get("vnfPkgId")
    if request.method == "PUT":
        logger.debug("Upload VNF package %s" % vnf_pkg_id)
        files = request.FILES.getlist('file')
        try:
            local_file_name = VnfPackage().upload(vnf_pkg_id, files[0])
            parse_vnfd_and_save(vnf_pkg_id, local_file_name)
            return Response(None, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            handle_upload_failed(vnf_pkg_id)
            raise e

    if request.method == "GET":
        file_range = request.META.get('HTTP_RANGE')
        file_iterator = VnfPackage().download(vnf_pkg_id, file_range)
        return StreamingHttpResponse(file_iterator, status=status.HTTP_200_OK)


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
@view_safe_call_with_log(logger=logger)
def upload_from_uri_c(request, **kwargs):
    vnf_pkg_id = kwargs.get("vnfPkgId")
    try:
        upload_vnf_from_uri_request = validate_data(request.data,
                                                    UploadVnfPackageFromUriRequestSerializer)
        VnfPkgUploadThread(upload_vnf_from_uri_request.data, vnf_pkg_id).start()
        return Response(None, status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        handle_upload_failed(vnf_pkg_id)
        raise e


@swagger_auto_schema(
    method='GET',
    operation_description="Query an individual VNF package resource",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: VnfPkgInfoSerializer(),
        status.HTTP_404_NOT_FOUND: "VNF package does not exist",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete an individual VNF package resource",
    request_body=no_body,
    responses={
        status.HTTP_204_NO_CONTENT: "No content",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['GET', 'DELETE'])
@view_safe_call_with_log(logger=logger)
def vnf_package_rd(request, **kwargs):
    vnf_pkg_id = kwargs.get("vnfPkgId")
    if request.method == 'GET':
        logger.debug("Query an individual VNF package> %s" % request.data)
        data = VnfPackage().query_single(vnf_pkg_id)
        validate_data(data, VnfPkgInfoSerializer)
        return Response(data=data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        logger.debug("Delete an individual VNF package> %s" % request.data)
        VnfPackage().delete_vnf_pkg(vnf_pkg_id)
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)
