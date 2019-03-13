# Copyright (C) 2019 Verizon. All Rights Reserved
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

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse

from catalog.packages.serializers.response import ProblemDetailsSerializer
from catalog.packages.biz.vnf_pkg_artifacts import FetchVnfPkgArtifact
from catalog.pub.exceptions import ResourceNotFoundException, ArtifactNotFoundException

logger = logging.getLogger(__name__)
VALID_FILTERS = ["callbackUri", "notificationTypes", "vnfdId", "vnfPkgId", "operationalState", "usageState"]


def get_problem_details_serializer(status_code, error_message):
    problem_details = {
        "status": status_code,
        "detail": error_message
    }
    problem_details_serializer = ProblemDetailsSerializer(data=problem_details)
    problem_details_serializer.is_valid()
    return problem_details_serializer


class FetchVnfPkgmArtifactsView(APIView):

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_404_NOT_FOUND: ProblemDetailsSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: ProblemDetailsSerializer()
        }
    )
    def get(self, request, vnfPkgId, artifactPath):
        logger.debug("FetchVnfPkgmArtifactsView--get::> ")
        try:

            resp_data = FetchVnfPkgArtifact().fetch(vnfPkgId, artifactPath)
            response = FileResponse(resp_data)

            return response
        except ResourceNotFoundException as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            problem_details_serializer = get_problem_details_serializer(status.HTTP_404_NOT_FOUND,
                                                                        traceback.format_exc())
            return Response(data=problem_details_serializer.data, status=status.HTTP_404_NOT_FOUND)
        except ArtifactNotFoundException as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            problem_details_serializer = get_problem_details_serializer(status.HTTP_404_NOT_FOUND,
                                                                        traceback.format_exc())
            return Response(data=problem_details_serializer.data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            problem_details_serializer = get_problem_details_serializer(status.HTTP_404_NOT_FOUND,
                                                                        traceback.format_exc())
            return Response(data=problem_details_serializer.data, status=status.HTTP_404_NOT_FOUND)
