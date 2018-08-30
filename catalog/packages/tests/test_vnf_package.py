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

import os
import json
import mock
import urllib2

from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from catalog.pub.config.config import CATALOG_ROOT_PATH
from catalog.packages.biz.vnf_package import VnfPkgUploadThread
from catalog.pub.database.models import VnfPackageModel
from catalog.pub.utils import toscaparser
from catalog.packages.const import PKG_STATUS
from catalog.packages.tests.const import vnfd_data


class MockReq():
    def read(self):
        return "1"

    def close(self):
        pass


class TestVnfPackage(TestCase):
    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        pass

    @mock.patch.object(toscaparser, 'parse_vnfd')
    def test_upload_vnf_pkg(self, mock_parse_vnfd):
        data = {'file': open(os.path.join(CATALOG_ROOT_PATH, "empty.txt"), "rb")}
        VnfPackageModel.objects.create(
            vnfPackageId="222",
            onboardingState="CREATED"
        )
        mock_parse_vnfd.return_value = json.JSONEncoder().encode(vnfd_data)
        response = self.client.put("/api/vnfpkgm/v1/vnf_packages/222/package_content", data=data)
        vnf_pkg = VnfPackageModel.objects.filter(vnfPackageId="222")
        self.assertEqual("zte-hss-1.0", vnf_pkg[0].vnfdId)
        self.assertEqual(PKG_STATUS.ONBOARDED, vnf_pkg[0].onboardingState)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        os.remove(vnf_pkg[0].localFilePath)
        os.removedirs(os.path.join(CATALOG_ROOT_PATH, vnf_pkg[0].vnfPackageId))

    @mock.patch.object(toscaparser, 'parse_vnfd')
    @mock.patch.object(urllib2, 'urlopen')
    def test_upload_nf_pkg_from_uri(self, mock_urlopen, mock_parse_vnfd):
        vnf_pkg = VnfPackageModel.objects.create(
            vnfPackageId="222",
            onboardingState="CREATED"
        )
        mock_parse_vnfd.return_value = json.JSONEncoder().encode(vnfd_data)
        req_data = {"addressInformation": "https://127.0.0.1:1234/sdc/v1/hss.csar"}
        mock_urlopen.return_value = MockReq()
        vnf_pkg_id = vnf_pkg.vnfPackageId
        VnfPkgUploadThread(req_data, vnf_pkg_id).run()
        vnf_pkg1 = VnfPackageModel.objects.filter(vnfPackageId="222")
        self.assertEqual("zte-hss-1.0", vnf_pkg1[0].vnfdId)

        os.remove(vnf_pkg1[0].localFilePath)
        os.removedirs(os.path.join(CATALOG_ROOT_PATH, vnf_pkg1[0].vnfPackageId))

    def test_create_vnf_pkg(self):
        req_data = {
            "userDefinedData": {"a": "A"}
        }
        response = self.client.post("/api/vnfpkgm/v1/vnf_packages", data=req_data, format="json")
        resp_data = json.loads(response.content)
        expect_resp_data = {
            "id": resp_data.get("id"),
            "onboardingState": "CREATED",
            "operationalState": "DISABLED",
            "usageState": "NOT_IN_USE",
            "userDefinedData": {"a": "A"},
            "_links": None  # TODO
        }
        self.assertEqual(expect_resp_data, resp_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_query_single_vnf(self):
        VnfPackageModel.objects.create(
            vnfPackageId="222",
            vnfdId="zte-hss-1.0",
            vnfVendor="zte",
            vnfdProductName="hss",
            vnfSoftwareVersion="1.0.0",
            vnfdVersion="1.0.0",
            checksum='{"algorithm":"111", "hash": "11"}',
            onboardingState="CREATED",
            operationalState="DISABLED",
            usageState="NOT_IN_USE",
            userDefinedData='{"a": "A"}'
        )
        response = self.client.get("/api/vnfpkgm/v1/vnf_packages/222")
        expect_data = {
            "id": "222",
            "vnfdId": "zte-hss-1.0",
            "vnfProductName": "hss",
            "vnfSoftwareVersion": "1.0.0",
            "vnfdVersion": "1.0.0",
            "checksum": {"algorithm": "111", "hash": "11"},
            "softwareImages": None,
            "additionalArtifacts": None,
            "onboardingState": "CREATED",
            "operationalState": "DISABLED",
            "usageState": "NOT_IN_USE",
            "userDefinedData": {"a": "A"},
            "_links": None
        }
        self.assertEqual(response.data, expect_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_query_multiple_vnf(self):
        VnfPackageModel.objects.create(
            vnfPackageId="111",
            vnfdId="zte-hss-1.0",
            vnfVendor="zte",
            vnfdProductName="hss",
            vnfSoftwareVersion="1.0.0",
            vnfdVersion="1.0.0",
            checksum='{"algorithm":"111", "hash": "11"}',
            onboardingState="CREATED",
            operationalState="DISABLED",
            usageState="NOT_IN_USE",
            userDefinedData='{"a": "A"}'
        )
        VnfPackageModel.objects.create(
            vnfPackageId="222",
            vnfdId="zte-hss-1.0",
            vnfVendor="zte",
            vnfdProductName="hss",
            vnfSoftwareVersion="1.0.0",
            vnfdVersion="1.0.0",
            checksum='{"algorithm":"111", "hash": "11"}',
            onboardingState="CREATED",
            operationalState="DISABLED",
            usageState="NOT_IN_USE",
            userDefinedData='{"a": "A"}'
        )
        response = self.client.get("/api/vnfpkgm/v1/vnf_packages")
        expect_data = [
            {
                "id": "111",
                "vnfdId": "zte-hss-1.0",
                "vnfProductName": "hss",
                "vnfSoftwareVersion": "1.0.0",
                "vnfdVersion": "1.0.0",
                "checksum": {"algorithm": "111", "hash": "11"},
                "softwareImages": None,
                "additionalArtifacts": None,
                "onboardingState": "CREATED",
                "operationalState": "DISABLED",
                "usageState": "NOT_IN_USE",
                "userDefinedData": {"a": "A"},
                "_links": None
            },
            {
                "id": "222",
                "vnfdId": "zte-hss-1.0",
                "vnfProductName": "hss",
                "vnfSoftwareVersion": "1.0.0",
                "vnfdVersion": "1.0.0",
                "checksum": {"algorithm": "111", "hash": "11"},
                "softwareImages": None,
                "additionalArtifacts": None,
                "onboardingState": "CREATED",
                "operationalState": "DISABLED",
                "usageState": "NOT_IN_USE",
                "userDefinedData": {"a": "A"},
                "_links": None
            }
        ]
        self.assertEqual(response.data, expect_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_single_vnf_pkg(self):
        VnfPackageModel.objects.create(
            vnfPackageId="222",
            vnfdId="zte-hss-1.0",
            vnfVendor="zte",
            vnfdProductName="hss",
            vnfSoftwareVersion="1.0.0",
            vnfdVersion="1.0.0",
            checksum='{"algorithm":"111", "hash": "11"}',
            onboardingState="CREATED",
            operationalState="DISABLED",
            usageState="NOT_IN_USE",
            userDefinedData='{"a": "A"}'
        )
        response = self.client.delete("/api/vnfpkgm/v1/vnf_packages/222")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    def test_delete_when_vnf_pkg_not_exist(self):
        response = self.client.delete("/api/vnfpkgm/v1/vnf_packages/222")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    def test_fetch_vnf_pkg(self):
        with open("vnfPackage.csar", "wb") as fp:
            fp.writelines("AAAABBBBCCCCDDDD")
        VnfPackageModel.objects.create(
            vnfPackageId="222",
            onboardingState="ONBOARDED",
            localFilePath="vnfPackage.csar"
        )
        response = self.client.get("/api/vnfpkgm/v1/vnf_packages/222/package_content")
        partial_file_content = ''
        for data in response.streaming_content:
            partial_file_content = partial_file_content + data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('AAAABBBBCCCCDDDD', partial_file_content)
        os.remove("vnfPackage.csar")

    def test_fetch_partical_vnf_pkg(self):
        with open("vnfPackage.csar", "wb") as fp:
            fp.writelines("AAAABBBBCCCCDDDD")
        VnfPackageModel.objects.create(
            vnfPackageId="222",
            onboardingState="ONBOARDED",
            localFilePath="vnfPackage.csar"
        )
        response = self.client.get("/api/vnfpkgm/v1/vnf_packages/222/package_content", RANGE="4-7")
        partial_file_content = ''
        for data in response.streaming_content:
            partial_file_content = partial_file_content + data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('BBBB', partial_file_content)
        os.remove("vnfPackage.csar")
