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

import logging
from catalog.pub.utils.syscomm import fun_name
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

logger = logging.getLogger(__name__)

@api_view(http_method_names=['GET'])
def nspackage_get(request, *args, **kwargs):
    logger.info("Enter method is %s", fun_name())
    ret, normal_status = None, None

    return Response(data=ret, status=status.HTTP_200_OK)

@api_view(http_method_names=['GET'])
def nfpackage_get(request, *args, **kwargs):
    logger.info("Enter method is %s", fun_name())
    ret, normal_status = None, None

    return Response(data=ret, status=status.HTTP_200_OK)



