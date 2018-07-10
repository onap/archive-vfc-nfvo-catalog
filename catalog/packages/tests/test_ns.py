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
from catalog.pub.database.models import NSPackageModel, VnfPackageModel
from catalog.pub.msapi import sdc


class TestNsPackage(TestCase):
    def setUp(self):
        self.client = Client()
        NSPackageModel.objects.filter().delete()
        VnfPackageModel.objects.filter().delete()
        self.nsd_data = {"vnffgs": [{"vnffg_id": "vnffg1",
                                     "description": "",
                                     "members": ["path1",
                                                 "path2"],
                                     "properties": {"vendor": "zte",
                                                    "connection_point": ["m6000_data_in",
                                                                         "m600_tunnel_cp",
                                                                         "m6000_data_out"],
                                                    "version": "1.0",
                                                    "constituent_vnfs": ["VFW",
                                                                         "VNAT"],
                                                    "number_of_endpoints": 3,
                                                    "dependent_virtual_link": ["sfc_data_network",
                                                                               "ext_datanet_net",
                                                                               "ext_mnet_net"]}}],
                         "inputs": {"sfc_data_network": {"type": "string",
                                                         "value": "sfc_data_network"},
                                    "externalDataNetworkName": {"type": "string",
                                                                "value": "vlan_4004_tunnel_net"},
                                    "externalManageNetworkName": {"type": "string",
                                                                  "value": "vlan_4008_mng_net"},
                                    "NatIpRange": {"type": "string",
                                                   "value": "192.167.0.10-192.168.0.20"},
                                    "externalPluginManageNetworkName": {"type": "string",
                                                                        "value": "vlan_4007_plugin_net"}},
                         "pnfs": [{"pnf_id": "m6000_s",
                                   "cps": [],
                                   "description": "",
                                   "properties": {"vendor": "zte",
                                                  "request_reclassification": False,
                                                  "pnf_type": "m6000s",
                                                  "version": "1.0",
                                                  "management_address": "111111",
                                                  "id": "m6000_s",
                                                  "nsh_aware": False}}],
                         "fps": [{"properties": {"symmetric": False,
                                                 "policy": {"type": "ACL",
                                                            "criteria": {"dest_port_range": "1-100",
                                                                         "ip_protocol": "tcp",
                                                                         "source_ip_range": ["119.1.1.1-119.1.1.10"],
                                                                         "dest_ip_range": [{"get_input": "NatIpRange"}],
                                                                         "dscp": 0,
                                                                         "source_port_range": "1-100"}}},
                                  "forwarder_list": [{"capability": "",
                                                      "type": "cp",
                                                      "node_name": "m6000_data_out"},
                                                     {"capability": "",
                                                      "type": "cp",
                                                      "node_name": "m600_tunnel_cp"},
                                                     {"capability": "vnat_fw_inout",
                                                      "type": "vnf",
                                                      "node_name": "VNAT"}],
                                  "description": "",
                                  "fp_id": "path2"},
                                 {"properties": {"symmetric": True,
                                                 "policy": {"type": "ACL",
                                                            "criteria": {"dest_port_range": "1-100",
                                                                         "ip_protocol": "tcp",
                                                                         "source_ip_range": ["1-100"],
                                                                         "dest_ip_range": ["1-100"],
                                                                         "dscp": 4,
                                                                         "source_port_range": "1-100"}}},
                                  "forwarder_list": [{"capability": "",
                                                      "type": "cp",
                                                      "node_name": "m6000_data_in"},
                                                     {"capability": "",
                                                      "type": "cp",
                                                      "node_name": "m600_tunnel_cp"},
                                                     {"capability": "vfw_fw_inout",
                                                      "type": "vnf",
                                                      "node_name": "VFW"},
                                                     {"capability": "vnat_fw_inout",
                                                      "type": "vnf",
                                                      "node_name": "VNAT"},
                                                     {"capability": "",
                                                      "type": "cp",
                                                      "node_name": "m600_tunnel_cp"},
                                                     {"capability": "",
                                                      "type": "cp",
                                                      "node_name": "m6000_data_out"}],
                                  "description": "",
                                  "fp_id": "path1"}],
                         "routers": [],
                         "vnfs": [{"vnf_id": "VFW",
                                   "description": "",
                                   "properties": {"plugin_info": "vbrasplugin_1.0",
                                                  "vendor": "zte",
                                                  "is_shared": False,
                                                  "adjust_vnf_capacity": True,
                                                  "name": "VFW",
                                                  "vnf_extend_type": "driver",
                                                  "csarVersion": "v1.0",
                                                  "csarType": "NFAR",
                                                  "csarProvider": "ZTE",
                                                  "version": "1.0",
                                                  "nsh_aware": True,
                                                  "cross_dc": False,
                                                  "vnf_type": "VFW",
                                                  "vmnumber_overquota_alarm": True,
                                                  "vnfd_version": "1.0.0",
                                                  "externalPluginManageNetworkName": "vlan_4007_plugin_net",
                                                  "id": "vcpe_vfw_zte_1_0",
                                                  "request_reclassification": False},
                                   "dependencies": [{"key_name": "vfw_ctrl_by_manager_cp",
                                                     "vl_id": "ext_mnet_net"},
                                                    {"key_name": "vfw_data_cp",
                                                     "vl_id": "sfc_data_network"}],
                                   "type": "tosca.nodes.nfv.ext.zte.VNF.VFW",
                                   "networks": []}],
                         "ns_exposed": {"external_cps": [],
                                        "forward_cps": []},
                         "policies": [{"file_url": "policies/abc.drl",
                                       "name": "aaa"}],
                         "vls": [{"route_id": "",
                                  "vl_id": "ext_mnet_net",
                                  "route_external": False,
                                  "description": "",
                                  "properties": {"name": "vlan_4008_mng_net",
                                                 "mtu": 1500,
                                                 "location_info": {"tenant": "admin",
                                                                   "vimid": 2,
                                                                   "availability_zone": "nova"},
                                                 "ip_version": 4,
                                                 "dhcp_enabled": True,
                                                 "network_name": "vlan_4008_mng_net",
                                                 "network_type": "vlan"}},
                                 {"route_id": "",
                                  "vl_id": "ext_datanet_net",
                                  "route_external": False,
                                  "description": "",
                                  "properties": {"name": "vlan_4004_tunnel_net",
                                                 "mtu": 1500,
                                                 "location_info": {"tenant": "admin",
                                                                   "vimid": 2,
                                                                   "availability_zone": "nova"},
                                                 "ip_version": 4,
                                                 "dhcp_enabled": True,
                                                 "network_name": "vlan_4004_tunnel_net",
                                                 "network_type": "vlan"}},
                                 {"route_id": "",
                                  "vl_id": "sfc_data_network",
                                  "route_external": False,
                                  "description": "",
                                  "properties": {"name": "sfc_data_network",
                                                 "dhcp_enabled": True,
                                                 "is_predefined": False,
                                                 "location_info": {"tenant": "admin",
                                                                   "vimid": 2,
                                                                   "availability_zone": "nova"},
                                                 "ip_version": 4,
                                                 "mtu": 1500,
                                                 "network_name": "sfc_data_network",
                                                 "network_type": "vlan"}}],
                         "cps": [{"pnf_id": "m6000_s",
                                  "vl_id": "path2",
                                  "description": "",
                                  "cp_id": "m6000_data_out",
                                  "properties": {"direction": "bidirectional",
                                                 "vnic_type": "normal",
                                                 "bandwidth": 0,
                                                 "mac_address": "11-22-33-22-11-44",
                                                 "interface_name": "xgei-0/4/1/5",
                                                 "ip_address": "176.1.1.2",
                                                 "order": 0,
                                                 "sfc_encapsulation": "mac"}},
                                 {"pnf_id": "m6000_s",
                                  "vl_id": "ext_datanet_net",
                                  "description": "",
                                  "cp_id": "m600_tunnel_cp",
                                  "properties": {"direction": "bidirectional",
                                                 "vnic_type": "normal",
                                                 "bandwidth": 0,
                                                 "mac_address": "00-11-00-22-33-00",
                                                 "interface_name": "gei-0/4/0/13",
                                                 "ip_address": "191.167.100.5",
                                                 "order": 0,
                                                 "sfc_encapsulation": "mac"}},
                                 {"pnf_id": "m6000_s",
                                  "vl_id": "path2",
                                  "description": "",
                                  "cp_id": "m6000_data_in",
                                  "properties": {"direction": "bidirectional",
                                                 "vnic_type": "normal",
                                                 "bandwidth": 0,
                                                 "mac_address": "11-22-33-22-11-41",
                                                 "interface_name": "gei-0/4/0/7",
                                                 "ip_address": "1.1.1.1",
                                                 "order": 0,
                                                 "sfc_encapsulation": "mac",
                                                 "bond": "none"}},
                                 {"pnf_id": "m6000_s",
                                  "vl_id": "ext_mnet_net",
                                  "description": "",
                                  "cp_id": "m600_mnt_cp",
                                  "properties": {"direction": "bidirectional",
                                                 "vnic_type": "normal",
                                                 "bandwidth": 0,
                                                 "mac_address": "00-11-00-22-33-11",
                                                 "interface_name": "gei-0/4/0/1",
                                                 "ip_address": "10.46.244.51",
                                                 "order": 0,
                                                 "sfc_encapsulation": "mac",
                                                 "bond": "none"}}],
                         "metadata": {"invariant_id": "vcpe_ns_sff_1",
                                      "name": "VCPE_NS",
                                      "csarVersion": "v1.0",
                                      "csarType": "NSAR",
                                      "csarProvider": "ZTE",
                                      "version": 1,
                                      "vendor": "ZTE",
                                      "id": "VCPE_NS",
                                      "description": "vcpe_ns"}}

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
                                        "nsdVersion": "2"}},
                       {"csarId": "14",
                        "packageInfo": {"csarName": "14.csar",
                                        "nsdProvider": "3",
                                        "nsdId": "3",
                                        "nsPackageId": "14",
                                        "downloadUrl": "http://127.0.0.1:8806/static/catalog/14/14.csar",
                                        "nsdModel": "",
                                        "nsdVersion": "3"}}]
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
                "downloadUrl": "http://127.0.0.1:8806/static/catalog/14/14.csar"}}
        self.assertEqual(expect_data, resp.data)

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
