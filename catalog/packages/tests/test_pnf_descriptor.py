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


import json
import os

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from catalog.pub.database.models import PnfPackageModel


class TestPnfDescriptor(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_defined_data = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3',
        }

    def tearDown(self):
        pass

    def test_pnfd_create_normal(self):
        request_data = {'userDefinedData': self.user_defined_data}
        expected_reponse_data = {
            'pnfdOnboardingState': 'CREATED',
            'pnfdUsageState': 'NOT_IN_USE',
            'userDefinedData': self.user_defined_data,
            '_links': None
        }
        response = self.client.post(
            '/api/nsd/v1/pnf_descriptors',
            data=request_data,
            format='json'
        )
        response.data.pop('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_reponse_data, response.data)

    def test_query_multiple_pnfds_normal(self):
        pass

    def test_query_single_pnfd_normal(self):
        pass

    def test_delete_single_pnfd_normal(self):
        pass

    def test_pnfd_content_upload_normal(self):
        user_defined_data_json = json.JSONEncoder().encode(self.user_defined_data)
        PnfPackageModel(
            pnfPackageId='22',
            usageState='NOT_IN_USE',
            userDefinedData=user_defined_data_json,
        ).save()
        with open('pnfd_content.txt', 'wb') as fp:
            fp.write('test')

        with open('pnfd_content.txt', 'rb') as fp:
            resp = self.client.put(
                "/api/nsd/v1/pnf_descriptors/22/pnfd_content",
                {'file': fp},
            )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual({}, resp.data)

        os.remove('pnfd_content.txt')

    def test_pnfd_content_upload_failure(self):
        pass
