# Copyright (c) 2019, CMCC Technologies. Co., Ltd.
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
import logging

from catalog.pub.utils.toscaparser.basemodel import BaseInfoModel
from catalog.pub.utils.toscaparser.servicemodel import SdcServiceModel

logger = logging.getLogger(__name__)


class SdInfoModel(BaseInfoModel):
    def __init__(self, path, params):
        super(SdInfoModel, self).__init__(path, params)

    def parseModel(self, tosca):
        self.metadata = self.buildMetadata(tosca)
        self.inputs = self.build_inputs(tosca)

        sdcModle = SdcServiceModel(tosca)
        if sdcModle:
            self.service = sdcModle.ns
            if hasattr(tosca, 'nodetemplates'):
                self.basepath = sdcModle.basepath
                self.vnfs = sdcModle.vnfs
                self.pnfs = sdcModle.pnfs
                self.vls = sdcModle.vls
                self.graph = sdcModle.graph

    def build_inputs(self, tosca):
        """ Get all the inputs for complex type"""
        result_inputs = {}

        if not tosca.inputs:
            return {}

        for input in tosca.inputs:
            type = input.schema.type
            if type.__eq__('list') or type.__eq__('map'):
                complex_input = []
                entry_schema = input.schema.schema['entry_schema']
                # get_child_input(complex_input, entry_schema, input)
                self.get_child_input_repeat(complex_input, entry_schema, input)
                result_inputs[input.schema.name] = complex_input

            else:
                simple_input = {
                    "type": input.schema.type,
                    "description": input.schema.description,
                    "required": input.schema.required,
                }
                result_inputs[input.schema.name] = simple_input
        return result_inputs

    def get_child_input_repeat(self, complex_input, entry_schema, input):
        custom_defs = input.custom_defs
        properties = custom_defs[entry_schema]['properties']
        for key, value in properties.iteritems():
            if value['type'].__eq__('list'):
                child_complex_input = []
                child_entry_schema = value['entry_schema']
                self.get_child_input_repeat(child_complex_input, child_entry_schema, input)
                complex_input.append({key: child_complex_input})
            else:
                if value.has_key('description'):
                    simple_input = {
                        key: "",
                        "type": value['type'],
                        "required": value['required'],
                        "description": value['description'],
                    }
                else:
                    simple_input = {
                        key: "",
                        "type": value['type'],
                        "required": value['required'],
                    }
                complex_input.append(simple_input)
