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

import ast
import json
import logging
import requests
import uuid

from collections import Counter

from rest_framework import status

from catalog.packages import const
from catalog.pub.database.models import NsdmSubscriptionModel
from catalog.pub.exceptions import CatalogException, \
    ResourceNotFoundException, \
    NsdmBadRequestException, NsdmDuplicateSubscriptionException
from catalog.pub.utils.values import ignore_case_get

logger = logging.getLogger(__name__)

PARAMSBASICKEYS = ["userName", "password"]

PARAMSOAUTH2CLIENTCREDENTIALSKEYS = ["clientId", "clientPassword",
                                     "tokenEndpoint"]


def is_filter_type_equal(new_filter, existing_filter):
    return Counter(list(set(new_filter))) == Counter(existing_filter)


class NsdmSubscription:

    def __init__(self):
        pass

    def query_multi_subscriptions(self, query_params):
        self.params = query_params
        query_data = {}
        logger.debug("Start QueryMultiSubscriptions get --> "
                     "Check for filters in query params" % self.params)
        for query, value in self.params.iteritems():
            if query in const.NSDM_NOTIFICATION_FILTERS and value:
                query_data[query + '__icontains'] = json.dumps(list(set(value)))
        # Query the database with filters if the request
        # has fields in request params, else fetch all records
        if query_data:
            subscriptions = NsdmSubscriptionModel.objects.filter(**query_data)
        else:
            subscriptions = NsdmSubscriptionModel.objects.all()
        if not subscriptions.exists():
            raise ResourceNotFoundException("Subscriptions doesn't exist")
        return [self.fill_resp_data(subscription)
                for subscription in subscriptions]

    def check_callbackuri_connection(self):
        logger.debug("Create Subscription --> Test Callback URI --"
                     "Sending GET request to %s" % self.callback_uri)
        try:
            response = requests.get(self.callback_uri, timeout=2)
            if response.status_code != status.HTTP_204_NO_CONTENT:
                raise CatalogException("callbackUri %s returns %s status "
                                       "code." % (self.callback_uri,
                                                  response.status_code))
        except Exception:
            raise CatalogException("callbackUri %s didn't return 204 status"
                                   "code." % self.callback_uri)

    def fill_resp_data(self, subscription):
        subscription_filter = dict()
        for filter_type in const.NSDM_NOTIFICATION_FILTERS:
            subscription_filter[filter_type] = \
                ast.literal_eval(subscription.__dict__[filter_type])
        resp_data = {
            'id': subscription.subscriptionid,
            'callbackUri': subscription.callback_uri,
            'filter': subscription_filter,
            '_links': json.loads(subscription.links)
        }
        return resp_data

    def create(self, data):
        logger.debug("Start Create Subscription... ")
        self.filter = ignore_case_get(data, "filter", {})
        self.callback_uri = ignore_case_get(data, "callbackUri")
        self.authentication = ignore_case_get(data, "authentication", {})
        self.subscription_id = str(uuid.uuid4())
        self.check_callbackuri_connection()
        self.check_valid_auth_info()
        self.check_filter_types()
        self.check_valid()
        self.save_db()
        subscription = \
            NsdmSubscriptionModel.objects.get(
                subscriptionid=self.subscription_id)
        return self.fill_resp_data(subscription)

    def check_filter_types(self):
        # Check if both nsdId and nsdInfoId
        # or pnfdId and pnfdInfoId are present
        logger.debug("Create Subscription --> Validating Filters... ")
        if self.filter and \
                self.filter.get("nsdId", "") and \
                self.filter.get("nsdInfoId", ""):
            raise NsdmBadRequestException("Notification Filter should contain"
                                          " either nsdId or nsdInfoId")
        if self.filter and \
                self.filter.get("pnfdId", "") and \
                self.filter.get("pnfdInfoIds", ""):
            raise NsdmBadRequestException("Notification Filter should contain"
                                          " either pnfdId or pnfdInfoIds")

    def check_valid_auth_info(self):
        logger.debug("Create Subscription --> Validating Auth "
                     "details if provided... ")
        if self.authentication.get("paramsBasic", {}) and \
                const.BASIC not in self.authentication.get("authType", ''):
            raise NsdmBadRequestException('Auth type should be ' + const.BASIC)
        if self.authentication.get("paramsOauth2ClientCredentials", {}) and \
                const.OAUTH2_CLIENT_CREDENTIALS not in \
                self.authentication.get("authType", ''):
            raise NsdmBadRequestException('Auth type should '
                                          'be ' + const.OAUTH2_CLIENT_CREDENTIALS)
        if const.BASIC in self.authentication.get("authType", '') and \
                "paramsBasic" in self.authentication.keys() and \
                not is_filter_type_equal(PARAMSBASICKEYS,
                                         self.authentication.
                                         get("paramsBasic").keys()):
            raise NsdmBadRequestException('userName and password needed '
                                          'for ' + const.BASIC)
        if const.OAUTH2_CLIENT_CREDENTIALS in \
                self.authentication.get("authType", '') and \
                "paramsOauth2ClientCredentials" in \
                self.authentication.keys() and \
                not is_filter_type_equal(PARAMSOAUTH2CLIENTCREDENTIALSKEYS,
                                         self.authentication.
                                         get("paramsOauth2ClientCredentials")
                                         .keys()):
            raise NsdmBadRequestException('clientId, clientPassword and '
                                          'tokenEndpoint required '
                                          'for ' + const.OAUTH2_CLIENT_CREDENTIALS)

    def check_filter_exists(self, subscription):
        for filter_type in const.NSDM_NOTIFICATION_FILTERS:
            if not is_filter_type_equal(self.filter.get(filter_type, []),
                                        ast.literal_eval(
                                            getattr(subscription,
                                                    filter_type))):
                return False
        return True

    def check_valid(self):
        logger.debug("Create Subscription --> Checking DB if "
                     "same subscription exists already exists... ")
        subscriptions = \
            NsdmSubscriptionModel.objects.filter(
                callback_uri=self.callback_uri)
        if not subscriptions.exists():
            return
        for subscription in subscriptions:
            if self.check_filter_exists(subscription):
                raise NsdmDuplicateSubscriptionException(
                    "Already Subscription exists with the "
                    "same callbackUri and filter")

    def save_db(self):
        logger.debug("Create Subscription --> Saving the subscription "
                     "%s to the database" % self.subscription_id)
        links = {
            "self": {
                "href":
                const.NSDM_SUBSCRIPTION_ROOT_URI + self.subscription_id
            }
        }
        subscription_save_db = {
            "subscriptionid": self.subscription_id,
            "callback_uri": self.callback_uri,
            "auth_info": self.authentication,
            "links": json.dumps(links)
        }
        for filter_type in const.NSDM_NOTIFICATION_FILTERS:
            subscription_save_db[filter_type] = json.dumps(
                list(set(self.filter.get(filter_type, []))))
        NsdmSubscriptionModel.objects.create(**subscription_save_db)
        logger.debug('Create Subscription[%s] success', self.subscription_id)
