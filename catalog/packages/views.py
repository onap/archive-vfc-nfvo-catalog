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
import traceback
from catalog.pub.utils.syscomm import fun_name
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


@api_view(http_method_names=['GET'])
def package_get(request, *args, **kwargs):
    logger.info("Enter %s%s, method is %s", fun_name(), request.data, request.method)
    ret, normal_status = None, None

    return Response(data=ret, status=status.HTTP_200_OK)



