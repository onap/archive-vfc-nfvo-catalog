/**
 *     Copyright (C) 2016 ZTE, Inc. and others. All rights reserved. (ZTE)
 *
 *     Licensed under the Apache License, Version 2.0 (the "License");
 *     you may not use this file except in compliance with the License.
 *     You may obtain a copy of the License at
 *
 *             http://www.apache.org/licenses/LICENSE-2.0
 *
 *     Unless required by applicable law or agreed to in writing, software
 *     distributed under the License is distributed on an "AS IS" BASIS,
 *     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *     See the License for the specific language governing permissions and
 *     limitations under the License.
 */
package org.openo.orchestrator.nfv.catalog.db.wrapper;

import java.util.ArrayList;
import java.util.Map;

import org.openo.orchestrator.nfv.catalog.db.common.CatalogResuorceType;
import org.openo.orchestrator.nfv.catalog.db.common.Parameters;
import org.openo.orchestrator.nfv.catalog.db.entity.ServiceTemplateMappingData;
import org.openo.orchestrator.nfv.catalog.db.entity.ServiceTemplateMappingData;
import org.openo.orchestrator.nfv.catalog.db.exception.CatalogResourceException;
import org.openo.orchestrator.nfv.catalog.db.util.CatalogDbUtil;
import org.openo.orchestrator.nfv.catalog.db.util.HqlFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * 
 ** @author 10159474
 */
public class ServiceTemplateMappingHandler extends BaseHandler<ServiceTemplateMappingData> {
    private static final Logger logger = LoggerFactory
            .getLogger(ServiceTemplateMappingHandler.class);

    public ServiceTemplateMappingData create(ServiceTemplateMappingData serviceTemplateMappingData)
            throws CatalogResourceException {
        logger.info("ServiceTemplateMappingHandler:start create serviceTemplateMapping info.");
        ServiceTemplateMappingData data = null;
        if (!CatalogDbUtil.isNotEmpty(serviceTemplateMappingData.getMappingId())) {

            logger.info("ServiceTemplateMappingHandler:mapping info does not have mappingId,generate UUID.");
            String id = CatalogDbUtil.generateId();
            serviceTemplateMappingData.setMappingId(id);
        }
        Object result =
                create(serviceTemplateMappingData,
                        CatalogResuorceType.SERVICETEMPLATEMAPPING.name());
        if (result != null)
            data = (ServiceTemplateMappingData) result;
        else
            logger.info("ServiceTemplateMappingHandler: query mapping info is null.");
        logger.info("ServiceTemplateMappingHandler: create mapping info end.");
        return data;
    }

    public void delete(String id) throws CatalogResourceException {
        logger.info("ServiceTemplateMappingHandler:start delete mapping info.");
        ServiceTemplateMappingData ServiceTemplateMappingData = new ServiceTemplateMappingData();
        ServiceTemplateMappingData.setMappingId(id);
        delete(ServiceTemplateMappingData, CatalogResuorceType.SERVICETEMPLATEMAPPING.name());
        logger.info("ServiceTemplateMappingHandler: delete mapping info end.");
    }

    public void delete(Map<String, String> delParam) throws CatalogResourceException {
        logger.info("ServiceTemplateMappingHandler:start delete mapping info.");
        delete(delParam, CatalogResuorceType.SERVICETEMPLATEMAPPING.name());
        logger.info("ServiceTemplateMappingHandler:delete mapping info end.");
    }

    public ArrayList<ServiceTemplateMappingData> query(Map<String, String> queryParam)
            throws CatalogResourceException {
        logger.info("ServiceTemplateMappingHandler:start query mapping info.");
        ArrayList<ServiceTemplateMappingData> data = new ArrayList<ServiceTemplateMappingData>();
        Object result = query(queryParam, CatalogResuorceType.SERVICETEMPLATEMAPPING.name());
        if (result != null)
            data = (ArrayList<ServiceTemplateMappingData>) result;
        else
            logger.info("ServiceTemplateMappingHandler: query mapping info is null.");
        logger.info("ServiceTemplateMappingHandler: query mapping info end.");
        return data;

    }

    @Override
    public void check(ServiceTemplateMappingData data) throws CatalogResourceException {
        // TODO Auto-generated method stub

    }



}
