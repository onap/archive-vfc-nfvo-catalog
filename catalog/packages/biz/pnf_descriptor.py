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
import uuid

from catalog.pub.config.config import CATALOG_ROOT_PATH
from catalog.pub.utils import fileutil
from catalog.pub.utils.values import ignore_case_get

logger = logging.getLogger(__name__)


def create(data):
    user_defined_data = ignore_case_get(data, 'userDefinedData')
    data = {
        'id': str(uuid.uuid4()),
        'pnfdOnboardingState': 'CREATED',
        'pnfdUsageState': 'NOT_IN_USE',
        'userDefinedData': user_defined_data,
        '_links': None  # TODO
    }
    return data


def upload(files, pnfd_info_id):
    remote_files = files
    for remote_file in remote_files:
        local_file_name = remote_file.name
        local_file_dir = os.path.join(CATALOG_ROOT_PATH, pnfd_info_id)
        local_file_name = os.path.join(local_file_dir, local_file_name)
        if not os.path.exists(local_file_dir):
            fileutil.make_dirs(local_file_dir)
        with open(local_file_name, 'wb') as local_file:
            if remote_file.multiple_chunks(chunk_size=None):  # TODO: chunk_size
                for chunk in remote_file.chunks():
                    local_file.write(chunk)
            else:
                data = remote_file.read()
                local_file.write(data)
