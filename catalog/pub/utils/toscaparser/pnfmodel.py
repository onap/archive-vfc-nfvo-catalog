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

import functools
import logging
from catalog.pub.utils.toscaparser.basemodel import BaseInfoModel
logger = logging.getLogger(__name__)


class PnfdInfoModel(BaseInfoModel):

    def __init__(self, path, params):
        super(PnfdInfoModel, self).__init__(path, params)

    def parseModel(self, tosca):
        self.metadata = self.buidMetadata(tosca)
        self.inputs = self.buildInputs(tosca)
        nodeTemplates = map(functools.partial(self.buildNode, tosca=tosca),
                            tosca.nodetemplates)
        self.basepath = self.get_base_path(tosca)
        self.pnf = {}
        self.get_all_cp(nodeTemplates)

    def get_substitution_mappings(self, tosca):
        pnf_substitution_mappings = tosca.tpl['topology_template']['substitution_mappings']
        if pnf_substitution_mappings:
            self.pnf['type'] = pnf_substitution_mappings['node_type']
            self.pnf['properties'] = pnf_substitution_mappings['properties']

    def get_all_cp(self, nodeTemplates):
        self.pnf['ExtPorts'] = []
        for node in nodeTemplates:
            if self.isPnfExtPort(node):
                cp = {}
                cp['id'] = node['name']
                cp['type'] = node['nodeType']
                cp['properties'] = node['properties']
                self.pnf['ExtPorts'].append(cp)

    def isPnfExtPort(self, node):
        return node['nodeType'].find('tosca.nodes.nfv.PnfExtPort') >= 0
