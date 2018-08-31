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

from catalog.pub.utils.toscaparser.basemodel import BaseInfoModel


class EtsiNsdInfoModel(BaseInfoModel):

    def __init__(self, path, params):
        tosca = self.buildToscaTemplate(path, params)
        self.parseModel(tosca)

    def parseModel(self, tosca):
        self.buidMetadata(tosca)
        if hasattr(tosca, 'topology_template') and hasattr(tosca.topology_template, 'inputs'):
            self.inputs = self.buildInputs(tosca.topology_template.inputs)

        nodeTemplates = map(functools.partial(self.buildNode, tosca=tosca),
                            tosca.nodetemplates)
        node_types = tosca.topology_template.custom_defs
        self.vnfs = self._get_all_vnf(nodeTemplates)
        self.pnfs = self._get_all_pnf(nodeTemplates)
        self.vls = self.get_all_vl(nodeTemplates, node_types)
        self.cps = self.get_all_cp(nodeTemplates, node_types)
        self.routers = self.get_all_router(nodeTemplates)
        self.fps = self._get_all_fp(nodeTemplates, node_types)
        self.vnffgs = self._get_all_vnffg(tosca.topology_template.groups)
        self.server_groups = self.get_all_server_group(tosca.topology_template.groups)
        self.ns_exposed = self.get_all_endpoint_exposed(tosca.topology_template)
        self.policies = self._get_policies_scaling(tosca.topology_template.policies)
        self.ns_flavours = self.get_all_flavour(tosca.topology_template.groups)
        self.nested_ns = self.get_all_nested_ns(nodeTemplates)

    def buildInputs(self, top_inputs):
        ret = {}
        for tmpinput in top_inputs:
            tmp = {}
            tmp['type'] = tmpinput.type
            tmp['description'] = tmpinput.description
            tmp['default'] = tmpinput.default

            ret[tmpinput.name] = tmp
        return ret

    def buildNode(self, nodeTemplate, tosca):
        inputs = tosca.inputs
        parsed_params = tosca.parsed_params
        ret = {}
        ret['name'] = nodeTemplate.name
        ret['nodeType'] = nodeTemplate.type
        if 'description' in nodeTemplate.entity_tpl:
            ret['description'] = nodeTemplate.entity_tpl['description']
        else:
            ret['description'] = ''
        if 'metadata' in nodeTemplate.entity_tpl:
            ret['metadata'] = nodeTemplate.entity_tpl['metadata']
        else:
            ret['metadata'] = ''
        props = self.buildProperties_ex(nodeTemplate, tosca.topology_template)
        ret['properties'] = self.verify_properties(props, inputs, parsed_params)
        ret['requirements'] = self.build_requirements(nodeTemplate)
        self.buildCapabilities(nodeTemplate, inputs, ret)
        self.buildArtifacts(nodeTemplate, inputs, ret)
        interfaces = self.build_interfaces(nodeTemplate)
        if interfaces:
            ret['interfaces'] = interfaces
        return ret

    def _get_all_vnf(self, nodeTemplates):
        vnfs = []
        for node in nodeTemplates:
            if self.isVnf(node):
                vnf = {}
                vnf['vnf_id'] = node['name']
                vnf['description'] = node['description']
                vnf['properties'] = node['properties']
                vnf['properties']['id'] = node['metadata'].get('UUID', 'undefined')
                # for key in vnf['properties'].iterkeys():
                #     if key.endswith('_version'):
                #         vnf['properties'].update(version=vnf['properties'].pop(key))
                #     if key.endswith('_id'):
                #         vnf['properties'].update(id=vnf['properties'].pop(key))
                #     if key.endswith('_csarProvider'):
                #         vnf['properties'].update(csarProvider=vnf['properties'].pop(key))
                #     if key.endswith('_csarVersion'):
                #         vnf['properties'].update(csarVersion=vnf['properties'].pop(key))
                #     if key.endswith('_vendor'):
                #         vnf['properties'].update(vendor=vnf['properties'].pop(key))
                #     if key.endswith('_csarType'):
                #         vnf['properties'].update(csarType=vnf['properties'].pop(key))
                #     if key.endswith('_vnfm_type') or key.endswith('_vnfmType'):
                #         vnf['properties'].update(vnfmType=vnf['properties'].pop(key))
                # vnf['dependencies'] = map(lambda x: self.get_requirement_node_name(x), self.getNodeDependencys(node))
                vnf['dependencies'] = self.get_networks(node)
                vnf['networks'] = self.get_networks(node)

                vnfs.append(vnf)
        return vnfs

    def _get_all_pnf(self, nodeTemplates):
        pnfs = []
        for node in nodeTemplates:
            if self.isPnf(node):
                pnf = {}
                pnf['pnf_id'] = node['name']
                pnf['description'] = node['description']
                pnf['properties'] = node['properties']
                pnf['cps'] = self.getVirtalBindingCpIds(node, nodeTemplates)

                pnfs.append(pnf)
        return pnfs

    def getVirtalBindingCpIds(self, node, nodeTemplates):
        return map(lambda x: x['name'], self.getVirtalBindingCps(node, nodeTemplates))

    def getVirtalBindingCps(self, node, nodeTemplates):
        cps = []
        for tmpnode in nodeTemplates:
            if 'requirements' in tmpnode:
                for item in tmpnode['requirements']:
                    for key, value in item.items():
                        if key.upper().startswith('VIRTUAL_BINDING'):
                            req_node_name = self.get_requirement_node_name(value)
                            if req_node_name is not None and req_node_name == node['name']:
                                cps.append(tmpnode)
        return cps

    def get_all_vl(self, nodeTemplates, node_types):
        vls = []
        for node in nodeTemplates:
            if self.isVl(node, node_types) or self._isExternalVL(node):
                vl = dict()
                vl['vl_id'] = node['name']
                vl['description'] = node['description']
                vl['properties'] = node['properties']
                vl['route_external'] = False if self.isVl(node, node_types) else True
                # vl['route_id'] = self._get_vl_route_id(node)
                vls.append(vl)
        return vls

    def _get_vl_route_id(self, node):
        route_ids = map(lambda x: self.get_requirement_node_name(x),
                        self.getRequirementByName(node, 'virtual_route'))
        if len(route_ids) > 0:
            return route_ids[0]
        return ""

    def _isExternalVL(self, node):
        return node['nodeType'].upper().find('.ROUTEEXTERNALVL') >= 0

    def get_all_cp(self, nodeTemplates, node_types):
        cps = []
        for node in nodeTemplates:
            if self.isCp(node, node_types):
                cp = {}
                cp['cp_id'] = node['name']
                cp['cpd_id'] = node['name']
                cp['description'] = node['description']
                cp['properties'] = node['properties']
                cp['vl_id'] = self.get_node_vl_id(node)
                binding_node_ids = map(lambda x: self.get_requirement_node_name(x), self.getVirtualbindings(node))
                #                 cp['vnf_id'] = self._filter_vnf_id(binding_node_ids, nodeTemplates)
                cp['pnf_id'] = self._filter_pnf_id(binding_node_ids, nodeTemplates)
                vls = self.buil_cp_vls(node)
                if len(vls) > 1:
                    cp['vls'] = vls
                cps.append(cp)
        return cps

    def buil_cp_vls(self, node):
        return map(lambda x: self._build_cp_vl(x), self.getVirtualLinks(node))

    def _build_cp_vl(self, req):
        cp_vl = {}
        cp_vl['vl_id'] = self.get_prop_from_obj(req, 'node')
        relationship = self.get_prop_from_obj(req, 'relationship')
        if relationship is not None:
            properties = self.get_prop_from_obj(relationship, 'properties')
            if properties is not None and isinstance(properties, dict):
                for key, value in properties.items():
                    cp_vl[key] = value
        return cp_vl

    def _filter_pnf_id(self, node_ids, node_templates):
        for node_id in node_ids:
            node = self.get_node_by_name(node_templates, node_id)
            if self.isPnf(node):
                return node_id
        return ""

    def get_all_router(self, nodeTemplates):
        rets = []
        for node in nodeTemplates:
            if self._isRouter(node):
                ret = {}
                ret['router_id'] = node['name']
                ret['description'] = node['description']
                ret['properties'] = node['properties']
                ret['external_vl_id'] = self._get_router_external_vl_id(node)
                ret['external_ip_addresses'] = self._get_external_ip_addresses(node)

                rets.append(ret)
        return rets

    def _isRouter(self, node):
        return node['nodeType'].upper().find('.ROUTER.') >= 0 or node['nodeType'].upper().endswith('.ROUTER')

    def _get_router_external_vl(self, node):
        return self.getRequirementByName(node, 'external_virtual_link')

    def _get_router_external_vl_id(self, node):
        ids = map(lambda x: self.get_requirement_node_name(x), self._get_router_external_vl(node))
        if len(ids) > 0:
            return ids[0]
        return ""

    def _get_external_ip_addresses(self, node):
        external_vls = self._get_router_external_vl(node)
        if len(external_vls) > 0:
            if 'relationship' in external_vls[0] and 'properties' in external_vls[0]['relationship'] and 'router_ip_address' in external_vls[0]['relationship']['properties']:
                return external_vls[0]['relationship']['properties']['router_ip_address']
        return []

    def _get_all_fp(self, nodeTemplates, node_types):
        fps = []
        for node in nodeTemplates:
            if self._isFp(node):
                fp = {}
                fp['fp_id'] = node['name']
                fp['description'] = node['description']
                fp['properties'] = node['properties']
                fp['forwarder_list'] = self._getForwarderList(node, nodeTemplates, node_types)

                fps.append(fp)
        return fps

    def _isFp(self, node):
        return node['nodeType'].upper().find('.FP.') >= 0 or node['nodeType'].upper().find('.SFP.') >= 0 or node[
            'nodeType'].upper().endswith('.FP') or node['nodeType'].upper().endswith('.SFP')

    def _getForwarderList(self, node, node_templates, node_types):
        forwarderList = []
        if 'requirements' in node:
            for item in node['requirements']:
                for key, value in item.items():
                    if key == 'forwarder':
                        tmpnode = self.get_node_by_req(node_templates, value)
                        type = 'cp' if self.isCp(tmpnode, node_types) else 'vnf'
                        req_node_name = self.get_requirement_node_name(value)
                        if isinstance(value, dict) and 'capability' in value:
                            forwarderList.append(
                                {"type": type, "node_name": req_node_name, "capability": value['capability']})
                        else:
                            forwarderList.append({"type": type, "node_name": req_node_name, "capability": ""})

        return forwarderList

    def get_node_by_req(self, node_templates, req):
        req_node_name = self.get_requirement_node_name(req)
        return self.get_node_by_name(node_templates, req_node_name)

    def _get_all_vnffg(self, groups):
        vnffgs = []
        for group in groups:
            if self._isVnffg(group):
                vnffg = {}
                vnffg['vnffg_id'] = group.name
                vnffg['description'] = group.description
                if 'properties' in group.tpl:
                    vnffg['properties'] = group.tpl['properties']
                vnffg['members'] = group.members

                vnffgs.append(vnffg)
        return vnffgs

    def _isVnffg(self, group):
        return group.type.upper().find('.VNFFG.') >= 0 or group.type.upper().find(
            '.SFC.') >= 0 or group.type.upper().endswith('.VNFFG') or group.type.upper().endswith('.SFC')

    def get_all_server_group(self, groups):
        rets = []
        for group in groups:
            if self._isServerGroup(group):
                ret = {}
                ret['group_id'] = group.name
                ret['description'] = group.description
                if 'properties' in group.tpl:
                    ret['properties'] = group.tpl['properties']
                ret['members'] = group.members

                rets.append(ret)
        return rets

    def _isServerGroup(self, group):
        return group.type.upper().find('.AFFINITYORANTIAFFINITYGROUP.') >= 0 or group.type.upper().endswith(
            '.AFFINITYORANTIAFFINITYGROUP')

    def get_all_endpoint_exposed(self, topo_tpl):
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

    def _get_policies_scaling(self, top_policies):
        policies_scaling = []
        scaling_policies = self.get_scaling_policies(top_policies)
        if len(scaling_policies) > 0:
            policies_scaling.append({"scaling": scaling_policies})
        return policies_scaling

    def get_policies_by_keyword(self, top_policies, keyword):
        ret = []
        for policy in top_policies:
            if policy.type.upper().find(keyword) >= 0:
                tmp = {}
                tmp['policy_id'] = policy.name
                tmp['description'] = policy.description
                if 'properties' in policy.entity_tpl:
                    tmp['properties'] = policy.entity_tpl['properties']
                tmp['targets'] = policy.targets
                ret.append(tmp)

        return ret

    def get_scaling_policies(self, top_policies):
        return self.get_policies_by_keyword(top_policies, '.SCALING')

    def get_all_flavour(self, groups):
        rets = []
        for group in groups:
            if self._isFlavour(group):
                ret = {}
                ret['flavour_id'] = group.name
                ret['description'] = group.description
                if 'properties' in group.tpl:
                    ret['properties'] = group.tpl['properties']
                ret['members'] = group.members

                rets.append(ret)
        return rets

    def _isFlavour(self, group):
        return group.type.upper().find('FLAVOUR') >= 0