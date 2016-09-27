/**
 * Copyright 2016 ZTE Corporation.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.openo.commontosca.catalog.model.common;

public enum EnumToscaNodeTypeDefinition {
  VNF {
    @Override
    public String getName() {
      return "tosca.nodes.nfv.VNF";
    }
  },
  VDU {
    @Override
    public String getName() {
      return "tosca.nodes.nfv.VDU";
    }
  },
  VNFC {
    @Override
    public String getName() {
      return "tosca.nodes.nfv.VNFC";
    }
  },
  VL {
    @Override
    public String getName() {
      return "tosca.nodes.nfv.VL";
    }
  },
  CP {
    @Override
    public String getName() {
      return "tosca.nodes.nfv.CP";
    }
  };

  public abstract String getName();

  /**
   * judge wether is tosca node type definition or not.
   * @param type node type
   * @return boolean
   */
  public static boolean isToscaNodeTypeDef(String type) {
    for (EnumToscaNodeTypeDefinition enumDef : EnumToscaNodeTypeDefinition.values()) {
      if (type.indexOf(enumDef.getName()) != -1) {
        return true;
      }
    }
    return false;
  }
}
