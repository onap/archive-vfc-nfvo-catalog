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
package org.openo.commontosca.catalog.model.parser;

import org.openo.commontosca.catalog.common.MsbAddrConfig;
import org.openo.commontosca.catalog.common.ToolUtil;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.model.common.TemplateUtils;
import org.openo.commontosca.catalog.model.entity.InputParameter;
import org.openo.commontosca.catalog.model.entity.NodeTemplate;
import org.openo.commontosca.catalog.model.entity.ServiceTemplateOperation;
import org.openo.commontosca.catalog.model.parser.yaml.yamlmodel.Input;
import org.openo.commontosca.catalog.model.parser.yaml.yamlmodel.Plan;
import org.openo.commontosca.catalog.model.plan.wso2.Wso2ServiceConsumer;
import org.openo.commontosca.catalog.model.plan.wso2.entity.DeployPackageResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

public abstract class AbstractModelParser {
  private static final Logger logger = LoggerFactory.getLogger(AbstractModelParser.class);

  public abstract String parse(String packageId, String fileLocation)
      throws CatalogResourceException;
  
  public String copyTemporaryFile2HttpServer(String fileLocation) throws CatalogResourceException {
    String destPath = org.openo.commontosca.catalog.filemanage.http.ToolUtil.getHttpServerAbsolutePath()
        + toTempFilePath(fileLocation);
    if (!org.openo.commontosca.catalog.filemanage.http.ToolUtil.copyFile(
        fileLocation, destPath, true)) {
      throw new CatalogResourceException("Copy Temporary To HttpServer Failed.");
    }
    
    logger.info("destPath = " + destPath);
    return destPath;
  }
  
  public String getUrlOnHttpServer(String path) {
    if (MsbAddrConfig.getMsbAddress().endsWith("/")) {
      return MsbAddrConfig.getMsbAddress() + "files/catalog-http" + path;
    } else {
      return MsbAddrConfig.getMsbAddress() + "/files/catalog-http" + path;
    }
  }
  
  protected String toTempFilePath(String fileLocation) {
    return "/temp/" + (new File(fileLocation)).getName();
  }
  
  protected EnumTemplateType getTemplateType(String substitutionType, List<NodeTemplate> ntList) {
    if (isNsType(substitutionType)) {
      return EnumTemplateType.NS;
    }

    if (isVnfType(substitutionType)) {
      return EnumTemplateType.VNF;
    }

    return getTemplateTypeFromNodeTemplates(ntList);
  }
  
  private boolean isVnfType(String type) {
    if (ToolUtil.isTrimedEmptyString(type)) {
      return false;
    }
    return type.toUpperCase().endsWith(".VNF") || type.toUpperCase().contains(".VNF.");
  }

  private boolean isNsType(String type) {
    if (ToolUtil.isTrimedEmptyString(type)) {
      return false;
    }
    return type.toUpperCase().endsWith(".NS") || type.toUpperCase().contains(".NS.");
  }
  
  private EnumTemplateType getTemplateTypeFromNodeTemplates(List<NodeTemplate> ntList) {
    for (NodeTemplate nt : ntList) {
      if (isNsType(nt.getType()) || isVnfType(nt.getType())) {
        return EnumTemplateType.NS;
      }
    }

    return EnumTemplateType.VNF;
  }
  
  private static final String TOSCA_META_FIELD_ENTRY_DEFINITIONS = "Entry-Definitions";
  
  protected String parseServiceTemplateFileName(String packageId, String fileLocation)
      throws CatalogResourceException {
    return "/" + parseToscaMeta(fileLocation).get(TOSCA_META_FIELD_ENTRY_DEFINITIONS);
  }
  
  private static final String TOSCA_META_FILE_NAME = "TOSCA-Metadata/TOSCA.meta";
  protected Map<String, String> parseToscaMeta(String zipLocation) throws CatalogResourceException {
    Map<String, String> toscaMeta = new HashMap<>();
    String[] lines = TemplateUtils.readFromZipFile(zipLocation, TOSCA_META_FILE_NAME);

    for (String line : lines) {
      String[] tmps;
      if (line.indexOf(":") > 0) {
        tmps = line.split(":");
        toscaMeta.put(tmps[0].trim(), tmps[1].trim());
      }
    }

    return toscaMeta;
  }
  
  /**
   * @param fileLocation
   * @return
   * @throws CatalogResourceException
   */
  protected ServiceTemplateOperation[] parseOperations(String fileLocation) throws CatalogResourceException {
    String sPlan = TemplateUtils.readStringFromZipFile(fileLocation, "Definitions/plans.yaml");
    Map<String, Plan> plans = TemplateUtils.loadPlan(sPlan);
    return parseAndDeployPlans(plans, fileLocation);
  }
  
  /**
   * @param plans
   * @param fileLocation
   * @return
   * @throws CatalogResourceException 
   */
  private ServiceTemplateOperation[] parseAndDeployPlans(Map<String, Plan> plans,
      String zipFileLocation) throws CatalogResourceException {
    if (plans == null || plans.isEmpty()) {
      return new ServiceTemplateOperation[0];
    }

    List<ServiceTemplateOperation> opList = new ArrayList<>();
    for (Entry<String, Plan> plan : plans.entrySet()) {
      ServiceTemplateOperation op = new ServiceTemplateOperation();
      op.setName(plan.getKey());
      op.setDescription(plan.getValue().getDescription());
      checkPlanLanguage(plan.getValue().getPlanLanguage());
      DeployPackageResponse response =
          Wso2ServiceConsumer.deployPackage(zipFileLocation, plan.getValue().getReference());
      op.setPackageName(parsePackageName(response));
      op.setProcessId(response.getProcessId());
      op.setInputs(parsePlanInputs(plan.getValue().getInputs()));

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

  /**
   * @param inputs
   * @return
   */
  private InputParameter[] parsePlanInputs(
      Map<String, Input> inputs) {
    if (inputs == null || inputs.isEmpty()) {
      return new InputParameter[0];
    }

    List<InputParameter> retList = new ArrayList<>();
    for (Entry<String, Input> input : inputs.entrySet()) {
      retList.add(new InputParameter(
          input.getKey(),
          input.getValue().getType(),
          input.getValue().getDescription(),
          input.getValue().getDefault(),
          input.getValue().isRequired()));
    }
    return retList.toArray(new InputParameter[0]);
  }
  
}
