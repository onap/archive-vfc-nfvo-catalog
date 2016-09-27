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
package org.openo.commontosca.catalog.model.parser.yaml.zte.entity;

import java.util.List;

public class ParseYamlRequestParemeter {
  private String path = "E:\\NFVO\\130. yaml2xml\\0. tosca-parser\\sample\\ag-vnfd-floatingIp.zip";

  private List<Extension> extensionList;

  public String getPath() {
    return path;
  }

  public void setPath(String path) {
    this.path = path;
  }

  public List<Extension> getExtensionList() {
    return extensionList;
  }

  public void setExtensionList(List<Extension> extensionList) {
    this.extensionList = extensionList;
  }

  public Extension createExtension() {
    return new Extension();
  }

  public class Extension {
    private String name;
    private String value;

    public String getName() {
      return name;
    }

    public void setName(String name) {
      this.name = name;
    }

    public String getValue() {
      return value;
    }

    public void setValue(String value) {
      this.value = value;
    }
  }
}
