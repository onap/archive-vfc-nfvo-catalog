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

from catalog.pub.utils.toscaparser.nsdmodel import EtsiNsdInfoModel
from catalog.pub.utils.toscaparser.vnfdmodel import EtsiVnfdInfoModel


class JobResponseSerializer(serializers.Serializer):
    progress = serializers.CharField(help_text="Job Progress", required=False)
    desc = serializers.CharField(help_text="Description", required=False)
    errcode = serializers.CharField(help_text="Error Code", required=False)


class JobResponseHistoryListSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="Status", required=False)
    progress = serializers.CharField(help_text="Job Progress", required=False)
    statusDescription = serializers.CharField(
        help_text="Status Description", required=False)
    errorCode = serializers.CharField(help_text="Error Code", required=False)
    responseId = serializers.CharField(help_text="Response Id", required=False)


class JobResponseDescriptorSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="Status", required=False)
    progress = serializers.CharField(help_text="Job Progress", required=False)
    statusDescription = serializers.CharField(
        help_text="Status Description", required=False)
    errorCode = serializers.CharField(help_text="Error Code", required=False)
    responseId = serializers.CharField(help_text="Response Id", required=False)
    responseHistoryList = JobResponseHistoryListSerializer(
        many=True, help_text="Response History List", required=False)


class JobRequestSerializer(serializers.Serializer):
    jobId = serializers.CharField(
        help_text="Job Id",
        required=False)
    responseDescriptor = JobResponseDescriptorSerializer(
        help_text="Job Response Descriptor", required=False)


class PostJobResponseResultSerializer(serializers.Serializer):
    result = serializers.CharField(help_text="Result", required=True)
    msg = serializers.CharField(help_text="Message", required=False)


class NsPackageDistributeRequestSerializer(serializers.Serializer):
    csarId = serializers.CharField(help_text="csarId", required=True)


class NsPackageInfoSerializer(serializers.Serializer):
    nsdId = serializers.CharField(help_text="NSD ID", required=True)
    nsPackageId = serializers.CharField(
        help_text="NS Package ID", required=True)
    nsdProvider = serializers.CharField(
        help_text="NSD Provider", required=True)
    nsdVersion = serializers.CharField(help_text="NSD Version", required=True)
    csarName = serializers.CharField(help_text="CSAR name", required=True)
    nsdModel = serializers.CharField(help_text="NSD Model", required=True)
    downloadUrl = serializers.CharField(
        help_text="URL to download NSD Model", required=True)


class NsPackageSerializer(serializers.Serializer):
    csarId = serializers.CharField(help_text="CSAR ID", required=True)
    package_info = NsPackageInfoSerializer(
        help_text="NS Package Info", required=True)


class NsPackagesSerializer(serializers.ListSerializer):
    child = NsPackageSerializer(many=True)


class NfPackageDistributeRequestSerializer(serializers.Serializer):
    csar_id = serializers.CharField(help_text="CSAR ID", required=True)
    vim_ids = serializers.ListField(
        help_text="vim_ids",
        child=serializers.CharField(),
        required=False)
    lab_vim_id = serializers.CharField(
        help_text="A list of VIM IDs.", required=False)


class NfPackageInfoSerializer(serializers.Serializer):
    vnfdId = serializers.CharField(help_text="VNFD ID", required=True)
    vnfPackageId = serializers.CharField(
        help_text="VNF Package ID", required=True)
    vnfdProvider = serializers.CharField(
        help_text="VNFD Provider", required=True)
    vnfdVersion = serializers.CharField(
        help_text="VNFD Version", required=True)
    vnfVersion = serializers.CharField(help_text="VNF Version", required=True)
    csarName = serializers.CharField(help_text="CSAR Name", required=True)
    vnfdModel = serializers.CharField(help_text="VNFD Model", required=True)
    downloadUrl = serializers.CharField(
        help_text="URL to download VNFD Model", required=True)


class NfImageInfoSerializer(serializers.Serializer):
    index = serializers.CharField(
        help_text="Index of VNF Image",
        required=True)
    fileName = serializers.CharField(
        help_text="Image file name", required=True)
    imageId = serializers.CharField(help_text="Image ID", required=True)
    vimId = serializers.CharField(help_text="VIM ID", required=True)
    vimUser = serializers.CharField(help_text="User of VIM", required=True)
    tenant = serializers.CharField(help_text="Tenant", required=True)
    status = serializers.CharField(help_text="Status", required=True)


class NfPackageSerializer(serializers.Serializer):
    csarId = serializers.CharField(help_text="CSAR ID", required=True)
    packageInfo = NfPackageInfoSerializer(
        help_text="VNF Package Info", required=True)
    imageInfo = NfImageInfoSerializer(help_text="Image Info", required=False)


class NfPackagesSerializer(serializers.ListSerializer):
    child = NfPackageSerializer(many=True)


class PostJobResponseSerializer(serializers.Serializer):
    jobId = serializers.CharField(help_text="jobId", required=True)


class ParseModelRequestSerializer(serializers.Serializer):
    csarId = serializers.CharField(help_text="CSAR ID", required=True)
    inputs = serializers.JSONField(help_text="Inputs", required=False)


class EtsiNsdInfoModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = EtsiNsdInfoModel


class EtsiVnfdInfoModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = EtsiVnfdInfoModel


class ParseNSPackageResponseSerializer(serializers.Serializer):
    model = EtsiNsdInfoModelSerializer(help_text="NSD Model", required=True)


class ParseNfPackageResponseSerializer(serializers.Serializer):
    model = EtsiVnfdInfoModelSerializer(help_text="VNFD Model", required=True)
