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

import functools
import logging
from catalog.pub.config.config import VNFD_SCHEMA_VERSION_DEFAULT
from catalog.pub.utils.toscaparser.basemodel import BaseInfoModel
from catalog.pub.utils.toscaparser.vnfdparser import CreateVnfdSOLParser


logger = logging.getLogger(__name__)

NFV_VNF_RELATIONSHIPS = [["tosca.relationships.nfv.VirtualLinksTo", "tosca.relationships.nfv.VduAttachesTo", "tosca.relationships.nfv.AttachesTo", "tosca.relationships.nfv.Vdu.AttachedTo", "tosca.relationships.DependsOn"],
                         ["tosca.nodes.relationships.VirtualBindsTo", "tosca.relationships.nfv.VirtualBindsTo"]]


class EtsiVnfdInfoModel(BaseInfoModel):

    def __init__(self, path, params):
        self.vnf = {}
        super(EtsiVnfdInfoModel, self).__init__(path, params)

    def parseModel(self, tosca):
        self.metadata = self.buildMetadata(tosca)
        self.inputs = self.buildInputs(tosca)
        nodeTemplates = list(map(functools.partial(self.buildNode, tosca=tosca), tosca.nodetemplates))
        self.basepath = self.get_base_path(tosca)
        node_types = tosca.topology_template.custom_defs
        sol_version = self.metadata.get("VNFD_SCHEMA_VERSION", VNFD_SCHEMA_VERSION_DEFAULT) if isinstance(self.metadata, dict) else VNFD_SCHEMA_VERSION_DEFAULT
        vnfd_sol_parser = CreateVnfdSOLParser(sol_version, self)
        self.vnf = vnfd_sol_parser.build_vnf(tosca)
        self.volume_storages = vnfd_sol_parser.get_all_volume_storage(nodeTemplates, node_types)
        self.vdus = vnfd_sol_parser.get_all_vdu(nodeTemplates, node_types)
        self.vls = vnfd_sol_parser.get_all_vl(nodeTemplates, node_types)
        self.cps = vnfd_sol_parser.get_all_cp(nodeTemplates, node_types)
        self.vnf_exposed = vnfd_sol_parser.get_all_endpoint_exposed()
        self.graph = self.get_deploy_graph(tosca, NFV_VNF_RELATIONSHIPS)
