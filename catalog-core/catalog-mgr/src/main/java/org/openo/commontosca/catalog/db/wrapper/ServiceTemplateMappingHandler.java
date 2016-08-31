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
import org.openo.commontosca.catalog.db.entity.ServiceTemplateMappingData;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.util.CatalogDbUtil;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.Map;


public class ServiceTemplateMappingHandler extends BaseHandler<ServiceTemplateMappingData> {
  private static final Logger logger = LoggerFactory.getLogger(ServiceTemplateMappingHandler.class);

  /**
   * create service template data.
   * @param serviceTemplateMappingData service template maping data
   * @return ServiceTemplateMappingData
   * @throws CatalogResourceException e
   */
  public ServiceTemplateMappingData create(ServiceTemplateMappingData serviceTemplateMappingData)
      throws CatalogResourceException {
    logger.info("ServiceTemplateMappingHandler:start create serviceTemplateMapping info.");
    ServiceTemplateMappingData data = null;
    if (!CatalogDbUtil.isNotEmpty(serviceTemplateMappingData.getMappingId())) {
      logger.info(
          "ServiceTemplateMappingHandler:mapping info " + "does not have mappingId,generate UUID.");
      String id = CatalogDbUtil.generateId();
      serviceTemplateMappingData.setMappingId(id);
    }
    Object result =
        create(serviceTemplateMappingData, CatalogResuorceType.SERVICETEMPLATEMAPPING.name());
    if (result != null) {
      data = (ServiceTemplateMappingData) result;
    } else {
      logger.info("ServiceTemplateMappingHandler: query mapping info is null.");
    }
    logger.info("ServiceTemplateMappingHandler: create mapping info end.");
    return data;
  }

  /**
   * delete data by id.
   * @param id service template id
   * @throws CatalogResourceException e
   */
  public void delete(String id) throws CatalogResourceException {
    logger.info("ServiceTemplateMappingHandler:start delete mapping info.");
    ServiceTemplateMappingData serviceTemplateMappingData = new ServiceTemplateMappingData();
    serviceTemplateMappingData.setMappingId(id);
    delete(serviceTemplateMappingData, CatalogResuorceType.SERVICETEMPLATEMAPPING.name());
    logger.info("ServiceTemplateMappingHandler: delete mapping info end.");
  }

  /**
   * delete data.
   * @param delParam delete data according to delParam
   * @throws CatalogResourceException e
   */
  public void delete(Map<String, String> delParam) throws CatalogResourceException {
    logger.info("ServiceTemplateMappingHandler:start delete mapping info.");
    delete(delParam, CatalogResuorceType.SERVICETEMPLATEMAPPING.name());
    logger.info("ServiceTemplateMappingHandler:delete mapping info end.");
  }

  /**
   * query service template mapping data.
   * @param queryParam query map
   * @return ServiceTemplateMappingData list
   * @throws CatalogResourceException e
   */
  public ArrayList<ServiceTemplateMappingData> query(Map<String, String> queryParam)
      throws CatalogResourceException {
    logger.info("ServiceTemplateMappingHandler:start query mapping info.");
    ArrayList<ServiceTemplateMappingData> data = new ArrayList<ServiceTemplateMappingData>();
    Object result = query(queryParam, CatalogResuorceType.SERVICETEMPLATEMAPPING.name());
    if (result != null) {
      data = (ArrayList<ServiceTemplateMappingData>) result;
    } else {
      logger.info("ServiceTemplateMappingHandler: query mapping info is null.");
    }
    logger.info("ServiceTemplateMappingHandler: query mapping info end.");
    return data;

  }

  @Override
  public void check(ServiceTemplateMappingData data) throws CatalogResourceException {
    // TODO Auto-generated method stub

  }



}
