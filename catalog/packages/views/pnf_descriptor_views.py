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
import os
import traceback

from django.http import FileResponse

from catalog.packages.biz.pnf_descriptor import create, delete_single, download, query_multiple, query_single, upload
from catalog.packages.serializers.create_pnfd_info_request import CreatePnfdInfoRequestSerializer
from catalog.packages.serializers.pnfd_info import PnfdInfoSerializer
from catalog.packages.serializers.pnfd_infos import PnfdInfosSerializer
from catalog.pub.exceptions import CatalogException, ResourceNotFoundException
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method='GET',
    operation_description="Query a PNFD",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: PnfdInfoSerializer(),
        status.HTTP_404_NOT_FOUND: "PNFD does not exist.",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete a PNFD",
    request_body=no_body,
    responses={
        status.HTTP_204_NO_CONTENT: None,
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['GET', 'DELETE'])
def pnfd_info_rd(request, pnfdInfoId):  # TODO
    if request.method == 'GET':
        logger.debug("Query an individual PNF descriptor> %s" % request.data)
        try:
            data = query_single(pnfdInfoId)
            pnfd_info = validate_data(data, PnfdInfoSerializer)
            return Response(data=pnfd_info.data, status=status.HTTP_200_OK)
        except ResourceNotFoundException as e:
            logger.error(e.message)
            return Response(data={'error': "PNFD does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except CatalogException as e:
            logger.error(e.message)
            error_msg = {'error': 'Query of a PNFD failed.'}
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_msg = {'error': 'Query of a PNFD failed.'}
        return Response(data=error_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'DELETE':
        logger.debug("Delete an individual PNFD resource> %s" % request.data)
        try:
            delete_single(pnfdInfoId)
            return Response(data=None, status=status.HTTP_204_NO_CONTENT)
        except CatalogException as e:
            logger.error(e.message)
            error_msg = {'error': 'Deletion of a PNFD failed.'}
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_msg = {'error': 'Deletion of a PNFD failed.'}
        return Response(data=error_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='POST',
    operation_description="Create a  PNFD",
    request_body=CreatePnfdInfoRequestSerializer(),
    responses={
        status.HTTP_201_CREATED: PnfdInfoSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@swagger_auto_schema(
    method='GET',
    operation_description="Query multiple PNFDs",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: PnfdInfosSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['POST', 'GET'])
def pnf_descriptors_rc(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            create_pnfd_info_request = validate_data(request.data, CreatePnfdInfoRequestSerializer)
            data = create(create_pnfd_info_request.data)
            pnfd_info = validate_data(data, PnfdInfoSerializer)
            return Response(data=pnfd_info.data, status=status.HTTP_201_CREATED)
        except CatalogException as e:
            logger.error(e.message)
            error_msg = {'error': 'Creating a pnfd failed.'}
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_msg = {'error': 'Creating a pnfd failed.'}
        return Response(data=error_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'GET':
        try:
            data = query_multiple()
            pnfd_infos = validate_data(data, PnfdInfosSerializer)
            return Response(data=pnfd_infos.data, status=status.HTTP_200_OK)
        except CatalogException as e:
            logger.error(e.message)
            error_msg = {'error': 'Query of multiple PNFDs failed.'}
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_msg = {'error': 'Query of multiple PNFDs failed.'}
        return Response(data=error_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='PUT',
    operation_description="Upload PNFD content",
    request_body=no_body,
    responses={
        status.HTTP_204_NO_CONTENT: None,
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@swagger_auto_schema(
    method='GET',
    operation_description="Fetch PNFD content",
    request_body=no_body,
    responses={
        status.HTTP_204_NO_CONTENT: 'PNFD file',
        status.HTTP_404_NOT_FOUND: "PNFD does not exist.",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['PUT', 'GET'])
def pnfd_content_ru(request, *args, **kwargs):
    pnfd_info_id = kwargs.get("pnfdInfoId")
    if request.method == 'PUT':
        files = request.FILES.getlist('file')
        try:
            upload(files[0], pnfd_info_id)
            return Response(data=None, status=status.HTTP_204_NO_CONTENT)
        except CatalogException as e:
            logger.error(e.message)
            error_msg = {'error': 'Uploading PNFD content failed.'}
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_msg = {'error': 'Uploading PNFD content failed.'}
        return Response(data=error_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'GET':
        try:
            file_path = download(pnfd_info_id)
            file_name = file_path.split('/')[-1]
            file_name = file_name.split('\\')[-1]
            response = FileResponse(open(file_path, 'rb'), status=status.HTTP_200_OK)
            response['Content-Disposition'] = 'attachment; filename=%s' % file_name.encode('utf-8')
            response['Content-Length'] = os.path.getsize(file_path)
            return response
        except ResourceNotFoundException as e:
            logger.error(e.message)
            return Response(data={'error': "PNFD does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except CatalogException as e:
            logger.error(e.message)
            error_msg = {'error': 'Downloading PNFD content failed.'}
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_msg = {'error': 'Downloading PNFD content failed.'}
        return Response(data=error_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def validate_data(data, serializer):
    serialized_data = serializer(data=data)
    if not serialized_data.is_valid():
        logger.error('Data validation failed.')
        raise CatalogException(serialized_data.error)
    return serialized_data
