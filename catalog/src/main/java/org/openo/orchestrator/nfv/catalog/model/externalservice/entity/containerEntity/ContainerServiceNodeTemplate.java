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

import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlElementWrapper;
import javax.xml.bind.annotation.XmlRootElement;

import org.openo.orchestrator.nfv.catalog.common.ToolUtil;


@XmlRootElement
@XmlAccessorType(XmlAccessType.NONE)
public class ContainerServiceNodeTemplate {

    @XmlAttribute(name = "nodetemplateid")
    private String id;

    @XmlAttribute(name = "nodetemplatename")
    private String name;

    @XmlAttribute
    private String type;

    @XmlElementWrapper(name = "properties")
    @XmlElement(name = "property")
    private List<ContainerServiceCommonParam> properties;

    @XmlElementWrapper(name = "relationshipInfos")
    @XmlElement(name = "relationship")
    private List<ContainerServiceRelationShip> relationShips;

    @XmlElement(name = "Capabilities")
    private ContainerServiceNodeTemplate.Capablitiies capabilities;

    public ContainerServiceNodeTemplate.Capablitiies getCapabilities() {
        return capabilities;
    }

    public void setCapabilities(
            ContainerServiceNodeTemplate.Capablitiies capabilities) {
        this.capabilities = capabilities;
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

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public List<ContainerServiceCommonParam> getProperties() {
        return properties;
    }

    public void setProperties(List<ContainerServiceCommonParam> properties) {
        this.properties = properties;
    }

    public List<ContainerServiceRelationShip> getRelationShips() {
        return relationShips;
    }

    public void setRelationShips(
            List<ContainerServiceRelationShip> relationShips) {
        this.relationShips = relationShips;
    }

    @XmlRootElement
    @XmlAccessorType(XmlAccessType.NONE)
    public static class Capablitiies {
        @XmlElement(name = "Capability")
        private List<ContainerServiceNodeTemplate.Capability> capabilityList;

        public List<ContainerServiceNodeTemplate.Capability> getCapabilityList() {
            return capabilityList;
        }

        public void setCapabilityList(
                List<ContainerServiceNodeTemplate.Capability> capabilityList) {
            this.capabilityList = capabilityList;
        }
    }

    @XmlRootElement
    @XmlAccessorType(XmlAccessType.NONE)
    public static class Capability {
        @XmlAttribute(name = "id")
        private String flavorName;

        @XmlElement(name = "Properties")
        private ContainerServiceNodeTemplate.CapabilityProperties properties;

        public String getFlavorName() {
            return flavorName;
        }

        public void setFlavorName(String flavorName) {
            this.flavorName = flavorName;
        }

        public ContainerServiceNodeTemplate.CapabilityProperties getProperties() {
            return properties;
        }

        public void setProperties(
                ContainerServiceNodeTemplate.CapabilityProperties properties) {
            this.properties = properties;
        }

    }

    @XmlRootElement
    @XmlAccessorType(XmlAccessType.NONE)
    public static class CapabilityProperties {
        @XmlElement(name = "Properties")
        private ContainerServiceNodeTemplate.CapabilityProperty property;

        public ContainerServiceNodeTemplate.CapabilityProperty getProperty() {
            return property;
        }

        public void setProperty(
                ContainerServiceNodeTemplate.CapabilityProperty property) {
            this.property = property;
        }
    }

    @XmlRootElement
    @XmlAccessorType(XmlAccessType.FIELD)
    public static class CapabilityProperty {
        @XmlElement
        private String vCPU;

        @XmlElement
        private String vRAM;

        @XmlElement
        private String rootDisk;

        @XmlElement
        private String swapDisk;

        @XmlElement
        private String tempDisk;

        public String getvCPU() {
            return vCPU;
        }

        public void setvCPU(String vCPU) {
            this.vCPU = vCPU;
        }

        public String getvRAM() {
            return vRAM;
        }

        public void setvRAM(String vRAM) {
            this.vRAM = vRAM;
        }

        public String getRootDisk() {
            return rootDisk;
        }

        public void setRootDisk(String rootDisk) {
            this.rootDisk = rootDisk;
        }

        public String getSwapDisk() {
            return swapDisk;
        }

        public void setSwapDisk(String swapDisk) {
            this.swapDisk = swapDisk;
        }

        public String getTempDisk() {
            return tempDisk;
        }

        public void setTempDisk(String tempDisk) {
            this.tempDisk = tempDisk;
        }
    }

    public class NTFlavor {
        private String flavorName;

        private String vCPU;

        private String vRAM;

        private String rootDisk;

        private String swapDisk;

        private String tempDisk;

        public String getFlavorName() {
            return flavorName;
        }

        public void setFlavorName(String flavorName) {
            this.flavorName = flavorName;
        }

        public String getvCPU() {
            return vCPU;
        }

        public void setvCPU(String vCPU) {
            this.vCPU = vCPU;
        }

        public String getvRAM() {
            return vRAM;
        }

        public void setvRAM(String vRAM) {
            this.vRAM = vRAM;
        }

        public String getRootDisk() {
            return rootDisk;
        }

        public void setRootDisk(String rootDisk) {
            this.rootDisk = rootDisk;
        }

        public String getSwapDisk() {
            return swapDisk;
        }

        public void setSwapDisk(String swapDisk) {
            this.swapDisk = swapDisk;
        }

        public String getTempDisk() {
            return tempDisk;
        }

        public void setTempDisk(String tempDisk) {
            this.tempDisk = tempDisk;
        }

    }

    public List<NTFlavor> getNTFlavorList() {
        if (null == this.capabilities
                || ToolUtil.isEmptyCollection(capabilities.getCapabilityList())) {
            return null;
        }

        List<NTFlavor> ntFlavors = new ArrayList<NTFlavor>();
        List<Capability> capabilityList = capabilities.getCapabilityList();
        for (Capability capabilty : capabilityList) {
            NTFlavor ntFlavor = convertCap2Flavor(capabilty);
            ntFlavors.add(ntFlavor);
        }

        return ntFlavors;
    }

    private NTFlavor convertCap2Flavor(Capability capabilty) {
        NTFlavor ntFlavor = new NTFlavor();
        ntFlavor.setFlavorName(capabilty.getFlavorName());
        if (null != capabilty.getProperties()
                && null != capabilty.getProperties().getProperty()) {
            CapabilityProperty property = capabilty.getProperties()
                    .getProperty();
            ntFlavor.setRootDisk(property.getRootDisk());
            ntFlavor.setSwapDisk(property.getSwapDisk());
            ntFlavor.setTempDisk(property.getTempDisk());
            ntFlavor.setvCPU(property.getvCPU());
            ntFlavor.setvRAM(property.getvRAM());
        }

        return ntFlavor;
    }

}
