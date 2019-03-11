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

import ast
import json
import logging
import traceback

from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from catalog.packages.serializers.nsdm_subscription import \
    NsdmSubscriptionSerializer, \
    NsdmSubscriptionRequestSerializer, \
    NsdmSubscriptionIdSerializer, \
    NsdmSubscriptionsSerializer
from catalog.packages.serializers.response \
    import ProblemDetailsSerializer
from catalog.packages import const
from catalog.pub.exceptions import CatalogException, \
    ResourceNotFoundException, \
    NsdmBadRequestException, NsdmDuplicateSubscriptionException
from catalog.packages.biz.nsdm_subscription import NsdmSubscription


logger = logging.getLogger(__name__)


def validate_data(data, serializer):
    serialized_data = serializer(data=data)
    if not serialized_data.is_valid():
        logger.error('Data validation failed.')
        raise NsdmBadRequestException(serialized_data.errors)
    return serialized_data


def get_problem_details_serializer(title, status_code, error_message):
    problem_details = {
        "title": title,
        "status": status_code,
        "detail": error_message
    }
    problem_details_serializer = ProblemDetailsSerializer(data=problem_details)
    problem_details_serializer.is_valid()
    return problem_details_serializer


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
@api_view(http_method_names=['POST'])
def nsd_subscription_rc(request):
    if request.method == 'POST':
        logger.debug("SubscribeNotification--post::> %s" % request.data)
        try:
            title = 'Creating Subscription Failed!'
            nsdm_subscription_request = \
                validate_data(request.data,
                              NsdmSubscriptionRequestSerializer)
            subscription = NsdmSubscription().create(
                               nsdm_subscription_request.data)
            subscription_resp = validate_data(subscription,
                                              NsdmSubscriptionSerializer)
            return Response(data=subscription_resp.data,
                            status=status.HTTP_201_CREATED)
        except NsdmDuplicateSubscriptionException as e:
            logger.error(e.message)
            problem_details_serializer = \
                get_problem_details_serializer(title,
                                               status.HTTP_303_SEE_OTHER,
                                               e.message)
            return Response(data=problem_details_serializer.data,
                            status=status.HTTP_303_SEE_OTHER)
        except NsdmBadRequestException as e:
            problem_details_serializer = \
                get_problem_details_serializer(title,
                                               status.HTTP_400_BAD_REQUEST,
                                               e.message)
            return Response(data=problem_details_serializer.data,
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            problem_details_serializer = \
                get_problem_details_serializer(
                    title,
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    e.message)
            return Response(data=problem_details_serializer.data,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
