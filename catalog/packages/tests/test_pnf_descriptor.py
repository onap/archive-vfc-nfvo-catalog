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


import copy
import json
import os
import mock


from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from catalog.pub.database.models import PnfPackageModel, NSPackageModel
from catalog.pub.utils import toscaparser
from catalog.packages.const import PKG_STATUS
from catalog.packages.tests.const import pnfd_data
from catalog.packages.biz.pnf_descriptor import PnfPackage


class TestPnfDescriptor(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_defined_data = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3',
        }
        self.expected_pnfd_info = {
            'id': None,
            'pnfdId': None,
            'pnfdName': None,
            'pnfdVersion': None,
            'pnfdProvider': None,
            'pnfdInvariantId': None,
            'pnfdOnboardingState': 'CREATED',
            'onboardingFailureDetails': None,
            'pnfdUsageState': 'NOT_IN_USE',
            'userDefinedData': self.user_defined_data,
            '_links': None
        }
        self.nsdModel = {
            "pnfs": [{"properties": {"id": "m6000_s"}}]
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
        expected_reponse_data = [
            copy.deepcopy(self.expected_pnfd_info),
            copy.deepcopy(self.expected_pnfd_info)
        ]
        expected_reponse_data[0]['id'] = '0'
        expected_reponse_data[1]['id'] = '1'

        user_defined_data = json.JSONEncoder().encode(self.user_defined_data)
        for i in range(2):
            PnfPackageModel(
                pnfPackageId=str(i),
                onboardingState='CREATED',
                usageState='NOT_IN_USE',
                userDefinedData=user_defined_data
            ).save()
        response = self.client.get('/api/nsd/v1/pnf_descriptors', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_reponse_data, response.data)

    def test_query_single_pnfd_normal(self):
        expected_reponse_data = copy.deepcopy(self.expected_pnfd_info)
        expected_reponse_data['id'] = '22'

        user_defined_data = json.JSONEncoder().encode(self.user_defined_data)
        PnfPackageModel(
            pnfPackageId='22',
            onboardingState='CREATED',
            usageState='NOT_IN_USE',
            userDefinedData=user_defined_data
        ).save()

        response = self.client.get('/api/nsd/v1/pnf_descriptors/22', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_reponse_data, response.data)

    def test_query_single_pnfd_failed(self):
        response = self.client.get('/api/nsd/v1/pnf_descriptors/22', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_single_pnfd_normal(self):
        user_defined_data = json.JSONEncoder().encode(self.user_defined_data)
        PnfPackageModel(
            pnfPackageId='22',
            usageState=PKG_STATUS.NOT_IN_USE,
            userDefinedData=user_defined_data,
            pnfdModel='test'
        ).save()
        NSPackageModel.objects.create(
            nsPackageId="111",
            nsdModel=json.JSONEncoder().encode(self.nsdModel)
        )
        resp = self.client.delete("/api/nsd/v1/pnf_descriptors/22", format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(None, resp.data)

    @mock.patch.object(toscaparser, "parse_pnfd")
    def test_pnfd_content_upload_normal(self, mock_parse_pnfd):
        user_defined_data_json = json.JSONEncoder().encode(self.user_defined_data)
        PnfPackageModel(
            pnfPackageId='22',
            usageState=PKG_STATUS.NOT_IN_USE,
            userDefinedData=user_defined_data_json,
        ).save()
        mock_parse_pnfd.return_value = json.JSONEncoder().encode(pnfd_data)
        with open('pnfd_content.txt', 'wb') as fp:
            fp.write('test')

        with open('pnfd_content.txt', 'rb') as fp:
            resp = self.client.put(
                "/api/nsd/v1/pnf_descriptors/22/pnfd_content",
                {'file': fp},
            )
        pnf_pkg = PnfPackageModel.objects.filter(pnfPackageId="22")
        self.assertEqual(pnf_pkg[0].pnfdId, "zte-1.0")
        self.assertEqual(pnf_pkg[0].onboardingState, PKG_STATUS.ONBOARDED)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(None, resp.data)
        os.remove('pnfd_content.txt')

    def test_pnfd_content_upload_when_pnf_not_exist(self):
        with open('pnfd_content.txt', 'wb') as fp:
            fp.write('test')

        with open('pnfd_content.txt', 'rb') as fp:
            resp = self.client.put(
                "/api/nsd/v1/pnf_descriptors/22/pnfd_content",
                {'file': fp},
            )
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @mock.patch.object(toscaparser, "parse_pnfd")
    def test_pnfd_content_upload_when_pnfd_exist(self, mock_parse_pnfd):
        with open('pnfd_content.txt', 'wb') as fp:
            fp.write('test')
        PnfPackageModel(
            pnfPackageId='22',
            usageState=PKG_STATUS.NOT_IN_USE,
            pnfdId="zte-1.0"
        ).save()
        mock_parse_pnfd.return_value = json.JSONEncoder().encode(pnfd_data)
        with open('pnfd_content.txt', 'rb') as fp:
            resp = self.client.put(
                "/api/nsd/v1/pnf_descriptors/22/pnfd_content",
                {'file': fp},
            )
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_pnfd_download_normal(self):
        with open('pnfd_content.txt', 'wb') as fp:
            fp.writelines('test1')
            fp.writelines('test2')
        user_defined_data = json.JSONEncoder().encode(self.user_defined_data)
        PnfPackageModel(
            pnfPackageId='22',
            usageState=PKG_STATUS.NOT_IN_USE,
            onboardingState=PKG_STATUS.ONBOARDED,
            userDefinedData=user_defined_data,
            localFilePath="pnfd_content.txt",
            pnfdModel='test'
        ).save()
        resp = self.client.get("/api/nsd/v1/pnf_descriptors/22/pnfd_content")
        file_content = ""
        for data in resp.streaming_content:
            file_content = '%s%s' % (file_content, data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual('test1test2', file_content)
        os.remove('pnfd_content.txt')

    def test_pnfd_download_failed(self):
        response = self.client.get("/api/nsd/v1/pnf_descriptors/22/pnfd_content")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @mock.patch.object(PnfPackage, "create")
    def test_pnfd_create_when_catch_exception(self, mock_create):
        request_data = {'userDefinedData': self.user_defined_data}
        mock_create.side_effect = TypeError('integer type')
        response = self.client.post('/api/nsd/v1/pnf_descriptors', data=request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @mock.patch.object(PnfPackage, "delete_single")
    def test_delete_single_when_catch_exception(self, mock_delete_single):
        mock_delete_single.side_effect = TypeError("integer type")
        response = self.client.delete("/api/nsd/v1/pnf_descriptors/22", format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @mock.patch.object(PnfPackage, "query_single")
    def test_query_single_when_catch_exception(self, mock_query_single):
        mock_query_single.side_effect = TypeError("integer type")
        response = self.client.get('/api/nsd/v1/pnf_descriptors/22', format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @mock.patch.object(PnfPackage, "query_multiple")
    def test_query_multiple_when_catch_exception(self, mock_query_muitiple):
        mock_query_muitiple.side_effect = TypeError("integer type")
        response = self.client.get('/api/nsd/v1/pnf_descriptors', format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @mock.patch.object(PnfPackage, "upload")
    def test_upload_when_catch_exception(self, mock_upload):
        mock_upload.side_effect = TypeError("integer type")
        response = self.client.put("/api/nsd/v1/pnf_descriptors/22/pnfd_content")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @mock.patch.object(PnfPackage, "download")
    def test_download_when_catch_exception(self, mock_download):
        mock_download.side_effect = TypeError("integer type")
        response = self.client.get("/api/nsd/v1/pnf_descriptors/22/pnfd_content")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
