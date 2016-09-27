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
package org.openo.commontosca.catalog.model.parser.yaml.aria.entity;

import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AriaParserResult {
  private String description;
  private Map<String, String> metadata;
  private Node[] nodes;
  private Group[] groups;
  private Policy[] policies;
  private Substitution substitution;
  private Map<String, Input> inputs;
  private Map<String, Output> outpus;
  
  
  @Data
  public class Node {
    private String id;
    private String type_name;
    private String template_name;
    private Map<String, Property> properties;
    private Interface[] interfaces;
    private Artifact[] artifacts;
    private Capability[] capabilities;
    private Relationship[] relationships;
    
    @Data
    public class Artifact {
      private String name;
      private String type_name;
      private String source_path;
      private String target_path;
      private String repository_url;
      private Credential repository_credential;
      private Map<String, Property> properties;
      
      @Data
      public class Credential {
        private String protocol;
        private String token_type;
        private Map<String, String> keys;
        private String user;
      }
    }
    
    @Data
    public class Capability {
      private String name;
      private String type_name;
      private Map<String, Property> properties;
    }

    @Data
    public class Relationship {
      private String target_node_id;
      private String target_capability_name;
      private String type_name;
      private String template_name;
      private Map<String, Property> properties;
      private Interface[] source_interfaces;
      private Interface[] target_interfaces;
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
  
  @Data
  public class Group {
    private String id;
    private String type_name;
    private String template_name;
    private Map<String, Property> properties;
    private Interface[] interfaces;
    private GroupPolicy[] policies;
    private String[] member_node_ids;
    
    @Data
    public class GroupPolicy {
      private String id;
      private String type_name;
      private Map<String, Property> properties;
      private Trigger[] triggers;
      
      @Data
      public class Trigger {
        private String name;
        private String implementation;
        private Map<String, Property> properties;
      }
    }
    
  }

  
  @Data
  public class Policy {
    private String name;
    private String type_name;
    private Map<String, Property> properties;
    private String[] target_node_ids;
    private String[] target_group_ids;
  }
  
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
}


@Data
class Property {
  private String type_name;
  private Object value;
  private String description;
}

@Data
class Interface {
  private String name;
  private String type_name;
  private Map<String, Property> inputs;
  private Operation[] operation;
  
  @Data
  class Operation {
    private String name;
    private String implementation;
    private String[] dependencies;
    private String executor;
    private int max_retries;
    private int retry_interval;
    private Map<String, Property> inputs;
  }
}

