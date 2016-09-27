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
package org.openo.commontosca.catalog.db.wrapper;

import org.openo.commontosca.catalog.db.common.CatalogResuorceType;
import org.openo.commontosca.catalog.db.entity.NodeTemplateData;
import org.openo.commontosca.catalog.db.entity.ServiceTemplateData;
import org.openo.commontosca.catalog.db.entity.TemplateData;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.util.CatalogDbUtil;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;

public class TemplateHandler extends BaseHandler<TemplateData> {
  private static final Logger logger = LoggerFactory.getLogger(TemplateHandler.class);

  /**
   * create template data.
   * @param templateData template data to create
   * @return TemplateData
   * @throws CatalogResourceException e
   */
  public TemplateData create(TemplateData templateData) throws CatalogResourceException {
    logger.info("TemplateHandler create template info.");
    TemplateData data = null;
    String serviceTemplateOid = templateData.getServiceTemplate().getServiceTemplateId();
    if (!CatalogDbUtil.isNotEmpty(serviceTemplateOid)) {
      logger.info("TemplateHandler:template info does not have oid,generate UUID.");
      serviceTemplateOid = CatalogDbUtil.generateId();
      templateData.getServiceTemplate().setServiceTemplateId(serviceTemplateOid);
    }
    for (NodeTemplateData nodeData : templateData.getNodeTemplates()) {
      nodeData.setNodeTemplateId(CatalogDbUtil.generateId());
      nodeData.setServiceTemplateId(serviceTemplateOid);
    }
    Object result = create(templateData, CatalogResuorceType.TEMPLATE.name());
    if (result != null) {
      data = (TemplateData) result;
    } else {
      logger.info("TemplateHandler: query template info is null.");
    }
    logger.info("TemplateHandler: create template info end.");
    return data;
  }

  @Override
  public void check(TemplateData data) throws CatalogResourceException {
    // TODO Auto-generated method stub

  }

  /**
   * delete node template.
   * @param serviceTemplateId service template id
   * @param nodeTemplateList node template list
   * @throws CatalogResourceException e
   */
  public void delete(String serviceTemplateId, ArrayList<NodeTemplateData> nodeTemplateList)
      throws CatalogResourceException {
    logger.info("TemplateHandler delete Template info.");
    TemplateData templateData = new TemplateData();
    ServiceTemplateData serviceTemplateData = new ServiceTemplateData();
    serviceTemplateData.setServiceTemplateId(serviceTemplateId);
    templateData.setServiceTemplate(serviceTemplateData);
    templateData.setNodeTemplates(nodeTemplateList);
    delete(templateData, CatalogResuorceType.TEMPLATE.name());
    logger.info("TemplateHandler: delete Template info end.");
  }

}
