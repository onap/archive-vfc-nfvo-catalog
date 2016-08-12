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

import java.util.List;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlElementWrapper;
import javax.xml.bind.annotation.XmlRootElement;

@XmlRootElement
@XmlAccessorType(XmlAccessType.NONE)
public class ContainerServiceTemplate {
    @XmlAttribute
    private String templateid;

    @XmlAttribute
    private String templatename;

    @XmlElement(name = "BoundaryDefinitions")
    private BoundaryDefinitions boundary;

    public String getTemplateid() {
        return templateid;
    }

    public void setTemplateid(String templateid) {
        this.templateid = templateid;
    }

    public String getTemplatename() {
        return templatename;
    }

    public void setTemplatename(String templatename) {
        this.templatename = templatename;
    }

    public BoundaryDefinitions getBoundary() {
        return boundary;
    }

    public void setBoundary(BoundaryDefinitions boundary) {
        this.boundary = boundary;
    }

    @XmlRootElement
    @XmlAccessorType(XmlAccessType.NONE)
    public static class BoundaryDefinitions {
        @XmlElement(name = "Properties", namespace = "http://docs.oasis-open.org/tosca/ns/2011/12")
        private BoundaryProperties properties;

        public BoundaryProperties getProperties() {
            return properties;
        }

        public void setProperties(BoundaryProperties properties) {
            this.properties = properties;
        }

    }

    @XmlRootElement
    @XmlAccessorType(XmlAccessType.NONE)
    public static class BoundaryProperties {
        @XmlElement(name = "Properties")
        private BoundaryProperty property;

        public BoundaryProperty getProperty() {
            return property;
        }

        public void setProperty(BoundaryProperty property) {
            this.property = property;
        }
    }

    @XmlRootElement
    @XmlAccessorType(XmlAccessType.NONE)
    public static class BoundaryProperty {
        public String getTemplateVersion() {
            return templateVersion;
        }

        public void setTemplateVersion(String templateVersion) {
            this.templateVersion = templateVersion;
        }

        public String getTemplateAuthor() {
            return templateAuthor;
        }

        public void setTemplateAuthor(String templateAuthor) {
            this.templateAuthor = templateAuthor;
        }

        public String getVendor() {
            return vendor;
        }

        public void setVendor(String vendor) {
            this.vendor = vendor;
        }

        public String getVersion() {
            return version;
        }

        public void setVersion(String version) {
            this.version = version;
        }

        public String getNfvType() {
            return nfvType;
        }

        public void setNfvType(String nfvType) {
            this.nfvType = nfvType;
        }

        public String getMoc() {
            return moc;
        }

        public void setMoc(String moc) {
            this.moc = moc;
        }

        public String getFlavor() {
            return flavor;
        }

        public void setFlavor(String flavor) {
            this.flavor = flavor;
        }

        public List<STFlavor> getStFlavor() {
            return stFlavor;
        }

        public void setStFlavor(List<STFlavor> stFlavor) {
            this.stFlavor = stFlavor;
        }

        @XmlElement
        private String templateVersion;

        @XmlElement
        private String templateAuthor;

        @XmlElement
        private String vendor;

        @XmlElement
        private String version;

        @XmlElement
        private String nfvType;

        @XmlElement
        private String moc;

        @XmlElement
        private String flavor;

        @XmlElementWrapper(name = "flavorList")
        @XmlElement(name = "flavor")
        private List<STFlavor> stFlavor;
    }

    @XmlRootElement
    @XmlAccessorType(XmlAccessType.NONE)
    public static class STFlavor {
        @XmlAttribute
        private String name;

        @XmlAttribute
        private String desc;

        @XmlElementWrapper(name = "nodeList")
        @XmlElement(name = "node")
        private List<STFlavorConstituent> stFlavorConstituent;

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public String getDesc() {
            return desc;
        }

        public void setDesc(String desc) {
            this.desc = desc;
        }

        public List<STFlavorConstituent> getStFlavorConstituent() {
            return stFlavorConstituent;
        }

        public void setStFlavorConstituent(
                List<STFlavorConstituent> stFlavorConstituent) {
            this.stFlavorConstituent = stFlavorConstituent;
        }
    }

    @XmlRootElement
    @XmlAccessorType(XmlAccessType.NONE)
    public static class STFlavorConstituent {
        @XmlAttribute
        private String numberOfInstances;

        @XmlAttribute
        private String name;

        @XmlAttribute
        private String refNodeFlavor;

        @XmlAttribute
        private String affinity;

        @XmlAttribute
        private String redundancyModel;

        @XmlAttribute
        private String capability;

        public String getAffinity() {
            return affinity;
        }

        public void setAffinity(String affinity) {
            this.affinity = affinity;
        }

        public String getRedundancyModel() {
            return redundancyModel;
        }

        public void setRedundancyModel(String redundancyModel) {
            this.redundancyModel = redundancyModel;
        }

        public String getCapability() {
            return capability;
        }

        public void setCapability(String capability) {
            this.capability = capability;
        }

        public String getNumberOfInstances() {
            return numberOfInstances;
        }

        public void setNumberOfInstances(String numberOfInstances) {
            this.numberOfInstances = numberOfInstances;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public String getRefNodeFlavor() {
            return refNodeFlavor;
        }

        public void setRefNodeFlavor(String refNodeFlavor) {
            this.refNodeFlavor = refNodeFlavor;
        }
    }

    private Boolean propNullFlag;

    private boolean isPropNotNull() {
        if (null == propNullFlag) {
            propNullFlag = null != this.getBoundary()
                    && null != this.getBoundary().getProperties()
                    && null != this.getBoundary().getProperties().getProperty();
        }
        return propNullFlag;
    }

    public String getProductType() {
        return isPropNotNull() ? this.getBoundary().getProperties()
                .getProperty().getMoc() : null;
    }

    public String getVendor() {
        return isPropNotNull() ? this.getBoundary().getProperties()
                .getProperty().getVendor() : null;
    }

    public String getVersion() {
        return isPropNotNull() ? this.getBoundary().getProperties()
                .getProperty().getVersion() : null;
    }

    public String getNfvtype() {
        return isPropNotNull() ? this.getBoundary().getProperties()
                .getProperty().getNfvType() : null;
    }

    public String getFlavor() {
        return isPropNotNull() ? this.getBoundary().getProperties()
                .getProperty().getFlavor() : null;
    }

    public List<STFlavor> getSTFlavorList() {
        return isPropNotNull() ? this.getBoundary().getProperties()
                .getProperty().getStFlavor() : null;
    }
}
