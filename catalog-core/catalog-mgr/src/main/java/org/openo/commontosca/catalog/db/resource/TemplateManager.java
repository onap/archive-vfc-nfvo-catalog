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
package org.openo.commontosca.catalog.db.resource;

import org.openo.commontosca.catalog.db.common.Parameters;
import org.openo.commontosca.catalog.db.entity.NodeTemplateData;
import org.openo.commontosca.catalog.db.entity.PackageData;
import org.openo.commontosca.catalog.db.entity.ServiceTemplateData;
import org.openo.commontosca.catalog.db.entity.ServiceTemplateMappingData;
import org.openo.commontosca.catalog.db.entity.TemplateData;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.util.CatalogDbUtil;
import org.openo.commontosca.catalog.db.util.HqlFactory;
import org.openo.commontosca.catalog.db.wrapper.NodeTemplateHandler;
import org.openo.commontosca.catalog.db.wrapper.ServiceTemplateHandler;
import org.openo.commontosca.catalog.db.wrapper.ServiceTemplateMappingHandler;
import org.openo.commontosca.catalog.db.wrapper.TemplateHandler;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class TemplateManager {
  private static final Logger LOGGER = LoggerFactory.getLogger(TemplateManager.class);
  private static TemplateManager manager;
  ServiceTemplateHandler handler = new ServiceTemplateHandler();
  NodeTemplateHandler nodeTemplateHandler = new NodeTemplateHandler();
  TemplateHandler templateHandler = new TemplateHandler();
  ServiceTemplateMappingHandler mappingHandler = new ServiceTemplateMappingHandler();

  /**
   * get TemplateManager instance.
   * @return TemplateManager instance
   */
  public static synchronized TemplateManager getInstance() {
    if (manager == null) {
      manager = new TemplateManager();
    }
    return manager;
  }

  private TemplateManager() {}

  /**
   * add service template.
   * 
   * @param templateData TemplateData
   * @return TemplateData
   * @throws CatalogResourceException e
   */
  public TemplateData addServiceTemplate(TemplateData templateData)
      throws CatalogResourceException {
    LOGGER
        .info("start add template info  to db.info:" + CatalogDbUtil.objectToString(templateData));
    TemplateData data = templateHandler.create(templateData);
    LOGGER.info(" template info  to db end.info:" + CatalogDbUtil.objectToString(data));
    return data;
  }

  /**
   * add service template mapping.
   * @param templateMappingData mapping data
   * @return ServiceTemplateMappingData
   * @throws CatalogResourceException e
   */
  public ServiceTemplateMappingData addServiceTemplateMapping(
      ServiceTemplateMappingData templateMappingData) throws CatalogResourceException {
    LOGGER.info("start add servicetemplate Mapping  info  to db.info:"
        + CatalogDbUtil.objectToString(templateMappingData));
    ServiceTemplateMappingData data = mappingHandler.create(templateMappingData);
    LOGGER.info(" template mapping info  to db end.info:" + CatalogDbUtil.objectToString(data));
    return data;
  }

  /**
   * query service template mapping by id.
   * @param id id
   * @return ServiceTemplateMappingData list
   * @throws CatalogResourceException e
   */
  public ArrayList<ServiceTemplateMappingData> queryServiceTemplateMappingById(String id)
      throws CatalogResourceException {
    Map<String, String> queryParam = new HashMap<String, String>();
    queryParam.put(Parameters.mappingId.name(), id);
    LOGGER.info("start query serviceTemplateMapping info by id." + id);
    ArrayList<ServiceTemplateMappingData> data = mappingHandler.query(queryParam);
    LOGGER.info("query serviceTemplateMapping info end.size:" + data.size() + "detail:"
        + CatalogDbUtil.objectToString(data));
    return data;
  }

  /**
   * delete service template mapping by id.
   * @param id id
   * @throws CatalogResourceException e
   */
  public void deleteServiceTemplateMappingById(String id) throws CatalogResourceException {

    LOGGER.info("start delete serviceTemplateMapping info by id." + id);
    mappingHandler.delete(id);
    LOGGER.info("delete serviceTemplateMapping info end");
  }

  /**
   * delete service template mapping.
   * @param nodeType node type
   * @param serviceTemplateId service template id
   * @throws CatalogResourceException e
   */
  public void deleteServiceTemplateMapping(String nodeType, String serviceTemplateId)
      throws CatalogResourceException {
    Map<String, String> delParam = new HashMap<String, String>();
    if (CatalogDbUtil.isNotEmpty(nodeType)) {
      delParam.put(Parameters.nodeType.name(), nodeType);
    }
    if (CatalogDbUtil.isNotEmpty(serviceTemplateId)) {
      delParam.put(Parameters.serviceTemplateId.name(), serviceTemplateId);
    }
    LOGGER.info("start delete serviceTemplateMapping info.nodeType:" + nodeType
        + " serviceTemplateId:" + serviceTemplateId);
    mappingHandler.delete(delParam);
    LOGGER.info("delete serviceTemplateMapping info ");
  }

  /**
   * query service template mapping.
   * @param nodeType nodeType
   * @param serviceTemplateId serviceTemplateId
   * @return ServiceTemplateMappingData list
   * @throws CatalogResourceException e
   */
  public ArrayList<ServiceTemplateMappingData> queryServiceTemplateMapping(String nodeType,
      String serviceTemplateId) throws CatalogResourceException {
    Map<String, String> queryParam = new HashMap<String, String>();
    if (CatalogDbUtil.isNotEmpty(nodeType)) {
      queryParam.put(Parameters.nodeType.name(), nodeType);
    }
    if (CatalogDbUtil.isNotEmpty(serviceTemplateId)) {
      queryParam.put(Parameters.serviceTemplateId.name(), serviceTemplateId);
    }
    LOGGER.info("start query serviceTemplateMapping info.nodeType:" + nodeType
        + " serviceTemplateId:" + serviceTemplateId);
    ArrayList<ServiceTemplateMappingData> data = mappingHandler.query(queryParam);
    LOGGER.info("query serviceTemplateMapping info end.size:" + data.size() + "detail:"
        + CatalogDbUtil.objectToString(data));
    return data;
  }

  /**
   * query service template by id.
   * @param id service template id
   * @return ServiceTemplateData list
   * @throws CatalogResourceException e
   */
  public ArrayList<ServiceTemplateData> queryServiceTemplateById(String id)
      throws CatalogResourceException {
    Map<String, String> queryParam = new HashMap<String, String>();
    queryParam.put(Parameters.serviceTemplateId.name(), id);
    LOGGER.info("start query serviceTemplate info by id." + id);
    ArrayList<ServiceTemplateData> data = handler.query(queryParam);
    LOGGER.info("query serviceTemplate info end.size:" + data.size() + "detail:"
        + CatalogDbUtil.objectToString(data));
    return data;
  }

  /**
   * query service template according to condition.
   * @param type template type
   * @param version template version
   * @param vendor template vendor
   * @return ServiceTemplateData list
   * @throws CatalogResourceException e
   */
  public ArrayList<ServiceTemplateData> queryServiceTemplate(String type, String version,
      String vendor) throws CatalogResourceException {
    LOGGER.info("start query serviceTemplate info.type:" + type + " vendor:" + vendor + " version:"
        + version);
    Map<String, String> queryParam = new HashMap<String, String>();
    if (CatalogDbUtil.isNotEmpty(type)) {
      queryParam.put(Parameters.type.name(), type);
    }
    if (CatalogDbUtil.isNotEmpty(vendor)) {
      queryParam.put(Parameters.vendor.name(), vendor);
    }
    if (CatalogDbUtil.isNotEmpty(version)) {
      queryParam.put(Parameters.version.name(), version);
    }
    ArrayList<ServiceTemplateData> data = handler.query(queryParam);
    LOGGER.info("query serviceTemplate info end.size:" + data.size() + "detail:"
        + CatalogDbUtil.objectToString(data));
    return data;
  }

  /**
   * query node template service template id.
   * @param serviceTemplateId service template id
   * @return NodeTemplateData list
   * @throws CatalogResourceException e
   */
  public ArrayList<NodeTemplateData> queryNodeTemplateBySeriviceTemplateId(String serviceTemplateId)
      throws CatalogResourceException {
    LOGGER.info("start query NodeTemplate info.serviceTemplateId:" + serviceTemplateId);
    Map<String, String> queryParam = new HashMap<String, String>();
    queryParam.put(Parameters.serviceTemplateId.name(), serviceTemplateId);
    ArrayList<NodeTemplateData> data = nodeTemplateHandler.query(queryParam);
    LOGGER.info("query NodeTemplate info end.size:" + data.size() + "detail:"
        + CatalogDbUtil.objectToString(data));
    return data;
  }

  /**
   * query node template by id.
   * @param serviceTemplateId service template id
   * @param nodeTemplateId nodetemplate id
   * @return NodeTemplateData list
   * @throws CatalogResourceException e
   */
  public ArrayList<NodeTemplateData> queryNodeTemplateById(String serviceTemplateId,
      String nodeTemplateId) throws CatalogResourceException {
    LOGGER.info("start query NodeTemplate info.serviceTemplateId:" + serviceTemplateId
        + "nodeTemplateId:" + nodeTemplateId);
    Map<String, String> queryParam = new HashMap<String, String>();
    if (CatalogDbUtil.isNotEmpty(serviceTemplateId)) {
      queryParam.put(Parameters.serviceTemplateId.name(), serviceTemplateId);
    }
    if (CatalogDbUtil.isNotEmpty(nodeTemplateId)) {
      queryParam.put(Parameters.nodeTemplateId.name(), nodeTemplateId);
    }
    ArrayList<NodeTemplateData> data = nodeTemplateHandler.query(queryParam);
    LOGGER.info("query NodeTemplate info end.size:" + data.size() + "detail:"
        + CatalogDbUtil.objectToString(data));
    return data;
  }

  /**
   * query service template by package infomation.
   * @param packageInfo package information
   * @return ServiceTemplateData list
   * @throws CatalogResourceException e
   */
  public ArrayList<ServiceTemplateData> queryServiceTemplateByCsarPackageInfo(
      PackageData packageInfo) throws CatalogResourceException {
    LOGGER.info("start query serviceTemplate info by package.package:"
        + CatalogDbUtil.objectToString(packageInfo));
    String filter =
        HqlFactory.getQueryHqlByFilter(ServiceTemplateData.class, packageInfo,
            Parameters.csarId.name());
    ArrayList<ServiceTemplateData> data = handler.unionQuery(filter);
    LOGGER.info("query serviceTemplate info end.size:" + data.size() + "detail:"
        + CatalogDbUtil.objectToString(data));
    return data;
  }

  /**
   * delete service template by id.
   * @param serviceTemplateId service template id
   * @throws CatalogResourceException e
   */
  public void deleteServiceTemplateById(String serviceTemplateId) throws CatalogResourceException {
    LOGGER.info("start delete serviceTemplate info.id:" + serviceTemplateId);
    ArrayList<NodeTemplateData> nodeTemplateList =
        queryNodeTemplateBySeriviceTemplateId(serviceTemplateId);
    templateHandler.delete(serviceTemplateId, nodeTemplateList);
    LOGGER.info(" delete serviceTemplate info end id." + serviceTemplateId);
  }

  /**
   * delete service template by package info.
   * @param packageInfo package information
   * @throws CatalogResourceException e
   */
  public void deleteServiceTemplateByCsarPackageInfo(PackageData packageInfo)
      throws CatalogResourceException {
    LOGGER.info("start delete serviceTemplate info by package.package:"
        + CatalogDbUtil.objectToString(packageInfo));

    ArrayList<ServiceTemplateData> serviceTemplate =
        queryServiceTemplateByCsarPackageInfo(packageInfo);
    for (int i = 0; i < serviceTemplate.size(); i++) {
      deleteServiceTemplateById(serviceTemplate.get(i).getServiceTemplateId());
    }
    LOGGER.info("delete serviceTemplate info end.");

  }
}
