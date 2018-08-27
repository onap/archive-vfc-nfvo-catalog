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


class MockReq():
    def read(self):
        return "1"

    def close(self):
        pass


class TestVnfPackage(TestCase):
    def setUp(self):
        self.client = APIClient()
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

    @mock.patch.object(toscaparser, 'parse_vnfd')
    def test_upload_vnf_pkg(self, mock_parse_vnfd):
        data = {'file': open(os.path.join(CATALOG_ROOT_PATH, "empty.txt"), "rb")}
        VnfPackageModel.objects.create(
            vnfPackageId="222",
            onboardingState="CREATED"
        )
        mock_parse_vnfd.return_value = json.JSONEncoder().encode(self.vnfd_data)
        response = self.client.put("/api/vnfpkgm/v1/vnf_packages/222/package_content", data=data)
        vnf_pkg1 = VnfPackageModel.objects.filter(vnfPackageId="222")
        self.assertEqual("zte-hss-1.0", vnf_pkg1[0].vnfdId)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        os.remove(vnf_pkg1[0].localFilePath)
        os.removedirs(os.path.join(CATALOG_ROOT_PATH, vnf_pkg1[0].vnfPackageId))

    @mock.patch.object(toscaparser, 'parse_vnfd')
    @mock.patch.object(urllib2, 'urlopen')
    def test_upload_nf_pkg_from_uri(self, mock_urlopen, mock_parse_vnfd):
        vnf_pkg = VnfPackageModel.objects.create(
            vnfPackageId="222",
            onboardingState="CREATED"
        )
        mock_parse_vnfd.return_value = json.JSONEncoder().encode(self.vnfd_data)
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
