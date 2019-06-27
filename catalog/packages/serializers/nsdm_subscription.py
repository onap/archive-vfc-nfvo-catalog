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

from rest_framework import serializers

from .link import LinkSerializer
from .subscription_auth_data import SubscriptionAuthenticationSerializer
from .nsdm_filter_data import NsdmNotificationsFilter


class NsdmSubscriptionLinkSerializer(serializers.Serializer):
    self = LinkSerializer(
        help_text="Links to resources related to this resource.",
        required=True
    )


class NsdmSubscriptionSerializer(serializers.Serializer):
    id = serializers.CharField(
        help_text="Identifier of this subscription resource.",
        max_length=255,
        required=True,
        allow_null=False
    )
    callbackUri = serializers.CharField(
        help_text="The URI of the endpoint to send the notification to.",
        max_length=255,
        required=True,
        allow_null=False
    )
    filter = NsdmNotificationsFilter(
        help_text="Filter settings for this subscription, to define the "
        "of all notifications this subscription relates to.",
        required=False
    )
    _links = NsdmSubscriptionLinkSerializer(
        help_text="Links to resources related to this resource.",
        required=True
    )


class NsdmSubscriptionsSerializer(serializers.ListSerializer):
    child = NsdmSubscriptionSerializer()


class NsdmSubscriptionIdSerializer(serializers.Serializer):
    subscription_id = serializers.UUIDField(
        help_text="Identifier of this subscription resource.",
        required=True,
        allow_null=False
    )


class NsdmSubscriptionRequestSerializer(serializers.Serializer):
    callbackUri = serializers.CharField(
        help_text="The URI of the endpoint to send the notification to.",
        required=True,
        allow_null=False
    )
    filter = NsdmNotificationsFilter(
        help_text="Filter settings for the subscription,"
                  " to define the subset of all "
                  "notifications this subscription relates to.",
        required=False,
        allow_null=True
    )
    authentication = SubscriptionAuthenticationSerializer(
        help_text="Authentication parameters to configure"
                  " the use of Authorization when sending "
                  "notifications corresponding to this subscription.",
        required=False,
        allow_null=True
    )
