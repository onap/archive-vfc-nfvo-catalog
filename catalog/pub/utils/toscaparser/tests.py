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
import json
import os

from django.test import TestCase

from catalog.pub.utils.toscaparser import parse_vnfd


class TestToscaparser(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_nsd_parse(self):
        csar_path = os.path.dirname(os.path.abspath(__file__)) + "/testdata/resource-ZteMmeFixVl-csar.csar"
        input_parameters = [{"value": "111111", "key": "sdncontroller"}]
        vnfd_json = parse_vnfd(csar_path, input_parameters)
        metadata = json.loads(vnfd_json).get("metadata")
        self.assertEqual("ZTE-MME-FIX-VL", metadata.get("name", ""))
