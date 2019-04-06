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


class VnfPackageArtifactInfoSerializer(serializers.Serializer):
    artifactPath = serializers.CharField(
        help_text="Path in the VNF package.",
        required=True,
        allow_null=False,
        allow_blank=False
    )
    checksum = ChecksumSerializer(
        help_text="Checksum of the artifact file.",
        required=True,
        allow_null=False
    )
    metadata = serializers.DictField(
        help_text="The metadata of the artifact that are available in the VNF package",
        child=serializers.CharField(
            help_text="KeyValue Pairs",
            allow_blank=True
        ),
        required=False,
        allow_null=True
    )
