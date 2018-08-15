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

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView


class ns_descriptors(APIView):
    @swagger_auto_schema(
        responses={
            # status.HTTP_200_OK: Serializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def get(self, request):
        return request

    @swagger_auto_schema(
        # request_body=CreateVnfReqSerializer(),
        responses={
            #     status.HTTP_201_CREATED: CreateVnfRespSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def post(self, request):
        return request


class ns_info(APIView):
    @swagger_auto_schema(
        responses={
            # status.HTTP_200_OK: Serializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def get(self, request):
        return request

    @swagger_auto_schema(
        # request_body=CreateVnfReqSerializer(),
        responses={
            #     status.HTTP_201_CREATED: CreateVnfRespSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def post(self, request):
        return request


class nsd_content(APIView):
    @swagger_auto_schema(
        responses={
            # status.HTTP_200_OK: Serializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def get(self, request):
        return request

    @swagger_auto_schema(
        # request_body=CreateVnfReqSerializer(),
        responses={
            #     status.HTTP_201_CREATED: CreateVnfRespSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def post(self, request):
        return request


class pnf_descriptors(APIView):
    @swagger_auto_schema(
        responses={
            # status.HTTP_200_OK: Serializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def get(self, request):
        return request

    @swagger_auto_schema(
        # request_body=CreateVnfReqSerializer(),
        responses={
            #     status.HTTP_201_CREATED: CreateVnfRespSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def post(self, request):
        return request


class pnfd_info(APIView):
    @swagger_auto_schema(
        responses={
            # status.HTTP_200_OK: Serializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def get(self, request):
        return request

    @swagger_auto_schema(
        # request_body=CreateVnfReqSerializer(),
        responses={
            #     status.HTTP_201_CREATED: CreateVnfRespSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def post(self, request):
        return request


class pnfd_content(APIView):
    @swagger_auto_schema(
        responses={
            # status.HTTP_200_OK: Serializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def get(self, request):
        return request

    @swagger_auto_schema(
        # request_body=CreateVnfReqSerializer(),
        responses={
            #     status.HTTP_201_CREATED: CreateVnfRespSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def post(self, request):
        return request


class nsd_subscriptions(APIView):
    @swagger_auto_schema(
        responses={
            # status.HTTP_200_OK: Serializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def get(self, request):
        return request

    @swagger_auto_schema(
        # request_body=CreateVnfReqSerializer(),
        responses={
            #     status.HTTP_201_CREATED: CreateVnfRespSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def post(self, request):
        return request


class nsd_subscription(APIView):
    @swagger_auto_schema(
        responses={
            # status.HTTP_200_OK: Serializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def get(self, request):
        return request

    @swagger_auto_schema(
        # request_body=CreateVnfReqSerializer(),
        responses={
            #     status.HTTP_201_CREATED: CreateVnfRespSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def post(self, request):
        return request
