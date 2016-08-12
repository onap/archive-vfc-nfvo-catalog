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
package org.openo.orchestrator.nfv.catalog.db.resource;

import java.util.ArrayList;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Assert;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openo.orchestrator.nfv.catalog.db.dao.DaoManager;
import org.openo.orchestrator.nfv.catalog.db.entity.NodeTemplateData;
import org.openo.orchestrator.nfv.catalog.db.entity.ServiceTemplateData;
import org.openo.orchestrator.nfv.catalog.db.entity.TemplateData;
import org.openo.orchestrator.nfv.catalog.db.exception.CatalogResourceException;
import org.openo.orchestrator.nfv.catalog.db.util.H2DbServer;
import org.openo.orchestrator.nfv.catalog.db.util.HibernateSession;

public class TemplateManagerTest {
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
            H2DbServer.shutDown();
        } catch (Exception e) {
            Assert.fail("Exception" + e.getMessage());
        }
    }

    @Before
    public void setUp() {
        ServiceTemplateData serviceData = new ServiceTemplateData();
        TemplateData data = new TemplateData();
        ArrayList<NodeTemplateData> nodelist = new ArrayList<NodeTemplateData>();
        serviceData.setCsarId("10001");
        serviceData.setServiceTemplateId("20001");
        serviceData.setRowData("EEEEEEWERWEREWRERWEREW");
        serviceData.setOperations("SDFSDFDSERWERWE");
        serviceData.setVendor("ZTE");
        serviceData.setVersion("v1.0");
        NodeTemplateData nodeData = new NodeTemplateData();
        nodeData.setName("node");
        nodeData.setNodeTemplateId("30001");
        nodeData.setServiceTemplateId("20001");
        nodelist.add(nodeData);
        data.setServiceTemplate(serviceData);
        data.setNodeTemplates(nodelist);
        try {
            manager.addServiceTemplate(data);
        } catch (CatalogResourceException e) {
            Assert.fail("Exception" + e.getMessage());
        }
    }

    @After
    public void tearDown() {
        try {
            manager.deleteServiceTemplateById("20001");
        } catch (CatalogResourceException e) {
            Assert.fail("Exception" + e.getMessage());
        }
    }

    @Test
    public void testAddServiceTemplateRepeat() {
        ServiceTemplateData serviceData = new ServiceTemplateData();
        TemplateData data = new TemplateData();
        data.setServiceTemplate(serviceData);
        ArrayList<NodeTemplateData> nodelist = new ArrayList<NodeTemplateData>();
        serviceData.setCsarId("10001");
        serviceData.setServiceTemplateId("20001");
        serviceData.setVendor("ZTE");
        serviceData.setVersion("v1.0");
        NodeTemplateData nodeData = new NodeTemplateData();
        nodeData.setName("node");
        nodeData.setServiceTemplateId("20001");
        nodelist.add(nodeData);
        data.setNodeTemplates(nodelist);
        try {
            manager.addServiceTemplate(data);
            Assert.fail("no exception");
        } catch (CatalogResourceException e) {
            Assert.assertTrue(true);
        }
    }

    @Test
    public void testQueryServiceTemplateById() {
        ArrayList<ServiceTemplateData> list = new ArrayList<ServiceTemplateData>();
        try {
            list = manager.queryServiceTemplateById("20001");
        } catch (CatalogResourceException e) {
            Assert.fail("Exception" + e.getMessage());
        }
        Assert.assertTrue(list.size() > 0);
    }

    @Test
    public void testQueryServiceTemplate() {

        ArrayList<ServiceTemplateData> list = new ArrayList<ServiceTemplateData>();
        try {
            list = manager.queryServiceTemplate(null, "v1.0", "ZTE");
        } catch (CatalogResourceException e) {
            Assert.fail("Exception" + e.getMessage());
        }
        Assert.assertTrue(list.size() > 0);

    }

    @Test
    public void testQueryNodeTemplateBySeriviceTemplateId() {
        ArrayList<NodeTemplateData> list = new ArrayList<NodeTemplateData>();
        try {
            list = manager.queryNodeTemplateBySeriviceTemplateId("20001");
        } catch (CatalogResourceException e) {
            Assert.fail("Exception" + e.getMessage());
        }
        Assert.assertTrue(list.size() > 0);
    }

    @Test
    public void testQueryNodeTemplateById() {
        ArrayList<NodeTemplateData> list = new ArrayList<NodeTemplateData>();
        try {
            list = manager.queryNodeTemplateById("20001", null);
        } catch (CatalogResourceException e) {
            Assert.fail("Exception" + e.getMessage());
        }
        Assert.assertTrue(list.size() > 0);
    }

}
