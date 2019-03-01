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

from catalog.packages.serializers import subscription_auth_data
from catalog.packages.serializers import vnf_pkg_notifications


class LinkSerializer(serializers.Serializer):
    href = serializers.CharField(
        help_text="URI of the referenced resource.",
        required=True,
        allow_null=False,
        allow_blank=False)

    class Meta:
        ref_name = 'VNF_SUBSCRIPTION_LINKSERIALIZER'


class LinkSelfSerializer(serializers.Serializer):
    self = LinkSerializer(
        help_text="URI of this resource.",
        required=True,
        allow_null=False)


class PkgmSubscriptionRequestSerializer(serializers.Serializer):
    filters = vnf_pkg_notifications.PkgmNotificationsFilter(
        help_text="Filter settings for this subscription, "
                  "to define the subset of all notifications"
                  " this subscription relates to",
        required=False,
        allow_null=False
    )
    callbackUri = serializers.URLField(
        help_text="Callback URI to send"
                  "the notification",
        required=True,
        allow_null=False)
    authentication = subscription_auth_data.SubscriptionAuthenticationSerializer(
        help_text="Authentication parameters to configure the use of "
                  "authorization when sending notifications corresponding to"
                  "this subscription",
        required=False,
        allow_null=False
    )


class PkgmSubscriptionSerializer(serializers.Serializer):
    id = serializers.UUIDField(
        help_text="Identifier of this subscription resource.",
        required=True,
        allow_null=False)
    callbackUri = serializers.URLField(
        help_text="The URI of the endpoint to send the notification to.",
        required=True,
        allow_null=False)

    _links = LinkSelfSerializer(
        help_text="Links to resources related to this resource.",
        required=True,
        allow_null=False)

    filter = vnf_pkg_notifications.PkgmNotificationsFilter(
        help_text="Filter settings for this subscription, "
                  "to define the subset of all notifications"
                  " this subscription relates to",
        required=False,
        allow_null=False
    )


class PkgmSubscriptionsSerializer(serializers.ListSerializer):
    child = PkgmSubscriptionSerializer()
    allow_empty = True
