# Copyright 2017 ZTE Corporation.
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

import unittest
import json
from django.test import Client
from rest_framework import status


class PackageTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.nsdata = None
        self.nfdata = None
        self.ns_csarId = 123
        self.nf_csarId = 456

        self.nsdata = {
            "csarId": self.ns_csarId
        }

        self.nfdata = {
            "csarId": self.nf_csarId
        }


    def tearDown(self):
        pass

    def test_nspackage_get(self):
        response = self.client.get("/api/nfvocatalog/v1/nspackages")
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.content)

    def test_nfpackage_get(self):
        response = self.client.get("/api/nfvocatalog/v1/vnfpackages")
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.content)

    def test_ns_distribute(self):
        response = self.client.post("/api/nfvocatalog/v1/nspackages",self.nsdata)
        #self.assertEqual(status.HTTP_200_OK, response.status_code, response.content)


    def test_nf_distribute(self):
        response = self.client.post("/api/nfvocatalog/v1/vnfpackages",self.nfdata)
        #self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code, response.content)
        

    def test_ns_package_delete(self):
        response = self.client.delete("/api/nfvocatalog/v1/nspackages/" + str(self.ns_csarId))
        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code, response.content)

    def test_nf_package_delete(self):
        #response = self.client.delete("/api/nfvocatalog/v1/vnfpackages/" + str(self.nf_csarId))
        #self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code, response.content)
        pass
