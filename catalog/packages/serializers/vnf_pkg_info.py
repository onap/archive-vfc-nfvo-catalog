# Copyright 2018 ZTE Corporation.
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
from checksum import ChecksumSerializer
from vnf_pkg_software_image_info import VnfPackageSoftwareImageInfoSerializer
from vnf_pkg_artifact_info import VnfPackageArtifactInfoSerializer
from link import LinkSerializer


class _LinkSerializer(serializers.Serializer):
    self = LinkSerializer(
        help_text='URI of this resource.',
        required=True,
        allow_null=False
    )
    vnfd = LinkSerializer(
        help_text='Link to the VNFD resource.',
        required=False,
        allow_null=False
    )
    packageContent = LinkSerializer(
        help_text='Link to the "VNF package content resource.',
        required=True,
        allow_null=False
    )

    class Meta:
        ref_name = 'VNF_PKGM_Link_Serializer'


class VnfPkgInfoSerializer(serializers.Serializer):
    id = serializers.CharField(
        help_text="Identifier of the on-boarded VNF package.",
        required=True,
        allow_null=False,
        allow_blank=False
    )
    vnfdId = serializers.CharField(
        help_text="This identifier, which is managed by the VNF provider, "
        "identifies the VNF package and the VNFD in a globally unique way.",
        required=False,
        allow_null=True,
        allow_blank=True
    )
    vnfProvider = serializers.CharField(
        help_text="Provider of the VNF package and the VNFD.",
        required=False,
        allow_null=True,
        allow_blank=True
    )
    vnfProductName = serializers.CharField(
        help_text="Name to identify the VNF product.",
        required=False,
        allow_null=True,
        allow_blank=True
    )
    vnfSoftwareVersion = serializers.CharField(
        help_text="Software version of the VNF.",
        required=False,
        allow_null=True,
        allow_blank=True
    )
    vnfdVersion = serializers.CharField(
        help_text="The version of the VNvFD.",
        required=False,
        allow_null=True,
        allow_blank=True
    )
    checksum = ChecksumSerializer(
        help_text="Checksum of the on-boarded VNF package.",
        required=False,
        allow_null=True
    )
    softwareImages = VnfPackageSoftwareImageInfoSerializer(
        help_text="Information about VNF package artifacts that are software images.",
        required=False,
        allow_null=True,
        many=True
    )
    additionalArtifacts = VnfPackageArtifactInfoSerializer(
        help_text="Information about VNF package artifacts contained in "
        "the VNF package that are not software images.",
        required=False,
        allow_null=True,
        many=True
    )
    onboardingState = serializers.ChoiceField(
        help_text="On-boarding state of the VNF package.",
        choices=["CREATED", "UPLOADING", "PROCESSING", "ONBOARDED"],
        required=True,
        allow_null=True
    )
    operationalState = serializers.ChoiceField(
        help_text="Operational state of the VNF package.",
        choices=["ENABLED", "DISABLED"],
        required=True,
        allow_null=True
    )
    usageState = serializers.ChoiceField(
        help_text="Usage state of the VNF package.",
        choices=["IN_USE", "NOT_IN_USE"],
        required=True,
        allow_null=True
    )
    userDefinedData = serializers.DictField(
        help_text="User defined data for the VNF package.",
        child=serializers.CharField(help_text="KeyValue Pairs", allow_blank=True),
        required=False,
        allow_null=True
    )
    _links = _LinkSerializer(
        help_text='Links to resources related to this resource.',
        required=True,
        allow_null=True  # TODO supposed to be False
    )
