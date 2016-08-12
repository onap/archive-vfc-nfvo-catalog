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
package org.openo.orchestrator.nfv.catalog.db.dao;

import org.hibernate.HibernateException;
import org.hibernate.SessionFactory;
import org.openo.orchestrator.nfv.catalog.db.entity.NodeTemplateData;
import org.openo.orchestrator.nfv.catalog.db.entity.TemplateData;
import org.openo.orchestrator.nfv.catalog.db.exception.CatalogResourceException;
import org.openo.orchestrator.nfv.catalog.db.util.CatalogDbUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * DAO class
 * 
 * *@author 10159474
 * 
 */
public class TemplateDao extends BaseDao<TemplateData> {
    private static final Logger logger = LoggerFactory.getLogger(TemplateDao.class);

    public TemplateDao(SessionFactory sessionFactory) {
        super(sessionFactory);
    }

    public TemplateData create(TemplateData data) throws CatalogResourceException {
        logger.info("TemplateDao:start add template.info:" + CatalogDbUtil.objectToString(data));
        beginTransaction();
        try {
            this.session.persist(data.getServiceTemplate());
            for (NodeTemplateData nodeData : data.getNodeTemplates()) {
                this.session.persist(nodeData);
            }
            closeTransaction();
        } catch (HibernateException e) {
            logger.error("TemplateDao:error while add template data.errorMsg:" + e.getMessage());
            throw new CatalogResourceException("error while add template data" + e.getMessage(), e);
        } finally {
            closeSession();
        }
        logger.info("TemplateDao: add template end .");
        return data;
    }

    public void delete(TemplateData data) throws CatalogResourceException {
        logger.info("TemplateDao:start delete template.info:" + CatalogDbUtil.objectToString(data));
        beginTransaction();
        try {
            for (NodeTemplateData nodeData : data.getNodeTemplates()) {
                this.session.delete(nodeData);
            }
            this.session.delete(data.getServiceTemplate());
            closeTransaction();
        } catch (HibernateException e) {
            logger.error("TemplateDao:error while delete template data.errorMsg:" + e.getMessage());
            throw new CatalogResourceException("error while delete template data" + e.getMessage(),
                    e);
        } finally {
            closeSession();
        }
        logger.info("TemplateDao: delete template end .");
    }
}
