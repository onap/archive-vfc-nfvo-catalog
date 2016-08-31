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

package org.openo.commontosca.catalog.db.wrapper;

import org.openo.commontosca.catalog.db.common.CatalogResuorceType;
import org.openo.commontosca.catalog.db.common.Parameters;
import org.openo.commontosca.catalog.db.entity.PackageData;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.util.CatalogDbUtil;
import org.openo.commontosca.catalog.db.util.HqlFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.Map;

public class PackageHandler extends BaseHandler<PackageData> {
  private static final Logger logger = LoggerFactory.getLogger(PackageHandler.class);

  /**
   * create package data.
   * @param packageData package data to create
   * @return PackageData
   * @throws CatalogResourceException e1
   */
  public PackageData create(PackageData packageData) throws CatalogResourceException {
    logger.info("packageHandler:start create package info.");
    PackageData data = null;
    if (!CatalogDbUtil.isNotEmpty(packageData.getCsarId())) {

      logger.info("packageHandler:package info does not have csarid,generate UUID.");
      String id = CatalogDbUtil.generateId();
      packageData.setCsarId(id);
    }
    Object result = create(packageData, CatalogResuorceType.PACKAGE.name());
    if (result != null) {
      data = (PackageData) result;
    } else {
      logger.info("packageHandler: query package info is null.");
    }
    logger.info("packageHandler: create package info end.");
    return data;
  }

  /**
   * delete data.
   * @param id package id
   * @throws CatalogResourceException e
   */
  public void delete(String id) throws CatalogResourceException {
    logger.info("packageHandler:start delete package info.");
    PackageData packageData = new PackageData();
    packageData.setCsarId(id);
    delete(packageData, CatalogResuorceType.PACKAGE.name());
    logger.info("packageHandler: delete package info end.");
  }

  /**
   * delete data.
   * @param queryParam query parameter
   * @throws CatalogResourceException e
   */
  public void delete(Map<String, String> queryParam) throws CatalogResourceException {
    logger.info("packageHandler:start delete package info.");
    delete(queryParam, CatalogResuorceType.PACKAGE.name());
    logger.info("packageHandler:delete package info end.");
  }

  /**
   * update data. 
   * @param packageData packate data to update
   * @param id package id
   * @throws CatalogResourceException e
   */
  public void update(PackageData packageData, String id) throws CatalogResourceException {
    // HostData host = gson.fromJson(hostJson, HostData.class);
    logger.info("packageHandler:start update  package info.");
    update(packageData, HqlFactory.getOidFilter(Parameters.csarId.name(), id),
        CatalogResuorceType.PACKAGE.name());
    logger.info("packageHandler:update  package info end.");
  }

  /**
   * union delete.
   * @param filter delete filter
   * @return int
   * @throws CatalogResourceException e
   */
  public int unionDelete(String filter) throws CatalogResourceException {
    logger.info("packageHandler delete package info by union.filter:" + filter);
    int num = 0;
    Object result = unionDelete(filter, CatalogResuorceType.PACKAGE.name());
    if (result != null) {
      num = (int) result;
    } else {
      logger.warn("packageHandler: delete package info is null.");
    }
    logger.info("packageHandler: delete package info end.num:" + num);
    return num;
  }

  /**
   * union query.
   * @param filter query filter
   * @return PackageData list
   * @throws CatalogResourceException e
   */
  public ArrayList<PackageData> unionQuery(String filter) throws CatalogResourceException {
    logger.info("packageHandler query package info by union.filter:" + filter);
    ArrayList<PackageData> data = new ArrayList<PackageData>();
    Object result = unionQuery(filter, CatalogResuorceType.PACKAGE.name());
    if (result != null) {
      data = data = (ArrayList<PackageData>) result;
    } else {
      logger.info("packageHandler: query package info is null.");
    }
    logger.info("packageHandler: query package info end");
    return data;
  }

  /**
   * query package data by map.
   * @param queryParam map data
   * @return PackageData list
   * @throws CatalogResourceException e
   */
  public ArrayList<PackageData> query(Map<String, String> queryParam)
      throws CatalogResourceException {
    logger.info("packageHandler:start query package info.");
    ArrayList<PackageData> data = new ArrayList<PackageData>();
    Object result = query(queryParam, CatalogResuorceType.PACKAGE.name());
    if (result != null) {
      data = (ArrayList<PackageData>) result;
    } else {
      logger.info("packageHandler: query package info is null.");
    }
    logger.info("packageHandler: query package info end.");
    return data;
  }

  @Override
  public void check(PackageData packageData) throws CatalogResourceException {

  }

}
