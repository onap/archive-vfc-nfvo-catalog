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
package org.openo.commontosca.catalog.model.service;

import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.resource.TemplateManager;
import org.openo.commontosca.catalog.model.entity.ServiceTemplate;
import org.openo.commontosca.catalog.model.entity.ServiceTemplateOperation;
import org.openo.commontosca.catalog.model.plan.wso2.Wso2ServiceConsumer;
import org.openo.commontosca.catalog.model.wrapper.ServiceTemplateWrapper;
import org.openo.commontosca.catalog.resources.CatalogBadRequestException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ModelService {
  private static final Logger logger = LoggerFactory.getLogger(ModelService.class);

  private static ModelService instance;

  public static ModelService getInstance() {
    if (instance == null) {
      instance = new ModelService();
    }
    return instance;
  }


  /**
   * delete service template according package id.
   * 
   * @param packageId package id
   * @throws CatalogBadRequestException e1
   * @throws CatalogResourceException e2
   */
  public void delete(String packageId) throws CatalogResourceException {
    logger.info("delete package model data begin.");

    ServiceTemplate st = getServiceTemplateByCsarIdIgnoreError(packageId);
    if (st == null) {
      return;
    }

    undeployOperationPackage(st.getOperations());

    TemplateManager.getInstance().deleteServiceTemplateById(st.getServiceTemplateId());
    TemplateManager.getInstance().deleteServiceTemplateMapping(null, st.getServiceTemplateId());

    logger.info("delete package model data end.");
  }

  private void undeployOperationPackage(ServiceTemplateOperation[] operations)
      throws CatalogResourceException {
    if (operations != null && operations.length > 0) {
      for (ServiceTemplateOperation op : operations) {
        Wso2ServiceConsumer.deletePackage(op.getPackageName());
      }
    }
  }

  private ServiceTemplate getServiceTemplateByCsarIdIgnoreError(String packageId) {
    try {
      return ServiceTemplateWrapper.getInstance().getServiceTemplateByCsarId(packageId);
    } catch (CatalogBadRequestException ignore) {
      logger.info("delete package model data ignore.", ignore);
    } catch (CatalogResourceException ignore) {
      logger.info("delete package model data ignore.", ignore);
    }

    return null;
  }

  /**
   * delete service template data only, not undeploy operation package.
   * 
   * @param packageId package id
   * @throws CatalogBadRequestException e1
   * @throws CatalogResourceException e2
   */
  public void deleteServiceTemplateData(String packageId) throws CatalogResourceException {
    logger.info("delete service template data begin.");

    ServiceTemplate st = getServiceTemplateByCsarIdIgnoreError(packageId);
    if (st == null) {
      return;
    }

    TemplateManager.getInstance().deleteServiceTemplateById(st.getServiceTemplateId());
    TemplateManager.getInstance().deleteServiceTemplateMapping(null, st.getServiceTemplateId());

    logger.info("delete service template data end.");
  }

  /**
   * undeploy operation package of the service template.
   * 
   * @param packageId package id
   * @throws CatalogBadRequestException e1
   * @throws CatalogResourceException e2
   */
  public void undeployOperationPackage(String packageId) throws CatalogResourceException {
    logger.info("undeploy operation package begin.");

    ServiceTemplate st = getServiceTemplateByCsarIdIgnoreError(packageId);
    if (st == null) {
      return;
    }

    undeployOperationPackage(st.getOperations());

    logger.info("undeploy operation package end.");
  }

}
