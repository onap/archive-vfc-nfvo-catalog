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

vnfd_data = {
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
    },
    "vnf": {
        "properties": {
            "descriptor_id": "zte-hss-1.0",
            "descriptor_verison": "1.0.0",
            "software_version": "1.0.0",
            "provider": "zte"
        },
        "metadata": {
        }
    }
}

nsd_data = {"vnffgs": [{"vnffg_id": "vnffg1",
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
                         "description": "vcpe_ns"},
            "ns": {
                "properties": {
                    "descriptor_id": "VCPE_NS",
                    "version": 1,
                    "name": "VCPE_NS",
                    "desginer": "ZTE",
                    "invariant_id": "vcpe_ns_sff_1"
                }
}
}

pnfd_data = {
    "metadata": {
        "id": "zte-1.0",
    }
}
