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
package org.openo.commontosca.catalog.model.externalservice.entity.container;

import java.util.List;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlElementWrapper;
import javax.xml.bind.annotation.XmlRootElement;

@XmlAccessorType(XmlAccessType.FIELD)
@XmlRootElement(name = "Application", namespace = ContainerSelfService.NAMESPACE_OF_SELFSERVICE)
public class ContainerSelfService {
  public static final String NAMESPACE_OF_SELFSERVICE =
      "http://www.eclipse.org/winery/model/selfservice";

  @XmlElement(namespace = NAMESPACE_OF_SELFSERVICE)
  private String displayName;

  @XmlElement(namespace = NAMESPACE_OF_SELFSERVICE)
  private String description;

  @XmlElement(namespace = NAMESPACE_OF_SELFSERVICE)
  private String iconUrl;

  @XmlElement(namespace = NAMESPACE_OF_SELFSERVICE)
  private String imageUrl;

  @XmlElementWrapper(name = "options", namespace = NAMESPACE_OF_SELFSERVICE)
  @XmlElement(name = "option", namespace = NAMESPACE_OF_SELFSERVICE)
  private List<ContainerSelfServiceOption> optionList;

  public String getDisplayName() {
    return displayName;
  }

  public void setDisplayName(String displayName) {
    this.displayName = displayName;
  }

  public String getDescription() {
    return description;
  }

  public void setDescription(String description) {
    this.description = description;
  }

  public String getIconUrl() {
    return iconUrl;
  }

  public void setIconUrl(String iconUrl) {
    this.iconUrl = iconUrl;
  }

  public String getImageUrl() {
    return imageUrl;
  }

  public void setImageUrl(String imageUrl) {
    this.imageUrl = imageUrl;
  }

  public List<ContainerSelfServiceOption> getOptionList() {
    return optionList;
  }

  public void setOptionList(List<ContainerSelfServiceOption> optionList) {
    this.optionList = optionList;
  }
}
