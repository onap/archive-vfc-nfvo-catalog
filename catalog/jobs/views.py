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

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from catalog.jobs.job_get import GetJobInfoService
from catalog.pub.utils.jobutil import JobUtil
from catalog.pub.utils.values import ignore_case_get
from catalog.serializers import JobResponseSerializer
from catalog.serializers import PostJobResponseResultSerializer
from catalog.serializers import PostJobRequestSerializer

logger = logging.getLogger(__name__)


class JobView(APIView):

    input_job_id = openapi.Parameter('job_id', openapi.IN_QUERY, description="job id", type=openapi.TYPE_STRING)
    input_response_id = openapi.Parameter('responseId', openapi.IN_QUERY, description="response id", type=openapi.TYPE_STRING)

    @swagger_auto_schema(
        operation_description="Get job status",
        manual_parameters=[input_job_id, input_response_id],
        responses={status.HTTP_200_OK: JobResponseSerializer()})
    def get(self, request, job_id):
        response_id = ignore_case_get(request.META, 'responseId')
        ret = GetJobInfoService(job_id, response_id).do_biz()
        return Response(data=ret, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=PostJobRequestSerializer(),
        operation_description="Update job status",
        manual_parameters=[input_job_id],
        responses={
            status.HTTP_202_ACCEPTED: PostJobResponseResultSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: PostJobResponseResultSerializer()
        }
    )
    def post(self, request, job_id):
        try:
            logger.debug("Enter JobView:post, %s, %s ", job_id, request.data)
            jobs = JobUtil.query_job_status(job_id)
            if len(jobs) > 0 and jobs[-1].errcode == '255':
                return Response(data={'result': 'ok'})
            progress = request.data.get('progress')
            desc = request.data.get('desc', '%s' % progress)
            errcode = '0' if request.data.get('errcode') in ('true', 'active') else '255'
            logger.debug("errcode=%s", errcode)
            JobUtil.add_job_status(job_id, progress, desc, error_code=errcode)
            return Response(data={'result': 'ok'}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            return Response(data={'result': 'error', 'msg': e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
