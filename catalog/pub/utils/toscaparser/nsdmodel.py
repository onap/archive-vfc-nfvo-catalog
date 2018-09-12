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
from catalog.pub.utils.toscaparser.basemodel import BaseInfoModel
logger = logging.getLogger(__name__)

SECTIONS = (NS_TYPE, NS_VNF_TYPE, NS_VL_TYPE, NS_PNF_TYPE, NS_NFP_TYPE, NS_VNFFG_TYPE) = \
    ('tosca.nodes.nfv.NS',
     'tosca.nodes.nfv.VNF',
     'tosca.nodes.nfv.NsVirtualLink',
     'tosca.nodes.nfv.PNF',
     'tosca.nodes.nfv.NFP',
     'tosca.nodes.nfv.VNFFG')


class EtsiNsdInfoModel(BaseInfoModel):

    def __init__(self, path, params):
        super(EtsiNsdInfoModel, self).__init__(path, params)

    def parseModel(self, tosca):
        self.metadata = self.buildMetadata(tosca)
        self.inputs = self.buildInputs(tosca)
        nodeTemplates = map(functools.partial(self.buildNode, tosca=tosca), tosca.nodetemplates)
        types = tosca.topology_template.custom_defs
        self.basepath = self.get_base_path(tosca)
        self.vnfs = self._get_all_vnf(nodeTemplates, types)
        self.pnfs = self._get_all_pnf(nodeTemplates, types)
        self.vls = self._get_all_vl(nodeTemplates, types)
        self.fps = self._get_all_fp(nodeTemplates, types)
        self.vnffgs = self._get_all_vnffg(tosca.topology_template.groups, types)
        self.ns_exposed = self._get_all_endpoint_exposed(tosca.topology_template)
        self.nested_ns = self._get_all_nested_ns(nodeTemplates, types)

    def _get_all_vnf(self, nodeTemplates, node_types):
        vnfs = []
        for node in nodeTemplates:
            if self.isNodeTypeX(node, node_types, NS_VNF_TYPE):
                vnf = {}
                vnf['vnf_id'] = node['name']
                vnf['description'] = node['description']
                vnf['properties'] = node['properties']
                if node['metadata']:
                    vnf['properties']['id'] = node['metadata'].get('UUID', 'undefined')
                vnf['dependencies'] = self._get_networks(node, node_types)
                vnf['networks'] = self._get_networks(node, node_types)
                vnfs.append(vnf)
        return vnfs

    def _get_all_pnf(self, nodeTemplates, node_types):
        pnfs = []
        for node in nodeTemplates:
            if self.isNodeTypeX(node, node_types, NS_PNF_TYPE):
                pnf = {}
                pnf['pnf_id'] = node['name']
                pnf['description'] = node['description']
                pnf['properties'] = node['properties']
                pnf['networks'] = self._get_networks(node, node_types)
                pnfs.append(pnf)
        return pnfs

    def _get_all_vl(self, nodeTemplates, node_types):
        vls = []
        for node in nodeTemplates:
            if self.isNodeTypeX(node, node_types, NS_VL_TYPE):
                vl = dict()
                vl['vl_id'] = node['name']
                vl['description'] = node['description']
                vl['properties'] = node['properties']
                vls.append(vl)
        return vls

    def _get_all_fp(self, nodeTemplates, node_types):
        fps = []
        for node in nodeTemplates:
            if self.isNodeTypeX(node, node_types, NS_NFP_TYPE):
                fp = {}
                fp['fp_id'] = node['name']
                fp['description'] = node['description']
                fp['properties'] = node['properties']
                fp['forwarder_list'] = self._getForwarderList(node, nodeTemplates, node_types)
                fps.append(fp)
        return fps

    def _getForwarderList(self, node, node_templates, node_types):
        forwarderList = []
        if 'requirements' in node:
            for item in node['requirements']:
                for key, value in item.items():
                    if key == 'forwarder':
                        tmpnode = self.get_node_by_req(node_templates, value)
                        type = 'pnf' if self.isNodeTypeX(tmpnode, node_types, NS_PNF_TYPE) else 'vnf'
                        req_node_name = self.get_requirement_node_name(value)
                        if isinstance(value, dict) and 'capability' in value:
                            forwarderList.append(
                                {"type": type, "node_name": req_node_name, "capability": value['capability']})
                        else:
                            forwarderList.append({"type": type, "node_name": req_node_name, "capability": ""})
        return forwarderList

    def _get_all_vnffg(self, groups, group_types):
        vnffgs = []
        for group in groups:
            if self.isGroupTypeX(group, group_types, NS_VNFFG_TYPE):
                vnffg = {}
                vnffg['vnffg_id'] = group.name
                vnffg['description'] = group.description
                if 'properties' in group.tpl:
                    vnffg['properties'] = group.tpl['properties']
                vnffg['members'] = group.members
                vnffgs.append(vnffg)
        return vnffgs

    def _get_all_endpoint_exposed(self, topo_tpl):
        if 'substitution_mappings' in topo_tpl.tpl:
            external_cps = self._get_external_cps(topo_tpl.tpl['substitution_mappings'])
            forward_cps = self._get_forward_cps(topo_tpl.tpl['substitution_mappings'])
            return {"external_cps": external_cps, "forward_cps": forward_cps}
        return {}

    def _get_external_cps(self, subs_mappings):
        external_cps = []
        if 'requirements' in subs_mappings:
            for key, value in subs_mappings['requirements'].items():
                if isinstance(value, list) and len(value) > 0:
                    external_cps.append({"key_name": key, "cpd_id": value[0]})
                else:
                    external_cps.append({"key_name": key, "cpd_id": value})
        return external_cps

    def _get_forward_cps(self, subs_mappings):
        forward_cps = []
        if 'capabilities' in subs_mappings:
            for key, value in subs_mappings['capabilities'].items():
                if isinstance(value, list) and len(value) > 0:
                    forward_cps.append({"key_name": key, "cpd_id": value[0]})
                else:
                    forward_cps.append({"key_name": key, "cpd_id": value})
        return forward_cps

    def _get_all_nested_ns(self, nodes, node_types):
        nss = []
        for node in nodes:
            if self.isNodeTypeX(node, node_types, NS_TYPE):
                ns = {}
                ns['ns_id'] = node['name']
                ns['description'] = node['description']
                ns['properties'] = node['properties']
                ns['networks'] = self._get_networks(node)
                nss.append(ns)
        return nss

    def _get_networks(self, node, node_types):
        rets = []
        if 'requirements' in node and (self.isNodeTypeX(node, node_types, NS_TYPE) or self.isNodeTypeX(node, node_types, NS_VNF_TYPE)):
            for item in node['requirements']:
                for key, value in item.items():
                    rets.append({"key_name": key, "vl_id": self.get_requirement_node_name(value)})
        return rets
