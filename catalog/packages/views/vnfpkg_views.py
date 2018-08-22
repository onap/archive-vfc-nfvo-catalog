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

import os
import traceback
import logging
from catalog.pub.config.config import CATALOG_ROOT_PATH
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from catalog.packages.biz.nf_package import VnfpkgUploadThread
from catalog.pub.exceptions import CatalogException
from catalog.packages.serializers.upload_vnf_pkg_from_uri_req import UploadVnfPackageFromUriRequestSerializer

logger = logging.getLogger(__name__)


class vnf_packages(APIView):
    @swagger_auto_schema(
        responses={
            # status.HTTP_200_OK: Serializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def get(self, request):
        # TODO
        return None

    @swagger_auto_schema(
        # request_body=CreateVnfReqSerializer(),
        responses={
            #     status.HTTP_201_CREATED: CreateVnfRespSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def post(self, request):
        # TODO
        return None


class vnf_package(APIView):
    @swagger_auto_schema(
        responses={
            # status.HTTP_200_OK: Serializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def get(self, request):
        # TODO
        return None

    @swagger_auto_schema(
        # request_body=CreateVnfReqSerializer(),
        responses={
            #     status.HTTP_201_CREATED: CreateVnfRespSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def post(self, request):
        # TODO
        return None


class vnfd(APIView):
    @swagger_auto_schema(
        responses={
            # status.HTTP_200_OK: Serializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def get(self, request):
        # TODO
        return None

    @swagger_auto_schema(
        # request_body=CreateVnfReqSerializer(),
        responses={
            #     status.HTTP_201_CREATED: CreateVnfRespSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def post(self, request):
        # TODO
        return None


class package_content(APIView):
    @swagger_auto_schema(
        responses={
            # status.HTTP_200_OK: Serializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def get(self, request):
        # TODO
        return None

    @swagger_auto_schema(
        # request_body=CreateVnfReqSerializer(),
        responses={
            #     status.HTTP_201_CREATED: CreateVnfRespSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def post(self, request):
        # TODO
        return None

    def put(self, request, vnfPkgId):
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


class upload_from_uri(APIView):
    @swagger_auto_schema(
        responses={
            # status.HTTP_200_OK: Serializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def get(self, request):
        # TODO
        return None

    @swagger_auto_schema(
        request_body=UploadVnfPackageFromUriRequestSerializer(),
        responses={
            status.HTTP_202_ACCEPTED: "Successfully",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def post(self, request, vnfPkgId):
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


class artifacts(APIView):
    @swagger_auto_schema(
        responses={
            # status.HTTP_200_OK: Serializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def get(self, request):
        # TODO
        return None

    @swagger_auto_schema(
        # request_body=CreateVnfReqSerializer(),
        responses={
            #     status.HTTP_201_CREATED: CreateVnfRespSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def post(self, request):
        # TODO
        return None


class vnfpkg_subscriptions(APIView):
    @swagger_auto_schema(
        responses={
            # status.HTTP_200_OK: Serializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def get(self, request):
        # TODO
        return None

    @swagger_auto_schema(
        # request_body=CreateVnfReqSerializer(),
        responses={
            #     status.HTTP_201_CREATED: CreateVnfRespSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def post(self, request):
        # TODO
        return None


class vnfpkg_subscription(APIView):
    @swagger_auto_schema(
        responses={
            # status.HTTP_200_OK: Serializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def get(self, request):
        # TODO
        return None

    @swagger_auto_schema(
        # request_body=CreateVnfReqSerializer(),
        responses={
            #     status.HTTP_201_CREATED: CreateVnfRespSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def post(self, request):
        # TODO
        return None
