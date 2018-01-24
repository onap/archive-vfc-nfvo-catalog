from django.contrib.auth.models import User
from rest_framework import serializers

from catalog.pub.utils.toscaparser.nsdmodel import EtsiNsdInfoModel
from catalog.pub.utils.toscaparser.vnfdmodel import EtsiVnfdInfoModel


class JobResponseSerializer(serializers.Serializer):
    progress = serializers.CharField(help_text="progress", required=False)
    desc = serializers.CharField(help_text="desc", required=False)
    errcode = serializers.CharField(help_text="errcode", required=False)


class JobResponseHistoryListSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="status", required=False)
    progress = serializers.CharField(help_text="progress", required=False)
    statusDescription = serializers.CharField(
        help_text="statusDescription", required=False)
    errorCode = serializers.CharField(help_text="errcode", required=False)
    responseId = serializers.CharField(help_text="responseId", required=False)


class JobResponseDescriptorSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="status", required=False)
    progress = serializers.CharField(help_text="progress", required=False)
    statusDescription = serializers.CharField(
        help_text="statusDescription", required=False)
    errorCode = serializers.CharField(help_text="errcode", required=False)
    responseId = serializers.CharField(help_text="responseId", required=False)
    responseHistoryList = JobResponseHistoryListSerializer(
        many=True, help_text="responseHistoryList", required=False)


class JobRequestSerializer(serializers.Serializer):
    jobId = serializers.CharField(
        help_text="this field is generated from a query_serializer",
        required=False)
    responseDescriptor = JobResponseDescriptorSerializer(
        help_text="this one too!", required=False)


class PostJobResponseSerializer(serializers.Serializer):
    result = serializers.CharField(help_text="result", required=True)
    msg = serializers.CharField(help_text="msg", required=False)


class NsPackageDistributeRequestSerializer(serializers.Serializer):
    csarId = serializers.CharField(help_text="csarId", required=True)


class NsPackageInfoSerializer(serializers.Serializer):
    nsdId = serializers.CharField(help_text="csarId", required=True)
    nsPackageId = serializers.CharField(help_text="csarId", required=True)
    nsdProvider = serializers.CharField(help_text="csarId", required=True)
    nsdVersion = serializers.CharField(help_text="csarId", required=True)
    csarName = serializers.CharField(help_text="csarId", required=True)
    nsdModel = serializers.CharField(help_text="csarId", required=True)
    downloadUrl = serializers.CharField(help_text="csarId", required=True)


class NsPackageSerializer(serializers.Serializer):
    csarId = serializers.CharField(help_text="csarId", required=True)
    package_info = NsPackageInfoSerializer(
        help_text="package_info", required=True)


class NsPackagesSerializer(serializers.ListSerializer):
    child = NsPackageSerializer(many=True)


class NfPackageDistributeRequestSerializer(serializers.Serializer):
    csar_id = serializers.CharField(help_text="csarId", required=True)
    vim_ids = serializers.ListField(
        help_text="vim_ids",
        child=serializers.CharField(),
        required=False)
    lab_vim_id = serializers.CharField(help_text="lab_vim_id", required=False)


class NfPackageInfoSerializer(serializers.Serializer):
    vnfdId = serializers.CharField(required=True)
    vnfPackageId = serializers.CharField(required=True)
    vnfdProvider = serializers.CharField(required=True)
    vnfdVersion = serializers.CharField(required=True)
    vnfVersion = serializers.CharField(required=True)
    csarName = serializers.CharField(required=True)
    vnfdModel = serializers.CharField(required=True)
    downloadUrl = serializers.CharField(required=True)


class NfImageInfoSerializer(serializers.Serializer):
    index = serializers.CharField(required=True)
    fileName = serializers.CharField(required=True)
    imageId = serializers.CharField(required=True)
    vimId = serializers.CharField(required=True)
    vimUser = serializers.CharField(required=True)
    tenant = serializers.CharField(required=True)
    status = serializers.CharField(required=True)


class NfPackageSerializer(serializers.Serializer):
    csarId = serializers.CharField(help_text="csarId", required=True)
    packageInfo = NfPackageInfoSerializer(
        help_text="packageInfo", required=True)
    imageInfo = NfImageInfoSerializer(help_text="imageInfo", required=False)


class NfPackagesSerializer(serializers.ListSerializer):
    child = NfPackageSerializer(many=True)


class PostJobResponseSerializer(serializers.Serializer):
    jobId = serializers.CharField(help_text="jobId", required=True)


class ParseModelRequestSerializer(serializers.Serializer):
    csarId = serializers.CharField(help_text="csarId", required=True)
    inputs = serializers.JSONField(help_text="inputs", required=False)


class EtsiNsdInfoModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = EtsiNsdInfoModel


class EtsiVnfdInfoModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = EtsiVnfdInfoModel


class ParseNSPackageResponseSerializer(serializers.Serializer):
    model = EtsiNsdInfoModelSerializer(help_text="model", required=True)


class ParseNfPackageResponseSerializer(serializers.Serializer):
    model = EtsiVnfdInfoModelSerializer(help_text="model", required=True)
