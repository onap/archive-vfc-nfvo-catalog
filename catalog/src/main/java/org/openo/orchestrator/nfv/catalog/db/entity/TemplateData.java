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

import java.util.ArrayList;

public class TemplateData extends BaseData {
    private ServiceTemplateData serviceTemplate;
    private ArrayList<NodeTemplateData> nodeTemplates = new ArrayList<NodeTemplateData>();

    public ServiceTemplateData getServiceTemplate() {
        return serviceTemplate;
    }

    public void setServiceTemplate(ServiceTemplateData serviceTemplate) {
        this.serviceTemplate = serviceTemplate;
    }

    public ArrayList<NodeTemplateData> getNodeTemplates() {
        return nodeTemplates;
    }

    public void setNodeTemplates(ArrayList<NodeTemplateData> nodeTemplates) {
        this.nodeTemplates = nodeTemplates;
    }


}
