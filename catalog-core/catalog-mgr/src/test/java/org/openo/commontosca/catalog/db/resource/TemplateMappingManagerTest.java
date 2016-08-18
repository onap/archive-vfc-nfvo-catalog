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
package org.openo.commontosca.catalog.db.resource;

import java.util.ArrayList;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Assert;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.dao.DaoManager;
import org.openo.commontosca.catalog.db.entity.ServiceTemplateMappingData;
import org.openo.commontosca.catalog.db.util.H2DbServer;
import org.openo.commontosca.catalog.db.util.HibernateSession;

public class TemplateMappingManagerTest {
    private static TemplateManager manager;

    @BeforeClass
    public static void setUpBeforeClass() throws Exception {
        H2DbServer.startUp();
        DaoManager.getInstance().setSessionFactory(HibernateSession.init());
        manager = TemplateManager.getInstance();
    }

    @AfterClass
    public static void tearDownAfterClass() throws Exception {
        try {
            HibernateSession.destory();
            DaoManager.getInstance().setTemplateDao(null);
            H2DbServer.shutDown();
        } catch (Exception e) {
            Assert.fail("Exception" + e.getMessage());
        }
    }

    @Before
    public void setUp() {
        ServiceTemplateMappingData serviceMappingData = new ServiceTemplateMappingData();
        serviceMappingData.setCapabilities("wsectdSDFSDFDSXCVFertregdDFGDFG");
        serviceMappingData.setRequirements("REWREWRWE#$#");
        serviceMappingData.setNodeType("NS");
        serviceMappingData.setServiceTemplateId("10020");
        serviceMappingData.setMappingId("10000");
        try {
            manager.addServiceTemplateMapping(serviceMappingData);
        } catch (CatalogResourceException e) {
            Assert.fail("Exception" + e.getMessage());
        }
    }

    @After
    public void tearDown() {
        try {
            manager.deleteServiceTemplateMappingById("10000");
        } catch (CatalogResourceException e) {
            Assert.fail("Exception" + e.getMessage());
        }
    }

    @Test
    public void testAddServiceTemplateRepeat() {
        ServiceTemplateMappingData serviceMappingData = new ServiceTemplateMappingData();
        serviceMappingData.setCapabilities("wsectdSDFSDFDSXCVFertregdDFGDFG");
        serviceMappingData.setRequirements("REWREWRWE#$#");
        serviceMappingData.setNodeType("NS");
        serviceMappingData.setServiceTemplateId("10020");
        serviceMappingData.setMappingId("10000");
        try {
            manager.addServiceTemplateMapping(serviceMappingData);
            Assert.fail("no exception");
        } catch (CatalogResourceException e) {
            Assert.assertTrue(true);
        }
    }

    @Test
    public void testServiceTemplateMappingById() {
        ArrayList<ServiceTemplateMappingData> list = new ArrayList<ServiceTemplateMappingData>();
        try {
            list = manager.queryServiceTemplateMappingById("10000");
        } catch (CatalogResourceException e) {
            Assert.fail("Exception" + e.getMessage());
        }
        Assert.assertTrue(list.size() > 0);
    }

    @Test
    public void testQueryServiceTemplateMapping() {

        ArrayList<ServiceTemplateMappingData> list = new ArrayList<ServiceTemplateMappingData>();
        try {
            list = manager.queryServiceTemplateMapping("NS", "10020");
        } catch (CatalogResourceException e) {
            Assert.fail("Exception" + e.getMessage());
        }
        Assert.assertTrue(list.size() > 0);
        try {
            list = manager.queryServiceTemplateMapping("NS", "");
        } catch (CatalogResourceException e) {
            Assert.fail("Exception" + e.getMessage());
        }
        Assert.assertTrue(list.size() > 0);
        try {
            list = manager.queryServiceTemplateMapping("", "10020");
        } catch (CatalogResourceException e) {
            Assert.fail("Exception" + e.getMessage());
        }
        Assert.assertTrue(list.size() > 0);
    }

    @Test
    public void testDeleteServiceTemplateMapping() {

        ArrayList<ServiceTemplateMappingData> list = new ArrayList<ServiceTemplateMappingData>();
        try {
            manager.deleteServiceTemplateMapping("NS", "10020");
        } catch (CatalogResourceException e) {
            Assert.fail("Exception" + e.getMessage());
        }
        try {
            list = manager.queryServiceTemplateMapping("NS", "10020");
        } catch (CatalogResourceException e) {
            Assert.fail("Exception" + e.getMessage());
        }
        Assert.assertTrue(list.size() == 0);
    }

    @Test
    public void testQueryAllServiceTemplateMapping() {

        ArrayList<ServiceTemplateMappingData> list = new ArrayList<ServiceTemplateMappingData>();
        try {
            list = manager.queryServiceTemplateMapping("", "");
        } catch (CatalogResourceException e) {
            Assert.fail("Exception" + e.getMessage());
        }
        Assert.assertTrue(list.size() > 0);
    }

}
