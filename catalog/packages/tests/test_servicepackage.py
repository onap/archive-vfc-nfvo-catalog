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

from django.test import TestCase, Client
from mock import mock
from rest_framework import status

from catalog.packages.biz.sdc_service_package import ServicePackage
from catalog.packages.const import PKG_STATUS
from catalog.pub.database.models import ServicePackageModel, VnfPackageModel, PnfPackageModel
from catalog.pub.exceptions import PackageNotFoundException, PackageHasExistsException, CatalogException
from catalog.pub.msapi import sdc
from catalog.pub.utils import toscaparser

PARSER_BASE_URL = "/api/parser/v1"


class TestServicePackage(TestCase):
    """ Test case for Service Package operations"""

    def setUp(self):
        self.client = Client()
        ServicePackageModel.objects.filter().delete()
        self.sd_data = {
            "inputs": {
                "sdwanvpnresource_list": [
                    {
                        "sdwanvpn_topology": "",
                        "required": True,
                        "type": "string"
                    },
                    {
                        "sdwansitelan_list": [
                            {
                                "deviceName": "",
                                "required": True,
                                "type": "string",
                                "description": "The device name in the site"
                            }
                        ]
                    }
                ],
                "sdwansiteresource_list": [
                    {
                        "sdwansite_controlPoint": "",
                        "required": False,
                        "type": "string",
                        "description": "The control point of the site,only for sd-wan-edge"
                    },
                    {
                        "sdwandevice_list": [
                            {
                                "systemIp": "",
                                "required": False,
                                "type": "string",
                                "description": "The system ip of the device"
                            }
                        ]
                    }
                ]
            },
            "pnfs": [
                {
                    "pnf_id": "m6000_s",
                    "cps": [],
                    "description": "",
                    "properties": {
                        "vendor": "zte",
                        "request_reclassification": False,
                        "pnf_type": "m6000s",
                        "version": "1.0",
                        "management_address": "111111",
                        "id": "m6000_s",
                        "nsh_aware": False
                    }
                }
            ],
            "description": "",
            "graph": {
                "sdwansiteresource": [
                    "sdwanvpnresource"
                ],
                "sdwanvpnresource": []
            },
            "basepath": "c:\\users\\cmcc\\appdata\\local\\temp\\tmpn79jwc\\Definitions",
            "vnfs": [
                {
                    "vnf_id": "sdwansiteresource",
                    "description": "",
                    "properties": {
                        "sdwandevice_type": "",
                        "sdwandevice_class": "PNF",
                        "multi_stage_design": "False",
                        "min_instances": "1",
                        "sdwansite_controlPoint": "",
                        "id": "cd557883-ac4b-462d-aa01-421b5fa606b1",
                        "sdwansite_longitude": "",
                        "sdwansite_latitude": "",
                        "sdwansite_postcode": "",
                        "sdwansite_type": "",
                        "nf_naming": {
                            "ecomp_generated_naming": True
                        },
                        "sdwansite_emails": "",
                        "sdwansite_role": "",
                        "vnfm_info": "",
                        "sdwansite_address": "",
                        "sdwansite_description": "",
                        "availability_zone_max_count": "1",
                        "sdwansite_name": ""
                    },
                    "dependencies": [],
                    "networks": [],
                    "metadata": {
                        "category": "Configuration",
                        "subcategory": "Configuration",
                        "UUID": "cd557883-ac4b-462d-aa01-421b5fa606b1",
                        "invariantUUID": "c83b621e-e267-4910-a75a-a2a5957296e4",
                        "name": "sdwansiteresource",
                        "customizationUUID": "673dd6b3-3a06-4ef0-8ad0-8c26224b08f7",
                        "resourceVendorRelease": "1.0",
                        "version": "1.0",
                        "resourceVendor": "onap",
                        "resourceVendorModelNumber": "",
                        "type": "VF",
                        "description": "sdwansiteresource"
                    }
                }
            ],
            "vls": [],
            "service": {
                "type": "org.openecomp.service.EnhanceService",
                "requirements": {
                    "sdwanvpnresource.sdwanvpn.dependency": [
                        "sdwanvpnresource",
                        "sdwanvpn.dependency"
                    ],
                    "sdwansiteresource.sdwansitewan.dependency": [
                        "sdwansiteresource",
                        "sdwansitewan.dependency"
                    ],
                    "sdwansiteresource.sdwandevice.dependency": [
                        "sdwansiteresource",
                        "sdwandevice.dependency"
                    ],
                    "sdwanvpnresource.sdwansitelan.dependency": [
                        "sdwanvpnresource",
                        "sdwansitelan.dependency"
                    ],
                    "sdwanvpnresource.sdwanvpn.device": [
                        "sdwanvpnresource",
                        "sdwanvpn.device"
                    ],
                    "sdwansiteresource.sdwansite.device": [
                        "sdwansiteresource",
                        "sdwansite.device"
                    ],
                    "sdwansiteresource.sdwansite.dependency": [
                        "sdwansiteresource",
                        "sdwansite.dependency"
                    ],
                    "sdwanvpnresource.sdwansitelan.device": [
                        "sdwanvpnresource",
                        "sdwansitelan.device"
                    ],
                    "sdwansiteresource.sdwansitewan.device": [
                        "sdwansiteresource",
                        "sdwansitewan.device"
                    ],
                    "sdwansiteresource.sdwandevice.device": [
                        "sdwansiteresource",
                        "sdwandevice.device"
                    ]
                },
                "properties": {
                    "descriptor_id": "49ee73f4-1e31-4054-b871-eb9b1c29999b",
                    "designer": "",
                    "invariant_id": "5de07996-7ff0-4ec1-b93c-e3a00bb3f207",
                    "name": "Enhance_Service",
                    "verison": ""
                },
                "capabilities": {
                    "sdwansiteresource.sdwandevice.feature": [
                        "sdwansiteresource",
                        "sdwandevice.feature"
                    ],
                    "sdwanvpnresource.sdwanvpn.feature": [
                        "sdwanvpnresource",
                        "sdwanvpn.feature"
                    ],
                    "sdwanvpnresource.sdwanvpn.link": [
                        "sdwanvpnresource",
                        "sdwanvpn.link"
                    ],
                    "sdwansiteresource.sdwansite.feature": [
                        "sdwansiteresource",
                        "sdwansite.feature"
                    ],
                    "sdwansiteresource.sdwansitewan.feature": [
                        "sdwansiteresource",
                        "sdwansitewan.feature"
                    ],
                    "sdwanvpnresource.sdwansitelan.feature": [
                        "sdwanvpnresource",
                        "sdwansitelan.feature"
                    ]
                },
                "metadata": {
                    "category": "E2E Service",
                    "serviceType": "",
                    "description": "Enhance_Service",
                    "instantiationType": "A-la-carte",
                    "type": "Service",
                    "environmentContext": "General_Revenue-Bearing",
                    "serviceEcompNaming": True,
                    "UUID": "49ee73f4-1e31-4054-b871-eb9b1c29999b",
                    "ecompGeneratedNaming": True,
                    "serviceRole": "",
                    "invariantUUID": "5de07996-7ff0-4ec1-b93c-e3a00bb3f207",
                    "namingPolicy": "",
                    "name": "Enhance_Service"
                }
            },
            "metadata": {
                "category": "E2E Service",
                "serviceType": "",
                "description": "Enhance_Service",
                "instantiationType": "A-la-carte",
                "type": "Service",
                "environmentContext": "General_Revenue-Bearing",
                "serviceEcompNaming": True,
                "UUID": "49ee73f4-1e31-4054-b871-eb9b1c29999b",
                "ecompGeneratedNaming": True,
                "serviceRole": "",
                "invariantUUID": "5de07996-7ff0-4ec1-b93c-e3a00bb3f207",
                "namingPolicy": "",
                "name": "Enhance_Service"
            }
        }

    def tearDown(self):
        pass

    ###############################################################

    def test_service_pkg_distribute_when_pkg_exists(self):
        ServicePackageModel(servicePackageId="1", servicedId="2").save()
        csar_id = "1"
        try:
            ServicePackage().on_distribute(csar_id)
        except PackageHasExistsException as e:
            self.assertEqual("Service CSAR(1) already exists.", e.args[0])

    @mock.patch.object(sdc, 'get_artifact')
    def test_service_pkg_distribute_when_fail_get_artifacts(self, mock_get_artifact):
        mock_get_artifact.side_effect = CatalogException("Failed to query artifact(services,1) from sdc.")
        csar_id = "1"
        try:
            ServicePackage().on_distribute(csar_id)
        except Exception as e:
            self.assertTrue(isinstance(e, CatalogException))
            self.assertEqual("Failed to query artifact(services,1) from sdc.", e.args[0])

    @mock.patch.object(sdc, 'get_artifact')
    @mock.patch.object(sdc, 'download_artifacts')
    def test_service_pkg_distribute_when_fail_download_artifacts(self, mock_get_artifact, mock_download_artifacts):
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
        csar_id = "1"
        try:
            ServicePackage().on_distribute(csar_id)
        except Exception as e:
            self.assertTrue(isinstance(e, CatalogException))
            self.assertEqual("Failed to download 1 from sdc.", e.args[0])

    @mock.patch.object(sdc, 'get_artifact')
    @mock.patch.object(sdc, 'download_artifacts')
    @mock.patch.object(toscaparser, 'parse_sd')
    def test_service_pkg_distribute(self, mock_parse_sd, mock_download_artifacts, mock_get_artifact):
        mock_parse_sd.return_value = json.JSONEncoder().encode(self.sd_data)
        mock_download_artifacts.return_value = "/test.csar"
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
        VnfPackageModel(vnfPackageId="1", vnfdId="cd557883-ac4b-462d-aa01-421b5fa606b1").save()
        PnfPackageModel(pnfPackageId="1", pnfdId="m6000_s").save()
        ServicePackage().on_distribute(csar_id="1")

        service_package = ServicePackageModel.objects.filter(servicePackageId="1").first()
        self.assertEqual("5de07996-7ff0-4ec1-b93c-e3a00bb3f207", service_package.invariantId)
        self.assertEqual("Enhance_Service", service_package.servicedName)
        self.assertEqual(PKG_STATUS.ONBOARDED, service_package.onboardingState)
        self.assertEqual(PKG_STATUS.ENABLED, service_package.operationalState)
        self.assertEqual(PKG_STATUS.NOT_IN_USE, service_package.usageState)

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
            self.assertEqual("Service package[1000] not Found.", e.args[0])

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
            self.assertEqual("Service package[8000] not Found.", e.args[0])

    def test_api_service_pkg_normal_delete(self):
        ServicePackageModel(servicePackageId="8", servicedId="2").save()
        resp = self.client.delete(PARSER_BASE_URL + "/service_packages/8")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    ###############################################################

    @mock.patch.object(toscaparser, 'parse_sd')
    def test_service_pkg_parser(self, mock_parse_sd):
        ServicePackageModel(servicePackageId="8", servicedId="2").save()
        mock_parse_sd.return_value = json.JSONEncoder().encode({"a": "b"})

        inputs = []
        ret = ServicePackage().parse_serviced("8", inputs)
        self.assertTrue({"model": '{"c": "d"}'}, ret)

    def test_service_pkg_parser_not_found(self):
        try:
            csar_id = "8000"
            inputs = []
            ServicePackage().parse_serviced(csar_id, inputs)
        except PackageNotFoundException as e:
            self.assertEqual("Service CSAR(8000) does not exist.", e.args[0])

    def test_api_service_pkg_parser_not_found(self):
        query_data = {
            "csarId": "1",
            "packageType": "Service",
            "inputs": "string"
        }
        resp = self.client.post(PARSER_BASE_URL + "/parser", query_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
