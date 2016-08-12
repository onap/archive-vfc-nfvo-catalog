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
package org.openo.orchestrator.nfv.catalog.db.entity;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@Entity
@Table(name = "catalog_service_template_table")
@JsonIgnoreProperties(ignoreUnknown = true)
public class ServiceTemplateData extends BaseData {
    @Id
    @Column(name = "SERVICETEMPLATEID")
    private String serviceTemplateId;
    @Column(name = "TEMPLATENAME")
    private String templateName;

    @Column(name = "TYPE")
    private String type;

    @Column(name = "VENDOR")
    private String vendor;

    @Column(name = "VERSION")
    private String version;

    @Column(name = "CSARID")
    private String csarId;

    @Column(name = "INPUTS")
    private String inputs;

    @Column(name = "DOWNLOADURI")
    private String downloadUri;

    @Column(name = "ROWDATA")
    private String rowData;
    @Column(name = "OPERATIONS")
    private String operations;

    public String getRowData() {
        return rowData;
    }

    public void setRowData(String rowData) {
        this.rowData = rowData;
    }

    public String getOperations() {
        return operations;
    }

    public void setOperations(String operations) {
        this.operations = operations;
    }

    public String getTemplateName() {
        return templateName;
    }

    public void setTemplateName(String templateName) {
        this.templateName = templateName;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
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

    public String getCsarId() {
        return csarId;
    }

    public void setCsarId(String csarId) {
        this.csarId = csarId;
    }

    public String getInputs() {
        return inputs;
    }

    public void setInputs(String inputs) {
        this.inputs = inputs;
    }

    public String getDownloadUri() {
        return downloadUri;
    }

    public void setDownloadUri(String downloadUri) {
        this.downloadUri = downloadUri;
    }

    public void setServiceTemplateId(String serviceTemplateId) {
        this.serviceTemplateId = serviceTemplateId;
    }

    public String getServiceTemplateId() {
        return serviceTemplateId;
    }

}
