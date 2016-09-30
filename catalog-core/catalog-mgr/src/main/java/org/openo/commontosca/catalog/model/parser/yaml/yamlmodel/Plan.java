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
package org.openo.commontosca.catalog.model.parser.yaml.yamlmodel;

import java.util.HashMap;
import java.util.Map;

/**
 * 
 */
public class Plan extends YAMLElement {
    private String reference = "";
    private String planLanguage = "";
    private Map<String, Input> inputs = new HashMap<String, Input>();
    public String getReference() {
      return reference;
    }
    public void setReference(String reference) {
      this.reference = reference;
    }
    public String getPlanLanguage() {
      return planLanguage;
    }
    public void setPlanLanguage(String planLanguage) {
      this.planLanguage = planLanguage;
    }
    public Map<String, Input> getInputs() {
      return inputs;
    }
    public void setInputs(Map<String, Input> inputs) {
      this.inputs = inputs;
    }

}
