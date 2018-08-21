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


class CreatePnfdInfoRequestSerializer(serializers.Serializer):
    userDefinedData = serializers.DictField(
        help_text='User-defined data for the PNF descriptor resource to be created. \
        It shall be present when the user defined data is set for the individual PNF descriptor resource to be created.',
        child=serializers.CharField(help_text='Key Value Pairs', allow_blank=True),
        required=False,
        allow_null=True
    )
