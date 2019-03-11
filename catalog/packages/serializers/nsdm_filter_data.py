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

from catalog.packages.const import NSDM_NOTIFICATION_TYPES


class NsdmNotificationsFilter(serializers.Serializer):
    notificationTypes = serializers.ListField(
        child=serializers.ChoiceField(
            required=True,
            choices=NSDM_NOTIFICATION_TYPES),
        help_text="Match particular notification types",
        allow_null=False,
        required=False)
    nsdInfoId = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="Match NS packages with particular nsdInfoIds",
        allow_null=False,
        required=False)
    nsdId = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="Match NS Packages with particular nsdIds",
        allow_null=False,
        required=False)
    nsdName = serializers.ListField(
        child=serializers.CharField(max_length=255, required=True),
        help_text="Match NS Packages with particular nsdNames",
        allow_null=False,
        required=False)
    nsdVersion = serializers.ListField(
        child=serializers.CharField(max_length=255, required=True),
        help_text="match NS packages that belong to certain nsdversion",
        required=False,
        allow_null=False)
    nsdInvariantId = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="Match NS Packages with particular nsdInvariantIds",
        allow_null=False,
        required=False)
    vnfPkgIds = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="Match NS Packages that has VNF PackageIds",
        allow_null=False,
        required=False)
    nestedNsdInfoIds = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="Match NS Packages with particular nsdInvariantIds",
        allow_null=False,
        required=False)
    nsdOnboardingState = serializers.ListField(
        child=serializers.ChoiceField(required=True,
                                      choices=['CREATED', 'UPLOADING',
                                               'PROCESSING', 'ONBOARDED']),
        help_text="Match NS Packages with particular NS Onboarding State",
        allow_null=False,
        required=False)
    nsdOperationalState = serializers.ListField(
        child=serializers.ChoiceField(required=True,
                                      choices=['ENABLED', 'DISABLED']),
        help_text="Match NS Packages with particular NS Operational State",
        allow_null=False,
        required=False)
    nsdUsageState = serializers.ListField(
        child=serializers.ChoiceField(required=True,
                                      choices=['IN_USE', 'NOT_IN_USE']),
        help_text="Match NS Packages with particular NS Usage State",
        allow_null=False,
        required=False)
    pnfdInfoIds = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="Match PF packages with particular pnfdInfoIds",
        allow_null=False,
        required=False)
    pnfdId = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="Match PF packages with particular pnfdInfoIds",
        allow_null=False,
        required=False)
    pnfdName = serializers.ListField(
        child=serializers.CharField(max_length=255, required=True),
        help_text="Match PF Packages with particular pnfdNames",
        allow_null=False,
        required=False)
    pnfdVersion = serializers.ListField(
        child=serializers.CharField(max_length=255, required=True),
        help_text="match PF packages that belong to certain pnfd version",
        required=False,
        allow_null=False)
    pnfdProvider = serializers.ListField(
        child=serializers.CharField(max_length=255, required=True),
        help_text="Match PF Packages with particular pnfdProvider",
        allow_null=False,
        required=False)
    pnfdInvariantId = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="Match PF Packages with particular pnfdInvariantIds",
        allow_null=False,
        required=False)
    pnfdOnboardingState = serializers.ListField(
        child=serializers.ChoiceField(required=True,
                                      choices=['CREATED', 'UPLOADING',
                                               'PROCESSING', 'ONBOARDED']),
        help_text="Match PF Packages with particular PNF Onboarding State ",
        allow_null=False,
        required=False)
    pnfdUsageState = serializers.ListField(
        child=serializers.ChoiceField(
            required=True, choices=['IN_USE', 'NOT_IN_USE']),
        help_text="Match PF Packages with particular PNF usage State",
        allow_null=False,
        required=False)
