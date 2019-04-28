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
from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from catalog.packages.biz.sdc_vnf_package import NfDistributeThread, NfPkgDeleteThread
from catalog.pub.database.models import JobStatusModel, JobModel
from catalog.pub.database.models import VnfPackageModel
from catalog.pub.msapi import sdc
from catalog.pub.utils import restcall, toscaparser
from .const import vnfd_data


class TestNfPackage(TestCase):
    def setUp(self):
        self.client = APIClient()
        VnfPackageModel.objects.filter().delete()
        JobModel.objects.filter().delete()
        JobStatusModel.objects.filter().delete()
        self.vnfd_data = vnfd_data

    def tearDown(self):
        pass

    def assert_job_result(self, job_id, job_progress, job_detail):
        jobs = JobStatusModel.objects.filter(
            jobid=job_id,
            progress=job_progress,
            descp=job_detail)
        self.assertEqual(1, len(jobs))

    @mock.patch.object(NfDistributeThread, 'run')
    def test_nf_pkg_distribute_normal(self, mock_run):
        resp = self.client.post(
            "/api/catalog/v1/vnfpackages",
            {
                "csarId": "1",
                "vimIds": ["1"]
            },
            format='json'
        )
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)

    def test_nf_pkg_distribute_when_csar_already_exist(self):
        VnfPackageModel(
            vnfPackageId="1",
            vnfdId="vcpe_vfw_zte_1_0"
        ).save()
        NfDistributeThread(
            csar_id="1",
            vim_ids=["1"],
            lab_vim_id="",
            job_id="2"
        ).run()
        self.assert_job_result("2", 255, "NF CSAR(1) already exists.")

    @mock.patch.object(restcall, 'call_req')
    @mock.patch.object(sdc, 'download_artifacts')
    @mock.patch.object(toscaparser, 'parse_vnfd')
    def test_nf_pkg_distribute_when_vnfd_already_exist(self,
                                                       mock_parse_vnfd,
                                                       mock_download_artifacts,
                                                       mock_call_req):
        mock_parse_vnfd.return_value = json.JSONEncoder().encode(self.vnfd_data)
        mock_download_artifacts.return_value = "/home/hss.csar"
        mock_call_req.return_value = [0, json.JSONEncoder().encode([{
            "uuid": "1",
            "toscaModelURL": "https://127.0.0.1:1234/sdc/v1/hss.csar"
        }]), '200']
        VnfPackageModel(vnfPackageId="2", vnfdId="zte-hss-1.0").save()
        NfDistributeThread(
            csar_id="1",
            vim_ids=["1"],
            lab_vim_id="",
            job_id="2"
        ).run()
        self.assert_job_result("2", 255, "VNF package(zte-hss-1.0) already exists.")

    @mock.patch.object(restcall, 'call_req')
    @mock.patch.object(sdc, 'download_artifacts')
    @mock.patch.object(toscaparser, 'parse_vnfd')
    def test_nf_pkg_distribute_successfully(self,
                                            mock_parse_vnfd,
                                            mock_download_artifacts,
                                            mock_call_req):
        mock_parse_vnfd.return_value = json.JSONEncoder().encode(self.vnfd_data)
        mock_download_artifacts.return_value = "/home/hss.csar"
        mock_call_req.return_value = [0, json.JSONEncoder().encode([{
            "uuid": "1",
            "toscaModelURL": "https://127.0.0.1:1234/sdc/v1/hss.csar"
        }]), '200']
        NfDistributeThread(
            csar_id="1",
            vim_ids=["1"],
            lab_vim_id="",
            job_id="4"
        ).run()
        self.assert_job_result("4", 100, "CSAR(1) distribute successfully.")

    ###############################################################################################################

    @mock.patch.object(NfPkgDeleteThread, 'run')
    def test_nf_pkg_delete_normal(self, mock_run):
        resp = self.client.delete("/api/catalog/v1/vnfpackages/1")
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)

    def test_nf_pkg_normal_delete(self):
        VnfPackageModel(
            vnfPackageId="2",
            vnfdId="vcpe_vfw_zte_1_0"
        ).save()
        NfPkgDeleteThread(
            csar_id="2",
            job_id="2"
        ).run()
        self.assert_job_result("2", 100, "Delete CSAR(2) successfully.")

    def test_nf_pkg_get_all(self):
        VnfPackageModel(
            vnfPackageId="3",
            vnfdId="3",
            vnfVendor='3',
            vnfdVersion='3',
            vnfSoftwareVersion='',
            vnfPackageUri='',
            vnfdModel=''
        ).save()
        VnfPackageModel(
            vnfPackageId="4",
            vnfdId="4",
            vnfVendor='4',
            vnfdVersion='4',
            vnfSoftwareVersion='',
            vnfPackageUri='',
            vnfdModel=''
        ).save()
        resp = self.client.get("/api/catalog/v1/vnfpackages")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        expect_data = [
            {
                "imageInfo": [],
                "csarId": "3",
                "packageInfo": {
                    "csarName": "",
                    "vnfdModel": "",
                    "vnfdProvider": "3",
                    "vnfdId": "3",
                    "downloadUrl": "http://127.0.0.1:8806/static/catalog/3/",
                    "vnfVersion": "",
                    "vnfdVersion": "3",
                    "vnfPackageId": "3"
                }
            },
            {
                "imageInfo": [],
                "csarId": "4",
                "packageInfo": {
                    "csarName": "",
                    "vnfdModel": "",
                    "vnfdProvider": "4",
                    "vnfdId": "4",
                    "downloadUrl": "http://127.0.0.1:8806/static/catalog/4/",
                    "vnfVersion": "",
                    "vnfdVersion": "4",
                    "vnfPackageId": "4"
                }
            }
        ]
        self.assertEqual(expect_data, resp.data)

    def test_nf_pkg_get_one(self):
        VnfPackageModel(
            vnfPackageId="4",
            vnfdId="4",
            vnfVendor='4',
            vnfdVersion='4',
            vnfSoftwareVersion='',
            vnfPackageUri='',
            vnfdModel=''
        ).save()

        resp = self.client.get("/api/catalog/v1/vnfpackages/4")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        expect_data = {
            "imageInfo": [],
            "csarId": "4",
            "packageInfo": {
                "csarName": "",
                "vnfdModel": "",
                "vnfdProvider": "4",
                "vnfdId": "4",
                "downloadUrl": "http://127.0.0.1:8806/static/catalog/4/",
                "vnfVersion": "",
                "vnfdVersion": "4",
                "vnfPackageId": "4"
            }
        }
        self.assertEqual(expect_data, resp.data)

    def test_nf_pkg_get_one_failed(self):
        VnfPackageModel(
            vnfPackageId="4",
            vnfdId="4",
            vnfVendor='4',
            vnfdVersion='4',
            vnfSoftwareVersion='',
            vnfPackageUri='',
            vnfdModel=''
        ).save()

        resp = self.client.get("/api/catalog/v1/vnfpackages/2")
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual({'error': 'Vnf package[2] not Found.'}, resp.data)

    ###############################################################################################################

    @mock.patch.object(toscaparser, 'parse_vnfd')
    def test_vnfd_parse_normal(self, mock_parse_vnfd):
        VnfPackageModel(
            vnfPackageId="8",
            vnfdId="10"
        ).save()
        mock_parse_vnfd.return_value = json.JSONEncoder().encode({"c": "d"})
        req_data = {
            "csarId": "8",
            "inputs": []
        }
        resp = self.client.post(
            "/api/catalog/v1/parservnfd",
            req_data,
            format='json'
        )
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual({"model": '{"c": "d"}'}, resp.data)

    def test_vnfd_parse_when_csar_not_exist(self):
        req_data = {"csarId": "1", "inputs": []}
        resp = self.client.post(
            "/api/catalog/v1/parservnfd",
            req_data,
            format='json'
        )
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(resp.data, {"error": "VNF CSAR(1) does not exist."})
