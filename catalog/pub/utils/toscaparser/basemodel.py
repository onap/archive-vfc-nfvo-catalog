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

import ftplib
import json
import logging
import os
import re
import shutil
import urllib

import paramiko
from toscaparser.tosca_template import ToscaTemplate
from toscaparser.properties import Property
from toscaparser.functions import Function, Concat, GetInput, get_function, function_mappings
from catalog.pub.utils.toscaparser.graph import Graph

from catalog.pub.utils.toscaparser.dataentityext import DataEntityExt

logger = logging.getLogger(__name__)

METADATA = "metadata"
PROPERTIES = "properties"
DESCRIPTION = "description"
REQUIREMENTS = "requirements"
INTERFACES = "interfaces"
TOPOLOGY_TEMPLATE = "topology_template"
INPUTS = "inputs"
CAPABILITIES = "capabilities"
ATTRIBUTES = "attributes"
ARTIFACTS = "artifacts"
DERIVED_FROM = "derived_from"

NODE_NAME = "name"
NODE_TYPE = "nodeType"
NODE_ROOT = "tosca.nodes.Root"
GROUP_TYPE = "groupType"
GROUPS_ROOT = "tosca.groups.Root"


class BaseInfoModel(object):

    def __init__(self, path, params):
        tosca = self.buildToscaTemplate(path, params)
        self.parseModel(tosca)

    def parseModel(self, tosca):
        pass

    def buildInputs(self, tosca):
        topo = tosca.tpl.get(TOPOLOGY_TEMPLATE, None)
        return topo.get(INPUTS, {}) if topo else {}

    def buildToscaTemplate(self, path, params):
        file_name = None
        try:
            file_name = self._check_download_file(path)
            valid_params = self._validate_input_params(file_name, params)
            return self._create_tosca_template(file_name, valid_params)
        finally:
            if file_name is not None and file_name != path and os.path.exists(file_name):
                try:
                    os.remove(file_name)
                except Exception as e:
                    logger.error("Failed to parse package, error: %s", e.message)

    def _validate_input_params(self, path, params):
        valid_params = {}
        inputs = {}
        if isinstance(params, list):
            for param in params:
                key = param.get('key', 'undefined')
                value = param.get('value', 'undefined')
                inputs[key] = value
            params = inputs

        if params and len(params) > 0:
            tmp = self._create_tosca_template(path, None)
            if isinstance(params, dict):
                for key, value in params.items():
                    if hasattr(tmp, 'inputs') and len(tmp.inputs) > 0:
                        for input_def in tmp.inputs:
                            if (input_def.name == key):
                                valid_params[key] = DataEntityExt.validate_datatype(input_def.type, value)
        return valid_params

    def _create_tosca_template(self, file_name, valid_params):
        tosca_tpl = None
        try:
            tosca_tpl = ToscaTemplate(path=file_name,
                                      parsed_params=valid_params,
                                      no_required_paras_check=True,
                                      debug_mode=True)
        except Exception as e:
            print e.message
        finally:
            if tosca_tpl is not None and hasattr(tosca_tpl, "temp_dir") and os.path.exists(tosca_tpl.temp_dir):
                try:
                    shutil.rmtree(tosca_tpl.temp_dir)
                except Exception as e:
                    logger.error("Failed to create tosca template, error: %s", e.message)
                print "-----------------------------"
                print '\n'.join(['%s:%s' % item for item in tosca_tpl.__dict__.items()])
                print "-----------------------------"
            return tosca_tpl

    def _check_download_file(self, path):
        if (path.startswith("ftp") or path.startswith("sftp")):
            return self.downloadFileFromFtpServer(path)
        elif (path.startswith("http")):
            return self.download_file_from_httpserver(path)
        return path

    def download_file_from_httpserver(self, path):
        path = path.encode("utf-8")
        tmps = str.split(path, '/')
        localFileName = tmps[len(tmps) - 1]
        urllib.urlretrieve(path, localFileName)
        return localFileName

    def downloadFileFromFtpServer(self, path):
        path = path.encode("utf-8")
        tmp = str.split(path, '://')
        protocol = tmp[0]
        tmp = str.split(tmp[1], ':')
        if len(tmp) == 2:
            userName = tmp[0]
            tmp = str.split(tmp[1], '@')
            userPwd = tmp[0]
            index = tmp[1].index('/')
            hostIp = tmp[1][0:index]
            remoteFileName = tmp[1][index:len(tmp[1])]
            if protocol.lower() == 'ftp':
                hostPort = 21
            else:
                hostPort = 22

        if len(tmp) == 3:
            userName = tmp[0]
            userPwd = str.split(tmp[1], '@')[0]
            hostIp = str.split(tmp[1], '@')[1]
            index = tmp[2].index('/')
            hostPort = tmp[2][0:index]
            remoteFileName = tmp[2][index:len(tmp[2])]

        localFileName = str.split(remoteFileName, '/')
        localFileName = localFileName[len(localFileName) - 1]

        if protocol.lower() == 'sftp':
            self.sftp_get(userName, userPwd, hostIp, hostPort, remoteFileName, localFileName)
        else:
            self.ftp_get(userName, userPwd, hostIp, hostPort, remoteFileName, localFileName)
        return localFileName

    def sftp_get(self, userName, userPwd, hostIp, hostPort, remoteFileName, localFileName):
        # return
        t = None
        try:
            t = paramiko.Transport(hostIp, int(hostPort))
            t.connect(username=userName, password=userPwd)
            sftp = paramiko.SFTPClient.from_transport(t)
            sftp.get(remoteFileName, localFileName)
        finally:
            if t is not None:
                t.close()

    def ftp_get(self, userName, userPwd, hostIp, hostPort, remoteFileName, localFileName):
        f = None
        try:
            ftp = ftplib.FTP()
            ftp.connect(hostIp, hostPort)
            ftp.login(userName, userPwd)
            f = open(localFileName, 'wb')
            ftp.retrbinary('RETR ' + remoteFileName, f.write, 1024)
            f.close()
        finally:
            if f is not None:
                f.close()

    def buildMetadata(self, tosca):
        return tosca.tpl.get(METADATA, {}) if tosca else {}

    def buildNode(self, nodeTemplate, tosca):
        inputs = tosca.inputs
        parsed_params = tosca.parsed_params
        ret = {}
        ret[NODE_NAME] = nodeTemplate.name
        ret[NODE_TYPE] = nodeTemplate.type
        if DESCRIPTION in nodeTemplate.entity_tpl:
            ret[DESCRIPTION] = nodeTemplate.entity_tpl[DESCRIPTION]
        else:
            ret[DESCRIPTION] = ''
        if METADATA in nodeTemplate.entity_tpl:
            ret[METADATA] = nodeTemplate.entity_tpl[METADATA]
        else:
            ret[METADATA] = ''
        props = self.buildProperties_ex(nodeTemplate, tosca.topology_template)
        ret[PROPERTIES] = self.verify_properties(props, inputs, parsed_params)
        ret[REQUIREMENTS] = self.build_requirements(nodeTemplate)
        self.buildCapabilities(nodeTemplate, inputs, ret)
        self.buildArtifacts(nodeTemplate, inputs, ret)
        interfaces = self.build_interfaces(nodeTemplate)
        if interfaces:
            ret[INTERFACES] = interfaces
        return ret

    def buildProperties(self, nodeTemplate, parsed_params):
        properties = {}
        isMappingParams = parsed_params and len(parsed_params) > 0
        for k, item in nodeTemplate.get_properties().items():
            properties[k] = item.value
            if isinstance(item.value, GetInput):
                if item.value.result() and isMappingParams:
                    properties[k] = DataEntityExt.validate_datatype(item.type, item.value.result())
                else:
                    tmp = {}
                    tmp[item.value.name] = item.value.input_name
                    properties[k] = tmp
        if ATTRIBUTES in nodeTemplate.entity_tpl:
            for k, item in nodeTemplate.entity_tpl[ATTRIBUTES].items():
                properties[k] = str(item)
        return properties

    def buildProperties_ex(self, nodeTemplate, topology_template, properties=None):
        if properties is None:
            properties = nodeTemplate.get_properties()
        _properties = {}
        if isinstance(properties, dict):
            for name, prop in properties.items():
                if isinstance(prop, Property):
                    if isinstance(prop.value, Function):
                        if isinstance(prop.value, Concat):  # support one layer inner function.
                            value_str = ''
                            for arg in prop.value.args:
                                if isinstance(arg, str):
                                    value_str += arg
                                elif isinstance(arg, dict):
                                    raw_func = {}
                                    for k, v in arg.items():
                                        func_args = []
                                        func_args.append(v)
                                        raw_func[k] = func_args
                                    func = get_function(topology_template, nodeTemplate, raw_func)
                                    value_str += str(func.result())
                            _properties[name] = value_str
                        else:
                            _properties[name] = prop.value.result()
                    elif isinstance(prop.value, dict) or isinstance(prop.value, list):
                        _properties[name] = self.buildProperties_ex(nodeTemplate, topology_template, prop.value)
                    elif prop.type == 'string':
                        _properties[name] = prop.value
                    else:
                        _properties[name] = json.dumps(prop.value)
                elif isinstance(prop, dict):
                    _properties[name] = self.buildProperties_ex(nodeTemplate, topology_template, prop)
                elif isinstance(prop, list):
                    _properties[name] = self.buildProperties_ex(nodeTemplate, topology_template, prop)
                elif name in function_mappings:
                    raw_func = {}
                    func_args = []
                    func_args.append(prop)
                    raw_func[name] = func_args
                    if name == 'CONCAT':
                        value_str = ''
                        for arg in prop:
                            if isinstance(arg, str):
                                value_str += arg
                            elif isinstance(arg, dict):
                                raw_func = {}
                                for k, v in arg.items():
                                    func_args = []
                                    func_args.append(v)
                                    raw_func[k] = func_args
                                value_str += str(
                                    get_function(topology_template, nodeTemplate, raw_func).result())
                                value = value_str
                    else:
                        return get_function(topology_template, nodeTemplate, raw_func).result()
                else:
                    _properties[name] = prop
        elif isinstance(properties, list):
            value = []
            for para in properties:
                if isinstance(para, dict) or isinstance(para, list):
                    value.append(self.buildProperties_ex(nodeTemplate, topology_template, para))
                else:
                    value.append(para)
            return value
        return _properties

    def verify_properties(self, props, inputs, parsed_params):
        ret_props = {}
        if (props and len(props) > 0):
            for key, value in props.items():
                ret_props[key] = self._verify_value(value, inputs, parsed_params)
                #                 if isinstance(value, str):
                #                     ret_props[key] = self._verify_string(inputs, parsed_params, value);
                #                     continue
                #                 if isinstance(value, list):
                #                     ret_props[key] = map(lambda x: self._verify_dict(inputs, parsed_params, x), value)
                #                     continue
                #                 if isinstance(value, dict):
                #                     ret_props[key] = self._verify_map(inputs, parsed_params, value)
                #                     continue
                #                 ret_props[key] = value
        return ret_props

    def build_requirements(self, node_template):
        rets = []
        for req in node_template.requirements:
            for req_name, req_value in req.items():
                if (isinstance(req_value, dict)):
                    if ('node' in req_value and req_value['node'] not in node_template.templates):
                        continue  # No target requirement for aria parser, not add to result.
                rets.append({req_name: req_value})
        return rets

    def buildCapabilities(self, nodeTemplate, inputs, ret):
        capabilities = json.dumps(nodeTemplate.entity_tpl.get(CAPABILITIES, None))
        match = re.findall(r'\{"get_input":\s*"([\w|\-]+)"\}', capabilities)
        for m in match:
            aa = [input_def for input_def in inputs if m == input_def.name][0]
            capabilities = re.sub(r'\{"get_input":\s*"([\w|\-]+)"\}', json.dumps(aa.default), capabilities, 1)
        if capabilities != 'null':
            ret[CAPABILITIES] = json.loads(capabilities)

    def buildArtifacts(self, nodeTemplate, inputs, ret):
        artifacts = json.dumps(nodeTemplate.entity_tpl.get('artifacts', None))
        match = re.findall(r'\{"get_input":\s*"([\w|\-]+)"\}', artifacts)
        for m in match:
            aa = [input_def for input_def in inputs if m == input_def.name][0]
            artifacts = re.sub(r'\{"get_input":\s*"([\w|\-]+)"\}', json.dumps(aa.default), artifacts, 1)
        if artifacts != 'null':
            ret[ARTIFACTS] = json.loads(artifacts)

    def build_interfaces(self, node_template):
        if INTERFACES in node_template.entity_tpl:
            return node_template.entity_tpl[INTERFACES]
        return None

    def isNodeTypeX(self, node, nodeTypes, x):
        node_type = node[NODE_TYPE]
        while node_type != x:
            node_type_derived = node_type
            node_type = nodeTypes[node_type][DERIVED_FROM]
            if node_type == NODE_ROOT or node_type == node_type_derived:
                return False
        return True

    def get_requirement_node_name(self, req_value):
        return self.get_prop_from_obj(req_value, 'node')

    def getRequirementByNodeName(self, nodeTemplates, storage_name, prop):
        for node in nodeTemplates:
            if node[NODE_NAME] == storage_name:
                if prop in node:
                    return node[prop]

    def get_prop_from_obj(self, obj, prop):
        if isinstance(obj, str):
            return obj
        if (isinstance(obj, dict) and prop in obj):
            return obj[prop]
        return None

    def getNodeDependencys(self, node):
        return self.getRequirementByName(node, 'dependency')

    def getRequirementByName(self, node, requirementName):
        requirements = []
        if REQUIREMENTS in node:
            for item in node[REQUIREMENTS]:
                for key, value in item.items():
                    if key == requirementName:
                        requirements.append(value)
        return requirements

    def _verify_value(self, value, inputs, parsed_params):
        if value == '{}':
            return ''
        if isinstance(value, str):
            return self._verify_string(inputs, parsed_params, value)
        if isinstance(value, list) or isinstance(value, dict):
            return self._verify_object(value, inputs, parsed_params)
        return value

    def _verify_object(self, value, inputs, parsed_params):
        s = self._verify_string(inputs, parsed_params, json.dumps(value))
        return json.loads(s)

    def _get_input_name(self, getInput):
        input_name = getInput.split(':')[1]
        input_name = input_name.strip()
        return input_name.replace('"', '').replace('}', '')

    def _verify_string(self, inputs, parsed_params, value):
        getInputs = re.findall(r'{"get_input": "[a-zA-Z_0-9]+"}', value)
        for getInput in getInputs:
            input_name = self._get_input_name(getInput)
            if parsed_params and input_name in parsed_params:
                value = value.replace(getInput, json.dumps(parsed_params[input_name]))
            else:
                for input_def in inputs:
                    if input_def.default and input_name == input_def.name:
                        value = value.replace(getInput, json.dumps(input_def.default))
        return value

    def get_node_by_name(self, node_templates, name):
        for node in node_templates:
            if node[NODE_NAME] == name:
                return node
        return None

    def getCapabilityByName(self, node, capabilityName):
        if CAPABILITIES in node and capabilityName in node[CAPABILITIES]:
            return node[CAPABILITIES][capabilityName]
        return None

    def get_base_path(self, tosca):
        fpath, fname = os.path.split(tosca.path)
        return fpath

    def build_artifacts(self, node):
        rets = []
        if ARTIFACTS in node and len(node[ARTIFACTS]) > 0:
            artifacts = node[ARTIFACTS]
            for name, value in artifacts.items():
                ret = {}
                ret['artifact_name'] = name
                ret['file'] = value
                if isinstance(value, dict):
                    ret.update(value)
                rets.append(ret)
        return rets

    def get_node_by_req(self, node_templates, req):
        req_node_name = self.get_requirement_node_name(req)
        return self.get_node_by_name(node_templates, req_node_name)

    def isGroupTypeX(self, group, groupTypes, x):
        group_type = group[GROUP_TYPE]
        while group_type != x:
            group_type_derived = group_type
            group_type = groupTypes[group_type][DERIVED_FROM]
            if group_type == GROUPS_ROOT or group_type == group_type_derived:
                return False
        return True

    def setTargetValues(self, dict_target, target_keys, dict_source, source_keys):
        i = 0
        for item in source_keys:
            dict_target[target_keys[i]] = dict_source.get(item, "")
            i += 1
        return dict_target

    def get_deploy_graph(self, tosca, relations):
        nodes = tosca.graph.nodetemplates
        graph = Graph()
        for node in nodes:
            self._build_deploy_path(node, [], graph, relations)
        return graph.to_dict()

    def _build_deploy_path(self, node, node_parent, graph, relations):
        graph.add_node(node.name, node_parent)
        type_require_set = {}
        type_requires = node.type_definition.requirements
        for type_require in type_requires:
            type_require_set.update(type_require)
        for requirement in node.requirements:
            for k in requirement.keys():
                if type_require_set[k].get('relationship', None) in relations[0] or type_require_set[k].get('capability', None) in relations[0]:
                    if isinstance(requirement[k], dict):
                        next_node = requirement[k].get('node', None)
                    else:
                        next_node = requirement[k]
                    graph.add_node(next_node, [node.name])
                if type_require_set[k].get('relationship', None) in relations[1]:
                    if isinstance(requirement[k], dict):
                        next_node = requirement[k].get('node', None)
                    else:
                        next_node = requirement[k]
                    graph.add_node(next_node, [node.name])
