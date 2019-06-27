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
        help_text='URI of this resource.',
        required=True,
        allow_null=False
    )
    pnfd_content = LinkSerializer(
        help_text='Link to the PNFD content resource.',
        required=True,
        allow_null=False
    )


class PnfdInfoSerializer(serializers.Serializer):
    id = serializers.CharField(
        help_text='Identifier of the onboarded individual PNF descriptor resource. \
        This identifier is allocated by the NFVO.',
        required=True,
        allow_null=False,
        allow_blank=False
    )
    pnfdId = serializers.CharField(
        help_text='This identifier, which is allocated by the PNFD designer, \
        identifies the PNFD in a globally unique way. \
        It is copied from the PNFD content and shall be present after the PNFD content is on-boarded.',
        required=False,
        allow_null=True,
        allow_blank=True
    )
    pnfdName = serializers.CharField(
        help_text='Name of the onboarded PNFD. \
        This information is copied from the PNFD content and shall be present after the PNFD content is on-boarded.',
        required=False,
        allow_null=True,
        allow_blank=True
    )
    pnfdVersion = serializers.CharField(  # TODO: data type is version
        help_text='Version of the on-boarded PNFD. \
        This information is copied from the PNFD content and shall be present after the PNFD content is on-boarded.',
        required=False,
        allow_null=True,
        allow_blank=True
    )
    pnfdProvider = serializers.CharField(
        help_text='Provider of the on-boarded PNFD. \
        This information is copied from the PNFD content and shall be present after the PNFD content is on-boarded.',
        required=False,
        allow_null=True,
        allow_blank=True
    )
    pnfdInvariantId = serializers.CharField(
        help_text='Identifies a PNFD in a version independent manner. \
        This attribute is invariant across versions of PNFD.',
        required=False,
        allow_null=True,
        allow_blank=True
    )
    pnfdOnboardingState = serializers.ChoiceField(
        help_text='Onboarding state of the individual PNF descriptor resource.',
        choices=['CREATED', 'UPLOADING', 'PROCESSING', 'ONBOARDED'],
        required=True,
        allow_null=False,
        allow_blank=False
    )
    onboardingFailureDetails = ProblemDetailsSerializer(
        help_text='Failure details of current onboarding procedure. \
        It shall be present when the "pnfdOnboardingState" attribute is CREATED and the uploading or processing fails in NFVO.',
        required=False,
        allow_null=True,
    )
    pnfdUsageState = serializers.ChoiceField(
        help_text='Usage state of the individual PNF descriptor resource.',
        choices=['IN_USE', 'NOT_IN_USE'],
        required=True,
        allow_null=False,
    )
    userDefinedData = serializers.DictField(
        help_text='User defined data for the individual PNF descriptor resource. \
        This attribute can be modified with the PATCH method.',
        child=serializers.CharField(help_text='Key Value Pairs', allow_blank=True),
        required=False,
        allow_null=True
    )
    _links = _LinkSerializer(
        help_text='Links to resources related to this resource.',
        required=True,
        allow_null=True  # TODO: supposed to be False
    )
