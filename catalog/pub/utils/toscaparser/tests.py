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
import logging
import tempfile
import shutil

from django.test import TestCase

from catalog.pub.utils.toscaparser import parse_vnfd, parse_pnfd, parse_nsd
from catalog.pub.utils.toscaparser.graph import Graph

logger = logging.getLogger(__name__)


class TestToscaparser(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_vnfd_parse(self):
        self.remove_temp_dir()
        csar_path = os.path.dirname(os.path.abspath(__file__)) + "/testdata/vnf"
        input_parameters = [{"value": "222222", "key": "sdncontroller"}]
        vcpe = ["vgw"]
        for vcpe_part in vcpe:
            csar_file = ("%s/%s.csar" % (csar_path, vcpe_part))
            logger.debug("csar_file:%s", csar_file)
            vnfd_json = parse_vnfd(csar_file, input_parameters)
            metadata = json.loads(vnfd_json).get("metadata")
            logger.debug("metadata:%s", metadata)
            self.assertEqual(("vCPE_%s" % vcpe_part), metadata.get("template_name", ""))

    def test_pnfd_parse(self):
        self.remove_temp_dir()
        csar_path = os.path.dirname(os.path.abspath(__file__)) + "/testdata/pnf/ran-du.csar"
        pnfd_json = parse_pnfd(csar_path)
        metadata = json.loads(pnfd_json).get("metadata")
        self.assertEqual("RAN_DU", metadata.get("template_name", ""))

    """
    def test_nsd_parse(self):
        self.remove_temp_dir()
        ran_csar = os.path.dirname(os.path.abspath(__file__)) + "/testdata/ns/ran.csar"
        nsd_json = parse_nsd(ran_csar)
        metadata = json.loads(nsd_json).get("metadata")
        self.assertEqual("RAN-NS", metadata.get("template_name", ""))
   """

    def test_service_descriptor_parse(self):
        self.remove_temp_dir()
        service_test_csar = os.path.dirname(os.path.abspath(__file__)) + "/testdata/ns/service-vIMS.csar"
        test_json = parse_nsd(service_test_csar, [], False)
        metadata = json.loads(test_json).get("metadata")
        self.assertEqual("vIMS_v2", metadata.get("name", ""))

    def remove_temp_dir(self):
        tempdir = tempfile.gettempdir()
        for dir in os.listdir(tempdir):
            if dir.startswith("tmp"):
                path = tempfile.tempdir + "/" + dir
                if (not os.path.isfile(path)) and os.path.exists(path):
                    shutil.rmtree(tempfile.tempdir + "/" + dir)

    def test_graph(self):
        data = {
            "cucp": [],
            "du": [],
            "vl_flat_net": ["cucp", "cuup"],
            "vl_ext_net": ["cucp", "cuup"],
            "cuup": []
        }
        graph = Graph(data)
        self.assertEqual(['vl_ext_net', 'vl_flat_net'].sort(), graph.get_pre_nodes("cucp").sort())
