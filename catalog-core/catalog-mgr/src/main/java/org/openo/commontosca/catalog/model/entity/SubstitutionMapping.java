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

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * @author 10090474
 *
 */

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SubstitutionMapping {
    private String serviceTemplateId;
    private String node_type;
    private List<Map<String, String[]>> requirements = new ArrayList<>();
    private Map<String, String[]> capabilities = new HashMap<String, String[]>();

    /**
     * @param key
     * @param value
     * @return
     */
    public boolean putRequirement(String key, String[] value) {
        Map<String, String[]> requirement = new HashMap<>();
        requirement.put(key, value);
        return this.requirements.add(requirement);
    }

    /**
     * @param key
     * @param value
     * @return
     */
    public String[] putCapability(String key, String[] value) {
        return this.capabilities.put(key, value);
    }

    public SubstitutionMapping(String serviceTemplateId, String node_type) {
        super();
        this.serviceTemplateId = serviceTemplateId;
        this.node_type = node_type;
    }
}
