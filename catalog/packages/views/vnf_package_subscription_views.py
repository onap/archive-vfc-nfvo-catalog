# Copyright (C) 2019 Verizon. All Rights Reserved
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

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from catalog.packages.serializers.vnf_pkg_subscription import PkgmSubscriptionRequestSerializer
from catalog.packages.serializers.vnf_pkg_subscription import PkgmSubscriptionSerializer
from catalog.packages.serializers.vnf_pkg_subscription import PkgmSubscriptionsSerializer
from catalog.packages.serializers.response import ProblemDetailsSerializer
from catalog.packages.biz.vnf_pkg_subscription import CreateSubscription
from catalog.packages.biz.vnf_pkg_subscription import QuerySubscription
from catalog.packages.biz.vnf_pkg_subscription import TerminateSubscription
from catalog.packages.views.common import validate_data
from catalog.pub.exceptions import VnfPkgSubscriptionException
from catalog.pub.exceptions import BadRequestException
from .common import view_safe_call_with_log

logger = logging.getLogger(__name__)

VALID_FILTERS = [
    "callbackUri",
    "notificationTypes",
    "vnfdId",
    "vnfPkgId",
    "operationalState",
    "usageState"
]


class CreateQuerySubscriptionView(APIView):

    @swagger_auto_schema(
        request_body=PkgmSubscriptionRequestSerializer,
        responses={
            status.HTTP_201_CREATED: PkgmSubscriptionSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    @view_safe_call_with_log(logger=logger)
    def post(self, request):
        logger.debug("Create VNF package Subscription> %s" % request.data)

        vnf_pkg_subscription_request = validate_data(request.data, PkgmSubscriptionRequestSerializer)
        data = CreateSubscription(vnf_pkg_subscription_request.data).do_biz()
        subscription_info = validate_data(data, PkgmSubscriptionSerializer)
        return Response(data=subscription_info.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: PkgmSubscriptionSerializer(),
            status.HTTP_400_BAD_REQUEST: ProblemDetailsSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: ProblemDetailsSerializer()
        }
    )
    @view_safe_call_with_log(logger=logger)
    def get(self, request):
        logger.debug("SubscribeNotification--get::> %s" % request.query_params)

        if request.query_params and not set(request.query_params).issubset(set(VALID_FILTERS)):
            raise BadRequestException("Not a valid filter")

        resp_data = QuerySubscription().query_multi_subscriptions(request.query_params)

        subscriptions_serializer = PkgmSubscriptionsSerializer(data=resp_data)
        if not subscriptions_serializer.is_valid():
            raise VnfPkgSubscriptionException(subscriptions_serializer.errors)

        return Response(data=subscriptions_serializer.data, status=status.HTTP_200_OK)


class QueryTerminateSubscriptionView(APIView):

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: PkgmSubscriptionSerializer(),
            status.HTTP_404_NOT_FOUND: ProblemDetailsSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: ProblemDetailsSerializer()
        }
    )
    @view_safe_call_with_log(logger=logger)
    def get(self, request, subscriptionId):
        logger.debug("SubscribeNotification--get::> %s" % subscriptionId)

        resp_data = QuerySubscription().query_single_subscription(subscriptionId)

        subscription_serializer = PkgmSubscriptionSerializer(data=resp_data)
        if not subscription_serializer.is_valid():
            raise VnfPkgSubscriptionException(subscription_serializer.errors)

        return Response(data=subscription_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: "",
            status.HTTP_404_NOT_FOUND: ProblemDetailsSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: ProblemDetailsSerializer()
        }
    )
    @view_safe_call_with_log(logger=logger)
    def delete(self, request, subscriptionId):
        logger.debug("SubscribeNotification--get::> %s" % subscriptionId)

        TerminateSubscription().terminate(subscriptionId)
        return Response(status=status.HTTP_204_NO_CONTENT)
