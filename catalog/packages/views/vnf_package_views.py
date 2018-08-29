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
from catalog.pub.exceptions import CatalogException, VnfPkgNotFoundException
from catalog.packages.serializers.upload_vnf_pkg_from_uri_req import UploadVnfPackageFromUriRequestSerializer
from catalog.packages.serializers.create_vnf_pkg_info_req import CreateVnfPkgInfoRequestSerializer
from catalog.packages.serializers.vnf_pkg_info import VnfPkgInfoSerializer
from catalog.packages.serializers.vnf_pkg_infos import VnfPkgInfosSerializer
from catalog.packages.biz.vnf_package import create_vnf_pkg, query_multiple, VnfPkgUploadThread, \
    query_single, delete_vnf_pkg, parse_vnfd_and_save, fetch_vnf_pkg, handle_upload_failed
from catalog.pub.database.models import VnfPackageModel
from catalog.packages.views.ns_descriptor_views import validate_data

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
def vnf_packages_rc(request):
    if request.method == 'GET':
        logger.debug("Query VNF packages> %s" % request.data)
        try:
            res = query_multiple()
            query_serializer = validate_data(res, VnfPkgInfosSerializer)
            return Response(data=query_serializer.data, status=status.HTTP_200_OK)
        except CatalogException as e:
            logger.error(e.message)
            error_msg = {'error': 'Query VNF package failed.'}
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_msg = {'error': 'unexpected exception'}
        return Response(data=error_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'POST':
        logger.debug("Create VNF package> %s" % request.data)
        try:
            req_serializer = validate_data(request.data, CreateVnfPkgInfoRequestSerializer)
            res = create_vnf_pkg(req_serializer.data)
            create_vnf_pkg_resp_serializer = validate_data(res, VnfPkgInfoSerializer)
            return Response(data=create_vnf_pkg_resp_serializer.data, status=status.HTTP_201_CREATED)
        except CatalogException as e:
            logger.error(e.message)
            error_msg = {'error': 'Create VNF package failed.'}
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_msg = {'error': 'unexpected exception'}
        return Response(data=error_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
def upload_vnf_pkg_content(request, vnfPkgId):
    if request.method == "PUT":
        logger.debug("Upload VNF package %s" % vnfPkgId)
        try:
            vnf_pkg = VnfPackageModel.objects.filter(vnfPackageId=vnfPkgId)
            if vnf_pkg[0].onboardingState != "CREATED":
                raise CatalogException("VNF package (%s) is not created" % vnfPkgId)
            file_object = request.FILES.get('file')
            upload_path = os.path.join(CATALOG_ROOT_PATH, vnfPkgId)
            if not os.path.exists(upload_path):
                os.makedirs(upload_path, 0o777)

            upload_file_name = os.path.join(upload_path, file_object.name)
            with open(upload_file_name, 'wb+') as dest_file:
                for chunk in file_object.chunks():
                    dest_file.write(chunk)

            parse_vnfd_and_save(vnfPkgId, upload_file_name)
            return Response(None, status=status.HTTP_202_ACCEPTED)
        except CatalogException as e:
                handle_upload_failed(vnfPkgId)
                logger.debug(e.message)
                error_msg = {'error': 'Upload VNF package failed.'}
        except Exception as e:
            handle_upload_failed(vnfPkgId)
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_msg = {'error': 'unexpected exception'}
        return Response(data=error_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == "GET":
        try:
            response = fetch_vnf_pkg(request, vnfPkgId)
            return response
        except VnfPkgNotFoundException as e:
            logger.error(e.message)
            return Response(data={'error': "VNF package does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except CatalogException as e:
            logger.error(e.message)
            error_msg = {'error': 'Fetch VNF package failed.'}
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_msg = {'error': 'unexpected exception'}
        return Response(data=error_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        req_serializer = validate_data(request.data, UploadVnfPackageFromUriRequestSerializer)
        VnfPkgUploadThread(req_serializer.data, vnfPkgId).start()
        return Response(None, status=status.HTTP_202_ACCEPTED)
    except CatalogException as e:
        handle_upload_failed(vnfPkgId)
        logger.debug(e.message)
        error_msg = {'error': 'Upload VNF package failed.'}
    except Exception as e:
        handle_upload_failed(vnfPkgId)
        logger.error(e.message)
        logger.error(traceback.format_exc())
        error_msg = {'error': 'unexpected exception'}
    return Response(data=error_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            query_serializer = validate_data(res, VnfPkgInfoSerializer)
            return Response(data=query_serializer.data, status=status.HTTP_200_OK)
        except VnfPkgNotFoundException as e:
            logger.error(e.message)
            return Response(data={'error': "VNF package does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except CatalogException as e:
            logger.error(e.message)
            error_msg = {'error': 'Query an individual VNF package failed.'}
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_msg = {'error': 'unexpected exception'}
        return Response(data=error_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'DELETE':
        logger.debug("Delete an individual VNF package> %s" % request.data)
        try:
            delete_vnf_pkg(vnfPkgId)
            return Response(data=None, status=status.HTTP_204_NO_CONTENT)
        except CatalogException as e:
            logger.error(e.message)
            error_msg = {'error': 'Delete an individual VNF package failed.'}
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_msg = {'error': 'unexpected exception'}
        return Response(data=error_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
