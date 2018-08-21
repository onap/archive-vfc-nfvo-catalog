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


from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class TestNsDescriptor(TestCase):
    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        pass

    def test_nsd_create_normal(self):
        reqest_data = {
            'userDefinedData': {
                'key1': 'value1',
                'key2': 'value2',
                'key3': 'value3',
            }
        }
        expected_reponse_data = {
            'nsdOnboardingState': 'CREATED',
            'nsdOperationalState': 'DISABLED',
            'nsdUsageState': 'NOT_IN_USE',
            'userDefinedData': {
                'key1': 'value1',
                'key2': 'value2',
                'key3': 'value3',
            },
            '_links': None
        }
        response = self.client.post(
            '/api/nsd/v1/ns_descriptors',
            data=reqest_data,
            format='json'
        )
        response.data.pop('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(expected_reponse_data, response.data)

    def test_nsd_content_upload_normal(self):
        pass

    def test_nsd_content_upload_failure(self):
        pass
