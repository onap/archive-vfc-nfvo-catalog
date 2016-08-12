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
package org.openo.orchestrator.nfv.catalog.model.parser;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;
import java.util.zip.ZipInputStream;

import org.openo.orchestrator.nfv.catalog.common.ToolUtil;
import org.openo.orchestrator.nfv.catalog.db.exception.CatalogResourceException;
import org.openo.orchestrator.nfv.catalog.db.resource.TemplateManager;
import org.openo.orchestrator.nfv.catalog.entity.response.CsarFileUriResponse;
import org.openo.orchestrator.nfv.catalog.model.common.TemplateDataHelper;
import org.openo.orchestrator.nfv.catalog.model.entity.EnumDataType;
import org.openo.orchestrator.nfv.catalog.model.entity.InputParameter;
import org.openo.orchestrator.nfv.catalog.model.entity.NodeTemplate;
import org.openo.orchestrator.nfv.catalog.model.entity.RelationShip;
import org.openo.orchestrator.nfv.catalog.model.entity.ServiceTemplate;
import org.openo.orchestrator.nfv.catalog.model.entity.ServiceTemplateOperation;
import org.openo.orchestrator.nfv.catalog.model.entity.SubstitutionMapping;
import org.openo.orchestrator.nfv.catalog.model.parser.yaml.YamlParseServiceConsumer;
import org.openo.orchestrator.nfv.catalog.model.parser.yaml.entity.EnumYamlServiceTemplateInfo;
import org.openo.orchestrator.nfv.catalog.model.parser.yaml.entity.ParseYamlRequestParemeter;
import org.openo.orchestrator.nfv.catalog.model.parser.yaml.entity.ParseYamlResult;
import org.openo.orchestrator.nfv.catalog.model.parser.yaml.entity.ParseYamlResult.Plan;
import org.openo.orchestrator.nfv.catalog.model.parser.yaml.entity.ParseYamlResult.Plan.PlanValue.PlanInput;
import org.openo.orchestrator.nfv.catalog.model.parser.yaml.entity.ParseYamlResult.TopologyTemplate.Input;
import org.openo.orchestrator.nfv.catalog.model.parser.yaml.entity.ParseYamlResult.TopologyTemplate.NodeTemplate.Relationship;
import org.openo.orchestrator.nfv.catalog.wrapper.PackageWrapper;

public class ToscaYamlModelParser extends AbstractModelParser{

    private static final Object TOSCA_META_FIELD_ENTRY_DEFINITIONS = "Entry-Definitions";

    /**
     * 
     */
    @Override
    public String parse(String packageId, String fileLocation)
            throws CatalogResourceException {
        ParseYamlResult result = YamlParseServiceConsumer.getServiceTemplates(comboRequest(fileLocation));

        Map<String, String> toscaMeta = parseToscaMeta(fileLocation);
        String stFileName = toscaMeta.get(TOSCA_META_FIELD_ENTRY_DEFINITIONS);
        CsarFileUriResponse stDownloadUri = PackageWrapper.getInstance()
                .getCsarFileDownloadUri(packageId, stFileName);

        ServiceTemplate st = parseServiceTemplate(packageId, result,
                stDownloadUri.getDownloadUri());
        List<NodeTemplate> ntList = parseNodeTemplates(packageId,
                st.getServiceTemplateId(), result);
        st.setType(getTemplateType(result, ntList).toString());

        TemplateManager.getInstance().addServiceTemplate(
                TemplateDataHelper.convert2TemplateData(st,
                        ToolUtil.toJson(result), ntList));

        SubstitutionMapping stm = parseSubstitutionMapping(
                st.getServiceTemplateId(), result);
        if (stm != null) {
            TemplateManager.getInstance().addServiceTemplateMapping(
                    TemplateDataHelper.convert2TemplateMappingData(stm));
        }

        return st.getServiceTemplateId();
    }

    /**
     * @param fileLocation
     * @return
     * @throws CatalogResourceException
     */
    @SuppressWarnings("resource")
    private Map<String, String> parseToscaMeta(String fileLocation)
            throws CatalogResourceException {
        Map<String, String> toscaMeta = new HashMap<>();

        ZipInputStream zin = null;
        BufferedReader br = null;
        try {
            InputStream in = new BufferedInputStream(new FileInputStream(
                    fileLocation));
            zin = new ZipInputStream(in);
            ZipEntry ze;
            while ((ze = zin.getNextEntry()) != null) {
                if (("TOSCA-Metadata" + File.separator + "TOSCA.meta")
                        .equals(ze.getName())
                        || "TOSCA-Metadata/TOSCA.meta".equals(ze.getName())) {
                    ZipFile zf = new ZipFile(fileLocation);
                    br = new BufferedReader(new InputStreamReader(
                            zf.getInputStream(ze)));
                    String line;
                    String[] tmps;
                    while ((line = br.readLine()) != null) {
                        if (line.indexOf(":") > 0) {
                            tmps = line.split(":");
                            toscaMeta.put(tmps[0].trim(), tmps[1].trim());
                        }
                    }

                    return toscaMeta;
                }
            }

        } catch (IOException e) {
            throw new CatalogResourceException("Parse Tosca Meta Fail.", e);
        } finally {
            closeStreamAndReader(zin, br);
        }

        return toscaMeta;
    }

    private void closeStreamAndReader(ZipInputStream zin, BufferedReader br) {
        if (br != null) {
            try {
                br.close();
            } catch (IOException e) {
            }
        }
        if (zin != null) {
            try {
                zin.closeEntry();
            } catch (IOException e) {
            }
        }
    }

    private ParseYamlRequestParemeter comboRequest(String fileLocation) {
        ParseYamlRequestParemeter request = new ParseYamlRequestParemeter();
        request.setPath(fileLocation);
        return request;
    }

    /**
     * @param serviceTemplateId
     * @param result
     * @return
     */
    private SubstitutionMapping parseSubstitutionMapping(
            String serviceTemplateId, ParseYamlResult result) {
        String type = getSubstitutionMappingType(result);
        if (ToolUtil.isTrimedEmptyString(type)) {
            return null;
        }

        org.openo.orchestrator.nfv.catalog.model.parser.yaml.entity.ParseYamlResult.TopologyTemplate.SubstitutionMapping stm = result
                .getTopologyTemplate().getSubstitutionMappings();
        return new SubstitutionMapping(serviceTemplateId, type,
                stm.getRequirementList(), stm.getCapabilityList());
    }

    private ServiceTemplate parseServiceTemplate(String packageId,
            ParseYamlResult result, String stDownloadUri) {
        ServiceTemplate st = new ServiceTemplate();

        st.setServiceTemplateId(ToolUtil.generateId());
        st.setTemplateName(result.getMetadata().get(
                EnumYamlServiceTemplateInfo.ID.getName()));
        st.setVendor(result.getMetadata().get(
                EnumYamlServiceTemplateInfo.PROVIDER.getName()));
        st.setVersion(result.getMetadata().get(
                EnumYamlServiceTemplateInfo.VERSION.getName()));
        st.setCsarid(packageId);
        st.setDownloadUri(stDownloadUri);
        st.setInputs(parseInputs(result));
        ServiceTemplateOperation[] operations = parseOperations(result
                .getPlanList());
        st.setOperations(operations);
        return st;
    }

    /**
     * @param planList
     * @return
     */
    private ServiceTemplateOperation[] parseOperations(List<Plan> planList) {
        if (planList == null || planList.isEmpty()) {
            return new ServiceTemplateOperation[0];
        }

        List<ServiceTemplateOperation> opList = new ArrayList<>();
        for (Plan plan : planList) {
            ServiceTemplateOperation op = new ServiceTemplateOperation();
            op.setName(plan.getName());
            op.setDescription(plan.getDescription());
            String processId = null; // TODO
            op.setProcessId(processId);
            InputParameter[] inputs = parsePlanInputs(plan.getInputList());
            op.setInputs(inputs);

            opList.add(op);

        }
        return opList.toArray(new ServiceTemplateOperation[0]);
    }

    /**
     * @param inputList
     * @return
     */
    private InputParameter[] parsePlanInputs(List<PlanInput> inputList) {
        if (inputList == null || inputList.isEmpty()) {
            return new InputParameter[0];
        }

        List<InputParameter> retList = new ArrayList<>();
        for (PlanInput input : inputList) {
            retList.add(new InputParameter(input.getName(),
                    getEnumDataType(input.getType()), input.getDescription(),
                    input.getDefault(), input.isRequired()));
        }
        return retList.toArray(new InputParameter[0]);
    }

    private InputParameter[] parseInputs(ParseYamlResult result) {
        List<Input> inputList = result.getTopologyTemplate().getInputs();
        if(inputList == null){
            return null;
        }
        ArrayList<InputParameter> retList = new ArrayList<InputParameter>();
        for(Input input : inputList){
            retList.add(new InputParameter(input.getName(),
                    getEnumDataType(input.getType()), input.getDescription(),
                    input.getDefault(), input.isRequired()));
        }
        return retList.toArray(new InputParameter[0]);
    }

    /**
     * @param type
     * @return
     */
    private EnumDataType getEnumDataType(String type) {
        if (EnumDataType.INTEGER.toString().equalsIgnoreCase(type)) {
            return EnumDataType.INTEGER;
        }

        if (EnumDataType.FLOAT.toString().equalsIgnoreCase(type)) {
            return EnumDataType.FLOAT;
        }

        if (EnumDataType.BOOLEAN.toString().equalsIgnoreCase(type)) {
            return EnumDataType.BOOLEAN;
        }

        return EnumDataType.STRING;
    }

    /**
     * @param csarId
     * @param templateId
     * @param result
     * @return
     */
    private List<NodeTemplate> parseNodeTemplates(String csarId,
            String templateId, ParseYamlResult result) {
        List<ParseYamlResult.TopologyTemplate.NodeTemplate> nodetemplateList = result.getTopologyTemplate().getNodeTemplates();
        if(nodetemplateList == null){
            return null;
        }
        
        List<NodeTemplate> retList = new ArrayList<>();
        for (ParseYamlResult.TopologyTemplate.NodeTemplate nodeTemplate : nodetemplateList) {
            NodeTemplate ret = new NodeTemplate();
            ret.setId(nodeTemplate.getName());
            ret.setName(nodeTemplate.getName());
            ret.setType(nodeTemplate.getNodeType());
            ret.setProperties(nodeTemplate.getPropertyList());
            List<RelationShip> relationShipList = parseNodeTemplateRelationShip(nodeTemplate
                    .getRelationships());
            ret.setRelationShips(relationShipList);

            retList.add(ret);
        }

        return retList;
    }
    
    
    private List<RelationShip> parseNodeTemplateRelationShip(
            List<Relationship> relationshipList) {
        List<RelationShip> retList = new ArrayList<>();

        if (relationshipList == null) {
            return retList;
        }

        for (Relationship relationship : relationshipList) {
            RelationShip ret = new RelationShip();
            ret.setSourceNodeId(relationship.getSourceNodeName());
            ret.setSourceNodeName(relationship.getSourceNodeName());
            ret.setTargetNodeId(relationship.getTargetNodeName());
            ret.setTargetNodeName(relationship.getTargetNodeName());
            ret.setType(relationship.getType());
            retList.add(ret);
        }

        return retList;
    }
    
    private EnumTemplateType getTemplateType(ParseYamlResult result,
            List<NodeTemplate> ntList) {
        String type = getSubstitutionMappingType(result);
        if (isNSType(type)) {
            return EnumTemplateType.NS;
        }
        
        if (isVNFType(type)) {
            return EnumTemplateType.VNF;
        }

        return getTemplateTypeFromNodeTemplates(ntList);
    }

    private String getSubstitutionMappingType(ParseYamlResult result) {
        if (result.getTopologyTemplate().getSubstitutionMappings() == null) {
            return null;
        }
        return result.getTopologyTemplate().getSubstitutionMappings()
                .getNode_type();
    }

    /**
     * @param ntList
     * @return
     */
    private EnumTemplateType getTemplateTypeFromNodeTemplates(
            List<NodeTemplate> ntList) {
        for (NodeTemplate nt : ntList) {
            if (isNSType(nt.getType()) || isVNFType(nt.getType())) {
                return EnumTemplateType.NS;
            }
        }

        return EnumTemplateType.VNF;
    }

    private boolean isVNFType(String type) {
        if (ToolUtil.isTrimedEmptyString(type)) {
            return false;
        }
        return type.toUpperCase().contains(".VNF");
    }

    private boolean isNSType(String type) {
        if (ToolUtil.isTrimedEmptyString(type)) {
            return false;
        }
        return type.toUpperCase().contains(".NS");
    }
}
