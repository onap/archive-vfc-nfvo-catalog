/**
 *     Copyright (C) 2016 ZTE, Inc. and others. All rights reserved. (ZTE)
 *
 *     Licensed under the Apache License, Version 2.0 (the "License");
 *     you may not use this file except in compliance with the License.
 *     You may obtain a copy of the License at
 *
 *             http://www.apache.org/licenses/LICENSE-2.0
 *
 *     Unless required by applicable law or agreed to in writing, software
 *     distributed under the License is distributed on an "AS IS" BASIS,
 *     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *     See the License for the specific language governing permissions and
 *     limitations under the License.
 */
package org.openo.orchestrator.nfv.catalog.model.externalservice.entity.containerEntity;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlTransient;

@XmlAccessorType(XmlAccessType.FIELD)
public class ContainerSelfServiceOption {
	@XmlElement(namespace=ContainerSelfService.NAMESPACE_OF_SELFSERVICE)
	private String description;
	@XmlElement(namespace=ContainerSelfService.NAMESPACE_OF_SELFSERVICE)
	private String iconUrl;
	@XmlElement(namespace=ContainerSelfService.NAMESPACE_OF_SELFSERVICE)
	private String planServiceName;
	@XmlElement(namespace=ContainerSelfService.NAMESPACE_OF_SELFSERVICE)
	private String planInputMessageUrl;
	@XmlAttribute
	private String id;
	@XmlAttribute
	private String name;
	@XmlTransient
	private String inputMessageSoap;
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
	public String getPlanServiceName() {
		return planServiceName;
	}
	public void setPlanServiceName(String planServiceName) {
		this.planServiceName = planServiceName;
	}
	public String getPlanInputMessageUrl() {
		return planInputMessageUrl;
	}
	public void setPlanInputMessageUrl(String planInputMessageUrl) {
		this.planInputMessageUrl = planInputMessageUrl;
	}
	public String getId() {
		return id;
	}
	public void setId(String id) {
		this.id = id;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public String getInputMessageSoap() {
		return inputMessageSoap;
	}
	public void setInputMessageSoap(String inputMessageSoap) {
		this.inputMessageSoap = inputMessageSoap;
	}
}
