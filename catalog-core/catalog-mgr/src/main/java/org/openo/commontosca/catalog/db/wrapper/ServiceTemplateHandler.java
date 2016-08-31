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
import org.openo.commontosca.catalog.db.entity.ServiceTemplateData;
import org.openo.commontosca.catalog.db.entity.TemplateData;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.Map;

public class ServiceTemplateHandler extends BaseHandler<TemplateData> {
  private static final Logger logger = LoggerFactory.getLogger(ServiceTemplateHandler.class);

  @Override
  public void check(TemplateData data) throws CatalogResourceException {
    // TODO Auto-generated method stub

  }

  /**
   * query service template data by map.
   * @param queryParam map data
   * @return ServiceTemplateData list
   * @throws CatalogResourceException e
   */
  public ArrayList<ServiceTemplateData> query(Map<String, String> queryParam)
      throws CatalogResourceException {
    logger.info("ServiceTemplateHandler query serviceTemplate info.");
    ArrayList<ServiceTemplateData> data = new ArrayList<ServiceTemplateData>();
    Object result = query(queryParam, CatalogResuorceType.SERVICETEMPLATE.name());
    if (result != null) {
      data = (ArrayList<ServiceTemplateData>) result;
    } else {
      logger.info("ServiceTemplateHandler: query serviceTemplate info is null.");
    }
    logger.info("ServiceTemplateHandler: query serviceTemplate info end.");
    return data;
  }

  /**
   * query service template by union query.
   * @param filter query filter
   * @return ServiceTemplateData list
   * @throws CatalogResourceException e
   */
  public ArrayList<ServiceTemplateData> unionQuery(String filter) throws CatalogResourceException {
    logger.info("ServiceTemplateHandler query serviceTemplate info by union.filter:" + filter);
    ArrayList<ServiceTemplateData> data = new ArrayList<ServiceTemplateData>();
    Object result = unionQuery(filter, CatalogResuorceType.SERVICETEMPLATE.name());
    if (result != null) {
      data = (ArrayList<ServiceTemplateData>) result;
    } else {
      logger.info("ServiceTemplateHandler: query serviceTemplate info is null.");
    }
    logger.info("ServiceTemplateHandler: query serviceTemplate info end.");
    return data;
  }

  /**
   * union delete.
   * @param filter delete filter
   * @return int 
   * @throws CatalogResourceException e
   */
  public int unionDelete(String filter) throws CatalogResourceException {
    logger.info("ServiceTemplateHandler delete serviceTemplate info by union.filter:" + filter);
    int num = 0;
    Object result = unionDelete(filter, CatalogResuorceType.SERVICETEMPLATE.name());
    if (result != null) {
      num = (int) result;
    } else {
      logger.info("ServiceTemplateHandler: delete serviceTemplate info is null.");
    }
    logger.info("ServiceTemplateHandler: delete serviceTemplate info end.num:" + num);
    return num;
  }

}
