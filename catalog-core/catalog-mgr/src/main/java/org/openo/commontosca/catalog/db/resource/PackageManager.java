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
import org.openo.commontosca.catalog.db.entity.PackageData;
import org.openo.commontosca.catalog.db.entity.ServiceTemplateData;

import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.util.CatalogDbUtil;
import org.openo.commontosca.catalog.db.util.HqlFactory;
import org.openo.commontosca.catalog.db.wrapper.PackageHandler;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class PackageManager {
  private static final Logger LOGGER = LoggerFactory.getLogger(PackageManager.class);
  private static PackageManager manager;
  PackageHandler handler = new PackageHandler();

  /**
   * get PackageManager instance.
   * @return PackageManager instance
   */
  public static synchronized PackageManager getInstance() {
    if (manager == null) {
      manager = new PackageManager();
    }
    return manager;
  }

  private PackageManager() {}

  /**
   * add package.
   * @param packageData package data
   * @return PackageData
   * @throws CatalogResourceException e
   */
  public PackageData addPackage(PackageData packageData) throws CatalogResourceException {
    LOGGER.info("start add package info  to db.info:" + CatalogDbUtil.objectToString(packageData));
    PackageData data = handler.create(packageData);
    LOGGER.info(" package info  to db end.info:" + CatalogDbUtil.objectToString(data));
    return data;
  }

  /**
   * query package by package id.
   * @param csarId package id
   * @return package data list
   * @throws CatalogResourceException e
   */
  public ArrayList<PackageData> queryPackageByCsarId(String csarId)
      throws CatalogResourceException {
    Map<String, String> queryParam = new HashMap<String, String>();
    queryParam.put(Parameters.csarId.name(), csarId);
    LOGGER.info("start query package info by csarid." + csarId);
    ArrayList<PackageData> data = handler.query(queryParam);
    LOGGER.info("query package info end.size:" + data.size() + "detail:"
        + CatalogDbUtil.objectToString(data));
    return data;
  }

  /**
   * query package by condition.
   * @param name package name
   * @param provider package provider
   * @param version package version
   * @param deletionPending deletionPending
   * @param type package type
   * @return package data list
   * @throws CatalogResourceException e
   */
  public ArrayList<PackageData> queryPackage(String name, String provider, String version,
      String deletionPending, String type) throws CatalogResourceException {
    LOGGER.info("start query package info.name:" + name + " provider:" + provider + " version:"
        + version + " type:" + type);
    Map<String, String> queryParam = new HashMap<String, String>();
    if (CatalogDbUtil.isNotEmpty(name)) {
      queryParam.put(Parameters.name.name(), name);
    }
    if (CatalogDbUtil.isNotEmpty(version)) {
      queryParam.put(Parameters.version.name(), version);
    }
    if (CatalogDbUtil.isNotEmpty(deletionPending)) {
      queryParam.put(Parameters.deletionPending.name(), deletionPending);
    }
    if (CatalogDbUtil.isNotEmpty(type)) {
      queryParam.put(Parameters.type.name(), type);
    }
    if (CatalogDbUtil.isNotEmpty(provider)) {
      queryParam.put(Parameters.provider.name(), provider);
    }
    ArrayList<PackageData> data = handler.query(queryParam);
    LOGGER.info("query package info end.size:" + data.size() + "detail:"
        + CatalogDbUtil.objectToString(data));
    return data;
  }

  /**
   * delete package according package id.
   * @param packageId package id
   * @throws CatalogResourceException e
   */
  public void deletePackage(String packageId) throws CatalogResourceException {
    LOGGER.info("start delete package info by id." + packageId);
    handler.delete(packageId);
    LOGGER.info(" delete package info end id." + packageId);
  }

  /**
   * delete package by service template id.
   * @param serviceTemplateId service template id
   * @throws CatalogResourceException e
   */
  public void deletePackageByServiceTemplateId(String serviceTemplateId)
      throws CatalogResourceException {
    LOGGER.info("start delete package info by serviceTemplateid." + serviceTemplateId);
    ServiceTemplateData serviceTemplate = new ServiceTemplateData();
    serviceTemplate.setServiceTemplateId(serviceTemplateId);
    String filter =
        HqlFactory.getDeleteHqlByFilter(PackageData.class, serviceTemplate,
            Parameters.csarId.name());
    int data = handler.unionDelete(filter);

    LOGGER.info("delete serviceTemplate info end.num:" + data);
  }

  /**
   * query package by service template id.
   * @param serviceTemplateId service template id
   * @return package data list
   * @throws CatalogResourceException e
   */
  public ArrayList<PackageData> queryPackageByServiceTemplateId(String serviceTemplateId)
      throws CatalogResourceException {
    LOGGER.info("start query package info by serviceTemplateid." + serviceTemplateId);
    ServiceTemplateData serviceTemplate = new ServiceTemplateData();
    serviceTemplate.setServiceTemplateId(serviceTemplateId);
    String filter =
        HqlFactory
            .getQueryHqlByFilter(PackageData.class, serviceTemplate, Parameters.csarId.name());
    ArrayList<PackageData> data = handler.unionQuery(filter);
    LOGGER.info("query package info end.size:" + data.size() + "detail:"
        + CatalogDbUtil.objectToString(data));
    return data;
  }

  /**
   * update package data.
   * 
   * @param packageData package data
   * @param csarId package id
   * @throws CatalogResourceException e
   */
  public void updatePackage(PackageData packageData, String csarId)
      throws CatalogResourceException {
    LOGGER.info("start update package info by id." + csarId + " info:"
        + CatalogDbUtil.objectToString(packageData));
    handler.update(packageData, csarId);
    LOGGER.info(" update package  end id." + csarId);
  }

}
