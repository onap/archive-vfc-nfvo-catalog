# Copyright (C) 2019 Verizon. All Rights Reserved
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

import uuid
import mock
from rest_framework.test import APIClient
from django.test import TestCase
from catalog.pub.database.models import VnfPkgSubscriptionModel


class TestNfPackageSubscription(TestCase):
    def setUp(self):
        self.client = APIClient()
        VnfPkgSubscriptionModel.objects.filter().delete()
        self.vnf_subscription_data = {
            "filters": {
                "notificationTypes": [
                    "VnfPackageOnboardingNotification"
                ],
                "vnfProductsFromProviders": {
                    "vnfProvider": "string",
                    "vnfProducts": {
                        "vnfProductName": "string",
                        "versions": {
                            "vnfSoftwareVersion": "string",
                            "vnfdVersions": [
                                "string"
                            ]
                        }
                    }
                },
                "vnfdId": [
                    "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                ],
                "vnfPkgId": [
                    "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                ],
                "operationalState": [
                    "ENABLED"
                ],
                "usageState": [
                    "IN_USE"
                ]
            },
            "callbackUri": "http://www.vnf1.com/notification",
            "authentication": {
                "authType": [
                    "BASIC"
                ],
                "paramsBasic": {
                    "userName": "string",
                    "password": "string"
                }
            }
        }

    def tearDown(self):
        pass

    @mock.patch("requests.get")
    @mock.patch.object(uuid, 'uuid4')
    def test_create_vnf_subscription(self, mock_uuid4, mock_requests):
        temp_uuid = "99442b18-a5c7-11e8-998c-bf1755941f13"
        mock_requests.return_value.status_code = 204
        mock_requests.get.status_code = 204
        mock_uuid4.return_value = temp_uuid
        response = self.client.post("/api/vnfpkgm/v1/subscriptions", data=self.vnf_subscription_data, format='json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(self.vnf_subscription_data["callbackUri"], response.data["callbackUri"])
        self.assertEqual(temp_uuid, response.data["id"])

    @mock.patch("requests.get")
    @mock.patch.object(uuid, 'uuid4')
    def test_duplicate_subscriptions(self, mock_uuid4, mock_requests):
        temp_uuid = "99442b18-a5c7-11e8-998c-bf1755941f13"
        temp1_uuid = "00342b18-a5c7-11e8-998c-bf1755941f12"
        mock_requests.return_value.status_code = 204
        mock_requests.get.status_code = 204
        mock_uuid4.side_effect = [temp_uuid, temp1_uuid]
        response = self.client.post("/api/vnfpkgm/v1/subscriptions", data=self.vnf_subscription_data, format='json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(self.vnf_subscription_data["callbackUri"], response.data["callbackUri"])
        self.assertEqual(temp_uuid, response.data["id"])
        temp_uuid = "00442b18-a5c7-11e8-998c-bf1755941f12"
        mock_requests.return_value.status_code = 204
        mock_requests.get.status_code = 204
        mock_uuid4.return_value = temp_uuid
        response = self.client.post("/api/vnfpkgm/v1/subscriptions", data=self.vnf_subscription_data, format='json')
        self.assertEqual(303, response.status_code)

    @mock.patch("requests.get")
    @mock.patch.object(uuid, 'uuid4')
    def test_get_subscriptions(self, mock_uuid4, mock_requests):
        temp_uuid = "99442b18-a5c7-11e8-998c-bf1755941f13"
        mock_requests.return_value.status_code = 204
        mock_requests.get.status_code = 204
        mock_uuid4.return_value = temp_uuid
        self.client.post("/api/vnfpkgm/v1/subscriptions",
                         data=self.vnf_subscription_data, format='json')
        response = self.client.get("/api/vnfpkgm/v1/subscriptions?usageState=IN_USE",
                                   format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))

    @mock.patch("requests.get")
    @mock.patch.object(uuid, 'uuid4')
    def test_get_subscriptions_with_invalid_params(self, mock_uuid4, mock_requests):
        temp_uuid = "99442b18-a5c7-11e8-998c-bf1755941f13"
        mock_requests.return_value.status_code = 204
        mock_requests.get.status_code = 204
        mock_uuid4.return_value = temp_uuid
        self.client.post("/api/vnfpkgm/v1/subscriptions",
                         data=self.vnf_subscription_data, format='json')
        response = self.client.get("/api/vnfpkgm/v1/subscriptions?dummy=dummy",
                                   format='json')
        self.assertEqual(400, response.status_code)

    @mock.patch("requests.get")
    @mock.patch.object(uuid, 'uuid4')
    def test_get_subscription_with_id(self, mock_uuid4, mock_requests):
        temp_uuid = "99442b18-a5c7-11e8-998c-bf1755941f13"
        mock_requests.return_value.status_code = 204
        mock_requests.get.status_code = 204
        mock_uuid4.return_value = temp_uuid
        self.client.post("/api/vnfpkgm/v1/subscriptions",
                         data=self.vnf_subscription_data, format='json')
        response = self.client.get("/api/vnfpkgm/v1/subscriptions/" + temp_uuid,
                                   format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(temp_uuid, response.data["id"])

    @mock.patch("requests.get")
    @mock.patch.object(uuid, 'uuid4')
    def test_get_subscription_with_id_not_exists(self, mock_uuid4, mock_requests):
        temp_uuid = "99442b18-a5c7-11e8-998c-bf1755941f13"
        dummy_uuid = str(uuid.uuid4())
        mock_requests.return_value.status_code = 204
        mock_requests.get.status_code = 204
        mock_uuid4.return_value = temp_uuid
        self.client.post("/api/vnfpkgm/v1/subscriptions",
                         data=self.vnf_subscription_data, format='json')
        response = self.client.get("/api/vnfpkgm/v1/subscriptions/" + dummy_uuid,
                                   format='json')
        self.assertEqual(404, response.status_code)

    @mock.patch("requests.get")
    @mock.patch.object(uuid, 'uuid4')
    def test_delete_subscription_with_id(self, mock_uuid4, mock_requests):
        temp_uuid = "99442b18-a5c7-11e8-998c-bf1755941f13"
        dummy_uuid = str(uuid.uuid4())
        mock_requests.return_value.status_code = 204
        mock_requests.get.status_code = 204
        mock_uuid4.return_value = temp_uuid
        self.client.post("/api/vnfpkgm/v1/subscriptions",
                         data=self.vnf_subscription_data, format='json')
        self.client.get("/api/vnfpkgm/v1/subscriptions/" + dummy_uuid,
                        format='json')
        response = self.client.delete("/api/vnfpkgm/v1/subscriptions/" + temp_uuid)
        self.assertEqual(204, response.status_code)

    @mock.patch("requests.get")
    @mock.patch.object(uuid, 'uuid4')
    def test_delete_subscription_with_id_not_exists(self, mock_uuid4, mock_requests):
        dummy_uuid = str(uuid.uuid4())
        response = self.client.delete("/api/vnfpkgm/v1/subscriptions/" + dummy_uuid)
        self.assertEqual(404, response.status_code)
