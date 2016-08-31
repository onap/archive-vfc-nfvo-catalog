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

package org.openo.commontosca.catalog.model.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.HashMap;
import java.util.Map;


@Data
@NoArgsConstructor
@AllArgsConstructor
public class SubstitutionMapping {
  private String serviceTemplateId;
  private String nodeType;
  private Map<String, String[]> requirements = new HashMap<String, String[]>();
  private Map<String, String[]> capabilities = new HashMap<String, String[]>();

  /**
   * put requirement.
   * @param key  key
   * @param value value
   * @return string list
   */
  public String[] putRequirement(String key, String[] value) {
    return this.requirements.put(key, value);
  }

  /** 
   * put capability.
   * @param key key
   * @param value value
   * @return string list
   */
  public String[] putCapability(String key, String[] value) {
    return this.capabilities.put(key, value);
  }

  /**
   * substitution mapping.
   * @param serviceTemplateId service template id
   * @param nodeType node type
   */
  public SubstitutionMapping(String serviceTemplateId, String nodeType) {
    super();
    this.serviceTemplateId = serviceTemplateId;
    this.nodeType = nodeType;
  }
}
