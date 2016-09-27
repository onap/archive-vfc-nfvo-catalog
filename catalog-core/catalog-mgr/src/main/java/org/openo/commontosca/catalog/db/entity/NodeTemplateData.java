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
package org.openo.commontosca.catalog.db.entity;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "catalog_node_template_table")
@JsonIgnoreProperties(ignoreUnknown = true)
public class NodeTemplateData extends BaseData {

  @Id
  @Column(name = "NODETEMPLATEID")
  private String nodeTemplateId;
  @Column(name = "NAME")
  private String name;

  @Column(name = "SERVICETEMPLATEID")
  private String serviceTemplateId;

  @Column(name = "TYPE")
  private String type;

  @Column(name = "PROPERTIES")
  private String properties;

  @Column(name = "RELATIONSHIPS")
  private String relationShips;

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getServiceTemplateId() {
    return serviceTemplateId;
  }

  public void setServiceTemplateId(String serviceTemplateId) {
    this.serviceTemplateId = serviceTemplateId;
  }

  public String getType() {
    return type;
  }

  public void setType(String type) {
    this.type = type;
  }

  public String getProperties() {
    return properties;
  }

  public void setProperties(String properties) {
    this.properties = properties;
  }

  public String getRelationShips() {
    return relationShips;
  }

  public void setRelationShips(String relationShips) {
    this.relationShips = relationShips;
  }

  public void setNodeTemplateId(String nodeTemplateId) {
    this.nodeTemplateId = nodeTemplateId;
  }

  public String getNodeTemplateId() {
    return nodeTemplateId;
  }


}
