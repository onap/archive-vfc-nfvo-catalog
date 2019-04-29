# Copyright 2019 ZTE Corporation.
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

from django.contrib import admin

from catalog.pub.database.models import NSPackageModel
from catalog.pub.database.models import ServicePackageModel
from catalog.pub.database.models import VnfPackageModel
from catalog.pub.database.models import PnfPackageModel
from catalog.pub.database.models import SoftwareImageModel
from catalog.pub.database.models import JobModel
from catalog.pub.database.models import JobStatusModel
from catalog.pub.database.models import NsdmSubscriptionModel
from catalog.pub.database.models import VnfPkgSubscriptionModel


@admin.register(NSPackageModel)
class NSPackageModelAdmin(admin.ModelAdmin):
    list_display_links = ('nsPackageId', 'nsdName')
    fields = [
        "nsPackageId",
        "nsPackageUri",
        "checksum",
        "sdcCsarId",
        "onboardingState",
        "operationalState",
        "usageState",
        "deletionPending",
        "nsdId",
        "invariantId",
        "nsdName",
        "nsdDesginer",
        "nsdDescription",
        "nsdVersion",
        "userDefinedData",
        "localFilePath",
        "nsdModel"
    ]

    list_display = [
        "nsPackageId",
        "nsPackageUri",
        "checksum",
        "sdcCsarId",
        "onboardingState",
        "operationalState",
        "usageState",
        "deletionPending",
        "nsdId",
        "invariantId",
        "nsdName",
        "nsdDesginer",
        "nsdDescription",
        "nsdVersion",
        "userDefinedData",
        "localFilePath",
        "nsdModel"
    ]

    search_fields = (
        "nsPackageId",
        "nsdId",
        "nsdName",
        "sdcCsarId"
    )


@admin.register(ServicePackageModel)
class ServicePackageModelAdmin(admin.ModelAdmin):
    list_display_links = ('servicePackageId', 'servicedName')
    fields = [
        "servicePackageId",
        "servicePackageUri",
        "checksum",
        "sdcCsarId",
        "onboardingState",
        "operationalState",
        "usageState",
        "deletionPending",
        "servicedId",
        "invariantId",
        "servicedName",
        "servicedDesigner",
        "servicedDescription",
        "servicedVersion",
        "userDefinedData",
        "localFilePath",
        "servicedModel"
    ]

    list_display = [
        "servicePackageId",
        "servicePackageUri",
        "checksum",
        "sdcCsarId",
        "onboardingState",
        "operationalState",
        "usageState",
        "deletionPending",
        "servicedId",
        "invariantId",
        "servicedName",
        "servicedDesigner",
        "servicedDescription",
        "servicedVersion",
        "userDefinedData",
        "localFilePath",
        "servicedModel"
    ]

    search_fields = (
        "servicePackageId",
        "sdcCsarId",
        "servicedName",
        "onboardingState"
    )


@admin.register(VnfPackageModel)
class VnfPackageModelAdmin(admin.ModelAdmin):
    list_display_links = ('vnfPackageId', 'vnfdId')
    fields = [
        "vnfPackageId",
        "vnfPackageUri",
        "SdcCSARUri",
        "checksum",
        "onboardingState",
        "operationalState",
        "usageState",
        "deletionPending",
        "vnfdId",
        "vnfVendor",
        "vnfdProductName",
        "vnfdVersion",
        "vnfSoftwareVersion",
        "userDefinedData",
        "localFilePath",
        "vnfdModel"
    ]

    list_display = [
        "vnfPackageId",
        "vnfPackageUri",
        "SdcCSARUri",
        "checksum",
        "onboardingState",
        "operationalState",
        "usageState",
        "deletionPending",
        "vnfdId",
        "vnfVendor",
        "vnfdProductName",
        "vnfdVersion",
        "vnfSoftwareVersion",
        "userDefinedData",
        "localFilePath",
        "vnfdModel"
    ]

    search_fields = (
        "vnfPackageId",
        "onboardingState",
        "vnfdId"
    )


@admin.register(PnfPackageModel)
class PnfPackageModelAdmin(admin.ModelAdmin):
    list_display_links = ('pnfPackageId', 'pnfdId')
    fields = [
        "pnfPackageId",
        "pnfPackageUri",
        "sdcCSARUri",
        "checksum",
        "onboardingState",
        "usageState",
        "deletionPending",
        "pnfdId",
        "pnfVendor",
        "pnfdProductName",
        "pnfdVersion",
        "pnfSoftwareVersion",
        "userDefinedData",
        "localFilePath",
        "pnfdModel",
        "pnfdName"
    ]

    list_display = [
        "pnfPackageId",
        "pnfPackageUri",
        "sdcCSARUri",
        "checksum",
        "onboardingState",
        "usageState",
        "deletionPending",
        "pnfdId",
        "pnfVendor",
        "pnfdProductName",
        "pnfdVersion",
        "pnfSoftwareVersion",
        "userDefinedData",
        "localFilePath",
        "pnfdModel",
        "pnfdName"
    ]

    search_fields = (
        "pnfPackageId",
        "onboardingState",
        "pnfdId"
    )


@admin.register(SoftwareImageModel)
class SoftwareImageModelAdmin(admin.ModelAdmin):
    list_display_links = ('imageid', 'vnfPackageId')
    fields = [
        "imageid",
        "containerFormat",
        "diskFormat",
        "mindisk",
        "minram",
        "usermetadata",
        "vnfPackageId",
        "filePath",
        "status",
        "vimid"
    ]

    list_display = [
        "imageid",
        "containerFormat",
        "diskFormat",
        "mindisk",
        "minram",
        "usermetadata",
        "vnfPackageId",
        "filePath",
        "status",
        "vimid"
    ]

    search_fields = (
        "imageid",
        "vnfPackageId",
        "vimid"
    )


@admin.register(NsdmSubscriptionModel)
class NsdmSubscriptionModelAdmin(admin.ModelAdmin):
    list_display_links = ('subscriptionid', 'notificationTypes')
    fields = [
        "subscriptionid",
        "notificationTypes",
        "auth_info",
        "callback_uri",
        "nsdInfoId",
        "nsdId",
        "nsdName",
        "nsdVersion",
        "nsdDesigner",
        "nsdInvariantId",
        "vnfPkgIds",
        "pnfdInfoIds",
        "nestedNsdInfoIds",
        "nsdOnboardingState",
        "nsdOperationalState",
        "nsdUsageState",
        "pnfdId",
        "pnfdName",
        "pnfdVersion",
        "pnfdProvider",
        "pnfdInvariantId",
        "pnfdOnboardingState",
        "pnfdUsageState",
        "links"
    ]

    list_display = [
        "subscriptionid",
        "notificationTypes",
        "auth_info",
        "callback_uri",
        "nsdInfoId",
        "nsdId",
        "nsdName",
        "nsdVersion",
        "nsdDesigner",
        "nsdInvariantId",
        "vnfPkgIds",
        "pnfdInfoIds",
        "nestedNsdInfoIds",
        "nsdOnboardingState",
        "nsdOperationalState",
        "nsdUsageState",
        "pnfdId",
        "pnfdName",
        "pnfdVersion",
        "pnfdProvider",
        "pnfdInvariantId",
        "pnfdOnboardingState",
        "pnfdUsageState",
        "links"
    ]

    search_fields = (
        "subscriptionid",
        "notificationTypes"
    )


@admin.register(VnfPkgSubscriptionModel)
class VnfPkgSubscriptionModelAdmin(admin.ModelAdmin):
    list_display_links = ('subscription_id', 'notification_types')
    fields = [
        "subscription_id",
        "callback_uri",
        "auth_info",
        "usage_states",
        "notification_types",
        "vnfd_id",
        "vnf_pkg_id",
        "operation_states",
        "vnf_products_from_provider",
        "links"
    ]

    list_display = [
        "subscription_id",
        "callback_uri",
        "auth_info",
        "usage_states",
        "notification_types",
        "vnfd_id",
        "vnf_pkg_id",
        "operation_states",
        "vnf_products_from_provider",
        "links"
    ]

    search_fields = (
        "subscription_id",
        "notification_types"
    )


admin.site.register(JobModel)
admin.site.register(JobStatusModel)
