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

import json
import mock
import uuid
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from catalog.packages.biz.nsdm_subscription import NsdmSubscription
from catalog.pub.database.models import NsdmSubscriptionModel


class TestNsdmSubscription(TestCase):

    def setUp(self):
        self.client = APIClient()
        NsdmSubscriptionModel.objects.all().delete()
        self.subscription_id = str(uuid.uuid4())
        self.subscription = {
            "callbackUri": "http://callbackuri.com",
            "authentication": {
                "authType": ["BASIC"],
                "paramsBasic": {
                    "userName": "username",
                    "password": "password"
                }
            }
        }
        self.links = {
            "self": {
                "href": "/api/v1/subscriptions/" + self.subscription_id
            }
        }
        self.test_subscription = {
            "callbackUri": "http://callbackuri.com",
            "id": self.subscription_id,
            "filter": {
                "notificationTypes": [
                    "NsdOnBoardingNotification"
                ],
                "nsdInfoId": [],
                "nsdId": [],
                "nsdName": [],
                "nsdVersion": [],
                "nsdInvariantId": [],
                "vnfPkgIds": [],
                "nestedNsdInfoIds": [],
                "nsdOnboardingState": [],
                "nsdOperationalState": [],
                "nsdUsageState": [],
                "pnfdInfoIds": [],
                "pnfdId": [],
                "pnfdName": [],
                "pnfdVersion": [],
                "pnfdProvider": [],
                "pnfdInvariantId": [],
                "pnfdOnboardingState": [],
                "pnfdUsageState": []
            },
            "_links": self.links,
        }

    def tearDown(self):
        pass

    @mock.patch("requests.get")
    @mock.patch.object(uuid, 'uuid4')
    def test_nsdm_subscribe_notification(self, mock_uuid4, mock_requests):
        temp_uuid = str(uuid.uuid4())
        mock_requests.return_value.status_code = 204
        mock_requests.get.return_value.status_code = 204
        mock_uuid4.return_value = temp_uuid
        response = self.client.post("/api/nsd/v1/subscriptions",
                                    data=self.subscription, format='json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(self.subscription["callbackUri"],
                         response.data["callbackUri"])
        self.assertEqual(temp_uuid, response.data["id"])

    @mock.patch("requests.get")
    @mock.patch.object(uuid, 'uuid4')
    def test_nsdm_subscribe_callbackFailure(self, mock_uuid4, mock_requests):
        temp_uuid = str(uuid.uuid4())
        mock_requests.return_value.status_code = 500
        mock_requests.get.return_value.status_code = 500
        mock_uuid4.return_value = temp_uuid
        expected_data = {
            'status': 500,
            'detail': "callbackUri http://callbackuri.com didn't"
                      " return 204 statuscode.",
            'title': 'Creating Subscription Failed!'
        }
        response = self.client.post("/api/nsd/v1/subscriptions",
                                    data=self.subscription, format='json')
        self.assertEqual(500, response.status_code)
        self.assertEqual(expected_data, response.data)

    @mock.patch("requests.get")
    def test_nsdm_second_subscription(self, mock_requests):
        mock_requests.return_value.status_code = 204
        mock_requests.get.return_value.status_code = 204
        response = self.client.post("/api/nsd/v1/subscriptions",
                                    data=self.subscription, format='json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(self.subscription["callbackUri"],
                         response.data["callbackUri"])
        dummy_subscription = {
            "callbackUri": "http://callbackuri.com",
            "authentication": {
                "authType": ["BASIC"],
                "paramsBasic": {
                    "userName": "username",
                    "password": "password"
                }
            },
            "filter": {
                "nsdId": ["b632bddc-bccd-4180-bd8d-4e8a9578eff7"],
            }
        }
        response = self.client.post("/api/nsd/v1/subscriptions",
                                    data=dummy_subscription, format='json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(dummy_subscription["callbackUri"],
                         response.data["callbackUri"])

    @mock.patch("requests.get")
    def test_nsdm_duplicate_subscription(self, mock_requests):
        mock_requests.return_value.status_code = 204
        mock_requests.get.return_value.status_code = 204
        response = self.client.post("/api/nsd/v1/subscriptions",
                                    data=self.subscription, format='json')
        self.assertEqual(201, response.status_code)
        self.assertEqual(self.subscription["callbackUri"],
                         response.data["callbackUri"])
        expected_data = {
            'status': 303,
            'detail': 'Already Subscription exists with'
                      ' the same callbackUri and filter',
            'title': 'Creating Subscription Failed!'
        }
        response = self.client.post("/api/nsd/v1/subscriptions",
                                    data=self.subscription, format='json')
        self.assertEqual(303, response.status_code)
        self.assertEqual(expected_data, response.data)

    @mock.patch("requests.get")
    def test_nsdm_bad_request(self, mock_requests):
        dummy_subscription = {
            "callbackUri": "http://callbackuri.com",
            "authentication": {
                "authType": ["BASIC"],
                "paramsBasic": {
                    "userName": "username",
                    "password": "password"
                }
            },
            "filter": {
                "nsdId": "b632bddc-bccd-4180-bd8d-4e8a9578eff7",
            }
        }
        response = self.client.post("/api/nsd/v1/subscriptions",
                                    data=dummy_subscription, format='json')
        self.assertEqual(400, response.status_code)

    @mock.patch("requests.get")
    def test_nsdm_invalid_authtype_subscription(self, mock_requests):
        dummy_subscription = {
            "callbackUri": "http://callbackuri.com",
            "authentication": {
                "authType": ["OAUTH2_CLIENT_CREDENTIALS"],
                "paramsBasic": {
                    "userName": "username",
                    "password": "password"
                }
            }
        }
        mock_requests.return_value.status_code = 204
        mock_requests.get.return_value.status_code = 204
        expected_data = {
            'status': 400,
            'detail': 'Auth type should be BASIC',
            'title': 'Creating Subscription Failed!'
        }
        response = self.client.post("/api/nsd/v1/subscriptions",
                                    data=dummy_subscription, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected_data, response.data)

    @mock.patch("requests.get")
    def test_nsdm_invalid_authtype_oauthclient_subscription(
            self, mock_requests):
        dummy_subscription = {
            "callbackUri": "http://callbackuri.com",
            "authentication": {
                "authType": ["BASIC"],
                "paramsOauth2ClientCredentials": {
                    "clientId": "clientId",
                    "clientPassword": "password",
                    "tokenEndpoint": "http://tokenEndpoint"
                }
            }
        }
        mock_requests.return_value.status_code = 204
        mock_requests.get.return_value.status_code = 204
        expected_data = {
            'status': 400,
            'detail': 'Auth type should be OAUTH2_CLIENT_CREDENTIALS',
            'title': 'Creating Subscription Failed!'
        }
        response = self.client.post("/api/nsd/v1/subscriptions",
                                    data=dummy_subscription, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected_data, response.data)

    @mock.patch("requests.get")
    def test_nsdm_invalid_authparams_subscription(self, mock_requests):
        dummy_subscription = {
            "callbackUri": "http://callbackuri.com",
            "authentication": {
                "authType": ["BASIC"],
                "paramsBasic": {
                    "userName": "username"
                }
            }
        }
        mock_requests.return_value.status_code = 204
        mock_requests.get.return_value.status_code = 204
        expected_data = {
            'status': 400,
            'detail': 'userName and password needed for BASIC',
            'title': 'Creating Subscription Failed!'
        }
        response = self.client.post("/api/nsd/v1/subscriptions",
                                    data=dummy_subscription, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected_data, response.data)

    @mock.patch("requests.get")
    def test_nsdm_invalid_authparams_oauthclient_subscription(
            self, mock_requests):
        dummy_subscription = {
            "callbackUri": "http://callbackuri.com",
            "authentication": {
                "authType": ["OAUTH2_CLIENT_CREDENTIALS"],
                "paramsOauth2ClientCredentials": {
                    "clientPassword": "password",
                    "tokenEndpoint": "http://tokenEndpoint"
                }
            }
        }
        mock_requests.return_value.status_code = 204
        mock_requests.get.return_value.status_code = 204
        expected_data = {
            'status': 400,
            'detail': 'clientId, clientPassword and tokenEndpoint'
                      ' required for OAUTH2_CLIENT_CREDENTIALS',
            'title': 'Creating Subscription Failed!'
        }
        response = self.client.post("/api/nsd/v1/subscriptions",
                                    data=dummy_subscription, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected_data, response.data)

    @mock.patch("requests.get")
    def test_nsdm_invalid_filter_subscription(self, mock_requests):
        dummy_subscription = {
            "callbackUri": "http://callbackuri.com",
            "authentication": {
                "authType": ["BASIC"],
                "paramsBasic": {
                    "userName": "username",
                    "password": "password"
                }
            },
            "filter": {
                "nsdId": ["b632bddc-bccd-4180-bd8d-4e8a9578eff7"],
                "nsdInfoId": ["d0ea5ec3-0b98-438a-9bea-488230cff174"]
            }
        }
        mock_requests.return_value.status_code = 204
        mock_requests.get.return_value.status_code = 204
        expected_data = {
            'status': 400,
            'detail': 'Notification Filter should contain'
                      ' either nsdId or nsdInfoId',
            'title': 'Creating Subscription Failed!'
        }
        response = self.client.post("/api/nsd/v1/subscriptions",
                                    data=dummy_subscription, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected_data, response.data)

    @mock.patch("requests.get")
    def test_nsdm_invalid_filter_pnfd_subscription(self, mock_requests):
        dummy_subscription = {
            "callbackUri": "http://callbackuri.com",
            "authentication": {
                "authType": ["BASIC"],
                "paramsBasic": {
                    "userName": "username",
                    "password": "password"
                }
            },
            "filter": {
                "pnfdId": ["b632bddc-bccd-4180-bd8d-4e8a9578eff7"],
                "pnfdInfoIds": ["d0ea5ec3-0b98-438a-9bea-488230cff174"]
            }
        }
        mock_requests.return_value.status_code = 204
        mock_requests.get.return_value.status_code = 204
        expected_data = {
            'status': 400,
            'detail': 'Notification Filter should contain'
                      ' either pnfdId or pnfdInfoIds',
            'title': 'Creating Subscription Failed!'
        }
        response = self.client.post("/api/nsd/v1/subscriptions",
                                    data=dummy_subscription, format='json')
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected_data, response.data)

    @mock.patch.object(NsdmSubscription, 'create')
    def test_nsdmsubscription_create_when_catch_exception(self, mock_create):
        mock_create.side_effect = TypeError("Unicode type")
        response = self.client.post('/api/nsd/v1/subscriptions',
                                    data=self.subscription, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_nsdm_get_subscriptions(self):
        NsdmSubscriptionModel(subscriptionid=self.subscription_id,
                              callback_uri="http://callbackuri.com",
                              auth_info={},
                              notificationTypes=json.dumps(
                                  ["NsdOnBoardingNotification"]),
                              nsdId=[], nsdVersion=[],
                              nsdInfoId=[], nsdDesigner=[],
                              nsdName=[], nsdInvariantId=[],
                              vnfPkgIds=[], pnfdInfoIds=[],
                              nestedNsdInfoIds=[], nsdOnboardingState=[],
                              nsdOperationalState=[], nsdUsageState=[],
                              pnfdId=[], pnfdVersion=[], pnfdProvider=[],
                              pnfdName=[], pnfdInvariantId=[],
                              pnfdOnboardingState=[], pnfdUsageState=[],
                              links=json.dumps(self.links)).save()
        response = self.client.get("/api/nsd/v1/subscriptions",
                                   format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([self.test_subscription], response.data)

    def test_nsdm_get_subscriptions_filter(self):
        NsdmSubscriptionModel(subscriptionid=self.subscription_id,
                              callback_uri="http://callbackuri.com",
                              auth_info={},
                              notificationTypes=json.dumps(
                                  ["NsdOnBoardingNotification"]),
                              nsdId=[], nsdVersion=[],
                              nsdInfoId=[], nsdDesigner=[],
                              nsdName=[], nsdInvariantId=[],
                              vnfPkgIds=[], pnfdInfoIds=[],
                              nestedNsdInfoIds=[], nsdOnboardingState=[],
                              nsdOperationalState=[], nsdUsageState=[],
                              pnfdId=[], pnfdVersion=[], pnfdProvider=[],
                              pnfdName=[], pnfdInvariantId=[],
                              pnfdOnboardingState=[], pnfdUsageState=[],
                              links=json.dumps(self.links)).save()
        response = self.client.get("/api/nsd/v1/subscriptions"
                                   "?notificationTypes"
                                   "=NsdOnBoardingNotification",
                                   format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([self.test_subscription], response.data)

    def test_nsdm_get_subscriptions_filter_failure(self):
        NsdmSubscriptionModel(subscriptionid=self.subscription_id,
                              callback_uri="http://callbackuri.com",
                              auth_info={},
                              notificationTypes=json.dumps(
                                  ["NsdOnBoardingNotification"]),
                              nsdId=[], nsdVersion=[],
                              nsdInfoId=[], nsdDesigner=[],
                              nsdName=[], nsdInvariantId=[],
                              vnfPkgIds=[], pnfdInfoIds=[],
                              nestedNsdInfoIds=[], nsdOnboardingState=[],
                              nsdOperationalState=[], nsdUsageState=[],
                              pnfdId=[], pnfdVersion=[], pnfdProvider=[],
                              pnfdName=[], pnfdInvariantId=[],
                              pnfdOnboardingState=[], pnfdUsageState=[],
                              links=json.dumps(self.links)).save()
        response = self.client.get("/api/nsd/v1/subscriptions"
                                   "?notificationTypes="
                                   "PnfdOnBoardingFailureNotification",
                                   format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_nsdm_get_subscriptions_invalid_filter(self):
        NsdmSubscriptionModel(subscriptionid=self.subscription_id,
                              callback_uri="http://callbackuri.com",
                              auth_info={},
                              notificationTypes=json.dumps(
                                  ["NsdOnBoardingNotification"]),
                              nsdId=[], nsdVersion=[],
                              nsdInfoId=[], nsdDesigner=[],
                              nsdName=[], nsdInvariantId=[],
                              vnfPkgIds=[], pnfdInfoIds=[],
                              nestedNsdInfoIds=[], nsdOnboardingState=[],
                              nsdOperationalState=[], nsdUsageState=[],
                              pnfdId=[], pnfdVersion=[], pnfdProvider=[],
                              pnfdName=[], pnfdInvariantId=[],
                              pnfdOnboardingState=[], pnfdUsageState=[],
                              links=json.dumps(self.links)).save()
        response = self.client.get("/api/nsd/v1/subscriptions"
                                   "?notificationTypes="
                                   "PnfdOnBoardingFailureNotificati",
                                   format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    @mock.patch.object(NsdmSubscription, 'query_multi_subscriptions')
    def test_nsdmsubscription_get_when_catch_exception(self, mock_create):
        mock_create.side_effect = TypeError("Unicode type")
        response = self.client.get('/api/nsd/v1/subscriptions', format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_nsdm_get_subscription(self):
        NsdmSubscriptionModel(subscriptionid=self.subscription_id,
                              callback_uri="http://callbackuri.com",
                              auth_info={},
                              notificationTypes=json.dumps(
                                  ["NsdOnBoardingNotification"]),
                              nsdId=[], nsdVersion=[],
                              nsdInfoId=[], nsdDesigner=[],
                              nsdName=[], nsdInvariantId=[],
                              vnfPkgIds=[], pnfdInfoIds=[],
                              nestedNsdInfoIds=[], nsdOnboardingState=[],
                              nsdOperationalState=[], nsdUsageState=[],
                              pnfdId=[], pnfdVersion=[], pnfdProvider=[],
                              pnfdName=[], pnfdInvariantId=[],
                              pnfdOnboardingState=[], pnfdUsageState=[],
                              links=json.dumps(self.links)).save()
        response = self.client.get('/api/nsd/v1/'
                                   'subscriptions/' + self.subscription_id,
                                   format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.test_subscription, response.data)

    def test_nsdm_get_subscription_failure(self):
        expected_data = {
            "title": "Query Subscription Failed!",
            "status": 404,
            "detail": "Subscription(" + self.subscription_id + ") "
            "doesn't exists"
        }
        response = self.client.get('/api/nsd/v1/'
                                   'subscriptions/' + self.subscription_id,
                                   format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_nsdm_get_subscription_failure_bad_request(self):
        response = self.client.get("/api/nsd/v1/subscriptions/123",
                                   format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    @mock.patch.object(NsdmSubscription, 'query_single_subscription')
    def test_nsdmsubscription_getsingle_when_catch_exception(
            self, mock_create):
        mock_create.side_effect = TypeError("Unicode type")
        response = self.client.get('/api/nsd/v1/'
                                   'subscriptions/' + self.subscription_id,
                                   format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)
