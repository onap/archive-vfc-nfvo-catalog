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


class TestNfPackage(TestCase):
    def setUp(self):
        self.client = APIClient()
        VnfPackageModel.objects.filter().delete()
        JobModel.objects.filter().delete()
        JobStatusModel.objects.filter().delete()
        self.vnfd_data = {
            "volume_storages": [
                {
                    "properties": {
                        "size_of_storage": {
                            "factor": 10,
                            "value": 10000000000,
                            "unit": "GB",
                            "unit_size": 1000000000
                        },
                        "type_of_storage": "volume",
                        "rdma_enabled": False,
                        "size": "10 GB"
                    },
                    "volume_storage_id": "vNAT_Storage_6wdgwzedlb6sq18uzrr41sof7",
                    "description": ""
                }
            ],
            "inputs": {},
            "vdus": [
                {
                    "volume_storages": [
                        "vNAT_Storage_6wdgwzedlb6sq18uzrr41sof7"
                    ],
                    "description": "",
                    "dependencies": [],
                    "vls": [],
                    "properties": {
                        "name": "vNat",
                        "configurable_properties": {
                            "test": {
                                "additional_vnfc_configurable_properties": {
                                    "aaa": "1",
                                    "bbb": "2",
                                    "ccc": "3"
                                }
                            }
                        },
                        "description": "the virtual machine of vNat",
                        "nfvi_constraints": [
                            "test"
                        ],
                        "boot_order": [
                            "vNAT_Storage"
                        ]
                    },
                    "vdu_id": "vdu_vNat",
                    "artifacts": [
                        {
                            "artifact_name": "vNatVNFImage",
                            "type": "tosca.artifacts.nfv.SwImage",
                            "properties": {
                                "operating_system": "linux",
                                "sw_image": "/swimages/vRouterVNF_ControlPlane.qcow2",
                                "name": "vNatVNFImage",
                                "container_format": "bare",
                                "min_ram": "1 GB",
                                "disk_format": "qcow2",
                                "supported_virtualisation_environments": [
                                    "test_0"
                                ],
                                "version": "1.0",
                                "checksum": "5000",
                                "min_disk": "10 GB",
                                "size": "10 GB"
                            },
                            "file": "/swimages/vRouterVNF_ControlPlane.qcow2"
                        }
                    ],
                    "nfv_compute": {
                        "flavor_extra_specs": {
                            "hw:cpu_sockets": "2",
                            "sw:ovs_dpdk": "true",
                            "hw:cpu_threads": "2",
                            "hw:numa_mem.1": "3072",
                            "hw:numa_mem.0": "1024",
                            "hw:numa_nodes": "2",
                            "hw:numa_cpus.0": "0,1",
                            "hw:numa_cpus.1": "2,3,4,5",
                            "hw:cpu_cores": "2",
                            "hw:cpu_threads_policy": "isolate"
                        },
                        "cpu_frequency": "2.4 GHz",
                        "num_cpus": 2,
                        "mem_size": "10 GB"
                    },
                    "local_storages": [],
                    "image_file": "vNatVNFImage",
                    "cps": []
                }
            ],
            "image_files": [
                {
                    "properties": {
                        "operating_system": "linux",
                        "sw_image": "/swimages/vRouterVNF_ControlPlane.qcow2",
                        "name": "vNatVNFImage",
                        "container_format": "bare",
                        "min_ram": "1 GB",
                        "disk_format": "qcow2",
                        "supported_virtualisation_environments": [
                            "test_0"
                        ],
                        "version": "1.0",
                        "checksum": "5000",
                        "min_disk": "10 GB",
                        "size": "10 GB"
                    },
                    "image_file_id": "vNatVNFImage",
                    "description": ""
                }
            ],
            "routers": [],
            "local_storages": [],
            "vnf_exposed": {
                "external_cps": [
                    {
                        "key_name": "sriov_plane",
                        "cp_id": "SRIOV_Port"
                    }
                ],
                "forward_cps": []
            },
            "vls": [
                {
                    "route_id": "",
                    "vl_id": "sriov_link",
                    "route_external": False,
                    "description": "",
                    "properties": {
                        "vl_flavours": {
                            "vl_id": "aaaa"
                        },
                        "connectivity_type": {
                            "layer_protocol": "ipv4",
                            "flow_pattern": "flat"
                        },
                        "description": "sriov_link",
                        "test_access": [
                            "test"
                        ]
                    }
                }
            ],
            "cps": [
                {
                    "vl_id": "sriov_link",
                    "vdu_id": "vdu_vNat",
                    "description": "",
                    "cp_id": "SRIOV_Port",
                    "properties": {
                        "address_data": [
                            {
                                "address_type": "ip_address",
                                "l3_address_data": {
                                    "ip_address_type": "ipv4",
                                    "floating_ip_activated": False,
                                    "number_of_ip_address": 1,
                                    "ip_address_assignment": True
                                }
                            }
                        ],
                        "description": "sriov port",
                        "layer_protocol": "ipv4",
                        "virtual_network_interface_requirements": [
                            {
                                "requirement": {
                                    "SRIOV": "true"
                                },
                                "support_mandatory": False,
                                "name": "sriov",
                                "description": "sriov"
                            },
                            {
                                "requirement": {
                                    "SRIOV": "False"
                                },
                                "support_mandatory": False,
                                "name": "normal",
                                "description": "normal"
                            }
                        ],
                        "role": "root",
                        "bitrate_requirement": 10
                    }
                }
            ],
            "metadata": {
                "vnfSoftwareVersion": "1.0.0",
                "vnfProductName": "zte",
                "localizationLanguage": [
                    "english",
                    "chinese"
                ],
                "vnfProvider": "zte",
                "vnfmInfo": "zte",
                "defaultLocalizationLanguage": "english",
                "vnfdId": "zte-hss-1.0",
                "id": "zte-hss-1.0",
                "vnfProductInfoDescription": "hss",
                "vnfdVersion": "1.0.0",
                "vnfProductInfoName": "hss"
            }
        }

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
        resp = self.client.post("/api/catalog/v1/vnfpackages", {
            "csarId": "1",
            "vimIds": ["1"]
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)

    def test_nf_pkg_distribute_when_csar_already_exist(self):
        VnfPackageModel(vnfPackageId="1", vnfdId="vcpe_vfw_zte_1_0").save()
        NfDistributeThread(csar_id="1",
                           vim_ids=["1"],
                           lab_vim_id="",
                           job_id="2").run()
        self.assert_job_result("2", 255, "NF CSAR(1) already exists.")

    @mock.patch.object(restcall, 'call_req')
    @mock.patch.object(sdc, 'download_artifacts')
    @mock.patch.object(toscaparser, 'parse_vnfd')
    def test_nf_pkg_distribute_when_vnfd_already_exist(self,
                                                       mock_parse_vnfd, mock_download_artifacts, mock_call_req):
        mock_parse_vnfd.return_value = json.JSONEncoder().encode(self.vnfd_data)
        mock_download_artifacts.return_value = "/home/hss.csar"
        mock_call_req.return_value = [0, json.JSONEncoder().encode([{
            "uuid": "1",
            "toscaModelURL": "https://127.0.0.1:1234/sdc/v1/hss.csar"
        }]), '200']
        VnfPackageModel(vnfPackageId="2", vnfdId="zte-hss-1.0").save()
        NfDistributeThread(csar_id="1",
                           vim_ids=["1"],
                           lab_vim_id="",
                           job_id="2").run()
        self.assert_job_result("2", 255, "NFD(zte-hss-1.0) already exists.")

    @mock.patch.object(restcall, 'call_req')
    @mock.patch.object(sdc, 'download_artifacts')
    @mock.patch.object(toscaparser, 'parse_vnfd')
    def test_nf_pkg_distribute_successfully(self,
                                            mock_parse_vnfd, mock_download_artifacts, mock_call_req):
        mock_parse_vnfd.return_value = json.JSONEncoder().encode(self.vnfd_data)
        mock_download_artifacts.return_value = "/home/hss.csar"
        mock_call_req.return_value = [0, json.JSONEncoder().encode([{
            "uuid": "1",
            "toscaModelURL": "https://127.0.0.1:1234/sdc/v1/hss.csar"
        }]), '200']
        NfDistributeThread(csar_id="1",
                           vim_ids=["1"],
                           lab_vim_id="",
                           job_id="4").run()
        self.assert_job_result("4", 100, "CSAR(1) distribute successfully.")

    ###############################################################################################################

    @mock.patch.object(NfPkgDeleteThread, 'run')
    def test_nf_pkg_delete_normal(self, mock_run):
        resp = self.client.delete("/api/catalog/v1/vnfpackages/1")
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)

    def test_nf_pkg_normal_delete(self):
        VnfPackageModel(vnfPackageId="2", vnfdId="vcpe_vfw_zte_1_0").save()
        NfPkgDeleteThread(csar_id="2", job_id="2").run()
        self.assert_job_result("2", 100, "Delete CSAR(2) successfully.")

    def test_nf_pkg_get_all(self):
        VnfPackageModel(vnfPackageId="3", vnfdId="3", vnfVendor='3', vnfdVersion='3',
                        vnfSoftwareVersion='', vnfPackageUri='', vnfdModel='').save()
        VnfPackageModel(vnfPackageId="4", vnfdId="4", vnfVendor='4', vnfdVersion='4',
                        vnfSoftwareVersion='', vnfPackageUri='', vnfdModel='').save()
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
        VnfPackageModel(vnfPackageId="4", vnfdId="4", vnfVendor='4', vnfdVersion='4',
                        vnfSoftwareVersion='', vnfPackageUri='', vnfdModel='').save()

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
        VnfPackageModel(vnfPackageId="4", vnfdId="4", vnfVendor='4', vnfdVersion='4',
                        vnfSoftwareVersion='', vnfPackageUri='', vnfdModel='').save()

        resp = self.client.get("/api/catalog/v1/vnfpackages/2")
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual({'error': 'Vnf package[2] not Found.'}, resp.data)

    ###############################################################################################################

    @mock.patch.object(toscaparser, 'parse_vnfd')
    def test_vnfd_parse_normal(self, mock_parse_vnfd):
        VnfPackageModel(vnfPackageId="8", vnfdId="10").save()
        mock_parse_vnfd.return_value = json.JSONEncoder().encode({"c": "d"})
        req_data = {"csarId": "8", "inputs": []}
        resp = self.client.post("/api/catalog/v1/parservnfd", req_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual({"model": '{"c": "d"}'}, resp.data)

    def test_vnfd_parse_when_csar_not_exist(self):
        req_data = {"csarId": "1", "inputs": []}
        resp = self.client.post("/api/catalog/v1/parservnfd", req_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(resp.data, {"error": "VNF CSAR(1) does not exist."})
