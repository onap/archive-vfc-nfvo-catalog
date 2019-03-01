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


import traceback
import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from catalog.packages.serializers.vnf_pkg_subscription import PkgmSubscriptionRequestSerializer, \
    PkgmSubscriptionSerializer, PkgmSubscriptionsSerializer
from catalog.packages.serializers.response import ProblemDetailsSerializer
from catalog.packages.biz.vnf_pkg_subscription import CreateSubscription
from catalog.packages.views.common import validate_data
from catalog.pub.exceptions import VnfPkgDuplicateSubscriptionException, VnfPkgSubscriptionException

logger = logging.getLogger(__name__)
VALID_FILTERS = ["callbackUri", "notificationTypes", "vnfdId", "vnfPkgId", "operationalState", "usageState"]


def get_problem_details_serializer(status_code, error_message):
    problem_details = {
        "status": status_code,
        "detail": error_message
    }
    problem_details_serializer = ProblemDetailsSerializer(data=problem_details)
    problem_details_serializer.is_valid()
    return problem_details_serializer


class SubscriptionsView(APIView):

    @swagger_auto_schema(
        request_body=PkgmSubscriptionRequestSerializer,
        responses={
            status.HTTP_201_CREATED: PkgmSubscriptionSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
        }
    )
    def post(self, request):
        logger.debug("Create VNF package Subscription> %s" % request.data)
        try:
            vnf_pkg_subscription_request = validate_data(request.data, PkgmSubscriptionRequestSerializer)
            data = CreateSubscription(vnf_pkg_subscription_request.data).do_biz()
            subscription_info = validate_data(data, PkgmSubscriptionSerializer)
            return Response(data=subscription_info.data, status=status.HTTP_201_CREATED)
        except VnfPkgDuplicateSubscriptionException as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_data = {'error': e.message}
            problem_details_serializer = get_problem_details_serializer(status.HTTP_303_SEE_OTHER,
                                                                        traceback.format_exc())
            return Response(data=problem_details_serializer.data, status=status.HTTP_303_SEE_OTHER)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            problem_details_serializer = get_problem_details_serializer(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                                        traceback.format_exc())
            return Response(data=problem_details_serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: PkgmSubscriptionSerializer(),
            status.HTTP_400_BAD_REQUEST: ProblemDetailsSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: ProblemDetailsSerializer()
        }
    )
    def get(self, request):
        logger.debug("SubscribeNotification--get::> %s" % request.query_params)
        try:
            if request.query_params and not set(request.query_params).issubset(set(VALID_FILTERS)):
                problem_details_serializer = get_problem_details_serializer(status.HTTP_400_BAD_REQUEST,
                                                                            "Not a valid filter")
                return Response(data=problem_details_serializer.data, status=status.HTTP_400_BAD_REQUEST)
            resp_data = QuerySubscription(request.query_params).query_multi_subscriptions()

            subscriptions_serializer = PkgmSubscriptionsSerializer(data=resp_data)
            if not subscriptions_serializer.is_valid():
                raise VnfPkgSubscriptionException(subscriptions_serializer.errors)

            logger.debug("SubscribeNotification--get::> Remove default fields if exclude_default" +
                         " is specified")
            return Response(data=subscriptions_serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            problem_details_serializer = get_problem_details_serializer(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                                        traceback.format_exc())
            return Response(data=problem_details_serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
