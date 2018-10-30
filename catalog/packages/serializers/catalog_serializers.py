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


class PostJobRequestSerializer(serializers.Serializer):
    progress = serializers.CharField(help_text="Job Progress", required=False)
    desc = serializers.CharField(help_text="Description", required=False)
    errcode = serializers.CharField(help_text="Error Code", required=False)


class JobResponseHistoryListSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="Status", required=False)
    progress = serializers.CharField(help_text="Job Progress", required=False)
    statusDescription = serializers.CharField(
        help_text="Status Description", required=False)
    errorCode = serializers.CharField(help_text="Error Code", required=False, allow_null=True)
    responseId = serializers.CharField(help_text="Response Id", required=False)


class JobResponseDescriptorSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="Status", required=False)
    progress = serializers.CharField(help_text="Job Progress", required=False)
    statusDescription = serializers.CharField(
        help_text="Status Description", required=False)
    errorCode = serializers.CharField(help_text="Error Code", required=False, allow_null=True)
    responseId = serializers.CharField(help_text="Response Id", required=False)
    responseHistoryList = JobResponseHistoryListSerializer(
        many=True, help_text="Response History List", required=False)


class GetJobResponseSerializer(serializers.Serializer):
    jobId = serializers.CharField(
        help_text="Job Id",
        required=False)
    responseDescriptor = JobResponseDescriptorSerializer(
        help_text="Job Response Descriptor", required=False)


class PostJobResponseResultSerializer(serializers.Serializer):
    result = serializers.CharField(help_text="Result", required=True)
    msg = serializers.CharField(help_text="Message", required=False)


class InternalErrorRequestSerializer(serializers.Serializer):
    error = serializers.CharField(help_text="Error", required=True)
    errorMessage = serializers.CharField(help_text="Error Message", required=False)


class NsPackageDistributeRequestSerializer(serializers.Serializer):
    csarId = serializers.CharField(help_text="csarId", required=True)


class NsPackageDistributeResponseSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="status", required=True)
    statusDescription = serializers.CharField(help_text="statusDescription", required=True)
    errorCode = serializers.CharField(help_text="errorCode", required=True, allow_null=True)


class NsPackageInfoSerializer(serializers.Serializer):
    nsdId = serializers.CharField(
        help_text="NSD ID",
        required=False,
        allow_null=True
    )
    nsPackageId = serializers.CharField(
        help_text="NS Package ID",
        allow_blank=True,
        required=False,
        allow_null=True
    )
    nsdProvider = serializers.CharField(
        help_text="NSD Provider",
        allow_blank=True,
        required=False,
        allow_null=True
    )
    nsdVersion = serializers.CharField(
        help_text="NSD Version",
        allow_blank=True,
        required=False,
        allow_null=True
    )
    csarName = serializers.CharField(
        help_text="CSAR name",
        allow_blank=True,
        required=False,
        allow_null=True
    )
    nsdModel = serializers.CharField(
        help_text="NSD Model",
        allow_blank=True,
        required=False,
        allow_null=True
    )
    downloadUrl = serializers.CharField(
        help_text="URL to download NSD Model",
        required=False,
        allow_null=True
    )


class NsPackageSerializer(serializers.Serializer):
    csarId = serializers.CharField(
        help_text="CSAR ID",
        required=False,
        allow_null=True
    )
    packageInfo = NsPackageInfoSerializer(
        help_text="NS Package Info",
        required=False,
        allow_null=True
    )


class NsPackagesSerializer(serializers.ListSerializer):
    child = NsPackageSerializer()


class NfPackageDistributeRequestSerializer(serializers.Serializer):
    csarId = serializers.CharField(help_text="CSAR ID", required=True)
    vimIds = serializers.ListField(
        help_text="A string for vimIds",
        child=serializers.CharField(),
        required=False)
    labVimId = serializers.CharField(
        help_text="A list of VIM IDs.",
        allow_blank=True,
        required=False)


class NfPackageInfoSerializer(serializers.Serializer):
    vnfdId = serializers.CharField(
        help_text="VNFD ID",
        required=False,
        allow_null=True,
        allow_blank=True)
    vnfPackageId = serializers.CharField(
        help_text="VNF Package ID", required=True)
    vnfdProvider = serializers.CharField(
        help_text="VNFD Provider",
        required=False,
        allow_null=True,
        allow_blank=True)
    vnfdVersion = serializers.CharField(
        help_text="VNFD Version",
        required=False,
        allow_null=True,
        allow_blank=True)
    vnfVersion = serializers.CharField(
        help_text="VNF Version",
        required=False,
        allow_null=True,
        allow_blank=True)
    csarName = serializers.CharField(
        help_text="CSAR Name",
        required=False,
        allow_null=True,
        allow_blank=True)
    vnfdModel = serializers.CharField(
        help_text="VNFD Model",
        required=False,
        allow_null=True,
        allow_blank=True)
    downloadUrl = serializers.CharField(
        help_text="URL to download VNFD Model",
        required=False,
        allow_null=True,
        allow_blank=True)


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
    imageInfo = NfImageInfoSerializer(
        help_text="Image Info",
        required=False,
        many=True,
        allow_null=True)


class NfPackagesSerializer(serializers.ListSerializer):
    child = NfPackageSerializer()


class PostJobResponseSerializer(serializers.Serializer):
    jobId = serializers.CharField(help_text="jobId", required=True)


class ParseModelRequestSerializer(serializers.Serializer):
    csarId = serializers.CharField(help_text="CSAR ID", required=True)
    inputs = serializers.JSONField(help_text="Inputs", required=False)


class ParseModelResponseSerializer(serializers.Serializer):
    model = serializers.JSONField(help_text="Model", required=True)


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
