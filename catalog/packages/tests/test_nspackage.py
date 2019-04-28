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

import json
import mock
from rest_framework import status
from django.test import TestCase
from django.test import Client

from catalog.pub.utils import restcall, toscaparser
from catalog.pub.database.models import NSPackageModel, VnfPackageModel, PnfPackageModel
from catalog.pub.msapi import sdc
from .const import nsd_data


class TestNsPackage(TestCase):
    def setUp(self):
        self.client = Client()
        NSPackageModel.objects.filter().delete()
        VnfPackageModel.objects.filter().delete()
        self.nsd_data = nsd_data

    def tearDown(self):
        pass

    def test_ns_pkg_distribute_when_ns_exists(self):
        NSPackageModel(nsPackageId="1", nsdId="2").save()
        resp = self.client.post(
            "/api/catalog/v1/nspackages", {"csarId": "1"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual("failed", resp.data["status"])
        self.assertEqual(
            "NS CSAR(1) already exists.",
            resp.data["statusDescription"])

    @mock.patch.object(restcall, 'call_req')
    def test_ns_pkg_distribute_when_csar_not_exist(self, mock_call_req):
        mock_call_req.return_value = [0, "[]", '200']
        resp = self.client.post(
            "/api/catalog/v1/nspackages", {"csarId": "1"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual("failed", resp.data["status"])
        self.assertEqual(
            "Failed to query artifact(services,1) from sdc.",
            resp.data["statusDescription"])

    @mock.patch.object(restcall, 'call_req')
    @mock.patch.object(sdc, 'download_artifacts')
    @mock.patch.object(toscaparser, 'parse_nsd')
    def test_ns_pkg_distribute_when_nsd_already_exists(
            self, mock_parse_nsd, mock_download_artifacts, mock_call_req):
        mock_parse_nsd.return_value = json.JSONEncoder().encode(self.nsd_data)
        mock_download_artifacts.return_value = "/home/vcpe.csar"
        mock_call_req.return_value = [0, json.JSONEncoder().encode([{
            "uuid": "1",
            "toscaModelURL": "https://127.0.0.1:1234/sdc/v1/vcpe.csar",
            "distributionStatus": "DISTRIBUTED"
        }]), '200']
        NSPackageModel(nsPackageId="2", nsdId="VCPE_NS").save()
        resp = self.client.post(
            "/api/catalog/v1/nspackages", {"csarId": "1"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual("failed", resp.data["status"])
        self.assertEqual(
            "NSD(VCPE_NS) already exists.",
            resp.data["statusDescription"])

    @mock.patch.object(restcall, 'call_req')
    @mock.patch.object(sdc, 'download_artifacts')
    @mock.patch.object(toscaparser, 'parse_nsd')
    def test_ns_pkg_distribute_when_nf_not_distributed(
            self, mock_parse_nsd, mock_download_artifacts, mock_call_req):
        mock_parse_nsd.return_value = json.JSONEncoder().encode(self.nsd_data)
        mock_download_artifacts.return_value = "/home/vcpe.csar"
        mock_call_req.return_value = [0, json.JSONEncoder().encode([{
            "uuid": "1",
            "toscaModelURL": "https://127.0.0.1:1234/sdc/v1/vcpe.csar",
            "distributionStatus": "DISTRIBUTED",
        }]), '200']
        resp = self.client.post(
            "/api/catalog/v1/nspackages", {"csarId": "1"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual("failed", resp.data["status"])
        self.assertEqual(
            "VNF package(vcpe_vfw_zte_1_0) is not distributed.",
            resp.data["statusDescription"])

    @mock.patch.object(restcall, 'call_req')
    @mock.patch.object(sdc, 'download_artifacts')
    @mock.patch.object(toscaparser, 'parse_nsd')
    def test_ns_pkg_distribute_when_successfully(
            self, mock_parse_nsd, mock_download_artifacts, mock_call_req):
        mock_parse_nsd.return_value = json.JSONEncoder().encode(self.nsd_data)
        mock_download_artifacts.return_value = "/home/vcpe.csar"
        mock_call_req.return_value = [0, json.JSONEncoder().encode([{
            "uuid": "1",
            "toscaModelURL": "https://127.0.0.1:1234/sdc/v1/vcpe.csar",
            "distributionStatus": "DISTRIBUTED"
        }]), '200']
        VnfPackageModel(vnfPackageId="1", vnfdId="vcpe_vfw_zte_1_0").save()
        PnfPackageModel(pnfPackageId="1", pnfdId="m6000_s").save()
        resp = self.client.post(
            "/api/catalog/v1/nspackages", {"csarId": "1"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual("success", resp.data["status"])
        self.assertEqual(
            "CSAR(1) distributed successfully.",
            resp.data["statusDescription"])

    @mock.patch.object(sdc, 'get_artifacts')
    def test_ns_when_not_distributed_by_sdc(self, mock_get_artifacts):
        mock_get_artifacts.return_value = [{
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
        }]
        resp = self.client.post(
            "/api/catalog/v1/nspackages", {"csarId": "1"}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual("failed", resp.data["status"])
        self.assertEqual(
            "The artifact (services,1) is not distributed from sdc.",
            resp.data["statusDescription"])

    ##########################################################################

    def test_ns_pkg_normal_delete(self):
        NSPackageModel(nsPackageId="8", nsdId="2").save()
        resp = self.client.delete("/api/catalog/v1/nspackages/8")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual("success", resp.data["status"])
        self.assertEqual(
            "Delete CSAR(8) successfully.",
            resp.data["statusDescription"])

    def test_ns_pkg_get_all(self):
        NSPackageModel(
            nsPackageId="13",
            nsdId="2",
            nsdDesginer="2",
            nsdVersion="2",
            nsPackageUri="13.csar",
            nsdModel="").save()
        NSPackageModel(
            nsPackageId="14",
            nsdId="3",
            nsdDesginer="3",
            nsdVersion="3",
            nsPackageUri="14.csar",
            nsdModel="").save()
        resp = self.client.get("/api/catalog/v1/nspackages")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        expect_data = [{"csarId": "13",
                        "packageInfo": {"csarName": "13.csar",
                                        "nsdProvider": "2",
                                        "nsdId": "2",
                                        "nsPackageId": "13",
                                        "downloadUrl": "http://127.0.0.1:8806/static/catalog/13/13.csar",
                                        "nsdModel": "",
                                        "nsdVersion": "2",
                                        "nsdInvariantId": None
                                        }},
                       {"csarId": "14",
                        "packageInfo": {"csarName": "14.csar",
                                        "nsdProvider": "3",
                                        "nsdId": "3",
                                        "nsPackageId": "14",
                                        "downloadUrl": "http://127.0.0.1:8806/static/catalog/14/14.csar",
                                        "nsdModel": "",
                                        "nsdVersion": "3",
                                        "nsdInvariantId": None}}]
        self.assertEqual(expect_data, resp.data)

    def test_ns_pkg_get_one(self):
        NSPackageModel(
            nsPackageId="14",
            nsdId="2",
            nsdDesginer="3",
            nsdVersion="4",
            nsPackageUri="14.csar",
            nsdModel="").save()
        resp = self.client.get("/api/catalog/v1/nspackages/14")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        expect_data = {
            "csarId": "14",
            "packageInfo": {
                "nsdId": "2",
                "nsPackageId": "14",
                "nsdProvider": "3",
                "nsdVersion": "4",
                "csarName": "14.csar",
                "nsdModel": "",
                "downloadUrl": "http://127.0.0.1:8806/static/catalog/14/14.csar",
                "nsdInvariantId": None}}
        self.assertEqual(expect_data, resp.data)

    def test_ns_pkg_get_one_not_found(self):
        resp = self.client.get("/api/catalog/v1/nspackages/22")
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(
            {"error": "Ns package[22] not Found."},
            resp.data)

    ##########################################################################

    @mock.patch.object(toscaparser, 'parse_nsd')
    def test_nsd_parse_normal(self, mock_parse_nsd):
        NSPackageModel(nsPackageId="18", nsdId="12").save()
        mock_parse_nsd.return_value = json.JSONEncoder().encode({"a": "b"})
        req_data = {"csarId": "18", "inputs": []}
        resp = self.client.post(
            "/api/catalog/v1/parsernsd",
            req_data,
            format='json')
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual({"model": '{"a": "b"}'}, resp.data)

    def test_nsd_parse_when_csar_not_exist(self):
        req_data = {"csarId": "1", "inputs": []}
        resp = self.client.post(
            "/api/catalog/v1/parsernsd",
            req_data,
            format='json')
        self.assertEqual(
            resp.status_code,
            status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(resp.data, {"error": "NS CSAR(1) does not exist."})
