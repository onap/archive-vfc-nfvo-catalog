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

import logging
import traceback

from django.http import StreamingHttpResponse
from catalog.packages.biz.ns_descriptor import NsDescriptor, parse_nsd_and_save, handle_upload_failed
from catalog.packages.serializers.create_nsd_info_request import CreateNsdInfoRequestSerializer
from catalog.packages.serializers.nsd_info import NsdInfoSerializer
from catalog.packages.serializers.nsd_infos import NsdInfosSerializer
from catalog.pub.exceptions import CatalogException, ResourceNotFoundException
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger(__name__)


@swagger_auto_schema(
    method='GET',
    operation_description="Query a NSD",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: NsdInfoSerializer(),
        status.HTTP_404_NOT_FOUND: 'NSDs do not exist.',
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete a NSD",
    request_body=no_body,
    responses={
        status.HTTP_204_NO_CONTENT: None,
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['GET', 'DELETE'])
def ns_info_rd(request, nsdInfoId):   # TODO
    if request.method == 'GET':
        try:
            data = NsDescriptor().query_single(nsdInfoId)
            nsd_info = validate_data(data, NsdInfoSerializer)
            return Response(data=nsd_info.data, status=status.HTTP_200_OK)
        except ResourceNotFoundException as e:
            logger.error(e.message)
            return Response(data={'error': 'NSDs do not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_msg = {'error': 'Query of a NSD failed.'}
        return Response(data=error_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'DELETE':
        try:
            NsDescriptor().delete_single(nsdInfoId)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CatalogException as e:
            logger.error(e.message)
            error_msg = {'error': 'Deletion of a NSD failed.'}
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_msg = {'error': 'Deletion of a NSD failed.'}
        return Response(data=error_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='POST',
    operation_description="Create a NSD",
    request_body=CreateNsdInfoRequestSerializer(),
    responses={
        status.HTTP_201_CREATED: NsdInfoSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@swagger_auto_schema(
    method='GET',
    operation_description="Query multiple NSDs",
    request_body=no_body,
    responses={
        status.HTTP_200_OK: NsdInfosSerializer(),
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['POST', 'GET'])
def ns_descriptors_rc(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            create_nsd_info_requst = validate_data(request.data, CreateNsdInfoRequestSerializer)
            data = NsDescriptor().create(create_nsd_info_requst.data)
            nsd_info = validate_data(data, NsdInfoSerializer)
            return Response(data=nsd_info.data, status=status.HTTP_201_CREATED)
        except CatalogException as e:
            logger.error(e.message)
            error_msg = {'error': 'Creating a NSD failed.'}
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_msg = {'error': 'Creating a NSD failed.'}
        return Response(data=error_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'GET':
        try:
            data = NsDescriptor().query_multiple()
            nsd_infos = validate_data(data, NsdInfosSerializer)
            return Response(data=nsd_infos.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_msg = {'error': 'Query of multiple NSDs failed.'}
        return Response(data=error_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='PUT',
    operation_description="Upload NSD content",
    request_body=no_body,
    responses={
        status.HTTP_204_NO_CONTENT: 'PNFD file',
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@swagger_auto_schema(
    method='GET',
    operation_description="Download NSD content",
    request_body=no_body,
    responses={
        status.HTTP_204_NO_CONTENT: None,
        status.HTTP_404_NOT_FOUND: 'NSD does not exist.',
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal error"
    }
)
@api_view(http_method_names=['PUT', 'GET'])
def nsd_content_ru(request, *args, **kwargs):
    nsd_info_id = kwargs.get("nsdInfoId")
    if request.method == 'PUT':
        files = request.FILES.getlist('file')
        try:
            local_file_name = NsDescriptor().upload(files[0], nsd_info_id)
            parse_nsd_and_save(nsd_info_id, local_file_name)
            return Response(data=None, status=status.HTTP_204_NO_CONTENT)
        except CatalogException as e:
            handle_upload_failed(nsd_info_id)
            logger.error(e.message)
            error_msg = {'error': 'Uploading NSD content failed.'}
        except Exception as e:
            handle_upload_failed(nsd_info_id)
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_msg = {'error': 'Uploading NSD content failed.'}
        return Response(data=error_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'GET':
        try:
            file_path, file_name, file_size = NsDescriptor().download(nsd_info_id)
            start, end = 0, file_size
            file_range = request.META.get('RANGE')
            if file_range:
                [start, end] = file_range.split('-')
                start, end = start.strip(), end.strip()
                start, end = int(start), int(end)
            response = StreamingHttpResponse(
                read_partial_file(file_path, start, end),
                status=status.HTTP_200_OK
            )
            response['Content-Range'] = '%s-%s' % (start, end)
            response['Content-Disposition'] = 'attachment; filename=%s' % file_name.encode('utf-8')
            response['Content-Length'] = end - start
            return response
        except ResourceNotFoundException as e:
            logger.error(e.message)
            return Response(data={'error': 'NSD does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except CatalogException as e:
            logger.error(e.message)
            error_msg = {'error': 'Downloading NSD content failed.'}
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            error_msg = {'error': 'Downloading NSD content failed.'}
        return Response(data=error_msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def read_partial_file(file_path, start, end):
    fp = open(file_path, 'rb')
    fp.seek(start)
    pos = start
    CHUNK_SIZE = 1024 * 8
    while pos + CHUNK_SIZE < end:
        yield fp.read(CHUNK_SIZE)
        pos = fp.tell()
    yield fp.read(end - pos)


def validate_data(data, serializer):
    serialized_data = serializer(data=data)
    if not serialized_data.is_valid():
        logger.error('Data validation failed.')
        raise CatalogException(serialized_data.errors)
    return serialized_data
