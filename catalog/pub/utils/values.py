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


def ignore_case_get(args, key, def_val=""):
    if not key:
        return def_val
    if key in args:
        return args[key]
    for old_key in args:
        if old_key.upper() == key.upper():
            return args[old_key]
    return def_val


def remove_none_key(data, none_list=None):
    none_list = none_list if none_list else [None, '', 'NULL', 'None', [], {}]
    if isinstance(data, dict):
        data = dict([(k, remove_none_key(v, none_list)) for k, v in list(data.items()) if v not in none_list])
    if isinstance(data, list):
        data = [remove_none_key(s, none_list) for s in data if s not in none_list]
    return data
