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

    def test_upload_vnf_pkg(self):
        data = {'file': open(os.path.join(CATALOG_ROOT_PATH, "empty.txt"), "rb")}
        VnfPackageModel.objects.create(
            vnfPackageId="222",
            onboardingState="CREATED"
        )
        response = self.client.put("/api/vnfpkgm/v1/vnf_packages/222/package_content", data=data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    @mock.patch.object(urllib2, 'urlopen')
    def test_upload_nf_pkg_from_uri(self, mock_urlopen):
        vnf_pkg = VnfPackageModel.objects.create(
            vnfPackageId="222",
            onboardingState="CREATED"
        )
        req_data = {"addressInformation": "https://127.0.0.1:1234/sdc/v1/hss.csar"}
        mock_urlopen.return_value = MockReq()
        vnf_pkg_id = vnf_pkg.vnfPackageId
        VnfPkgUploadThread(req_data, vnf_pkg_id).run()

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
