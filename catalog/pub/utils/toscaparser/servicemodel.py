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
from catalog.pub.utils.toscaparser.const import NS_METADATA_SECTIONS, PNF_METADATA_SECTIONS, VNF_SECTIONS, PNF_SECTIONS, VL_SECTIONS
from catalog.pub.utils.toscaparser.basemodel import BaseInfoModel
logger = logging.getLogger(__name__)

SDC_SERVICE_SECTIONS = (SERVICE_TYPE, SRV_DESCRIPTION) = (
    'org.openecomp.resource.abstract.nodes.service', 'description')

SDC_SERVICE_METADATA_SECTIONS = (SRV_UUID, SRV_INVARIANTUUID, SRV_NAME) = (
    'UUID', 'invariantUUID', 'name')

SDC_VL = (VL_TYPE) = ('nfv.ext.zte.VL')
SDC_VL_SECTIONS = (VL_ID, VL_METADATA, VL_PROPERTIES, VL_DESCRIPTION) = \
    ("name", "metadata", "properties", "description")

SDC_VF = (VF_TYPE, VF_UUID) = \
    ('org.openecomp.resource.abstract.nodes.VF', 'UUID')
SDC_VF_SECTIONS = (VF_ID, VF_METADATA, VF_PROPERTIES, VF_DESCRIPTION) = \
    ("name", "metadata", "properties", "description")

SDC_PNF = (PNF_TYPE) = \
    ('org.openecomp.resource.abstract.nodes.PNF')
SDC_PNF_METADATA_SECTIONS = (SDC_PNF_UUID, SDC_PNF_INVARIANTUUID, SDC_PNF_NAME, SDC_PNF_METADATA_DESCRIPTION, SDC_PNF_VERSION) = \
    ("UUID", "invariantUUID", "name", "description", "version")
SDC_PNF_SECTIONS = (SDC_PNF_ID, SDC_PNF_METADATA, SDC_PNF_PROPERTIES, SDC_PNF_DESCRIPTION) = \
    ("name", "metadata", "properties", "description")

SERVICE_RELATIONSHIPS = [["tosca.relationships.network.LinksTo", "tosca.relationships.nfv.VirtualLinksTo", "tosca.capabilities.nfv.VirtualLinkable", "tosca.relationships.DependsOn"], []]


class SdcServiceModel(BaseInfoModel):

    def __init__(self, path, params):
        super(SdcServiceModel, self).__init__(path, params)

    def parseModel(self, tosca):
        self.metadata = self._buildServiceMetadata(tosca)
        self.inputs = self.buildInputs(tosca)
        if hasattr(tosca, 'nodetemplates'):
            nodeTemplates = map(functools.partial(self.buildNode, tosca=tosca), tosca.nodetemplates)
            types = tosca.topology_template.custom_defs
            self.basepath = self.get_base_path(tosca)
            self.vnfs = self._get_all_vnf(nodeTemplates, types)
            self.pnfs = self._get_all_pnf(nodeTemplates, types)
            self.vls = self._get_all_vl(nodeTemplates, types)
            self.graph = self.get_deploy_graph(tosca, SERVICE_RELATIONSHIPS)

    def _buildServiceMetadata(self, tosca):
        """ SDC service Meta Format
         invariantUUID: e2618ee1 - a29a - 44c4 - a52a - b718fe1269f4
         UUID: 2362d14a - 115f - 4a2b - b449 - e2f93c0b7c89
         name: demoVLB
         description: catalogservicedescription
         type: Service
         category: NetworkL1 - 3
         serviceType: ''
         serviceRole: ''
         serviceEcompNaming: true
         ecompGeneratedNaming: true
         namingPolicy: ''
        """
        metadata_temp = self.buildMetadata(tosca)
        metadata = {}
        return self.setTargetValues(metadata, NS_METADATA_SECTIONS, metadata_temp, SDC_SERVICE_METADATA_SECTIONS)

    def _get_all_vnf(self, nodeTemplates, node_types):
        """  SDC Resource Metadata
        invariantUUID: 9ed46ddc-8eb7-4cb0-a1b6-04136c921af4
        UUID: b56ba35d-45fb-41e3-b6b8-b4f66917baa1
        customizationUUID: af0a6e64-967b-476b-87bc-959dcf59c305
        version: '1.0'
        name: b7d2fceb-dd11-43cd-a3fa
        description: vendor software product
        type: VF
        category: Generic
        subcategory: Abstract
        resourceVendor: b9d9f9f7-7994-4f0d-8104
        resourceVendorRelease: '1.0'
        resourceVendorModelNumber: ''
        """
        vnfs = []
        for node in nodeTemplates:
            if self.isNodeTypeX(node, node_types, VF_TYPE):
                vnf = {}
                self.setTargetValues(vnf, VNF_SECTIONS, node, SDC_VF_SECTIONS)
                if not vnf['properties'].get('id', None):
                    vnf['properties']['id'] = vnf['properties'].get('descriptor_id',None)
                if not vnf['properties'].get('id', None) and node['metadata']:
                    vnf['properties']['id'] = node['metadata'].get('UUID', None)
                vnf['dependencies'] = self._get_networks(node, node_types)
                vnf['networks'] = self._get_networks(node, node_types)
                vnfs.append(vnf)
        return vnfs

    def _get_all_pnf(self, nodeTemplates, node_types):
        pnfs = []
        for node in nodeTemplates:
            if self.isNodeTypeX(node, node_types, PNF_TYPE):
                pnf = {}
                self.setTargetValues(pnf, PNF_SECTIONS, node, SDC_PNF_SECTIONS)
                self.setTargetValues(pnf['properties'], PNF_METADATA_SECTIONS, node['metadata'], SDC_PNF_METADATA_SECTIONS)
                pnf['networks'] = self._get_networks(node, node_types)
                pnfs.append(pnf)
        return pnfs

    def _get_all_vl(self, nodeTemplates, node_types):
        vls = []
        for node in nodeTemplates:
            if self.isNodeTypeX(node, node_types, VL_TYPE):
                vl = {}
                self.setTargetValues(vl, VL_SECTIONS, node, SDC_VL_SECTIONS)
                vls.append(vl)
        return vls

    def _get_networks(self, node, node_types):
        rets = []
        if 'requirements' in node and self.isNodeTypeX(node, node_types, VF_TYPE):
            for item in node['requirements']:
                for key, value in item.items():
                    rets.append({"key_name": key, "vl_id": self.get_requirement_node_name(value)})
        return rets
