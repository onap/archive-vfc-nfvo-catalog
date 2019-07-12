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

from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from catalog.packages.serializers.nsdm_filter_data import NsdmNotificationsFilter
from catalog.packages.serializers.nsdm_subscription import NsdmSubscriptionsSerializer
from catalog.packages.serializers.nsdm_subscription import NsdmSubscriptionIdSerializer
from catalog.packages.serializers.nsdm_subscription import NsdmSubscriptionSerializer
from catalog.packages.serializers.nsdm_subscription import NsdmSubscriptionRequestSerializer
from catalog.packages.serializers.response import ProblemDetailsSerializer

from catalog.pub.exceptions import NsdmBadRequestException
from catalog.packages.biz.nsdm_subscription import NsdmSubscription
from .common import view_safe_call_with_log

logger = logging.getLogger(__name__)


def validate_data(data, serializer):
    serialized_data = serializer(data=data)
    if not serialized_data.is_valid():
        logger.error('Data validation failed.')
        raise NsdmBadRequestException(serialized_data.errors)
    return serialized_data


@swagger_auto_schema(
    method='POST',
    operation_description="Create Subscription for NSD Management",
    request_body=NsdmSubscriptionRequestSerializer(),
    responses={
        status.HTTP_201_CREATED: NsdmSubscriptionSerializer,
        status.HTTP_303_SEE_OTHER: ProblemDetailsSerializer(),
        status.HTTP_400_BAD_REQUEST: ProblemDetailsSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: ProblemDetailsSerializer()
    }
)
@swagger_auto_schema(
    method='GET',
    operation_description="Query subscriptions for Nsd Management",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: NsdmSubscriptionsSerializer(),
        status.HTTP_400_BAD_REQUEST: ProblemDetailsSerializer(),
        status.HTTP_404_NOT_FOUND: ProblemDetailsSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: ProblemDetailsSerializer(),
    }
)
@api_view(http_method_names=['POST', 'GET'])
@view_safe_call_with_log(logger=logger)
def nsd_subscription_rc(request):
    if request.method == 'POST':
        logger.debug("SubscribeNotification--post::> %s" % request.data)
        nsdm_subscription_request = \
            validate_data(request.data,
                          NsdmSubscriptionRequestSerializer)
        subscription = NsdmSubscription().create(
            nsdm_subscription_request.data)
        validate_data(subscription, NsdmSubscriptionSerializer)
        return Response(data=subscription, status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        logger.debug("Subscription Notification GET %s" % request.query_params)
        request_query_params = {}
        if request.query_params:
            request_query_params = \
                validate_data(request.query_params,
                              NsdmNotificationsFilter).data
        subscription_data = \
            NsdmSubscription().query_multi_subscriptions(
                request_query_params)
        subscriptions = validate_data(subscription_data,
                                      NsdmSubscriptionsSerializer)
        return Response(data=subscriptions.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='GET',
    operation_description="Query subscriptions for Nsd Management",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: NsdmSubscriptionSerializer(),
        status.HTTP_400_BAD_REQUEST: ProblemDetailsSerializer(),
        status.HTTP_404_NOT_FOUND: ProblemDetailsSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: ProblemDetailsSerializer()
    }
)
@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete subscription for Nsd Management",
    request_body=no_body,
    responses={
        status.HTTP_204_NO_CONTENT: 'No_Content',
        status.HTTP_400_BAD_REQUEST: ProblemDetailsSerializer(),
        status.HTTP_404_NOT_FOUND: ProblemDetailsSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: ProblemDetailsSerializer()
    }
)
@api_view(http_method_names=['GET', 'DELETE'])
@view_safe_call_with_log(logger=logger)
def nsd_subscription_rd(request, **kwargs):
    subscription_id = kwargs.get("subscriptionId")
    validate_data({'subscription_id': subscription_id}, NsdmSubscriptionIdSerializer)
    if request.method == 'GET':
        subscription_data = NsdmSubscription().query_single_subscription(subscription_id)
        subscription = validate_data(subscription_data, NsdmSubscriptionSerializer)
        return Response(data=subscription.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        subscription_data = NsdmSubscription().delete_single_subscription(subscription_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
