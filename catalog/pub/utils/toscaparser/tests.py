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
        input_parameters = [{"value": "222222", "key": "sdncontroller"}]
        # vcpe = ["vgw", "infra", "vbng", "vbrgemu", "vgmux"]
        vcpe_part = 'vgw'
        sriov_path = os.path.dirname(os.path.abspath(__file__)) + "/testdata/vnf/vcpesriov"
        csar_file = ("%s/%s.csar" % (sriov_path, vcpe_part))
        logger.debug("csar_file:%s", csar_file)
        vnfd_json = parse_vnfd(csar_file, input_parameters)
        metadata = json.loads(vnfd_json).get("metadata")
        logger.debug("sriov metadata:%s", metadata)
        self.assertEqual(("vCPE_%s" % vcpe_part), metadata.get("template_name", ""))
        if vcpe_part == "infra":
            self.assertEqual("b1bb0ce7-1111-4fa7-95ed-4840d70a1177", json.loads(vnfd_json)["vnf"]["properties"]["descriptor_id"])

        dpdk_path = os.path.dirname(os.path.abspath(__file__)) + "/testdata/vnf/vcpedpdk"
        csar_file = ("%s/%s.csar" % (dpdk_path, vcpe_part))
        logger.debug("csar_file:%s", csar_file)
        vnfd_json = parse_vnfd(csar_file, input_parameters)
        metadata = json.loads(vnfd_json).get("metadata")
        logger.debug("dpdk metadata:%s", metadata)
        self.assertEqual(("vCPE_%s" % vcpe_part), metadata.get("template_name", ""))

    def test_pnfd_parse(self):
        self.remove_temp_dir()
        csar_path = os.path.dirname(os.path.abspath(__file__)) + "/testdata/pnf/ran-du.csar"
        pnfd_json = parse_pnfd(csar_path)
        pnfd_dict = json.loads(pnfd_json)
        metadata = pnfd_dict.get("metadata")
        self.assertEqual("RAN_DU", metadata.get("template_name", ""))
        descriptor_id = pnfd_dict["pnf"]["properties"]["descriptor_id"]
        self.assertEqual(1, descriptor_id)

    def test_nsd_parse(self):
        self.remove_temp_dir()
        # ran_csar = os.path.dirname(os.path.abspath(__file__)) + "/testdata/ns/ran.csar"
        # nsd_json = parse_nsd(ran_csar, [])
        # logger.debug("NS ran json: %s" % nsd_json)
        # metadata = json.loads(nsd_json).get("metadata")
        # self.assertEqual("RAN-NS", metadata.get("nsd_name", ""))

    def test_service_descriptor_parse(self):
        self.remove_temp_dir()
        service_test_csar = os.path.dirname(os.path.abspath(__file__)) + "/testdata/ns/service-vIMS.csar"
        test_json = parse_nsd(service_test_csar, [])
        logger.debug("service-vIMS json: %s" % test_json)
        metadata = json.loads(test_json).get("metadata")
        self.assertEqual("vIMS_v2", metadata.get("nsd_name", ""))

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
