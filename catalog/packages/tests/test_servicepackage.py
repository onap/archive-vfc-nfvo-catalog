# Copyright (c) 2019, CMCC Technologies. Co., Ltd.
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

from django.test import TestCase, Client
from mock import mock
from rest_framework import status

from catalog.packages.biz.sdc_service_package import ServicePackage
from catalog.pub.database.models import ServicePackageModel
from catalog.pub.exceptions import PackageNotFoundException, PackageHasExistsException, CatalogException
from catalog.pub.msapi import sdc
from catalog.pub.utils import toscaparser
from catalog.settings import BASE_DIR

PARSER_BASE_URL = "/api/parser/v1"


class TestServicePackage(TestCase):
    """ Test case for Service Package operations"""

    def setUp(self):
        self.client = Client()
        ServicePackageModel.objects.filter().delete()

    def tearDown(self):
        pass

    ###############################################################

    @mock.patch.object(sdc, 'get_artifact')
    @mock.patch.object(sdc, 'download_artifacts')
    @mock.patch.object(toscaparser, 'parse_nsd')
    def test_service_pkg_distribute(self, mock_get_artifact, mock_download_artifacts, mock_parse_nsd):
        mock_get_artifact.return_value = {
            "uuid": "1",
            "invariantUUID": "63eaec39-ffbe-411c-a838-448f2c73f7eb",
            "name": "underlayvpn",
            "version": "2.0",
            "toscaModelURL": "/sdc/v1/catalog/resources/c94490a0-f7ef-48be-b3f8-8d8662a37236/toscaModel",
            "category": "Volte",
            "subCategory": "VolteVNF",
            "resourceType": "VF",
            "lifecycleState": "CERTIFIED",
            "distributionStatus": "DISTRIBUTION_APPROVED",
            "lastUpdaterUserId": "jh0003"
        }
        mock_download_artifacts.return_value = os.path.join(os.path.join(BASE_DIR, "resources"), 'resource_test.csar')
        mock_parse_nsd.return_value = {}
        try:
            csar_id = '1'
            ServicePackage().on_distribute(csar_id)

            sPkg = ServicePackageModel.objects.filter(servicePackageId=csar_id)
            self.assertIsNotNone(sPkg)
        except Exception as e:
            pass

    def test_service_pkg_distribute_when_pkg_exists(self):
        ServicePackageModel(servicePackageId="1", servicedId="2").save()
        csar_id = 1
        try:
            ServicePackage().on_distribute(csar_id)
        except PackageHasExistsException as e:
            self.assertEqual("Service CSAR(1) already exists.", e.message)

    @mock.patch.object(sdc, 'get_artifact')
    def test_service_pkg_distribute_when_fail_get_artifacts(self, mock_get_artifact):
        mock_get_artifact.side_effect = CatalogException("Failed to query artifact(services,1) from sdc.")
        csar_id = 1
        try:
            ServicePackage().on_distribute(csar_id)
        except Exception as e:
            self.assertTrue(isinstance(e, CatalogException))
            self.assertEqual("Failed to query artifact(services,1) from sdc.", e.message)

    @mock.patch.object(sdc, 'get_artifact')
    @mock.patch.object(sdc, 'download_artifacts')
    def test_api_service_pkg_distribute_when_fail_download_artifacts(self, mock_get_artifact, mock_download_artifacts):
        mock_get_artifact.return_value = {
            "uuid": "1",
            "invariantUUID": "63eaec39-ffbe-411c-a838-448f2c73f7eb",
            "name": "underlayvpn",
            "version": "2.0",
            "toscaModelURL": "/sdc/v1/catalog/resources/c94490a0-f7ef-48be-b3f8-8d8662a37236/toscaModel",
            "category": "Volte",
            "subCategory": "VolteVNF",
            "resourceType": "VF",
            "lifecycleState": "CERTIFIED",
            "distributionStatus": "DISTRIBUTION_APPROVED",
            "lastUpdaterUserId": "jh0003"
        }
        mock_download_artifacts.side_effect = CatalogException("Failed to download 1 from sdc.")
        csar_id = 1
        try:
            ServicePackage().on_distribute(csar_id)
        except Exception as e:
            self.assertTrue(isinstance(e, CatalogException))
            self.assertEqual("Failed to download 1 from sdc.", e.message)

    def test_api_service_pkg_distribute_when_pkg_exists(self):
        ServicePackageModel(servicePackageId="1", servicedId="2").save()
        resp = self.client.post(
            PARSER_BASE_URL + "/service_packages", {"csarId": "1"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("Service CSAR(1) already exists.", resp.data["errorMessage"])

    ###############################################################

    def test_service_pkg_get_all(self):
        ServicePackageModel(
            servicePackageId="13",
            servicedId="2",
            servicedDesigner="2",
            servicedVersion="2",
            servicePackageUri="13.csar",
            servicedModel="").save()
        ServicePackageModel(
            servicePackageId="14",
            servicedId="3",
            servicedDesigner="3",
            servicedVersion="3",
            servicePackageUri="14.csar",
            servicedModel="").save()
        csars = ServicePackage().get_csars()
        self.assertEqual(2, len(csars))

    def test_api_service_pkg_get_all(self):
        ServicePackageModel(
            servicePackageId="13",
            servicedId="2",
            servicedDesigner="2",
            servicedVersion="2",
            servicePackageUri="13.csar",
            servicedModel="").save()
        ServicePackageModel(
            servicePackageId="14",
            servicedId="3",
            servicedDesigner="3",
            servicedVersion="3",
            servicePackageUri="14.csar",
            servicedModel="").save()
        resp = self.client.get(PARSER_BASE_URL + "/service_packages")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    ###############################################################

    def test_service_pkg_get_one(self):
        ServicePackageModel(
            servicePackageId="14",
            servicedId="2",
            servicedDesigner="3",
            servicedVersion="4",
            servicePackageUri="14.csar",
            servicedModel="").save()
        csar = ServicePackage().get_csar(14)
        self.assertEqual(14, csar['csarId'])

    def test_service_pkg_get_one_not_found(self):
        try:
            ServicePackage().get_csar(1000)
        except PackageNotFoundException as e:
            self.assertEqual("Service package[1000] not Found.", e.message)

    def test_api_service_pkg_get_one(self):
        ServicePackageModel(
            servicePackageId="14",
            servicedId="2",
            servicedDesigner="3",
            servicedVersion="4",
            servicePackageUri="14.csar",
            servicedModel="").save()
        resp = self.client.get(PARSER_BASE_URL + "/service_packages/14")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_api_service_pkg_get_one_not_found(self):
        resp = self.client.get(PARSER_BASE_URL + "/service_packages/22")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            {"errorMessage": "Service package[22] not Found.", 'error': 404},
            resp.data)

    ###############################################################

    def test_service_pkg_normal_delete(self):
        ServicePackageModel(servicePackageId="8", servicedId="2").save()
        sp = ServicePackageModel.objects.filter(servicePackageId=8)
        self.assertEqual(1, len(sp))
        ServicePackage().delete_csar("8")
        sp = ServicePackageModel.objects.filter(servicePackageId=8)
        self.assertEqual(0, len(sp))

    def test_service_pkg_normal_delete_not_found(self):
        try:
            ServicePackage().delete_csar("8000")
        except PackageNotFoundException as e:
            self.assertEqual("Service package[8000] not Found.", e.message)

    def test_api_service_pkg_normal_delete(self):
        ServicePackageModel(servicePackageId="8", servicedId="2").save()
        resp = self.client.delete(PARSER_BASE_URL + "/service_packages/8")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    ###############################################################

    @mock.patch.object(toscaparser, 'parse_nsd')
    def test_service_pkg_parser(self, mock_parse_nsd):
        ServicePackageModel(servicePackageId="8", servicedId="2").save()
        mock_parse_nsd.return_value = json.JSONEncoder().encode({"a": "b"})

        inputs = []
        ret = ServicePackage().parse_serviced(8, inputs)
        self.assertTrue({"model": '{"c": "d"}'}, ret)

    def test_service_pkg_parser_not_found(self):
        try:
            csar_id = 8000
            inputs = []
            ServicePackage().parse_serviced(csar_id, inputs)
        except PackageNotFoundException as e:
            self.assertEqual("Service CSAR(8000) does not exist.", e.message)

    def test_api_service_pkg_parser_not_found(self):
        query_data = {
            "csarId": "1",
            "packageType": "Service",
            "inputs": "string"
        }
        resp = self.client.post(PARSER_BASE_URL + "/parser", query_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
