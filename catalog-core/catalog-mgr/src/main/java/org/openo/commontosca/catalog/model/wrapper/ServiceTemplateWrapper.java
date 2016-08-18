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
package org.openo.commontosca.catalog.model.wrapper;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.openo.commontosca.catalog.model.entity.ServiceTemplateOperation;
import org.openo.commontosca.catalog.resources.CatalogBadRequestException;
import org.openo.commontosca.catalog.common.ToolUtil;
import org.openo.commontosca.catalog.db.entity.NodeTemplateData;
import org.openo.commontosca.catalog.db.entity.PackageData;
import org.openo.commontosca.catalog.db.entity.ServiceTemplateData;
import org.openo.commontosca.catalog.db.entity.ServiceTemplateMappingData;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.resource.TemplateManager;
import org.openo.commontosca.catalog.model.common.TemplateDataHelper;
import org.openo.commontosca.catalog.model.entity.InputParameter;
import org.openo.commontosca.catalog.model.entity.NfvTemplate;
import org.openo.commontosca.catalog.model.entity.NodeTemplate;
import org.openo.commontosca.catalog.model.entity.QueryRawDataCondition;
import org.openo.commontosca.catalog.model.entity.ServiceTemplate;
import org.openo.commontosca.catalog.model.entity.ServiceTemplateRawData;
import org.openo.commontosca.catalog.model.entity.SubstitutionMapping;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * 
 * @author 10090474
 * 
 */
public class ServiceTemplateWrapper {
    private static ServiceTemplateWrapper instance;
    private static final Logger logger = LoggerFactory.getLogger(ServiceTemplateWrapper.class);

    public static ServiceTemplateWrapper getInstance() {
        if (instance == null) {
            instance = new ServiceTemplateWrapper();
        }
        return instance;
    }

    /**
     * 
     * @param serviceTemplateId
     * @return
     * @throws CatalogResourceException
     */
    public ServiceTemplate getServiceTemplateById(String serviceTemplateId)
            throws CatalogResourceException {
        logger.info("getServiceTemplateById. serviceTemplateId = "
                + serviceTemplateId);

        List<ServiceTemplateData> stdList = TemplateManager.getInstance()
                .queryServiceTemplateById(serviceTemplateId);
        if (stdList == null || stdList.isEmpty()) {
            throw new CatalogResourceException("Can't find this servcie template");
        }
        
        return TemplateDataHelper.convert2ServiceTemplate(stdList.get(0));
    }


    /**
     * 
     * @param status
     * @param deletionPending
     * @return
     * @throws CatalogResourceException
     */
    public ServiceTemplate[] getServiceTemplates(String status,
            boolean deletionPending) throws CatalogResourceException {
        PackageData pd = new PackageData();
        pd.setUsageState(status);
        pd.setDeletionPending(String.valueOf(deletionPending));

        List<ServiceTemplateData> stdList = TemplateManager.getInstance()
                .queryServiceTemplateByCsarPackageInfo(pd);

        return TemplateDataHelper.convert2ServiceTemplates(stdList);
    }


    /**
     * @param nodeTypeIds
     * @return
     * @throws CatalogResourceException
     */
    public ServiceTemplate[] getNestingServiceTemplate(String[] nodeTypeIds)
            throws CatalogResourceException {
        ServiceTemplate[] sts = new ServiceTemplate[nodeTypeIds.length];
        for (int i = 0; i < nodeTypeIds.length; i++) {
            SubstitutionMapping stm = getSubstitutionMappingsByNodeTypeId(nodeTypeIds[i]);
            if (stm == null) {
                sts[i] = null;
            } else {
                sts[i] = getServiceTemplateById(stm.getServiceTemplateId());
            }
        }

        return sts;
    }

    /**
     * @param nodeTypeId
     * @return
     * @throws CatalogResourceException
     */
    private SubstitutionMapping getSubstitutionMappingsByNodeTypeId(
            String nodeTypeId) throws CatalogResourceException {
        List<ServiceTemplateMappingData> stmDataList = TemplateManager
                .getInstance().queryServiceTemplateMapping(nodeTypeId, null);
        if (stmDataList == null || stmDataList.isEmpty()) {
            return null;
        }

        return TemplateDataHelper.convert2SubstitutionMapping(stmDataList
                .get(0));
    }


    /**
     * @param queryCondition
     * @return
     * @throws CatalogResourceException
     * @throws CatalogBadRequestException
     */
    public ServiceTemplateRawData getServiceTemplateRawData(
            QueryRawDataCondition queryCondition)
            throws CatalogResourceException, CatalogBadRequestException {
        if (ToolUtil.isTrimedEmptyString(queryCondition.getCsarId())) {
            throw new CatalogBadRequestException("CsarId is null.");
        }
        PackageData pd = new PackageData();
        pd.setCsarId(queryCondition.getCsarId());

        List<ServiceTemplateData> stdList = TemplateManager.getInstance()
                .queryServiceTemplateByCsarPackageInfo(pd);

        if (stdList == null || stdList.isEmpty()) {
            throw new CatalogResourceException(
                    "Can't find this servcie template");
        }

        return new ServiceTemplateRawData(stdList.get(0).getRowData());
    }

    /**
     * 
     * @param serviceTemplateId
     * @return
     * @throws CatalogResourceException
     */
    public InputParameter[] getServiceTemplateParameters(
            String serviceTemplateId) throws CatalogResourceException {
        ServiceTemplate st = getServiceTemplateById(serviceTemplateId);
        return st.getInputs();
    }

    /**
     * 
     * @param serviceTemplateId
     * @return
     */
    public ServiceTemplateOperation[] getTemplateOperations(
            String serviceTemplateId) throws CatalogResourceException {
        ServiceTemplate st = getServiceTemplateById(serviceTemplateId);

        if (st.getOperations() == null) {
            return new ServiceTemplateOperation[0];
        }
        return st.getOperations();
    }

    /**
     * @param serviceTemplateId
     * @param operationName
     * @return
     * @throws CatalogResourceException
     */
    public InputParameter[] getParametersByOperationName(
            String serviceTemplateId, String operationName)
            throws CatalogResourceException {
        if (ToolUtil.isTrimedEmptyString(operationName)) {
            throw new CatalogResourceException("Operation Name is null.");
        }

        ServiceTemplateOperation[] operations = getTemplateOperations(serviceTemplateId);
        for (int i = 0; i < operations.length; i++) {
            if (operationName.equals(operations[i].getName())) {
                return operations[i].getInputs();
            }
        }

        throw new CatalogResourceException("Can't find this operation.");
    }


    /**
     * @param serviceTemplateId
     * @param nodeTemplateId
     * @return
     * @throws CatalogResourceException
     */
    public NodeTemplate getNodeTemplateById(String serviceTemplateId,
            String nodeTemplateId) throws CatalogResourceException {
        List<NodeTemplateData> ntdList = TemplateManager.getInstance()
                .queryNodeTemplateById(serviceTemplateId, nodeTemplateId);

        if (ntdList == null || ntdList.isEmpty()) {
            throw new CatalogResourceException("Can't find this node template.");
        }

        return TemplateDataHelper.convert2NodeTemplate(ntdList.get(0));
    }

    /**
     * @param serviceTemplateId
     * @param types
     * @return
     * @throws CatalogResourceException
     */
    public NodeTemplate[] getNodeTemplates(String serviceTemplateId,
            String[] types) throws CatalogResourceException {
        List<NodeTemplateData> ntdList = TemplateManager.getInstance()
                .queryNodeTemplateBySeriviceTemplateId(serviceTemplateId);
        if (ntdList == null || ntdList.isEmpty()) {
            return new NodeTemplate[0];
        }

        if (ToolUtil.isTrimedEmptyArray(types)) { // return all node templates
            return TemplateDataHelper.convert2NodeTemplates(ntdList);
        }

        List<NodeTemplate> ntList = new ArrayList<>();
        for (String type : types) {
            if (!ToolUtil.isTrimedEmptyString(type)) {
                List<NodeTemplateData> typedNtdList = filterNodeTemplateDataListByType(
                        ntdList, type);
                ntList.addAll(Arrays
.asList(TemplateDataHelper
                        .convert2NodeTemplates(typedNtdList)));
            }
        }
        return ntList.toArray(new NodeTemplate[0]);
    }

    /**
     * @param ntdList
     * @param type
     * @return
     */
    private List<NodeTemplateData> filterNodeTemplateDataListByType(
            List<NodeTemplateData> ntdList, String type) {
        List<NodeTemplateData> retList = new ArrayList<>();
        for (NodeTemplateData ntd : ntdList) {
            if (type.equals(ntd.getType())) {
                retList.add(ntd);
            }
        }
        return retList;
    }


    /**
     * @param serviceTemlateId
     * @return
     * @throws CatalogResourceException
     */
    public NfvTemplate getNfvTemplate(String serviceTemlateId)
            throws CatalogResourceException {
        NodeTemplate[] nts = getNodeTemplates(serviceTemlateId, null);

        List<NodeTemplate> vduNodes = new ArrayList<>();
        List<NodeTemplate> networkNodes = new ArrayList<>();
        List<NodeTemplate> vnfcNodes = new ArrayList<>();
        List<NodeTemplate> vnfNodes = new ArrayList<>();
        for (NodeTemplate nt : nts) {
            if (isVduNode(nt.getType())) {
                vduNodes.add(nt);
                continue;
            }

            if (isNetworkNode(nt.getType())) {
                networkNodes.add(nt);
                continue;
            }
            
            if (isVnfcNode(nt.getType())) {
                vnfcNodes.add(nt);
                continue;
            }
            
            if (isVnfNode(nt.getType())) {
                vnfNodes.add(nt);
                continue;
            }
        }
        
        return new NfvTemplate(vduNodes, networkNodes, vnfcNodes, vnfNodes);
    }

    /**
     * @param type
     * @return
     */
    private boolean isVnfNode(String type) {
        return type.toUpperCase().indexOf(".VNF") > 0;
    }

    /**
     * @param type
     * @return
     */
    private boolean isVnfcNode(String type) {
        return type.toUpperCase().indexOf(".VNFC") > 0;
    }

    /**
     * @param type
     * @return
     */
    private boolean isNetworkNode(String type) {
        return type.toUpperCase().indexOf(".VL") > 0
                || type.toUpperCase().indexOf(".VIRTUALLINK") > 0;
    }

    /**
     * @param type
     * @return
     */
    private boolean isVduNode(String type) {
        return type.toUpperCase().indexOf(".VDU") > 0;
    }

}
