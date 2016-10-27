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
package org.openo.commontosca.catalog.model.common;

import org.openo.commontosca.catalog.common.ToolUtil;
import org.openo.commontosca.catalog.db.entity.NodeTemplateData;
import org.openo.commontosca.catalog.db.entity.ServiceTemplateData;
import org.openo.commontosca.catalog.db.entity.ServiceTemplateMappingData;
import org.openo.commontosca.catalog.db.entity.TemplateData;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.resource.TemplateManager;
import org.openo.commontosca.catalog.entity.response.CsarFileUriResponse;
import org.openo.commontosca.catalog.model.entity.NodeTemplate;
import org.openo.commontosca.catalog.model.entity.Parameters;
import org.openo.commontosca.catalog.model.entity.RelationShip;
import org.openo.commontosca.catalog.model.entity.ServiceTemplate;
import org.openo.commontosca.catalog.model.entity.ServiceTemplateOperation;
import org.openo.commontosca.catalog.model.entity.SubstitutionMapping;
import org.openo.commontosca.catalog.wrapper.PackageWrapper;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonPrimitive;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

public class TemplateDataHelper {

  /**
   * convert to template data.
   * @param st ServiceTemplate
   * @param ntList NodeTemplate list
   * @return TemplateData
   */
  public static TemplateData convert2TemplateData(ServiceTemplate st, String rawData,
      List<NodeTemplate> ntList) {
    TemplateData td = new TemplateData();
    td.setServiceTemplate(convert2ServiceTemplateData(st, rawData));
    td.setNodeTemplates(convert2NodeTemplateDataList(ntList, st.getServiceTemplateId()));
    return td;
  }

  /**
   * convert to service template data.
   * @param st ServiceTemplate
   * @return ServiceTemplateData
   */
  private static ServiceTemplateData convert2ServiceTemplateData(ServiceTemplate st,
      String rawData) {
    ServiceTemplateData std = new ServiceTemplateData();
    std.setServiceTemplateId(st.getServiceTemplateId());
    std.setServiceTemplateOriginalId(st.getId());
    std.setTemplateName(st.getTemplateName());
    std.setVendor(st.getVendor());
    std.setVersion(st.getVersion());
    std.setCsarId(st.getCsarId());
    std.setType(st.getType());
    std.setDownloadUri(st.getDownloadUri());
    Parameters parameters = new Parameters(st.getInputs(), st.getOutputs());
    std.setInputs(ToolUtil.toJson(parameters));
    std.setOperations(ToolUtil.toJson(st.getOperations()));
    std.setRowData(rawData);
    return std;
  }

  /**
   * convert to nodeTemplate data list.
   * @param ntList NodeTemplate list
   * @param serviceTemplateId service template id
   * @return NodeTemplateData list
   */
  private static ArrayList<NodeTemplateData> convert2NodeTemplateDataList(List<NodeTemplate> ntList,
      String serviceTemplateId) {
    ArrayList<NodeTemplateData> ntdList = new ArrayList<>();
    for (NodeTemplate nt : ntList) {
      ntdList.add(convert2NodeTemplateData(nt, serviceTemplateId));

    }
    return ntdList;
  }


  /**
   * convert to nodeTemplate data.
   * @param nt NodeTemplate
   * @param serviceTemplateId service template id
   * @return NodeTemplateData
   */
  private static NodeTemplateData convert2NodeTemplateData(NodeTemplate nt,
      String serviceTemplateId) {
    NodeTemplateData ntd = new NodeTemplateData();

    ntd.setNodeTemplateId(nt.getId());
    ntd.setName(nt.getName());
    ntd.setType(nt.getType());
    ntd.setServiceTemplateId(serviceTemplateId);
    ntd.setProperties(ToolUtil.toJson(nt.getProperties()));
    ntd.setRelationShips(ToolUtil.toJson(nt.getRelationShips()));

    return ntd;
  }


  /**
   * convert to service templates.
   * @param stdList ServiceTemplateData list
   * @return ServiceTemplate list
   * @throws CatalogResourceException 
   */
  public static ServiceTemplate[] convert2ServiceTemplates(List<ServiceTemplateData> stdList) throws CatalogResourceException {
    List<ServiceTemplate> stList = new ArrayList<>();
    for (ServiceTemplateData std : stdList) {
      stList.add(convert2ServiceTemplate(std));
    }

    return stList.toArray(new ServiceTemplate[0]);
  }

  /**
   * covert to service template.
   * @param std ServiceTemplateData
   * @return ServiceTemplate
   * @throws CatalogResourceException 
   */
  public static ServiceTemplate convert2ServiceTemplate(ServiceTemplateData std) throws CatalogResourceException {
    Parameters parameters = ToolUtil.fromJson(std.getInputs(), Parameters.class);
    ServiceTemplateOperation[] operations =
        ToolUtil.fromJson(std.getOperations(), ServiceTemplateOperation[].class);
    String downloadUri = buildSTDownloadUri(std.getCsarId(), std.getDownloadUri());
    
    return new ServiceTemplate(std.getServiceTemplateId(), std.getServiceTemplateOriginalId(),
        std.getTemplateName(), std.getVendor(),
        std.getVersion(), std.getCsarId(), std.getType(), downloadUri,
        parameters.getInputs(), parameters.getOutputs(), operations,
        getSubstitutionMappingsByServiceTemplateId(std.getServiceTemplateId()));
  }
  
  private static SubstitutionMapping getSubstitutionMappingsByServiceTemplateId(String serviceTemplateId)
      throws CatalogResourceException {
    List<ServiceTemplateMappingData> stmDataList =
        TemplateManager.getInstance().queryServiceTemplateMapping(null, serviceTemplateId);
    if (stmDataList == null || stmDataList.isEmpty()) {
      return null;
    }

    return convert2SubstitutionMapping(stmDataList.get(0));
  }

  private static String buildSTDownloadUri(String packageId, String stFileName)
      throws CatalogResourceException {
    CsarFileUriResponse stDownloadUri =
        PackageWrapper.getInstance().getCsarFileDownloadUri(packageId, stFileName);
    return stDownloadUri.getDownloadUri();
  }

  /**
   * covert to nodeTemplates.
   * @param ntdList NodeTemplateData list
   * @return NodeTemplate list
   */
  public static NodeTemplate[] convert2NodeTemplates(List<NodeTemplateData> ntdList) {
    List<NodeTemplate> ntList = new ArrayList<>();
    for (NodeTemplateData ntd : ntdList) {
      ntList.add(convert2NodeTemplate(ntd));
    }
    return ntList.toArray(new NodeTemplate[0]);
  }

  /**
   * covert to nodeTemplate.
   * @param ntd NodeTemplateData
   * @return NodeTemplate
   */
  public static NodeTemplate convert2NodeTemplate(NodeTemplateData ntd) {
    List<RelationShip> relationShips = convert2RelationShipList(ntd.getRelationShips());
    return new NodeTemplate(ntd.getNodeTemplateId(), ntd.getName(), ntd.getType(),
        convert2Property(ntd.getProperties()), relationShips);
  }

  /**
   * covert to relationship list.
   * @param sRelationShips relationships
   * @return RelationShip list
   */
  private static List<RelationShip> convert2RelationShipList(String srelationShips) {
    RelationShip[] relationShips = ToolUtil.fromJson(srelationShips, RelationShip[].class);
    return Arrays.asList(relationShips);
  }

  /**
   * convert to propterty.
   * @param properties properties to covert 
   * @return map
   */
  private static Map<String, Object> convert2Property(String properties) {
    JsonObject jsonObject = new Gson().fromJson(properties, JsonObject.class);
    return parseMapValue(jsonObject);
  }

  private static Map<String, Object> parseMapValue(JsonObject jsonObject) {
    Map<String, Object> map = new HashMap<>();

    Iterator<Entry<String, JsonElement>> iterator = jsonObject.entrySet().iterator();
    while (iterator.hasNext()) {
      Entry<String, JsonElement> next = iterator.next();
      if (next.getValue() instanceof JsonPrimitive) {
        map.put(next.getKey(), next.getValue().getAsString());
        continue;
      }

      if (next.getValue() instanceof JsonObject) {
        map.put(next.getKey(), parseMapValue((JsonObject) next.getValue()));
        continue;
      }
    }
    return map;
  }


  /** 
   * covert to template mapping data.
   * @param stm data to convert
   * @return ServiceTemplateMappingData
   */
  public static ServiceTemplateMappingData convert2TemplateMappingData(SubstitutionMapping stm) {
    ServiceTemplateMappingData stmd = new ServiceTemplateMappingData();

    stmd.setMappingId(ToolUtil.generateId());
    stmd.setServiceTemplateId(stm.getServiceTemplateId());
    stmd.setNodeType(stm.getNodeType());
    stmd.setRequirements(ToolUtil.toJson(stm.getRequirements()));
    stmd.setCapabilities(ToolUtil.toJson(stm.getCapabilities()));

    return stmd;
  }

  /**
   * convert to substitution mapping.
   * @param stmData data to covert
   * @return SubstitutionMapping
   */
  public static SubstitutionMapping convert2SubstitutionMapping(
      ServiceTemplateMappingData stmData) {
    return new SubstitutionMapping(stmData.getServiceTemplateId(), stmData.getNodeType());
  }

}
