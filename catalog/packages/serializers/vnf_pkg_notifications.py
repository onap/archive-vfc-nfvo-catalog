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

from catalog.packages.const import NOTIFICATION_TYPES

PackageOperationalStateType = ["ENABLED", "DISABLED"]
PackageUsageStateType = ["IN_USE", "NOT_IN_USE"]


class VersionSerializer(serializers.Serializer):
    vnfSoftwareVersion = serializers.CharField(
        help_text="VNF software version to match.",
        max_length=255,
        required=True,
        allow_null=False
    )
    vnfdVersions = serializers.ListField(
        child=serializers.CharField(),
        help_text="Match VNF packages that contain "
                  "VNF products with certain VNFD versions",
        required=False,
        allow_null=False
    )


class vnfProductsSerializer(serializers.Serializer):
    vnfProductName = serializers.CharField(
        help_text="Name of the VNF product to match.",
        max_length=255,
        required=True,
        allow_null=False
    )
    versions = VersionSerializer(
        help_text="match VNF packages that contain "
                  "VNF products with certain versions",
        required=False,
        allow_null=False
    )


class vnfProductsProvidersSerializer(serializers.Serializer):
    vnfProvider = serializers.CharField(
        help_text="Name of the VNFprovider to match.",
        max_length=255,
        required=True,
        allow_null=False
    )
    vnfProducts = vnfProductsSerializer(
        help_text="match VNF packages that contain "
                  "VNF products with certain product names, "
                  "from one particular provider",
        required=False,
        allow_null=False
    )


class PkgmNotificationsFilter(serializers.Serializer):
    notificationTypes = serializers.ListField(
        child=serializers.ChoiceField(
            required=True,
            choices=NOTIFICATION_TYPES
        ),
        help_text="Match particular notification types",
        allow_null=False,
        required=False
    )
    vnfProductsFromProviders = vnfProductsProvidersSerializer(
        help_text="Match VNF packages that contain "
                  "VNF products from certain providers.",
        allow_null=False,
        required=False
    )
    vnfdId = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="Match VNF packages with a VNFD identifier"
                  "listed in the attribute",
        required=False,
        allow_null=False
    )
    vnfPkgId = serializers.ListField(
        child=serializers.UUIDField(),
        help_text="Match VNF packages with a VNFD identifier"
                  "listed in the attribute",
        required=False,
        allow_null=False
    )
    operationalState = serializers.ListField(
        child=serializers.ChoiceField(
            required=True,
            choices=PackageOperationalStateType
        ),
        help_text="Operational state of the VNF package.",
        allow_null=False,
        required=False
    )
    usageState = serializers.ListField(
        child=serializers.ChoiceField(
            required=True,
            choices=PackageUsageStateType
        ),
        help_text="Operational state of the VNF package.",
        allow_null=False,
        required=False
    )
