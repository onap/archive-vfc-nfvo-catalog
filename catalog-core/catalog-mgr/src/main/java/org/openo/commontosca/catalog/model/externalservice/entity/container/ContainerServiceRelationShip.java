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

package org.openo.commontosca.catalog.model.externalservice.entity.container;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;

@XmlAccessorType(XmlAccessType.FIELD)
public class ContainerServiceRelationShip {
  @XmlElement
  private String sourceNodeName;

  @XmlElement
  private String targetNodeName;

  @XmlElement
  private String sourceNodeId;

  @XmlElement
  private String targetNodeId;

  @XmlElement
  private String type;

  public String getSourceNodeId() {
    return sourceNodeId;
  }

  public void setSourceNodeId(String sourceNodeId) {
    this.sourceNodeId = sourceNodeId;
  }

  public String getTargetNodeId() {
    return targetNodeId;
  }

  public void setTargetNodeId(String targetNodeId) {
    this.targetNodeId = targetNodeId;
  }

  public String getSourceNodeName() {
    return sourceNodeName;
  }

  public void setSourceNodeName(String sourceNodeName) {
    this.sourceNodeName = sourceNodeName;
  }

  public String getTargetNodeName() {
    return targetNodeName;
  }

  public void setTargetNodeName(String targetNodeName) {
    this.targetNodeName = targetNodeName;
  }

  public String getType() {
    return type;
  }

  public void setType(String type) {
    this.type = type;
  }

}
