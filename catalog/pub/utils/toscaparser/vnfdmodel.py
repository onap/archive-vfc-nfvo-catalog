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
import os
from catalog.pub.utils.toscaparser.basemodel import BaseInfoModel
# from catalog.pub.exceptions import CatalogException

logger = logging.getLogger(__name__)

SECTIONS = (VDU_COMPUTE_TYPE, VNF_VL_TYPE, VDU_CP_TYPE, VDU_STORAGE_TYPE) = \
           ('tosca.nodes.nfv.Vdu.Compute', 'tosca.nodes.nfv.VnfVirtualLink', 'tosca.nodes.nfv.VduCp', 'tosca.nodes.nfv.Vdu.VirtualStorage')

NFV_VNF_RELATIONSHIPS = [["tosca.relationships.nfv.VirtualLinksTo", "tosca.relationships.nfv.VduAttachesTo", "tosca.relationships.nfv.AttachesTo", "tosca.relationships.nfv.Vdu.AttachedTo", "tosca.relationships.DependsOn"],
                         ["tosca.nodes.relationships.VirtualBindsTo", "tosca.relationships.nfv.VirtualBindsTo"]]


class EtsiVnfdInfoModel(BaseInfoModel):

    def __init__(self, path, params):
        super(EtsiVnfdInfoModel, self).__init__(path, params)

    def parseModel(self, tosca):
        self.vnf = {}
        self.vnf = self._build_vnf(tosca)
        self.metadata = self.buildMetadata(tosca)
        self.inputs = self.buildInputs(tosca)
        nodeTemplates = map(functools.partial(self.buildNode, tosca=tosca),
                            tosca.nodetemplates)
        node_types = tosca.topology_template.custom_defs
        self.basepath = self.get_base_path(tosca)
        self.volume_storages = self._get_all_volume_storage(nodeTemplates, node_types)
        self.vdus = self._get_all_vdu(nodeTemplates, node_types)
        self.vls = self._get_all_vl(nodeTemplates, node_types)
        self.cps = self._get_all_cp(nodeTemplates, node_types)
        self.vnf_exposed = self._get_all_endpoint_exposed()
        self.graph = self.get_deploy_graph(tosca, NFV_VNF_RELATIONSHIPS)

    def _get_all_volume_storage(self, nodeTemplates, node_types):
        rets = []
        for node in nodeTemplates:
            if self.isNodeTypeX(node, node_types, VDU_STORAGE_TYPE):
                ret = {}
                ret['volume_storage_id'] = node['name']
                if 'description' in node:
                    ret['description'] = node['description']
                ret['properties'] = node['properties']
                # image_file should be gotten form artifacts TODO
                # ret['artifacts'] = self._build_artifacts(node)
                rets.append(ret)
        return rets

    def _get_all_vdu(self, nodeTemplates, node_types):
        rets = []
        inject_files = []
        for node in nodeTemplates:
            logger.debug("nodeTemplates :%s", node)
            if self.isNodeTypeX(node, node_types, VDU_COMPUTE_TYPE):
                ret = {}
                ret['vdu_id'] = node['name']
                ret['type'] = node['nodeType']
                if 'description' in node:
                    ret['description'] = node['description']
                ret['properties'] = node['properties']
                if 'inject_files' in node['properties']:
                    inject_files = node['properties']['inject_files']
                if inject_files is not None:
                    if isinstance(inject_files, list):
                        for inject_file in inject_files:
                            source_path = os.path.join(self.basepath, inject_file['source_path'])
                            with open(source_path, "rb") as f:
                                source_data = f.read()
                                source_data_base64 = source_data.encode("base64")
                                inject_file["source_data_base64"] = source_data_base64
                    if isinstance(inject_files, dict):
                        source_path = os.path.join(self.basepath, inject_files['source_path'])
                        with open(source_path, "rb") as f:
                            source_data = f.read()
                            source_data_base64 = source_data.encode("base64")
                            inject_files["source_data_base64"] = source_data_base64
                virtual_storages = self.getRequirementByName(node, 'virtual_storage')
                ret['virtual_storages'] = map(functools.partial(self._trans_virtual_storage), virtual_storages)
                ret['dependencies'] = map(lambda x: self.get_requirement_node_name(x), self.getNodeDependencys(node))
                virtual_compute = self.getCapabilityByName(node, 'virtual_compute')
                if virtual_compute is not None and 'properties' in virtual_compute:
                    ret['virtual_compute'] = virtual_compute['properties']
                ret['vls'] = self._get_linked_vl_ids(node, nodeTemplates)
                ret['cps'] = self._get_virtal_binding_cp_ids(node, nodeTemplates)
                ret['artifacts'] = self.build_artifacts(node)
                rets.append(ret)
        logger.debug("rets:%s", rets)
        return rets

    def _trans_virtual_storage(self, virtual_storage):
        if isinstance(virtual_storage, str):
            return {"vitual_storage_id": virtual_storage}
        else:
            ret = {}
            ret['vitual_storage_id'] = self.get_requirement_node_name(virtual_storage)
            return ret

    def _get_linked_vl_ids(self, node, node_templates):
        vl_ids = []
        cps = self._get_virtal_binding_cps(node, node_templates)
        for cp in cps:
            vl_reqs = self.getRequirementByName(cp, 'virtual_link')
            for vl_req in vl_reqs:
                vl_ids.append(self.get_requirement_node_name(vl_req))
        return vl_ids

    def _get_virtal_binding_cp_ids(self, node, nodeTemplates):
        return map(lambda x: x['name'], self._get_virtal_binding_cps(node, nodeTemplates))

    def _get_virtal_binding_cps(self, node, nodeTemplates):
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

    def _get_all_vl(self, nodeTemplates, node_types):
        vls = []
        for node in nodeTemplates:
            if self.isNodeTypeX(node, node_types, VNF_VL_TYPE):
                vl = dict()
                vl['vl_id'] = node['name']
                vl['description'] = node['description']
                vl['properties'] = node['properties']
                vls.append(vl)
        return vls

    def _get_all_cp(self, nodeTemplates, node_types):
        cps = []
        for node in nodeTemplates:
            if self.isNodeTypeX(node, node_types, VDU_CP_TYPE):
                cp = {}
                cp['cp_id'] = node['name']
                cp['cpd_id'] = node['name']
                cp['description'] = node['description']
                cp['properties'] = node['properties']
                cp['vl_id'] = self._get_node_vl_id(node)
                cp['vdu_id'] = self._get_node_vdu_id(node)
                vls = self._buil_cp_vls(node)
                if len(vls) > 1:
                    cp['vls'] = vls
                cps.append(cp)
        return cps

    def _get_node_vdu_id(self, node):
        vdu_ids = map(lambda x: self.get_requirement_node_name(x), self.getRequirementByName(node, 'virtual_binding'))
        if len(vdu_ids) > 0:
            return vdu_ids[0]
        return ""

    def _get_node_vl_id(self, node):
        vl_ids = map(lambda x: self.get_requirement_node_name(x), self.getRequirementByName(node, 'virtual_link'))
        if len(vl_ids) > 0:
            return vl_ids[0]
        return ""

    def _buil_cp_vls(self, node):
        return map(lambda x: self._build_cp_vl(x), self.getRequirementByName(node, 'virtual_link'))

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

    def _get_all_endpoint_exposed(self):
        if self.vnf:
            external_cps = self._get_external_cps(self.vnf.get('requirements', None))
            forward_cps = self._get_forward_cps(self.vnf.get('capabilities', None))
            return {"external_cps": external_cps, "forward_cps": forward_cps}
        return {}

    def _get_external_cps(self, vnf_requirements):
        external_cps = []
        if vnf_requirements:
            for key, value in vnf_requirements.items():
                if isinstance(value, list) and len(value) > 0:
                    external_cps.append({"key_name": key, "cpd_id": value[0]})
                else:
                    external_cps.append({"key_name": key, "cpd_id": value})
        return external_cps

    def _get_forward_cps(self, vnf_capabilities):
        forward_cps = []
        if vnf_capabilities:
            for key, value in vnf_capabilities.items():
                if isinstance(value, list) and len(value) > 0:
                    forward_cps.append({"key_name": key, "cpd_id": value[0]})
                else:
                    forward_cps.append({"key_name": key, "cpd_id": value})
        return forward_cps

    # def get_substitution_mappings(self, tosca):
    #    node = {}
    #    substitution_mappings = tosca.tpl['topology_template'].get('substitution_mappings', None)
    #    if substitution_mappings:
    #        node = substitution_mappings.get('properties', {})
    #        node['type'] = substitution_mappings['node_type']
    #    return node

    def _build_vnf(self, tosca):
        vnf = self.get_substitution_mappings(tosca)
        properties = vnf.get("properties", {})
        metadata = vnf.get("metadata", {})
        if properties.get("descriptor_id", "") == "":
            descriptor_id = metadata.get("descriptor_id", "")
            if descriptor_id == "":
                descriptor_id = metadata.get("id", "")
            if descriptor_id == "":
                descriptor_id = metadata.get("UUID", "")
            properties["descriptor_id"] = descriptor_id

        if properties.get("descriptor_verison", "") == "":
            version = metadata.get("template_version", "")
            if version == "":
                version = metadata.get("version", "")
            properties["descriptor_verison"] = version

        if properties.get("provider", "") == "":
            provider = metadata.get("template_author", "")
            if provider == "":
                provider = metadata.get("provider", "")
            properties["provider"] = provider

        if properties.get("template_name", "") == "":
            template_name = metadata.get("template_name", "")
            if template_name == "":
                template_name = metadata.get("template_name", "")
            properties["template_name"] = template_name

        return vnf
