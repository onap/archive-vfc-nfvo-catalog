/**
 * Copyright 2016 [ZTE] and others.
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

package org.openo.commontosca.catalog.model.parser.yaml.aria.entity;

import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import com.google.gson.JsonObject;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AriaParserResult {
  private String description;
  private Map<String, String> metadata;
  private Node[] nodes;
  private JsonObject groups;
  private JsonObject policies;
  private Substitution substitution;
  private Map<String, Input> inputs;
  private Map<String, Output> outpus;
  
  @Data
  public class Substitution {
    private String node_type_name;
    private Mapping[] requirement;
    private Mapping[] capabilities;
    
    @Data
    public class Mapping {
      private String mapped_name;
      private String node_id;
      private String name;
      
    }
  }

  @Data
  public class Input {
    private String type_name;
    private Object value;
    private String description;
  }
  
  @Data
  public class Output {
    private String type_name;
    private Object value;
    private String description;
  }

  @Data
  public class Node {
    private String id;
    private String name;
    private String type_name;
    private Map<String, Property> properties;
    private JsonObject[] interfaces;
    private JsonObject[] artifacts;
    private JsonObject[] capabilities;
    private Relationship[] relationships;
    
    @Data
    public class Property {
      private String type_name;
      private Object value;
      private String description;
    }

    @Data
    public class Relationship {
      private String target_node_id;
      private String target_capability_name;
      private String type_name;
      private String template_name;
      private Map<String, Property> properties;
      private JsonObject[] source_interfaces;
      private JsonObject[] target_interfaces;
      
      @Data
      public class Property {
        private String type_name;
        private Object value;
        private String description;
      }
    }

    /**
     * @return
     */
    public Map<String, Object> getPropertyAssignments() {
      if (this.properties == null || this.properties.isEmpty()) {
        return new HashMap<String, Object>();
      }
      
      Map<String, Object> ret = new HashMap<String, Object>();
      for (Entry<String, Property> e : this.properties.entrySet()) {
        ret.put(e.getKey(), e.getValue().getValue());
      }

      return ret;
    }
  }
}
