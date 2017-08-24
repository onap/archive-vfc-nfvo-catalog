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
    url(r'^api/catalog/v1/nspackages$', views.nspackage_get, name='nspackages_get'),
    url(r'^api/catalog/v1/nspackage/(?P<csarId>[0-9a-zA-Z\-\_]+)$', views.nspackage_get, name='nspackage_get'),
    url(r'^api/catalog/v1/nfpackages$', views.nspackage_get, name='nfpackages_get'),
    url(r'^api/catalog/v1/nfpackage/(?P<csarId>[0-9a-zA-Z\-\_]+)$', views.nfpackage_get, name='nfpackage_get'),
]


