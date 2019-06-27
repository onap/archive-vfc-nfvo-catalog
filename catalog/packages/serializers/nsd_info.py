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
from .problem_details import ProblemDetailsSerializer
from .link import LinkSerializer


class _LinkSerializer(serializers.Serializer):
    self = LinkSerializer(
        help_text="URI of this resource.",
        required=True,
        allow_null=False
    )
    nsd_content = LinkSerializer(
        help_text="Link to the NSD content resource.",
        required=True,
        allow_null=False
    )

    class Meta:
        ref_name = "NSD_LinkSerializer"


class NsdInfoSerializer(serializers.Serializer):
    id = serializers.CharField(
        help_text="Identifier of the onboarded individual NS descriptor resource."
        "This identifier is allocated by the NFVO.",
        required=True,
        allow_null=False,
        allow_blank=False
    )
    nsdId = serializers.CharField(
        help_text="This identifier, which is allocated by the NSD designer,"
        "identifies the NSD in a globally unique way."
        "It is copied from the NSD content and shall be present after the "
        "NSD content is on-boarded.",
        required=False,
        allow_null=True,
        allow_blank=True
    )
    nsdName = serializers.CharField(
        help_text="Name of the onboarded NSD."
        "This information is copied from the NSD content and shall be present "
        "after the NSD content is on-boarded.",
        required=False,
        allow_null=True,
        allow_blank=True
    )
    nsdVersion = serializers.CharField(  # TODO: data type is version
        help_text="Version of the on-boarded NSD."
        "This information is copied from the NSD content and shall be "
        "present after the NSD content is on-boarded.",
        required=False,
        allow_null=True,
        allow_blank=True
    )
    nsdDesigner = serializers.CharField(
        help_text="Designer of the on-boarded NSD."
        "This information is copied from the NSD content and shall be "
        "present after the NSD content is on-boarded.",
        required=False,
        allow_null=True,
        allow_blank=True
    )
    nsdInvariantId = serializers.CharField(
        help_text="This identifier, which is allocated by the NSD designer,"
        "identifies an NSD in a version independent manner."
        "This information is copied from the NSD content and shall be "
        "present after the NSD content is on-boarded.",
        required=False,
        allow_null=True,
        allow_blank=True
    )
    vnfPkgIds = serializers.ListSerializer(
        help_text="Identifies the VNF package for the VNFD referenced "
        "by the on-boarded NS descriptor resource.",
        child=serializers.CharField(
            help_text="Identifier of the VNF package",
            allow_blank=True
        ),
        required=False,
        allow_null=True,
        allow_empty=True
    )
    pnfdInfoIds = serializers.ListSerializer(
        help_text="Identifies the PnfdInfo element for the PNFD referenced "
        "by the on-boarded NS descriptor resource.",
        child=serializers.CharField(
            help_text="Identifier of the PnfdInfo element",
            allow_blank=True
        ),
        required=False,
        allow_null=True,
        allow_empty=True
    )
    nestedNsdInfoIds = serializers.ListSerializer(
        help_text="Identifies the NsdInfo element for the nested NSD referenced "
        "by the on-boarded NS descriptor resource.",
        child=serializers.CharField(
            help_text="Identifier of the NsdInfo element",
            allow_blank=True
        ),
        required=False,
        allow_null=True,
        allow_empty=True
    )
    nsdOnboardingState = serializers.ChoiceField(
        help_text="Onboarding state of the individual NS descriptor resource.",
        choices=["CREATED", "UPLOADING", "PROCESSING", "ONBOARDED"],
        required=True,
        allow_null=False,
        allow_blank=False
    )
    onboardingFailureDetails = ProblemDetailsSerializer(
        help_text="Failure details of current onboarding procedure."
        "It shall be present when the nsdOnboardingState attribute is CREATED "
        "and the uploading or processing fails in NFVO.",
        required=False,
        allow_null=True,
    )
    nsdOperationalState = serializers.ChoiceField(
        help_text="Operational state of the individual NS descriptor resource."
        "This attribute can be modified with the PATCH method.",
        choices=["ENABLED", "DISABLED"],
        required=True,
        allow_null=False,
        allow_blank=False
    )
    nsdUsageState = serializers.ChoiceField(
        help_text="Usage state of the individual NS descriptor resource.",
        choices=["IN_USE", "NOT_IN_USE"],
        required=True,
        allow_null=False,
    )
    userDefinedData = serializers.DictField(
        help_text="User defined data for the individual NS descriptor resource."
        "This attribute can be modified with the PATCH method.",
        child=serializers.CharField(
            help_text="Key Value Pairs",
            allow_blank=True
        ),
        required=False,
        allow_null=True
    )
    _links = _LinkSerializer(
        help_text="Links to resources related to this resource.",
        required=True,
        allow_null=True  # TODO: supposed to be False
    )
