# Copyright 2017-2018 ZTE Corporation.
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

from django.conf.urls import url

from catalog.packages.views import vnf_package_views
from catalog.packages.views import catalog_views, ns_descriptor_views, pnf_descriptor_views


urlpatterns = [
    url(r'^api/catalog/v1/nspackages$', catalog_views.nspackages_rc, name='nspackages_rc'),
    url(r'^api/catalog/v1/nspackages/(?P<csarId>[0-9a-zA-Z\-\_]+)$', catalog_views.ns_rd_csar, name='nspackage_rd'),
    url(r'^api/catalog/v1/vnfpackages$', catalog_views.nfpackages_rc, name='nfpackages_rc'),
    url(r'^api/catalog/v1/vnfpackages/(?P<csarId>[0-9a-zA-Z\-\_]+)$', catalog_views.nf_rd_csar, name='nfpackage_rd'),
    url(r'^api/catalog/v1/parsernsd$', catalog_views.ns_model_parser, name='nsmodelparser_rc'),
    url(r'^api/catalog/v1/parservnfd$', catalog_views.vnf_model_parser, name='vnfmodelparser_rc'),

    # NSD
    url(r'^api/nsd/v1/ns_descriptors$', ns_descriptor_views.ns_descriptors_rc, name='ns_descriptors_rc'),
    url(r'^api/nsd/v1/ns_descriptors/(?P<nsdInfoId>[0-9a-zA-Z\-\_]+)$', ns_descriptor_views.ns_info_rd, name='ns_info_rd'),
    url(r'^api/nsd/v1/ns_descriptors/(?P<nsdInfoId>[0-9a-zA-Z\-\_]+)/nsd_content$', ns_descriptor_views.nsd_content_ru, name='nsd_content_ru'),
    # url(r'^api/nsd/v1/subscriptions', nsd_subscriptions.as_view(), name='subscriptions_rc'),
    # url(r'^api/nsd/v1/subscriptions/(?P<subscriptionId>[0-9a-zA-Z\-\_]+)$', nsd_subscription.as_view(), name='subscription_rd'),

    # PNF
    url(r'^api/nsd/v1/pnf_descriptors$', pnf_descriptor_views.pnf_descriptors_rc, name='pnf_descriptors_rc'),
    url(r'^api/nsd/v1/pnf_descriptors/(?P<pnfdInfoId>[0-9a-zA-Z\-\_]+)$', pnf_descriptor_views.pnfd_info_rd, name='pnfd_info_rd'),
    url(r'^api/nsd/v1/pnf_descriptors/(?P<pnfdInfoId>[0-9a-zA-Z\-\_]+)/pnfd_content$', pnf_descriptor_views.pnfd_content_ru, name='pnfd_content_ru'),

    # TODO SOL005 & SOL003
    url(r'^api/vnfpkgm/v1/vnf_packages$', vnf_package_views.vnf_packages_rc, name='vnf_packages_rc'),
    url(r'^api/vnfpkgm/v1/vnf_packages/(?P<vnfPkgId>[0-9a-zA-Z\-\_]+)$', vnf_package_views.vnf_package_rd, name='vnf_package_rd'),
    url(r'^api/vnfpkgm/v1/vnf_packages/(?P<vnfPkgId>[0-9a-zA-Z\-\_]+)/package_content$', vnf_package_views.package_content_ru, name='package_content_ru'),
    url(r'^api/vnfpkgm/v1/vnf_packages/(?P<vnfPkgId>[0-9a-zA-Z\-\_]+)/package_content/upload_from_uri$', vnf_package_views.upload_from_uri_c, name='upload_from_uri_c'),
    # url(r'^api/vnfpkgm/v1/vnf_packages/(?P<vnfPkgId>[0-9a-zA-Z\-\_]+)/vnfd$', vnfd.as_view(), name='vnfd_r'),# url(r'^api/vnfpkgm/v1/vnf_packages/(?P<vnfPkgId>[0-9a-zA-Z\-\_]+)/artifacts/artifactPath$', artifacts.as_view(), name='artifacts_r'),
    # url(r'^api/vnfpkgm/v1/subscriptions', vnfpkg_subscriptions.as_view(), name='subscriptions_rc'),
    # url(r'^api/vnfpkgm/v1/subscriptions/(?P<subscriptionId>[0-9a-zA-Z\-\_]+)$', vnfpkg_subscription.as_view(), name='subscription_rd'),
]
