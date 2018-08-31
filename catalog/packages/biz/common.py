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

import os

from catalog.pub.config.config import CATALOG_ROOT_PATH
from catalog.pub.utils import fileutil


def save(remote_file, descriptor_id):
    local_file_name = remote_file.name
    local_file_dir = os.path.join(CATALOG_ROOT_PATH, descriptor_id)
    local_file_name = os.path.join(local_file_dir, local_file_name)
    if not os.path.exists(local_file_dir):
        fileutil.make_dirs(local_file_dir)
    with open(local_file_name, 'wb') as local_file:
        for chunk in remote_file.chunks(chunk_size=1024 * 8):
            local_file.write(chunk)
    return local_file_name
