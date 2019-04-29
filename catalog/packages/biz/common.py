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

CHUNK_SIZE = 1024 * 8


def save(remote_file, vnf_pkg_id):
    local_file_name = remote_file.name
    local_file_dir = os.path.join(CATALOG_ROOT_PATH, vnf_pkg_id)
    local_file_name = os.path.join(local_file_dir, local_file_name)
    if not os.path.exists(local_file_dir):
        fileutil.make_dirs(local_file_dir)
    with open(local_file_name, 'wb') as local_file:
        for chunk in remote_file.chunks(chunk_size=CHUNK_SIZE):
            local_file.write(chunk)
    return local_file_name


def read(file_path, start, end):
    fp = open(file_path, 'rb')
    fp.seek(start)
    pos = start
    while pos + CHUNK_SIZE < end:
        yield fp.read(CHUNK_SIZE)
        pos = fp.tell()
    yield fp.read(end - pos)


def parse_file_range(file_path, file_range):
    start, end = 0, os.path.getsize(file_path)
    if file_range:
        [start, range_end] = file_range.split('-')
        range_end = range_end.strip() if range_end.strip() else end
        start, end = int(start.strip()), int(range_end)
    return start, end
