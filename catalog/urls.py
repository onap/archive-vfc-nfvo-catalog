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
from catalog.pub.config.config import REG_TO_MSB_WHEN_START, REG_TO_MSB_REG_URL, REG_TO_MSB_REG_PARAM

import user_agents
from django.shortcuts import redirect
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


# Add code for generating swagger automatically.
swagger_info = openapi.Info(
    title="Snippets API",
    default_version='v1',
    description="""This is a VFC project for the catalog."""
)

SchemaView = get_schema_view(
    validators=['ssv', 'flex'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def root_redirect(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = user_agents.parse(user_agent_string)
    if user_agent.is_mobile:
        schema_view = 'cschema-redoc'
    else:
        schema_view = 'cschema-swagger-ui'
    return redirect(schema_view, permanent=True)


urlpatterns = [

    # Add code for generating swagger automatically.
    url(r'^swagger(?P<format>.json|.yaml)$', SchemaView.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', SchemaView.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^cached/swagger(?P<format>.json|.yaml)$', SchemaView.without_ui(cache_timeout=None), name='cschema-json'),
    url(r'^cached/swagger/$', SchemaView.with_ui('swagger', cache_timeout=None), name='cschema-swagger-ui'),
    url(r'^cached/redoc/$', SchemaView.with_ui('redoc', cache_timeout=None), name='cschema-redoc'),
    url(r'^$', root_redirect),
    url(r'^', include('catalog.samples.urls')),
    url(r'^', include('catalog.packages.urls')),
    url(r'^', include('catalog.jobs.urls')),
    url(r'^', include('catalog.swagger.urls')),
]

# regist to MSB when startup
if REG_TO_MSB_WHEN_START:
    import json
    from catalog.pub.utils.restcall import req_by_msb
    req_by_msb(REG_TO_MSB_REG_URL, "POST", json.JSONEncoder().encode(REG_TO_MSB_REG_PARAM))
