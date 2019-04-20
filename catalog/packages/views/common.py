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

import traceback
import logging

from rest_framework import status
from rest_framework.response import Response

from catalog.pub.exceptions import CatalogException
from catalog.pub.exceptions import NsdmBadRequestException
from catalog.pub.exceptions import PackageNotFoundException
from catalog.pub.exceptions import ResourceNotFoundException
from catalog.pub.exceptions import ArtifactNotFoundException
from catalog.pub.exceptions import NsdmDuplicateSubscriptionException

logger = logging.getLogger(__name__)


def validate_data(data, serializer):
    serialized_data = serializer(data=data)
    if not serialized_data.is_valid():
        logger.error('Data validation failed.')
        raise CatalogException(serialized_data.errors)
    return serialized_data


def fmt_error_rsp(error_message, status):
    return {"errorMessage": error_message, "error": status}


def make_error_resp(status, detail):
    return Response(
        data={
            'status': status,
            'detail': detail
        },
        status=status
    )


def view_safe_call_with_log(logger):
    def view_safe_call(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except NsdmDuplicateSubscriptionException as e:
                logger.error(e.message)
                return make_error_resp(
                    detail=e.message,
                    status=status.HTTP_303_SEE_OTHER
                )
            except PackageNotFoundException as e:
                logger.error(e.message)
                return make_error_resp(
                    detail=e.message,
                    status=status.HTTP_404_NOT_FOUND
                )
            except ResourceNotFoundException as e:
                logger.error(e.message)
                return make_error_resp(
                    detail=e.message,
                    status=status.HTTP_404_NOT_FOUND
                )
            except ArtifactNotFoundException as e:
                logger.error(e.message)
                return make_error_resp(
                    detail=e.message,
                    status=status.HTTP_404_NOT_FOUND
                )
            except NsdmBadRequestException as e:
                logger.error(e.message)
                return make_error_resp(
                    detail=e.message,
                    status=status.HTTP_400_BAD_REQUEST
                )
            except CatalogException as e:
                logger.error(e.message)
                return make_error_resp(
                    detail=e.message,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except Exception as e:
                logger.error(e.message)
                logger.error(traceback.format_exc())
                return make_error_resp(
                    detail='Unexpected exception',
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return wrapper
    return view_safe_call
