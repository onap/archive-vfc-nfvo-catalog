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

package org.openo.commontosca.catalog.model.service;

import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.resource.TemplateManager;
import org.openo.commontosca.catalog.model.entity.ServiceTemplate;
import org.openo.commontosca.catalog.model.entity.ServiceTemplateOperation;
import org.openo.commontosca.catalog.model.plan.wso2.Wso2ServiceConsumer;
import org.openo.commontosca.catalog.model.wrapper.ServiceTemplateWrapper;
import org.openo.commontosca.catalog.resources.CatalogBadRequestException;

public class ModelService {
  
  private static final ModelService instance = new ModelService();

  public static ModelService getInstance() {
    return instance;
  }

  /**
   * delete service template according package id.
   * @param packageId package id
   * @throws CatalogBadRequestException e1
   * @throws CatalogResourceException e2
   */
  public void delete(String packageId) throws CatalogBadRequestException, CatalogResourceException {
    ServiceTemplate st = ServiceTemplateWrapper.getInstance().getServiceTemplateByCsarId(packageId);

    TemplateManager.getInstance().deleteServiceTemplateById(st.getServiceTemplateId());
    TemplateManager.getInstance().deleteServiceTemplateMapping(null, st.getServiceTemplateId());

    ServiceTemplateOperation[] operations = st.getOperations();
    if (operations != null && operations.length > 0) {
      for (ServiceTemplateOperation op : operations) {
        Wso2ServiceConsumer.deletePackage(op.getPackageName());
      }
    }
  }

}
