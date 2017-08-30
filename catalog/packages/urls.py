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

from django.conf.urls import include, url
from catalog.packages import views

urlpatterns = [
    url(r'^api/catalog/v1/nspackages$', views.nspackages_rc, name='nspackages_rc'),
    url(r'^api/catalog/v1/nspackages/(?P<csarId>[0-9a-zA-Z\-\_]+)$', views.ns_rd_csar, name='nspackage_rd'),
    url(r'^api/catalog/v1/vnfpackages$', views.nfpackages_rc, name='nfpackages_rc'),
    url(r'^api/catalog/v1/vnfpackages/(?P<csarId>[0-9a-zA-Z\-\_]+)$', views.nf_rd_csar, name='nfpackage_rd'),
]


