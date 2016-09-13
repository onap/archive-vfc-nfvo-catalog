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

package org.openo.commontosca.catalog.model.parser.yaml.zte;

import org.openo.commontosca.catalog.common.MsbAddrConfig;
import org.openo.commontosca.catalog.common.ToolUtil;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.resource.TemplateManager;
import org.openo.commontosca.catalog.entity.response.CsarFileUriResponse;
import org.openo.commontosca.catalog.model.common.TemplateDataHelper;
import org.openo.commontosca.catalog.model.entity.EnumDataType;
import org.openo.commontosca.catalog.model.entity.InputParameter;
import org.openo.commontosca.catalog.model.entity.NodeTemplate;
import org.openo.commontosca.catalog.model.entity.OutputParameter;
import org.openo.commontosca.catalog.model.entity.RelationShip;
import org.openo.commontosca.catalog.model.entity.ServiceTemplate;
import org.openo.commontosca.catalog.model.entity.ServiceTemplateOperation;
import org.openo.commontosca.catalog.model.entity.SubstitutionMapping;
import org.openo.commontosca.catalog.model.parser.AbstractModelParser;
import org.openo.commontosca.catalog.model.parser.EnumTemplateType;
import org.openo.commontosca.catalog.model.parser.yaml.zte.entity.EnumYamlServiceTemplateInfo;
import org.openo.commontosca.catalog.model.parser.yaml.zte.entity.ParseYamlRequestParemeter;
import org.openo.commontosca.catalog.model.parser.yaml.zte.entity.ParseYamlResult;
import org.openo.commontosca.catalog.model.parser.yaml.zte.entity.ParseYamlResult.Plan;
import org.openo.commontosca.catalog.model.parser.yaml.zte.entity.ParseYamlResult.Plan.PlanValue.PlanInput;
import org.openo.commontosca.catalog.model.parser.yaml.zte.entity.ParseYamlResult.TopologyTemplate.Input;
import org.openo.commontosca.catalog.model.parser.yaml.zte.entity.ParseYamlResult.TopologyTemplate.Output;
import org.openo.commontosca.catalog.model.parser.yaml.zte.entity.ParseYamlResult.TopologyTemplate.NodeTemplate.Relationship;
import org.openo.commontosca.catalog.model.parser.yaml.zte.service.YamlParseServiceConsumer;
import org.openo.commontosca.catalog.model.plan.wso2.Wso2ServiceConsumer;
import org.openo.commontosca.catalog.model.plan.wso2.entity.DeployPackageResponse;
import org.openo.commontosca.catalog.wrapper.PackageWrapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

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


public class ToscaYamlModelParser extends AbstractModelParser {

  private static final Object TOSCA_META_FIELD_ENTRY_DEFINITIONS = "Entry-Definitions";
  private static final Logger LOGGER = LoggerFactory.getLogger(ToscaYamlModelParser.class);

  @Override
  public String parse(String packageId, String fileLocation) throws CatalogResourceException {
    ParseYamlResult result = getParseYamlResult(fileLocation);
    
    Map<String, String> toscaMeta = parseToscaMeta(fileLocation);
    String stFileName = toscaMeta.get(TOSCA_META_FIELD_ENTRY_DEFINITIONS);
    CsarFileUriResponse stDownloadUri =
        PackageWrapper.getInstance().getCsarFileDownloadUri(packageId, stFileName);

    ServiceTemplate st = parseServiceTemplate(packageId, result, stDownloadUri.getDownloadUri());
    ServiceTemplateOperation[] operations = parseOperations(result.getPlanList(), fileLocation);
    st.setOperations(operations);
    List<NodeTemplate> ntList = parseNodeTemplates(packageId, st.getServiceTemplateId(), result);
    st.setType(getTemplateType(result, ntList).toString());

    TemplateManager.getInstance().addServiceTemplate(
        TemplateDataHelper.convert2TemplateData(st, ToolUtil.toJson(result), ntList));

    SubstitutionMapping stm = parseSubstitutionMapping(st.getServiceTemplateId(), result);
    if (stm != null) {
      TemplateManager.getInstance()
          .addServiceTemplateMapping(TemplateDataHelper.convert2TemplateMappingData(stm));
    }

    return st.getServiceTemplateId();
  }

  private ParseYamlResult getParseYamlResult(String fileLocation) throws CatalogResourceException {
    String destPath = copyTemporaryFile2HttpServer(fileLocation);
    try {
      String url = getUrl(toTempFileLocalPath(fileLocation));
      return YamlParseServiceConsumer.getServiceTemplates(comboRequest(url));
    } finally {
      if (destPath != null && !destPath.isEmpty() && (new File(destPath)).exists()) {
        (new File(destPath)).delete();
      }
    }
  }

  private String toTempFileLocalPath(String fileLocation) {
    return File.separator + "temp" + File.separator + (new File(fileLocation)).getName();
  }
  
  private String getUrl(String uri) {
    String url = null;
    if ((MsbAddrConfig.getMsbAddress().endsWith("/")) && uri.startsWith("/")) {
      url = MsbAddrConfig.getMsbAddress() + uri.substring(1);
    }
    url = MsbAddrConfig.getMsbAddress() + uri;
    String urlresult = url.replace("\\", "/");
    return urlresult;
  }

  private String copyTemporaryFile2HttpServer(String fileLocation) throws CatalogResourceException {
    String destPath = Class.class.getClass().getResource("/").getPath()
        + org.openo.commontosca.catalog.filemanage.http.ToolUtil.getHttpServerPath()
        + toTempFileLocalPath(fileLocation);
    if (!org.openo.commontosca.catalog.filemanage.http.ToolUtil.copyFile(fileLocation, destPath,
        true)) {
      throw new CatalogResourceException("Copy Temporary To HttpServer Failed.");
    }
    return destPath;
  }

  @SuppressWarnings("resource")
  private Map<String, String> parseToscaMeta(String fileLocation) throws CatalogResourceException {
    Map<String, String> toscaMeta = new HashMap<>();

    ZipInputStream zin = null;
    BufferedReader br = null;
    try {
      InputStream in = new BufferedInputStream(new FileInputStream(fileLocation));
      zin = new ZipInputStream(in);
      ZipEntry ze;
      while ((ze = zin.getNextEntry()) != null) {
        if (("TOSCA-Metadata" + File.separator + "TOSCA.meta").equals(ze.getName())
            || "TOSCA-Metadata/TOSCA.meta".equals(ze.getName())) {
          ZipFile zf = new ZipFile(fileLocation);
          br = new BufferedReader(new InputStreamReader(zf.getInputStream(ze)));
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

    } catch (IOException e1) {
      throw new CatalogResourceException("Parse Tosca Meta Fail.", e1);
    } finally {
      closeStreamAndReader(zin, br);
    }

    return toscaMeta;
  }

  private void closeStreamAndReader(ZipInputStream zin, BufferedReader br) {
    if (br != null) {
      try {
        br.close();
      } catch (IOException e1) {
        LOGGER.error("Buffered reader close failed !");
      }
    }
    if (zin != null) {
      try {
        zin.closeEntry();
      } catch (IOException e2) {
        LOGGER.error("Zip inputStream close failed !");
      }
    }
  }

  private ParseYamlRequestParemeter comboRequest(String fileLocation) {
    ParseYamlRequestParemeter request = new ParseYamlRequestParemeter();
    request.setPath(fileLocation);
    return request;
  }

  private SubstitutionMapping parseSubstitutionMapping(String serviceTemplateId,
      ParseYamlResult result) {
    String type = getSubstitutionMappingType(result);
    if (ToolUtil.isTrimedEmptyString(type)) {
      return null;
    }

    org.openo.commontosca.catalog.model.parser.yaml.zte.entity.ParseYamlResult
        .TopologyTemplate.SubstitutionMapping stm =
        result.getTopologyTemplate().getSubstitutionMappings();
    return new SubstitutionMapping(serviceTemplateId, type, stm.getRequirementList(),
        stm.getCapabilityList());
  }

  private ServiceTemplate parseServiceTemplate(String packageId, ParseYamlResult result,
      String stDownloadUri) {
    ServiceTemplate st = new ServiceTemplate();

    st.setServiceTemplateId(ToolUtil.generateId());
    st.setTemplateName(result.getMetadata().get(EnumYamlServiceTemplateInfo.ID.getName()));
    st.setVendor(result.getMetadata().get(EnumYamlServiceTemplateInfo.PROVIDER.getName()));
    st.setVersion(result.getMetadata().get(EnumYamlServiceTemplateInfo.VERSION.getName()));
    st.setCsarid(packageId);
    st.setDownloadUri(stDownloadUri);
    st.setInputs(parseInputs(result));
    st.setOutputs(parseOutputs(result));
    return st;
  }

  private InputParameter[] parseInputs(ParseYamlResult result) {
    List<Input> inputList = result.getTopologyTemplate().getInputs();
    if (inputList == null) {
      return new InputParameter[0];
    }
    List<InputParameter> retList = new ArrayList<InputParameter>();
    for (Input input : inputList) {
      retList.add(new InputParameter(input.getName(), getEnumDataType(input.getType()),
          input.getDescription(), input.getDefault(), input.isRequired()));
    }
    return retList.toArray(new InputParameter[0]);
  }

  private OutputParameter[] parseOutputs(ParseYamlResult result) {
    List<Output> outputList = result.getTopologyTemplate().getOutputs();
    if (outputList == null || outputList.isEmpty()) {
      return new OutputParameter[0];
    }
    List<OutputParameter> retList = new ArrayList<OutputParameter>();
    for (Output output : outputList) {
      retList
          .add(new OutputParameter(output.getName(), output.getDescription(), output.getValue()));
    }
    return retList.toArray(new OutputParameter[0]);
  }

  private ServiceTemplateOperation[] parseOperations(List<Plan> planList, String zipFileLocation)
      throws CatalogResourceException {
    if (planList == null || planList.isEmpty()) {
      return new ServiceTemplateOperation[0];
    }

    List<ServiceTemplateOperation> opList = new ArrayList<>();
    for (Plan plan : planList) {
      ServiceTemplateOperation op = new ServiceTemplateOperation();
      op.setName(plan.getName());
      op.setDescription(plan.getDescription());
      checkPlanLanguage(plan.getPlanLanguage());
      DeployPackageResponse response =
          Wso2ServiceConsumer.deployPackage(zipFileLocation, plan.getReference());
      op.setPackageName(parsePackageName(response));
      op.setProcessId(response.getProcessId());
      op.setInputs(parsePlanInputs(plan.getInputList()));

      opList.add(op);

    }
    return opList.toArray(new ServiceTemplateOperation[0]);
  }

  private String parsePackageName(DeployPackageResponse response) {
    String packageName = response.getPackageName();
    if (packageName != null && packageName.indexOf("-") > 0) {
      packageName = packageName.substring(0, packageName.lastIndexOf("-"));
    }
    return packageName;
  }

  private void checkPlanLanguage(String planLanguage) throws CatalogResourceException {
    if (planLanguage == null || planLanguage.isEmpty()) {
      throw new CatalogResourceException("Plan Language is empty.");
    }
    if (planLanguage.equalsIgnoreCase("bpel")) {
      return;
    }
    if (planLanguage.equalsIgnoreCase("bpmn")) {
      return;
    }
    if (planLanguage.equalsIgnoreCase("bpmn4tosca")) {
      return;
    }
    throw new CatalogResourceException(
        "Plan Language is not supported. Language = " + planLanguage);
  }

  private InputParameter[] parsePlanInputs(List<PlanInput> inputList) {
    if (inputList == null || inputList.isEmpty()) {
      return new InputParameter[0];
    }

    List<InputParameter> retList = new ArrayList<>();
    for (PlanInput input : inputList) {
      retList.add(new InputParameter(input.getName(), getEnumDataType(input.getType()),
          input.getDescription(), input.getDefault(), input.isRequired()));
    }
    return retList.toArray(new InputParameter[0]);
  }

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

  private List<NodeTemplate> parseNodeTemplates(String csarId, String templateId,
      ParseYamlResult result) {
    List<ParseYamlResult.TopologyTemplate.NodeTemplate> nodetemplateList =
        result.getTopologyTemplate().getNodeTemplates();
    if (nodetemplateList == null) {
      return null;
    }

    List<NodeTemplate> retList = new ArrayList<>();
    for (ParseYamlResult.TopologyTemplate.NodeTemplate nodeTemplate : nodetemplateList) {
      NodeTemplate ret = new NodeTemplate();
      ret.setId(nodeTemplate.getName());
      ret.setName(nodeTemplate.getName());
      ret.setType(nodeTemplate.getNodeType());
      ret.setProperties(nodeTemplate.getPropertyList());
      List<RelationShip> relationShipList =
          parseNodeTemplateRelationShip(nodeTemplate.getRelationships());
      ret.setRelationShips(relationShipList);

      retList.add(ret);
    }

    return retList;
  }


  private List<RelationShip> parseNodeTemplateRelationShip(List<Relationship> relationshipList) {
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

  private EnumTemplateType getTemplateType(ParseYamlResult result, List<NodeTemplate> ntList) {
    String type = getSubstitutionMappingType(result);
    if (isNsType(type)) {
      return EnumTemplateType.NS;
    }

    if (isVnfType(type)) {
      return EnumTemplateType.VNF;
    }

    return getTemplateTypeFromNodeTemplates(ntList);
  }

  private String getSubstitutionMappingType(ParseYamlResult result) {
    if (result.getTopologyTemplate().getSubstitutionMappings() == null) {
      return null;
    }
    return result.getTopologyTemplate().getSubstitutionMappings().getNodeType();
  }

  private EnumTemplateType getTemplateTypeFromNodeTemplates(List<NodeTemplate> ntList) {
    for (NodeTemplate nt : ntList) {
      if (isNsType(nt.getType()) || isVnfType(nt.getType())) {
        return EnumTemplateType.NS;
      }
    }

    return EnumTemplateType.VNF;
  }

  private boolean isVnfType(String type) {
    if (ToolUtil.isTrimedEmptyString(type)) {
      return false;
    }
    return type.toUpperCase().contains(".VNF");
  }

  private boolean isNsType(String type) {
    if (ToolUtil.isTrimedEmptyString(type)) {
      return false;
    }
    return type.toUpperCase().contains(".NS");
  }
}
