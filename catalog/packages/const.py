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

from catalog.pub.utils.jobutil import enum

PKG_STATUS = enum(CREATED="CREATED", UPLOADING="UPLOADING", PROCESSING="PROCESSING", ONBOARDED="ONBOARDED",
                  IN_USE="IN_USE", NOT_IN_USE="NOT_IN_USE", ENABLED="ENABLED", DISABLED="DISABLED")

AUTH_TYPES = ["BASIC", "OAUTH2_CLIENT_CREDENTIALS", "TLS_CERT"]

BASIC = "BASIC"

OAUTH2_CLIENT_CREDENTIALS = "OAUTH2_CLIENT_CREDENTIALS"

NOTIFICATION_TYPES = ["VnfPackageOnboardingNotification", "VnfPackageChangeNotification"]

VNFPKG_SUBSCRIPTION_ROOT_URI = "api/vnfpkgm/v1/subscriptions/"

NSDM_SUBSCRIPTION_ROOT_URI = "api/nsd/v1/subscriptions/"

NSDM_NOTIFICATION_FILTERS = ["notificationTypes", "nsdInfoId", "nsdName",
                             "nsdId", "nsdVersion", "nsdDesigner",
                             "nsdInvariantId", "vnfPkgIds", "pnfdInfoIds",
                             "nestedNsdInfoIds", "nsdOnboardingState",
                             "nsdOperationalState", "nsdUsageState",
                             "pnfdId", "pnfdName", "pnfdVersion",
                             "pnfdProvider", "pnfdInvariantId",
                             "pnfdOnboardingState", "pnfdUsageState"]

NSDM_NOTIFICATION_TYPES = ["NsdOnBoardingNotification",
                           "NsdOnboardingFailureNotification",
                           "NsdChangeNotification",
                           "NsdDeletionNotification",
                           "PnfdOnBoardingNotification",
                           "PnfdOnBoardingFailureNotification",
                           "PnfdDeletionNotification"]
